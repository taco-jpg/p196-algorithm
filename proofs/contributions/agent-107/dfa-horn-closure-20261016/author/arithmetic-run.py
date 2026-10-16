#!/usr/bin/env python3
"""Retain one exact delegated Horn-arithmetic author check, including failures."""
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
SOURCE = ROOT / "proofs/Agent107DFAArithmetic.lean"
BUILD = BASE / "agent107-horn-arithmetic-build"
LEAN = BASE / "agent107-runtime/lean-4.19.0-linux/bin/lean"
EVIDENCE = Path(__file__).resolve().parent / sys.argv[1]
if not EVIDENCE.name.startswith("arithmetic-"):
    raise SystemExit("Use a fresh arithmetic-* evidence name")
EVIDENCE.mkdir(exist_ok=False)
BUILD.mkdir(exist_ok=True)
data = SOURCE.read_bytes()
(EVIDENCE / SOURCE.name).write_bytes(data)
cmd = [str(LEAN), "--trust=0", "-j1", "-DElab.async=false", "-o",
       str(BUILD / "Agent107DFAArithmetic.olean"), str(SOURCE)]
env = os.environ.copy()
env["LEAN_PATH"] = ":".join(str(p) for p in [BUILD, BASE / "agent107-horn-path-build", BASE / "agent107-horn-build",
    BASE / "agent107-runtime/reviewer-empty-_z2f9ejb"])
started = time.monotonic()
result = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True)
(EVIDENCE / "compiler.stdout.log").write_bytes(result.stdout)
(EVIDENCE / "compiler.stderr.log").write_bytes(result.stderr)
record = {
    "executor": "Agent #107 scope_scout delegated Horn-arithmetic author",
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "command": cmd, "cwd": str(ROOT), "lean_path": env["LEAN_PATH"],
    "source": str(SOURCE.relative_to(ROOT)),
    "source_sha256": hashlib.sha256(data).hexdigest(),
    "dependency_source_sha256": hashlib.sha256((ROOT / "proofs/Agent107DFAHorn.lean").read_bytes()).hexdigest(),
    "exit_code": result.returncode,
    "elapsed_seconds": round(time.monotonic() - started, 6),
    "verification_scope": "Author check of Agent107DFAArithmetic; imports frozen previously checked dependencies. Not an independent closure rebuild."
}
(EVIDENCE / "execution.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, ensure_ascii=False))
print(result.stdout.decode(), end="")
print(result.stderr.decode(), end="")
raise SystemExit(result.returncode)
