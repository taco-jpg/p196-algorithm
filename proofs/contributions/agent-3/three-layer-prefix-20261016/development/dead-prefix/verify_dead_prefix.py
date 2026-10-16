#!/usr/bin/env python3
"""Preserve each genuine source attempt and check the new module only."""

import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import time

EVIDENCE = Path(__file__).resolve().parent
CONTRIBUTION = EVIDENCE.parent.parent
SOURCE = CONTRIBUTION / "DeadPrefix.lean"
BUILD = EVIDENCE / "build"
WORKSPACE = Path("/workspace/scratch/4ce7c54d31f6")
LEAN = WORKSPACE / "lean-runtime/lean-4.19.0-linux/bin/lean"
DEPS = WORKSPACE / "agent3-history-build"
EXPECTED_DEPS = {
    "InverseFibers.lean": "64f4fa5df54d9365b1b3706eceeab3d3f358eb1040a95e3057ac4d9f82806b70",
    "PathCounts.lean": "588890faa1a29739b00dbe660a5f39971ac5087d997550cb9a740194eb592a33",
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path, obj):
    path.write_text(json.dumps(obj, indent=2) + "\n")


def run_lean(args, log):
    cmd = [str(LEAN), "--trust=0", *map(str, args)]
    env = dict(os.environ)
    env["LEAN_PATH"] = str(BUILD) + ":" + str(DEPS)
    start = time.monotonic()
    result = subprocess.run(cmd, cwd=CONTRIBUTION, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log.write_text(result.stdout)
    return {
        "command": cmd,
        "shell_display": shlex.join(cmd),
        "cwd": str(CONTRIBUTION),
        "LEAN_PATH": env["LEAN_PATH"],
        "exit_code": result.returncode,
        "elapsed_seconds": round(time.monotonic() - start, 3),
        "log": str(log.relative_to(CONTRIBUTION)),
        "log_sha256": sha(log),
    }


def main():
    attempt = int(sys.argv[1])
    prefix = EVIDENCE / f"attempt-{attempt:03d}"
    snapshot = prefix.with_suffix(".lean.txt")
    if snapshot.exists():
        raise SystemExit("Refusing to overwrite an existing attempt snapshot")
    BUILD.mkdir(parents=True, exist_ok=True)
    dependencies = []
    for name, expected in EXPECTED_DEPS.items():
        path = DEPS / name
        actual = sha(path)
        if actual != expected:
            raise SystemExit(f"Pinned dependency source mismatch: {name}: {actual}")
        obj = path.with_suffix(".olean")
        dependencies.append({"source": str(path), "sha256": actual,
                             "object": str(obj), "object_sha256": sha(obj)})
    snapshot.write_bytes(SOURCE.read_bytes())
    source_hash = sha(SOURCE)
    record = {
        "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "attempt": attempt,
        "source": str(SOURCE),
        "source_sha256": source_hash,
        "snapshot": str(snapshot.relative_to(CONTRIBUTION)),
        "dependencies": dependencies,
        "verification_scope": "New DeadPrefix module and explicit-declaration axiom audit; existing pinned dependency objects reused, not independently rebuilt in this check.",
    }
    record["compile"] = run_lean(["-o", BUILD / "DeadPrefix.olean", SOURCE],
                                  prefix.with_suffix(".log"))
    save_json(prefix.with_suffix(".json"), record)
    if record["compile"]["exit_code"]:
        print(json.dumps(record, indent=2))
        return record["compile"]["exit_code"]
    declarations = re.findall(r"^(?:def|theorem) ([A-Za-z0-9_]+)",
                              SOURCE.read_text(), flags=re.MULTILINE)
    audit = EVIDENCE / "DeadPrefixAudit.lean"
    audit.write_text("import DeadPrefix\n\n" + "\n".join(
        "#print axioms P196.Agent3.ThreeLayer." + d for d in declarations) + "\n")
    record["audit_source_sha256"] = sha(audit)
    record["declarations"] = declarations
    record["audit"] = run_lean([audit], EVIDENCE / "axiom-audit.log")
    audit_text = (EVIDENCE / "axiom-audit.log").read_text()
    allowed = {"Classical.choice", "Quot.sound", "propext"}
    reported = {}
    for line in audit_text.splitlines():
        match = re.fullmatch(r"'([^']+)' depends on axioms: \[(.*)\]", line)
        if match:
            reported[match[1]] = [] if not match[2] else match[2].split(", ")
        match_empty = re.fullmatch(r"'([^']+)' does not depend on any axioms", line)
        if match_empty:
            reported[match_empty[1]] = []
    expected_names = {"P196.Agent3.ThreeLayer." + d for d in declarations}
    audit_ok = record["audit"]["exit_code"] == 0 and set(reported) == expected_names
    audit_ok = audit_ok and all(set(xs) <= allowed for xs in reported.values())
    record["axioms"] = reported
    record["source_unchanged_during_check"] = sha(SOURCE) == source_hash
    record["object"] = str(BUILD / "DeadPrefix.olean")
    record["object_sha256"] = sha(BUILD / "DeadPrefix.olean")
    record["status"] = "PASS" if audit_ok and record["source_unchanged_during_check"] else "FAIL"
    save_json(prefix.with_suffix(".json"), record)
    save_json(EVIDENCE / "verification.json", record)
    print(json.dumps(record, indent=2))
    return 0 if record["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
