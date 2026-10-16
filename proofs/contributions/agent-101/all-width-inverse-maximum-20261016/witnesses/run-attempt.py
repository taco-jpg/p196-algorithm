#!/usr/bin/env python3
"""Freeze one real witness-source attempt and record its incremental Lean run."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import time

repo = Path('/workspace/scratch/2a8a87fd78df/p196-agent101')
packet = Path(__file__).resolve().parent
label = sys.argv[1]
if not label.startswith('attempt-') or not label[8:].isdigit():
    raise SystemExit('expected attempt-NNN')
evidence = packet / label
evidence.mkdir(exist_ok=False)
build = Path('/workspace/scratch/2a8a87fd78df/agent101-maximum-witness-build-01') / label
build.mkdir(exist_ok=False)
source = repo / 'proofs/Agent101MaximumWitnesses.lean'
data = source.read_bytes()
(evidence / source.name).write_bytes(data)
(build / source.name).write_bytes(data)
lean = '/workspace/scratch/2a8a87fd78df/agent101-runtime/toolchain/lean-4.19.0-linux/bin/lean'
base = '/workspace/scratch/2a8a87fd78df/agent101-generic-closure-bbbcc857/agent101-nonpalindromic-fibers/source'
dependencies = str(build.parent)
env = os.environ.copy()
env['LEAN_PATH'] = str(build) + ':' + dependencies + ':' + base
command = [lean, '--trust=0', '-j1', '-DElab.async=false', '-o', 'Agent101MaximumWitnesses.olean', source.name]
start = time.monotonic()
p = subprocess.run(command, cwd=build, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
elapsed = time.monotonic() - start
(evidence / 'compile.log').write_bytes(p.stdout)
result = {'status': 'PASS' if p.returncode == 0 else 'FAIL', 'command': command,
          'cwd': str(build), 'lean_path': env['LEAN_PATH'], 'exit_code': p.returncode,
          'seconds': elapsed, 'source_sha256': hashlib.sha256(data).hexdigest(),
          'log_sha256': hashlib.sha256(p.stdout).hexdigest(),
          'incremental': True, 'base_rebuilt': False}
(evidence / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2), flush=True)
print(p.stdout.decode(), flush=True)
sys.exit(p.returncode)
