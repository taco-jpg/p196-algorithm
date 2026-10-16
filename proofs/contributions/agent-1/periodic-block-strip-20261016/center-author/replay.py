#!/usr/bin/env python3
"""Fresh author replay of the exact whole-period center-strip source."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time


def sha(data):
    return hashlib.sha256(data).hexdigest()


p = argparse.ArgumentParser()
p.add_argument("--source-root", type=Path, required=True)
p.add_argument("--build-dir", type=Path, required=True)
p.add_argument("--evidence-dir", type=Path, required=True)
p.add_argument("--lean", required=True)
args = p.parse_args()
root = args.source_root.resolve()
build = args.build_dir.resolve()
evidence = args.evidence_dir.resolve()
build.mkdir(parents=True, exist_ok=False)
evidence.mkdir(parents=True, exist_ok=False)

registry = (root / "proofs/Agent1PeriodicGuard.registry.json").read_bytes()
if sha(registry) != "8c277ac7e49bfa8aada62f621693ea5fea1e604e08751435a1892004d54720e2":
    raise RuntimeError("Pinned dependency registry mismatch")
registered = json.loads(registry)["projects"]["agent1-periodic-guard"]["modules"]
order = ["PeriodObstructions", "ActualWordBridge", "PrefixSemantics",
         "LychrelDigitSums", "IncomingCarry", "Agent1RepeatedBlock",
         "Agent1RepeatedBlockContext", "Agent1PeriodicDigits",
         "Agent1PeriodicSlices", "Agent1PeriodicGuard"]
modules = [(m, registered[m]["path"], registered[m]["sha256"]) for m in order]
modules.append(("Agent1PeriodicCenterStrip", "proofs/Agent1PeriodicCenterStrip.lean",
                "566c7c5eac1fa54b98a9150a21f7ac61c403d8b0391b7aa92c1dbdea51c300c3"))
manifest = []
for module, path, expected in modules:
    data = (root / path).read_bytes()
    if sha(data) != expected:
        raise RuntimeError(f"Pinned source mismatch: {path}")
    (build / f"{module}.lean").write_bytes(data)
    if module == "Agent1PeriodicCenterStrip":
        (evidence / f"{module}.lean").write_bytes(data)
    manifest.append({"module": module, "path": path, "sha256": expected})
controls = Path(__file__).with_name("CenterControls.lean").read_bytes()
(build / "CenterControls.lean").write_bytes(controls)
(evidence / "CenterControls.lean").write_bytes(controls)
(evidence / "sources.json").write_text(json.dumps(manifest, indent=2) + "\n")

version = subprocess.run([args.lean, "--version"], text=True, capture_output=True, check=True)
(evidence / "version.log").write_text(version.stdout + version.stderr)
if "version 4.19.0" not in version.stdout or "6caaee842e94" not in version.stdout:
    raise RuntimeError("Unexpected Lean version")
compiler_sha = sha(Path(args.lean).read_bytes())
if compiler_sha != "92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023":
    raise RuntimeError("Unexpected compiler hash")

results = []
env = dict(os.environ, LEAN_PATH=str(build))
for module in [m for m, _, _ in modules] + ["CenterControls"]:
    cmd = [args.lean, "--trust=0", "-j1", "-DElab.async=false",
           "-o", f"{module}.olean", f"{module}.lean"]
    started = time.time()
    r = subprocess.run(cmd, cwd=build, env=env, text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (evidence / f"{module}.log").write_text(r.stdout)
    results.append({"module": module, "command": cmd, "exit_code": r.returncode,
                    "seconds": time.time() - started, "log_sha256": sha(r.stdout.encode())})
    (evidence / "commands.json").write_text(json.dumps(results, indent=2) + "\n")
    print(f"{module}: exit {r.returncode}", flush=True)
    if r.returncode:
        print(r.stdout, end="")
        raise SystemExit(r.returncode)

source = (build / "Agent1PeriodicCenterStrip.lean").read_text()
exports = re.findall(r"^(?:def|theorem)\s+(\w+)", source, re.M)
expected = ["stripPeriodMiddle", "stripPeriodMiddle_wrap", "stripPeriodCenter_test_iff",
            "stripPeriodCenterAux", "stripPeriodCenter", "stripPeriodCenter_empty",
            "stripPeriodCenterAux_decomposition", "stripPeriodMiddle_length_lt",
            "stripPeriodCenterAux_maximal", "stripPeriodCenter_decomposition",
            "stripPeriodCenter_maximal", "stripPeriodCenter_length",
            "stripPeriodCenter_length_le", "stripPeriodCenter_bounded",
            "stripPeriodCenter_symmetric"]
if exports != expected:
    raise RuntimeError(f"Unexpected explicit export inventory: {exports}")
for bad in ("sorry", "admit", "native_decide", "Lean.ofReduceBool", "unsafe", "axiom "):
    if bad in source:
        raise RuntimeError(f"Forbidden source token: {bad}")

audit = (evidence / "Agent1PeriodicCenterStrip.log").read_text()
parsed = re.findall(r"'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)", audit)
if [name for name, _ in parsed] != ["Agent1.Periodic." + n for n in exports]:
    raise RuntimeError("Missing, duplicate, or unexpected explicit-export axiom print")
axioms = set()
for _, values in parsed:
    axioms.update(x.strip() for x in values.split(",") if x.strip())
if not axioms <= {"propext", "Classical.choice", "Quot.sound"}:
    raise RuntimeError(f"Unexpected transitive axioms: {sorted(axioms)}")
control_log = (evidence / "CenterControls.log").read_text()
if control_log.count("does not depend on any axioms") != 6:
    raise RuntimeError("Expected six kernel-checked, axiom-free control theorems")
for module, path, expected_sha in modules:
    if sha((root / path).read_bytes()) != expected_sha or sha((build / f"{module}.lean").read_bytes()) != expected_sha:
        raise RuntimeError(f"Source drift: {path}")

(evidence / "verification.json").write_text(json.dumps({
    "status": "PASS", "scope": "Author clean replay; independent review not implied",
    "fresh_empty_build_directory": True, "project_object_reuse": False,
    "modules_compiled": len(modules), "control_module_compiled": True,
    "explicit_exports": exports, "explicit_export_count": len(exports),
    "theorem_count": len(re.findall(r"^theorem\s", source, re.M)),
    "definition_count": len(re.findall(r"^def\s", source, re.M)),
    "axiom_union": sorted(axioms), "kernel_control_theorems": 6,
    "source_drift": False, "compiler_version": version.stdout.strip(),
    "compiler_sha256": compiler_sha, "runner_sha256": sha(Path(__file__).read_bytes()),
    "controls_sha256": sha(controls), "build_dir": str(build),
    "base_commit": "95a17ceeaba51b7d2c14645401df5159a3d483d1",
    "claim_commit": "9f5d29396d3f1c379c504572c2f7189a6a96b729",
}, indent=2) + "\n")
print("PASS: eleven fresh modules; fifteen explicit exports; six semantic controls", flush=True)
