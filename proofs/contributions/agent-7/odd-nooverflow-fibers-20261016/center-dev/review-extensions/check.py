"""Independent fresh-kernel review of the frozen fixed-center/phase extensions."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import re
import subprocess

root = Path(__file__).resolve().parent
source = root / "source"
tool = Path("/workspace/scratch/aaafdd394dd6/agent7-runtime/lean-4.19.0-linux/bin/lean")
modules = ["InverseFibers", "PathCounts", "WordBridge", "OddCenter", "OddCounts",
           "OddCountsFixedCenter", "OddCountsPhase", "BoundaryControls", "AllExportsAudit"]
env = dict(os.environ, LEAN_PATH=str(source))
pins = json.loads((root / "source-sha256.json").read_text())
for mod, pin in pins.items():
    actual = hashlib.sha256((source / (mod + ".lean")).read_bytes()).hexdigest()
    assert actual == pin["sha256"], (mod, actual, pin["sha256"])
assert not list(source.glob("*.olean")), "Fresh review requires no preexisting local objects."
version = subprocess.run([str(tool), "--version"], text=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, check=True)
(root / "compiler-version.log").write_text(version.stdout)
records = []
for mod in modules:
    command = [str(tool), "--trust=0", "-j1", "-DElab.async=false", "-o",
               str(source / (mod + ".olean")), str(source / (mod + ".lean"))]
    result = subprocess.run(command, cwd=source, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (root / (mod + ".log")).write_text(result.stdout)
    records.append({"module": mod, "command": command, "cwd": str(source),
                    "exit_code": result.returncode,
                    "log_sha256": hashlib.sha256(result.stdout.encode()).hexdigest()})
    print(mod, "PASS" if result.returncode == 0 else "FAIL", flush=True)
    if result.returncode:
        print(result.stdout, flush=True)
        break
all_passed = len(records) == len(modules) and all(r["exit_code"] == 0 for r in records)
(root / "results.json").write_text(json.dumps({
    "completed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "lean_sha256": hashlib.sha256(tool.read_bytes()).hexdigest(),
    "records": records, "all_passed": all_passed}, indent=2) + "\n")
if not all_passed:
    raise SystemExit(1)
audit_log = (root / "AllExportsAudit.log").read_text()
allowed = {"propext", "Classical.choice", "Quot.sound"}
observed = set()
for group in re.findall(r"depends on axioms: \[([^\]]*)\]", audit_log):
    observed.update(x.strip() for x in group.split(",") if x.strip())
exports = json.loads((root / "exported-theorems.json").read_text())
reported = len(re.findall(r"^'P196\.Agent7\.OddFibers\.[^']+' (?:depends on axioms:|does not depend on any axioms)",
                          audit_log, re.MULTILINE))
axioms_passed = observed <= allowed and reported == exports["total"]
(root / "axiom-audit.json").write_text(json.dumps({
    "export_count": exports["total"], "reported_count": reported,
    "axiom_union": sorted(observed), "unexpected_axioms": sorted(observed - allowed),
    "all_passed": axioms_passed}, indent=2) + "\n")
print("All extension exports audited:", reported, "PASS" if axioms_passed else "FAIL", flush=True)
raise SystemExit(0 if axioms_passed else 1)
