#!/usr/bin/env python3
"""Incremental author checks; every attempt retains exact source and output."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[4]
BUILD = Path('/tmp/agent104-mass-author')
LEAN = Path('/workspace/scratch/a1d46b1077ac/agent103-runtime/toolchain/lean-4.19.0-linux/bin/lean')
name = sys.argv[1]
source = ROOT / (sys.argv[2] if len(sys.argv) > 2 else name + '.lean')
attempts = Path(__file__).resolve().parent / name
attempts.mkdir(parents=True, exist_ok=True)
n = 1
while (attempts / f'attempt-{n:03d}').exists():
    n += 1
dest = attempts / f'attempt-{n:03d}'
dest.mkdir()
BUILD.mkdir(parents=True, exist_ok=True)
shutil.copy2(source, dest / source.name)
shutil.copy2(source, BUILD / (name + '.lean'))
command = [str(LEAN), '--trust=0', '-j1', '-DElab.async=false', '-o', name + '.olean', name + '.lean']
env = dict(os.environ, LEAN_PATH=str(BUILD))
t0 = time.monotonic()
with (dest / 'lean.log').open('w') as out:
    proc = subprocess.run(command, cwd=BUILD, env=env, stdout=out, stderr=subprocess.STDOUT)
record = {'command': command, 'cwd': str(BUILD), 'LEAN_PATH': str(BUILD),
          'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
          'elapsed_seconds': time.monotonic() - t0, 'exit_code': proc.returncode,
          'verification_level': 'incremental author check; reused independently pinned base olean'}
(dest / 'result.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record))
print((dest / 'lean.log').read_text())
sys.exit(proc.returncode)
