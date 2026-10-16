#!/usr/bin/env python3
"""Author replay: exact nine-module ordinary-width closure, no object reuse."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time


def digest(data):
    return hashlib.sha256(data).hexdigest()


parser = argparse.ArgumentParser()
parser.add_argument("--source-root", type=Path, required=True)
parser.add_argument("--build-dir", type=Path, required=True)
parser.add_argument("--evidence-dir", type=Path, required=True)
parser.add_argument("--lean", required=True)
args = parser.parse_args()
root = args.source_root.resolve()
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
    ("Agent1RepeatedBlockContext", "Agent1RepeatedBlockContext.lean", "d73d6825fbae0da63595073d82ee32e7cdf7dad1a8c6aa4efa8e29cf99911eb3"),
    ("Agent1PeriodicDigits", "Agent1PeriodicDigits.lean", "dc6cc1dadb74c4927f0635107fdc1eb62cebac3038dea4e97ad4229fc8703eab"),
    ("Agent1PeriodicNumeric", "Agent1PeriodicNumeric.lean", "d3142b2a44bbe471df559e74bba993a9a663592b3bf04ce973e1ef94251873f7"),
]
manifest = []
for module, filename, expected in modules:
    data = (root / "proofs" / filename).read_bytes()
    if digest(data) != expected:
        raise RuntimeError(f"Pinned source mismatch: {filename}")
    (build / f"{module}.lean").write_bytes(data)
    if module in {"Agent1PeriodicDigits", "Agent1PeriodicNumeric"}:
        (evidence / f"{module}.lean").write_bytes(data)
    manifest.append({"module": module, "path": f"proofs/{filename}",
                     "sha256": expected})

(evidence / "sources.json").write_text(json.dumps(manifest, indent=2) + "\n")
version = subprocess.run([args.lean, "--version"], text=True, capture_output=True, check=True)
(evidence / "version.log").write_text(version.stdout + version.stderr)
if "version 4.19.0" not in version.stdout or "6caaee842e94" not in version.stdout:
    raise RuntimeError("Unexpected Lean version")
compiler_sha = digest(Path(args.lean).read_bytes())
if compiler_sha != "92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023":
    raise RuntimeError("Unexpected compiler binary hash")

environment = dict(os.environ, LEAN_PATH=str(build))
results = []
for module, _, _ in modules:
    command = [args.lean, "--trust=0", "-j1", "-DElab.async=false",
               "-o", f"{module}.olean", f"{module}.lean"]
    started = time.time()
    result = subprocess.run(command, cwd=build, env=environment, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (evidence / f"{module}.log").write_text(result.stdout)
    results.append({"module": module, "command": command,
                    "exit_code": result.returncode, "seconds": time.time() - started,
                    "log_sha256": digest(result.stdout.encode())})
    (evidence / "commands.json").write_text(json.dumps(results, indent=2) + "\n")
    print(f"{module}: exit {result.returncode}", flush=True)
    if result.returncode:
        print(result.stdout, end="")
        raise SystemExit(result.returncode)

source = (build / "Agent1PeriodicNumeric.lean").read_text()
exports = re.findall(r"^theorem\s+(\w+)", source, re.M)
expected_exports = [
    "terminalCarry_eq_actual_carry", "actual_step_canonical_width",
    "actual_step_decimalLength_normalize", "periodic_actual_carry",
    "periodic_actual_step_canonical_width", "periodic_actual_step_decimalLength",
]
if exports != expected_exports:
    raise RuntimeError(f"Unexpected theorem inventory: {exports}")
for bad in ("sorry", "admit", "native_decide", "Lean.ofReduceBool", "unsafe", "axiom "):
    if bad in source:
        raise RuntimeError(f"Forbidden new-source token: {bad}")

audit = (evidence / "Agent1PeriodicNumeric.log").read_text()
parsed = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", audit)
if [name for name, _ in parsed] != ["Agent1.Periodic." + x for x in exports]:
    raise RuntimeError("Missing, duplicate, or unexpected literal axiom print")
axioms = set()
for _, printed in parsed:
    axioms.update(x.strip() for x in printed.split(",") if x.strip())
if not axioms <= {"propext", "Classical.choice", "Quot.sound"}:
    raise RuntimeError(f"Unexpected transitive axioms: {sorted(axioms)}")
for module, filename, expected in modules:
    if digest((root / "proofs" / filename).read_bytes()) != expected:
        raise RuntimeError(f"Source drift after compilation: {filename}")
    if digest((build / f"{module}.lean").read_bytes()) != expected:
        raise RuntimeError(f"Build source drift: {module}")

(evidence / "verification.json").write_text(json.dumps({
    "status": "PASS", "scope": "Author clean replay; independent review not implied",
    "source_root": str(root), "build_dir": str(build),
    "fresh_empty_build_directory": True, "project_object_reuse": False,
    "modules_compiled": len(modules), "new_exported_theorems": exports,
    "all_new_exports_have_literal_axiom_print": True,
    "axiom_union": sorted(axioms), "source_drift": False,
    "compiler_version": version.stdout.strip(), "compiler_sha256": compiler_sha,
    "normalization_source_commit": "757b1a59f71a155779c27b7cc7842aa1fcd9a96b",
    "claim_commit": "9f7ff8f127741f0d03bb911bc6dbb5f9c366f1ca",
    "claim_receipt": "https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6224929353",
    "runner_sha256": digest(Path(__file__).read_bytes()),
}, indent=2) + "\n")
print("PASS: nine fresh modules; all six numeric exports audited", flush=True)
