#!/usr/bin/env python3
"""Fresh compilation of unchanged, byte-pinned project sources.

Use the supported executor escalation required by the genuine Lean runtime.
This runner never edits theorem sources or Git and never reuses project objects.
The separate audit_exact.py performs module-origin and axiom verification.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import time
import traceback

HERE = Path(__file__).resolve().parent
RUNTIME = HERE.parent
LEAN = RUNTIME / "lean-4.19.0-linux/bin/lean"
PARSER = RUNTIME / "source-snapshot/p196-algorithm-4b4edf976b2c7a9ba1dad80636c0e21c66350325/proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/verify_project.py"
EXPECTED_VERSION = "Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)"
FLAGS = [str(LEAN), "--trust=0", "-j1", "-DElab.async=false"]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def main() -> int:
    base = Path(sys.argv[1]).resolve()
    assert base.is_relative_to(HERE)
    source = base / "source"
    build = base / "build"
    build.mkdir(exist_ok=False)
    objects, logs = build / "objects", build / "logs"
    objects.mkdir()
    logs.mkdir()
    manifest = json.loads((base / "source-manifest.json").read_text())
    order = manifest["build_order"]
    by_module = {m["module"]: m for m in manifest["modules"]}
    assert set(order) == set(by_module) and len(order) == len(by_module)
    env = {"PATH": str(LEAN.parent) + ":/usr/bin:/bin", "LANG": "C.UTF-8", "LEAN_PATH": str(objects)}
    report = {
        "status": "RUNNING", "started_utc": utc(), "review_type": manifest["review_type"],
        "runner_path": str(Path(__file__).resolve()), "runner_sha256": sha(Path(__file__)),
        "source_manifest_sha256": sha(base / "source-manifest.json"),
        "source_branch_commit": manifest["source_branch_commit"],
        "source_branch_tree": manifest.get("source_branch_tree"),
        "fresh_project_objects": True, "reused_dependency_objects": False,
        "source_repairs": [], "git_mutations": False, "shim_used": False,
        "build_order": order, "modules": manifest["modules"], "commands": [],
    }

    def save() -> None:
        (build / "compilation.json").write_text(json.dumps(report, indent=2) + "\n")

    def run(label: str, argv: list[str]) -> str:
        start = time.monotonic()
        log = logs / (label + ".log")
        with log.open("wb") as stream:
            try:
                code = subprocess.run(argv, cwd=source, env=env, stdout=stream,
                                      stderr=subprocess.STDOUT, timeout=900).returncode
            except subprocess.TimeoutExpired:
                code = 124
        report["commands"].append({"label": label, "argv": argv, "cwd": str(source),
            "environment": env, "exit_code": code, "elapsed_seconds": round(time.monotonic()-start, 6),
            "log": str(log.relative_to(base)), "log_sha256": sha(log)})
        save()
        print(label, "exit=" + str(code), flush=True)
        if code:
            raise RuntimeError("Compilation command failed: " + label)
        return log.read_text()

    def check_sources() -> dict[str, str]:
        hashes = {}
        for name in order:
            rec = by_module[name]
            staged, live = source / (name + ".lean"), Path(rec["path"])
            data = staged.read_bytes()
            got = hashlib.sha256(data).hexdigest()
            blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            if got != rec["sha256"] or blob != rec["git_blob"] or live.read_bytes() != data:
                raise ValueError("Staged/original source pin mismatch: " + name)
            hashes[name] = got
        return hashes

    try:
        report["source_hashes_before"] = check_sources()
        version = run("lean-version", [str(LEAN), "--version"]).strip()
        if version != EXPECTED_VERSION:
            raise ValueError("Pinned Lean version mismatch")
        if sha(LEAN) != "92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023":
            raise ValueError("Pinned official Lean binary hash mismatch")
        prefix = Path(run("lean-prefix", [str(LEAN), "--print-prefix"]).strip())
        compiler_files = [LEAN, *sorted((prefix / "lib/lean").glob("*.so"))]
        compiler = {str(p): sha(p) for p in compiler_files}
        report["compiler"] = {"version": version, "prefix": str(prefix), "files": compiler,
            "official_runtime_receipt": str(RUNTIME / "runtime-receipt.json"), "shim_used": False}
        sys.dont_write_bytecode = True
        spec = importlib.util.spec_from_file_location("pinned_token_parser", PARSER)
        assert spec is not None and spec.loader is not None
        parser = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(parser)
        report["source_parser"] = {"path": str(PARSER), "sha256": sha(PARSER)}
        complete = set(manifest.get("external_modules", ["Std"]))
        for name in order:
            code = parser.code_only((source / (name + ".lean")).read_text())
            imports = [x for line in re.findall(r"^\s*import\s+([^\n]+)", code, re.M) for x in line.split()]
            if imports != by_module[name]["imports"] or not set(imports) <= complete:
                raise ValueError("Import pin/order mismatch: " + name)
            if re.search(r"(?<![\w'])\b(?:sorry|admit|axiom|sorryAx|native_decide|ofReduceBool|skipKernelTC|unsafe)\b(?![\w'])", code):
                raise ValueError("Forbidden source token: " + name)
            complete.add(name)
        report["token_scan"] = "PASS, nested comments and strings excluded by pinned parser"
        save()
        for name in order:
            run(name, FLAGS + ["--root=" + str(source), "-o", str(objects / (name + ".olean")), str(source / (name + ".lean"))])
        report["source_hashes_after"] = check_sources()
        for p, expected in compiler.items():
            if sha(Path(p)) != expected:
                raise ValueError("Compiler changed during execution: " + p)
        report["source_unchanged_before_after"] = True
        report["compiler_unchanged_before_after"] = True
        report["objects"] = {p.stem: {"path": str(p), "bytes": p.stat().st_size, "sha256": sha(p)} for p in sorted(objects.glob("*.olean"))}
        if set(report["objects"]) != set(order):
            raise ValueError("Object inventory mismatch")
        report["status"] = "COMPILED_PENDING_INDEPENDENT_AXIOM_AUDIT"
        report["finished_utc"] = utc()
        save()
        ready = {"status": report["status"], "object_directory": str(objects), "source_directory": str(source),
            "source_manifest": str(base / "source-manifest.json"), "source_manifest_sha256": sha(base / "source-manifest.json"),
            "compilation_receipt": str(build / "compilation.json"), "compilation_receipt_sha256": sha(build / "compilation.json"),
            "module_count": len(order), "objects": report["objects"], "created_utc": utc()}
        (base / "OBJECTS_READY.json").write_text(json.dumps(ready, indent=2) + "\n")
        print("OBJECTS_READY", str(objects), flush=True)
        return 0
    except Exception as error:
        report["status"] = "FAIL"
        report["error"] = str(error)
        (build / "failure.txt").write_text(traceback.format_exc())
        print("FAIL", error, flush=True)
        return 1
    finally:
        if "finished_utc" not in report:
            report["finished_utc"] = utc()
        save()


if __name__ == "__main__":
    raise SystemExit(main())
