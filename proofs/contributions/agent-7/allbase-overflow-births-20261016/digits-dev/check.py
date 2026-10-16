"""Fresh build of the fixed all-base imports and one retained digit-bridge draft."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys

root = Path(__file__).resolve().parent
contribution = root.parent
attempt = root / sys.argv[1]
source = attempt / "source"
source.mkdir(parents=True, exist_ok=False)
tool = Path("/workspace/scratch/aaafdd394dd6/agent7-runtime/lean-4.19.0-linux/bin/lean")
modules = ["SignedDigitUniqueness", "BaseReflection", "ResetNormalization", "PhysicalWidth",
           "SeamSafety", "ReverseAdd", "BaseBirths", "ActualBaseBirths", "OverflowDigits"]
dependency_pins = json.loads((contribution / "dependencies" / "SOURCE_PINS.json").read_text())
by_name = {r["module"]: r for r in dependency_pins["dependencies"]}
pins = {}
for mod in modules:
    original = (contribution if mod == "OverflowDigits" else contribution / "dependencies") / (mod + ".lean")
    digest = hashlib.sha256(original.read_bytes()).hexdigest()
    if mod in by_name:
        assert digest == by_name[mod]["sha256"], mod
    shutil.copyfile(original, source / (mod + ".lean"))
    pins[mod] = {"original": str(original), "sha256": digest}
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
(attempt / "verification.json").write_text(json.dumps({
    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "lean_sha256": hashlib.sha256(tool.read_bytes()).hexdigest(),
    "source_snapshots": pins, "records": records, "all_passed": passed}, indent=2) + "\n")
raise SystemExit(0 if passed else 1)
