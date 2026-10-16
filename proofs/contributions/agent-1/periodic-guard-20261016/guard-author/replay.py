#!/usr/bin/env python3
"""Fresh kernel replay of the pinned eleven-module raw-guard closure."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time


def digest(data):
    return hashlib.sha256(data).hexdigest()


parser = argparse.ArgumentParser()
parser.add_argument("--source-root", type=Path, default=Path(__file__).resolve().parents[5])
parser.add_argument("--build-dir", type=Path, required=True)
parser.add_argument("--evidence-dir", type=Path, required=True)
parser.add_argument("--lean", required=True)
args = parser.parse_args()
source = args.source_root.resolve()
build = args.build_dir.resolve()
evidence = args.evidence_dir.resolve()
build.mkdir(parents=True, exist_ok=False)
evidence.mkdir(parents=True, exist_ok=False)
manifest = json.loads(Path(__file__).with_name("pinned-sources.json").read_text())
for row in manifest:
    data = (source / row["source"]).read_bytes()
    if digest(data) != row["sha256"]:
        raise RuntimeError(f"Pinned source mismatch: {row['source']}")
    (build / (row["module"] + ".lean")).write_bytes(data)
    if row["module"] in ("Agent1PeriodicGuard", "Agent1PeriodicGuardFacts"):
        (evidence / (row["module"] + ".lean")).write_bytes(data)
(evidence / "sources.json").write_text(json.dumps(manifest, indent=2) + "\n")
version = subprocess.run([args.lean, "--version"], capture_output=True, text=True, check=True)
(evidence / "lean-version.txt").write_text(version.stdout)
env = dict(os.environ, LEAN_PATH=str(build))
results = []
axiom_union = set()
checked_exports = []
for row in manifest:
    module = row["module"]
    command = [args.lean, "--trust=0", "-j1", "-DElab.async=false",
               "-o", module + ".olean", module + ".lean"]
    started = time.time()
    result = subprocess.run(command, cwd=build, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (evidence / (module + ".log")).write_text(result.stdout)
    results.append({"module": module, "command": command, "exit_code": result.returncode,
                    "elapsed_seconds": time.time() - started,
                    "log_sha256": digest(result.stdout.encode())})
    (evidence / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(f"{module}: exit {result.returncode}", flush=True)
    if result.returncode:
        print(result.stdout, end="")
        sys.exit(result.returncode)
    if module.startswith("Agent1Periodic"):
        text = (build / (module + ".lean")).read_text()
        for forbidden in ("sorry", "admit", "native_decide", "Lean.ofReduceBool"):
            if forbidden in text:
                raise RuntimeError(f"Forbidden source token in {module}: {forbidden}")
        exports = re.findall(r"^#print axioms (\S+)", text, re.M)
        for name in exports:
            if f"'{name}' depends on axioms:" not in result.stdout:
                raise RuntimeError(f"Missing literal axiom print: {name}")
        checked_exports.extend(exports)
        for printed in re.findall(r"depends on axioms: \[([^\]]*)\]", result.stdout):
            axiom_union.update(x.strip() for x in printed.split(",") if x.strip())
        if not axiom_union <= {"propext", "Classical.choice", "Quot.sound"}:
            raise RuntimeError(f"Unexpected axiom set: {sorted(axiom_union)}")
(evidence / "audit-result.json").write_text(json.dumps({
    "modules_built": len(manifest), "checked_exports": checked_exports,
    "axiom_union": sorted(axiom_union), "source_token_check": "passed",
    "scope": "Author clean replay; independent review and Numeric root are separate",
}, indent=2) + "\n")
