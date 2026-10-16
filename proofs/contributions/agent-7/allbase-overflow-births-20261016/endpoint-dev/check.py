"""Fresh pinned closure, endpoint proof, boundary controls and all-export audit."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

root = Path(__file__).resolve().parent
contribution = root.parent
attempt = root / sys.argv[1]
source = attempt / "source"
source.mkdir(parents=True, exist_ok=False)
tool = Path("/workspace/scratch/aaafdd394dd6/agent7-runtime/lean-4.19.0-linux/bin/lean")
dependencies = ["SignedDigitUniqueness", "BaseReflection", "ResetNormalization", "PhysicalWidth",
                "SeamSafety", "ReverseAdd", "BaseBirths", "ActualBaseBirths"]
modules = dependencies + ["OverflowDigits", "OverflowEndpoints", "EndpointBoundaryControls", "AllExportsAudit"]
dependency_pins = json.loads((contribution / "dependencies" / "SOURCE_PINS.json").read_text())
by_name = {r["module"]: r for r in dependency_pins["dependencies"]}
by_name["OverflowDigits"] = {"sha256": "37926723ba9d0d95b567f27607a810ea40d4fc622d60571d79228a5d33f33f8f"}
pins = {}
for mod in modules[:-1]:
    origin = contribution / "dependencies" if mod in dependencies else root if mod == "EndpointBoundaryControls" else contribution
    original = origin / (mod + ".lean")
    digest = hashlib.sha256(original.read_bytes()).hexdigest()
    if mod in by_name:
        assert digest == by_name[mod]["sha256"], mod
    shutil.copyfile(original, source / (mod + ".lean"))
    pins[mod] = {"original": str(original), "sha256": digest}
exports = []
for mod, namespace in [("OverflowEndpoints", "P196.Agent7.AllBaseOverflow"),
                       ("EndpointBoundaryControls", "P196.Agent7.AllBaseOverflow.EndpointControls")]:
    names = re.findall(r"^theorem\s+(\w+)", (source / (mod + ".lean")).read_text(), re.MULTILINE)
    exports.extend(namespace + "." + name for name in names)
audit_source = "import EndpointBoundaryControls\n\n" + "\n".join("#print axioms " + name for name in exports) + "\n"
(source / "AllExportsAudit.lean").write_text(audit_source)
pins["AllExportsAudit"] = {"generated_from": exports, "sha256": hashlib.sha256(audit_source.encode()).hexdigest()}
(attempt / "source-sha256.json").write_text(json.dumps(pins, indent=2) + "\n")
version = subprocess.run([str(tool), "--version"], text=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, check=True)
(attempt / "compiler-version.log").write_text(version.stdout)
records = []
for mod in modules:
    command = [str(tool), "--trust=0", "-j1", "-DElab.async=false", "-o",
               str(source / (mod + ".olean")), str(source / (mod + ".lean"))]
    result = subprocess.run(command, cwd=source, env=dict(os.environ, LEAN_PATH=str(source)),
                            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (attempt / (mod + ".log")).write_text(result.stdout)
    records.append({"module": mod, "command": command, "cwd": str(source),
                    "exit_code": result.returncode,
                    "log_sha256": hashlib.sha256(result.stdout.encode()).hexdigest()})
    print(mod, "PASS" if result.returncode == 0 else "FAIL", flush=True)
    if result.returncode:
        print(result.stdout, flush=True)
        break
passed = len(records) == len(modules) and all(r["exit_code"] == 0 for r in records)
audits = {}
if passed:
    audit_log = (attempt / "AllExportsAudit.log").read_text()
    for name, values in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", audit_log):
        audits[name] = [s.strip() for s in values.split(",") if s.strip()]
    for name in re.findall(r"'([^']+)' does not depend on any axioms", audit_log):
        audits[name] = []
    allowed = {"propext", "Classical.choice", "Quot.sound"}
    audit_passed = set(audits) == set(exports) and all(set(a).issubset(allowed) for a in audits.values())
    (attempt / "axiom-audit.json").write_text(json.dumps({
        "all_export_declarations": exports, "reports": audits, "passed": audit_passed,
        "allowed_axioms": sorted(allowed)}, indent=2) + "\n")
    passed = passed and audit_passed
(attempt / "verification.json").write_text(json.dumps({
    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "lean_sha256": hashlib.sha256(tool.read_bytes()).hexdigest(),
    "source_snapshots": pins, "records": records, "all_passed": passed}, indent=2) + "\n")
raise SystemExit(0 if passed else 1)
