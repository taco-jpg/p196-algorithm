#!/usr/bin/env python3
"""Fresh author replay of exact repeated-block sources, with kernel checking."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time


def sha256(data):
    return hashlib.sha256(data).hexdigest()


parser = argparse.ArgumentParser()
parser.add_argument("--source-root", type=Path, default=Path(__file__).resolve().parents[5])
parser.add_argument("--build-dir", type=Path, required=True)
parser.add_argument("--evidence-dir", type=Path, required=True)
parser.add_argument("--lean", required=True)
args = parser.parse_args()

source_root = args.source_root.resolve()
build = args.build_dir.resolve()
evidence = args.evidence_dir.resolve()
build.mkdir(parents=True, exist_ok=False)
evidence.mkdir(parents=True, exist_ok=False)

modules = [
    ("PeriodObstructions", "PeriodObstructions__70ce034b31b5b218.lean", "83102a949036799a929ba72d74ce9d76bc2a11cb3adf61e0bc06b6013b22991a"),
    ("ActualWordBridge", "ActualWordBridge__7f032d27940694a8.lean", "3123e8f86fe751e61307ea528390bd265515a8d69c731f51e2808fb78d0a6ec6"),
    ("PrefixSemantics", "PrefixSemantics__3798a605dd95d8c6.lean", "5dca5a84536801f771020660d496063426c5946a4e1912ec2a17f0ae246b23b5"),
    ("LychrelDigitSums", "LychrelDigitSums__75febdc48f0ca802.lean", "ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57"),
    ("IncomingCarry", "IncomingCarry__13645dd30c0ce73b.lean", "d8a7cfa955204d03f454fcd1234ca66c2d15f361f9fbc036420dc91ac7579849"),
    ("Agent1RepeatedBlock", "Agent1RepeatedBlock.lean", "4dc552677e5b7f1484fa2c765378bae02236033a4c5d42858f84b258a9f30d12"),
]
manifest = []
for module, filename, expected in modules:
    data = (source_root / "proofs" / filename).read_bytes()
    digest = sha256(data)
    if expected is not None and digest != expected:
        raise RuntimeError(f"Pinned source mismatch: {filename}")
    (build / f"{module}.lean").write_bytes(data)
    if module == "Agent1RepeatedBlock":
        (evidence / f"{module}.lean").write_bytes(data)
    manifest.append({"module": module, "source": f"proofs/{filename}", "sha256": digest})
(evidence / "sources.json").write_text(json.dumps(manifest, indent=2) + "\n")

version = subprocess.run([args.lean, "--version"], text=True, capture_output=True, check=True)
(evidence / "lean-version.txt").write_text(version.stdout)
environment = dict(os.environ, LEAN_PATH=str(build))
results = []
for module, _, _ in modules:
    command = [args.lean, "--trust=0", "-o", f"{module}.olean", f"{module}.lean"]
    started = time.time()
    result = subprocess.run(command, cwd=build, env=environment,
                            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log = evidence / f"{module}.log"
    log.write_text(result.stdout)
    results.append({"module": module, "command": command, "exit_code": result.returncode,
                    "elapsed_seconds": time.time() - started,
                    "log_sha256": sha256(result.stdout.encode())})
    (evidence / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(f"{module}: exit {result.returncode}", flush=True)
    if result.returncode:
        print(result.stdout, end="")
        sys.exit(result.returncode)

new_source = (build / "Agent1RepeatedBlock.lean").read_text()
for forbidden in ("sorry", "admit", "native_decide", "Lean.ofReduceBool"):
    if forbidden in new_source:
        raise RuntimeError(f"Forbidden source token: {forbidden}")
audit = (evidence / "Agent1RepeatedBlock.log").read_text()
expected_exports = [
    "terminalCarry_eq_carryIn", "terminalCarry_idempotent", "terminalCarry_pow_succ",
    "fixedDigits_pow_succ", "normalize_pow_succ",
]
for name in expected_exports:
    if f"'Agent1.RepeatedBlock.{name}' depends on axioms:" not in audit:
        raise RuntimeError(f"Missing literal axiom print: {name}")
for forbidden in ("sorryAx", "Lean.ofReduceBool"):
    if forbidden in audit:
        raise RuntimeError(f"Forbidden transitive axiom: {forbidden}")
axioms = set()
for printed in re.findall(r"depends on axioms: \[([^\]]*)\]", audit):
    axioms.update(x.strip() for x in printed.split(",") if x.strip())
if not axioms <= {"propext", "Classical.choice", "Quot.sound"}:
    raise RuntimeError(f"Unexpected transitive axioms: {sorted(axioms)}")
(evidence / "audit-result.json").write_text(json.dumps({
    "exports": expected_exports, "source_token_check": "passed",
    "literal_axiom_prints": "present", "forbidden_axioms": "absent",
    "axiom_union": sorted(axioms),
    "scope": "Author replay; independent review not implied",
}, indent=2) + "\n")
