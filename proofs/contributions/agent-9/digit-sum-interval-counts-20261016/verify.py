#!/usr/bin/env python3
"""Fresh pinned-source build for Agent #9's finite interval-count theorem."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from datetime import datetime, timezone


NEW_MODULES = [
    "Agent9WindowIntervalCounts",
    "Agent9DigitSumIntervalCounts",
    "Agent9IntervalCountsAudit",
]
EXPORTS = [
    "intervalCount_append",
    "intervalCount_mono_length",
    "intervalCount_positive_of_witness",
    "window_property_complete_blocks",
    "window_property_interval_count",
    "digitSum_interval_count",
    "digitSum_interval_count_196",
]
NAMESPACE = "P196.Agent9.IntervalCounts."
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", required=True, type=Path)
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--build-dir", required=True, type=Path)
    parser.add_argument("--report-dir", required=True, type=Path)
    args = parser.parse_args()
    package = Path(__file__).resolve().parent
    repo = args.repo_root.resolve()
    lean = args.lean.resolve()
    build = args.build_dir.resolve()
    report = args.report_dir.resolve()
    if build.exists() or report.exists():
        raise SystemExit("Build 和 report directories must both be new.")
    build.mkdir(parents=True)
    report.mkdir(parents=True)
    (report / "new-source-snapshot").mkdir()
    summary = {
        "status": "RUNNING",
        "started_at_utc": utc_now(),
        "lean_executable": str(lean),
        "lean_executable_sha256": sha256(lean.read_bytes()),
        "build_directory": str(build),
        "fresh_build_directory": True,
        "copied_compiled_objects": False,
        "commands": [],
        "sources": [],
        "expected_exports": [NAMESPACE + name for name in EXPORTS],
        "axiom_union": [],
        "scope": "Finite interval counts only; no density limit or pointwise divergence.",
    }
    write_json(report / "summary.json", summary)

    def run(label, argv, cwd):
        start = time.perf_counter()
        env = os.environ.copy()
        env["LEAN_PATH"] = str(build)
        result = subprocess.run(argv, cwd=cwd, env=env, capture_output=True)
        stdout = label + ".stdout.log"
        stderr = label + ".stderr.log"
        (report / stdout).write_bytes(result.stdout)
        (report / stderr).write_bytes(result.stderr)
        record = {
            "label": label,
            "argv": list(map(str, argv)),
            "cwd": str(cwd),
            "exit_code": result.returncode,
            "elapsed_seconds": time.perf_counter() - start,
            "stdout_file": stdout,
            "stdout_sha256": sha256(result.stdout),
            "stderr_file": stderr,
            "stderr_sha256": sha256(result.stderr),
        }
        summary["commands"].append(record)
        write_json(report / "summary.json", summary)
        print(json.dumps({"module": label, "exit_code": result.returncode,
                          "elapsed_seconds": record["elapsed_seconds"]}), flush=True)
        if result.returncode != 0:
            raise RuntimeError("Compiler command failed: " + label)
        return result.stdout.decode()

    try:
        version = run("lean-version", [str(lean), "--version"], build)
        if "4.19.0" not in version or "6caaee842e94" not in version:
            raise RuntimeError("Compiler version does not match the official pinned release.")
        summary["lean_version"] = version.strip()
        dependencies = json.loads((package / "dependencies.json").read_text())
        for dep in dependencies:
            source = repo / dep["current_path"]
            data = source.read_bytes()
            if sha256(data) != dep["sha256"]:
                raise RuntimeError("Pinned dependency hash mismatch: " + str(source))
            (build / (dep["module"] + ".lean")).write_bytes(data)
            summary["sources"].append(dict(dep, new_source=False))
        for module in NEW_MODULES:
            source = package / (module + ".lean")
            data = source.read_bytes()
            (build / source.name).write_bytes(data)
            (report / "new-source-snapshot" / source.name).write_bytes(data)
            summary["sources"].append({"module": module, "new_source": True,
                                       "path": source.name, "sha256": sha256(data)})
        write_json(report / "summary.json", summary)
        modules = [dep["module"] for dep in dependencies] + NEW_MODULES
        audit = ""
        for module in modules:
            output = run(module, [str(lean), "-j1", "-DElab.async=false", "-o",
                                  module + ".olean", module + ".lean"], build)
            if module == "Agent9IntervalCountsAudit":
                audit = output
        found = {}
        for name, axioms in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", audit):
            found[name] = {item.strip() for item in axioms.split(",") if item.strip()}
        for name in re.findall(r"'([^']+)' does not depend on any axioms", audit):
            found[name] = set()
        for name in summary["expected_exports"]:
            if name not in found:
                raise RuntimeError("Missing literal transitive axiom report for " + name)
            if not found[name] <= ALLOWED_AXIOMS:
                raise RuntimeError("Unexpected axiom dependency for " + name)
        summary["axiom_union"] = sorted(set().union(*(found[name] for name in summary["expected_exports"])))
        summary["export_axioms"] = {name: sorted(found[name]) for name in summary["expected_exports"]}
        summary["status"] = "LEAN_CHECKED"
    except Exception as error:
        summary["status"] = "FAILED"
        summary["failure"] = str(error)
        raise
    finally:
        summary["finished_at_utc"] = utc_now()
        write_json(report / "summary.json", summary)


if __name__ == "__main__":
    main()
