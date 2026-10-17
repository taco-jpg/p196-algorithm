#!/usr/bin/env python3
"""Run the inspected one-shot packager and retain complete stdout/stderr."""
import datetime
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
command = [sys.executable, "-B", str(root / "package_evidence.py"), "--freeze-confirmed"]
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
with (root / "packaging.stdout").open("xb") as out, (root / "packaging.stderr").open("xb") as err:
    result = subprocess.run(command, cwd=root, stdout=out, stderr=err)
record = {"argv": command, "cwd": str(root), "started_utc": started,
          "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
          "exit_code": result.returncode, "stdout": "packaging.stdout", "stderr": "packaging.stderr",
          "remote_operations": False, "Lean_execution": "NOT_RUN"}
with (root / "packaging-command.json").open("x") as output:
    json.dump(record, output, indent=2)
    output.write("\n")
print(json.dumps(record, indent=2))
raise SystemExit(result.returncode)
