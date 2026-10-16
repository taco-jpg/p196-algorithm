"""Retain each genuine author attempt before invoking pinned Lean's kernel."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument("module")
parser.add_argument("--dependency-dir", action="append", default=[])
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
source = root / "agent6-checker/proofs/contributions/agent-6/certificate-coordinate-audit-20261016" / (args.module + ".lean")
attempts = root / "agent6-checker-dev/attempts"
attempts.mkdir(parents=True, exist_ok=True)
number = len(list(attempts.glob(args.module + "-*"))) + 1
attempt = attempts / f"{args.module}-{number:03d}"
attempt.mkdir()
raw = source.read_bytes()
(attempt / source.name).write_bytes(raw)
objects = root / "agent6-checker-dev/objects"
objects.mkdir(exist_ok=True)
lean = root / "runtime-agent6/lean-4.19.0-linux/bin/lean"
paths = [str(objects)] + args.dependency_dir
env = dict(os.environ)
env["LEAN_PATH"] = os.pathsep.join(paths)
command = [str(lean), "--trust=0", "-j1", "-DElab.async=false", "-o", str(objects / (args.module + ".olean")), str(attempt / source.name)]
started = time.time()
with (attempt / "compile.log").open("wb") as log:
    result = subprocess.run(command, cwd=attempt, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=240)
record = {"actor": "Agent #6", "role": "author", "module": args.module,
          "source_path": str(source), "source_sha256": hashlib.sha256(raw).hexdigest(),
          "compiler_sha256": hashlib.sha256(lean.read_bytes()).hexdigest(),
          "argv": command, "cwd": str(attempt), "lean_path": paths,
          "started_unix": started, "elapsed_seconds": time.time() - started,
          "exit_code": result.returncode}
(attempt / "verification.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, indent=2))
print((attempt / "compile.log").read_text())
raise SystemExit(result.returncode)
