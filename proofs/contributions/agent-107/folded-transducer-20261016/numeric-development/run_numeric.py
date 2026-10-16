#!/usr/bin/env python3
"""Retain an exact Numeric-module author check and its dependency hashes."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT.parent
SOURCE = ROOT / "proofs" / "Agent107TransducerNumeric.lean"
BUILD = BASE / "agent107-path-build"
LEAN = BASE / "agent107-runtime" / "lean-4.19.0-linux" / "bin" / "lean"
EVIDENCE = Path(__file__).resolve().parent / sys.argv[1]
EVIDENCE.mkdir(exist_ok=False)
BUILD.mkdir(exist_ok=True)
source_bytes = SOURCE.read_bytes()
(EVIDENCE / SOURCE.name).write_bytes(source_bytes)
cmd = [str(LEAN), "--trust=0", "-j1", "-DElab.async=false", "-o",
       str(BUILD / "Agent107TransducerNumeric.olean"), str(SOURCE)]
env = os.environ.copy()
env["LEAN_PATH"] = ":".join(str(p) for p in
    [BUILD, BASE / "agent107-build", BASE / "agent107-runtime" / "baseline"])
dependencies = {}
for module in ["Agent107TransducerDefs", "Agent107TransducerPath",
               "Agent107TransducerInput", "Agent107TransducerOutput"]:
    path = ROOT / "proofs" / (module + ".lean")
    dependencies[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
started = time.monotonic()
result = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True)
(EVIDENCE / "compiler.stdout.log").write_bytes(result.stdout)
(EVIDENCE / "compiler.stderr.log").write_bytes(result.stderr)
record = {
    "executor": "Agent #107 delegated path/input/numeric author",
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "command": cmd,
    "cwd": str(ROOT),
    "lean_path": env["LEAN_PATH"],
    "source": str(SOURCE.relative_to(ROOT)),
    "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
    "dependency_sources_sha256": dependencies,
    "exit_code": result.returncode,
    "seconds": round(time.monotonic() - started, 6),
    "review_status": "Author check; imports already-built dependency oleans, not independent closure rebuild."
}
(EVIDENCE / "execution.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, ensure_ascii=False))
print(result.stdout.decode(), end="")
print(result.stderr.decode(), end="")
raise SystemExit(result.returncode)
