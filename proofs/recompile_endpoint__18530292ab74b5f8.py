#!/usr/bin/env python3
"""Recompile only the endpoint against explicitly pinned clean-built objects.

This intentionally reuses dependency objects.  It must never be described as a
fresh build of all dependencies.  Invoke only after the independent full build
has finished and its verification.json reports PASS.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time

HERE = Path(__file__).resolve().parent
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean-report", required=True, type=Path)
    parser.add_argument("--clean-snapshot", required=True, type=Path)
    parser.add_argument("--build", required=True, type=Path)
    parser.add_argument("--evidence", required=True, type=Path)
    args = parser.parse_args()
    assert not args.build.exists() and not args.evidence.exists()
    clean_report_sha = sha(args.clean_report)
    clean = json.loads(args.clean_report.read_text())
    assert clean["status"] == "PASS" and clean["fresh_source_rebuild"] is True
    diagnostics_path = HERE / "diagnostics.json"
    diagnostics_sha = sha(diagnostics_path)
    diagnostics = json.loads(diagnostics_path.read_text())
    modules = diagnostics["conclusion_import_closure_modules"]
    source_pins = {Path(p).stem: h for p, h in diagnostics["source_sha256"].items()}
    assert len(source_pins) == len(modules)
    assert set(modules) <= set(clean["sources"])
    lean = Path(clean["compiler"]["wrapper"])
    compiler_pins = clean["compiler"]["fingerprints"]
    for path, expected in compiler_pins.items():
        assert sha(path) == expected, ("compiler changed", path)
    # Include standard-library fingerprints recorded by the independent build.
    external_object_pins = {
        name: entry for name, entry in clean["imported_object_fingerprints"].items()
        if name not in clean["sources"]}
    for name, entry in external_object_pins.items():
        assert sha(entry["path"]) == entry["sha256"], ("external object changed", name)

    args.build.mkdir(parents=True)
    args.evidence.mkdir(parents=True)
    reused = {}
    for module in modules:
        original_source = args.clean_snapshot / f"{module}.lean"
        assert sha(original_source) == source_pins[module], ("review/source mismatch", module)
        assert clean["sources"][module]["sha256"] == source_pins[module]
        shutil.copyfile(original_source, args.build / original_source.name)
        if module != "Conclusion739":
            original_object = args.clean_snapshot / f"{module}.olean"
            expected = clean["sources"][module]["object_sha256"]
            assert sha(original_object) == expected
            copied_object = args.build / original_object.name
            shutil.copyfile(original_object, copied_object)
            assert sha(copied_object) == expected
            reused[module] = {
                "original_path": str(original_object),
                "copied_path": str(copied_object),
                "source_sha256": source_pins[module],
                "object_sha256": expected,
            }
    audit_source = HERE / "EndpointAudit.lean"
    shutil.copyfile(audit_source, args.build / audit_source.name)
    env = os.environ.copy()
    inherited = {name: env.get(name) for name in ("LEAN_PATH", "LEAN_SRC_PATH", "LEAN_SYSROOT", "LD_PRELOAD")}
    assert env.get("LD_PRELOAD", "") == clean["compiler"]["inherited_LD_PRELOAD"]
    for name in ("LEAN_PATH", "LEAN_SRC_PATH", "LEAN_SYSROOT"):
        env.pop(name, None)
    env["LEAN_PATH"] = str(args.build)
    executions = []
    for module in ("Conclusion739", "EndpointAudit"):
        command = [str(lean), "-j1", "-DElab.async=false", "-o", f"{module}.olean", f"{module}.lean"]
        started = time.monotonic()
        result = subprocess.run(command, cwd=args.build, env=env, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                timeout=120, check=False)
        elapsed = time.monotonic() - started
        log = args.evidence / f"{module}.log"
        log.write_text(result.stdout)
        execution = {
            "module": module, "command": command, "cwd": str(args.build),
            "LEAN_PATH": str(args.build), "exit_code": result.returncode,
            "elapsed_seconds": round(elapsed, 6), "log_sha256": sha(log),
            "source_sha256": sha(args.build / f"{module}.lean"),
        }
        executions.append(execution)
        (args.evidence / "executions.json").write_text(json.dumps(executions, indent=2) + "\n")
        assert result.returncode == 0, execution
        execution["object_sha256"] = sha(args.build / f"{module}.olean")
        print(json.dumps(execution), flush=True)
    audit_output = (args.evidence / "EndpointAudit.log").read_text()
    audited = {}
    for line in audit_output.splitlines():
        m = re.fullmatch(r"'([^']+)' does not depend on any axioms", line)
        if m:
            audited[m[1]] = []
        m = re.fullmatch(r"'([^']+)' depends on axioms: \[(.*)\]", line)
        if m:
            audited[m[1]] = [a.strip() for a in m[2].split(",") if a.strip()]
    expected_names = re.findall(r"^#print axioms (\S+)$", audit_source.read_text(), re.M)
    assert set(audited) == set(expected_names), (audited.keys(), expected_names)
    assert all(set(axioms) <= ALLOWED for axioms in audited.values()), audited
    assert "sorryAx" not in audit_output and "Lean.ofReduceBool" not in audit_output
    for module, item in reused.items():
        assert sha(item["original_path"]) == item["object_sha256"]
        assert sha(item["copied_path"]) == item["object_sha256"]
    for module in modules:
        assert sha(args.clean_snapshot / f"{module}.lean") == source_pins[module]
        assert sha(args.build / f"{module}.lean") == source_pins[module]
    for path, expected in compiler_pins.items():
        assert sha(path) == expected
    for name, entry in external_object_pins.items():
        assert sha(entry["path"]) == entry["sha256"]
    assert sha(args.clean_report) == clean_report_sha
    assert sha(diagnostics_path) == diagnostics_sha
    manifest = {
        "status": "PASS", "scope": "Independent endpoint recompilation and exact-type/transitive-axiom audit",
        "fresh_full_dependency_rebuild_by_this_reviewer": False,
        "dependency_objects_reused": len(reused),
        "dependency_provenance": "Pinned copies of the separate independent clean specialist's fresh build",
        "clean_report": str(args.clean_report), "clean_report_sha256": clean_report_sha,
        "diagnostics_sha256": diagnostics_sha,
        "compiler": clean["compiler"], "inherited_environment": inherited,
        "dependency_objects": reused, "external_imported_objects": external_object_pins,
        "source_pins": source_pins, "executions": executions,
        "audit_source_sha256": sha(audit_source), "transitive_axioms": audited,
        "allowed_axioms": sorted(ALLOWED),
        "sources_objects_and_compiler_unchanged_at_completion": True,
    }
    (args.evidence / "verification.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "dependency_objects_reused": len(reused), "audited": audited}), flush=True)


if __name__ == "__main__":
    main()
