#!/usr/bin/env python3
"""Retain every author attempt of the structural finite-domain coverage proof."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

root = Path(__file__).resolve().parents[4]
name = 'Agent104Prefix620DataCoverage'
source = root / (name + '.lean')
build = Path('/tmp/agent104-prefix620-author')
dest = Path(__file__).resolve().parent / 'coverage'
dest.mkdir(exist_ok=True)
n = 1
while (dest / f'attempt-{n:03d}').exists():
    n += 1
dest = dest / f'attempt-{n:03d}'
dest.mkdir()
shutil.copy2(source, dest / source.name)
shutil.copy2(source, build / source.name)
lean = '/workspace/scratch/a1d46b1077ac/agent103-runtime/toolchain/lean-4.19.0-linux/bin/lean'
cmd = [lean, '--trust=0', '-j1', '-DElab.async=false', '-o', name + '.olean', name + '.lean']
t = time.monotonic()
with (dest / 'lean.log').open('w') as log:
    result = subprocess.run(cmd, cwd=build, env=dict(os.environ, LEAN_PATH=str(build)), stdout=log, stderr=subprocess.STDOUT)
record = {'command': cmd, 'cwd': str(build), 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
          'exit_code': result.returncode, 'elapsed_seconds': time.monotonic() - t,
          'verification_level': 'incremental author proof check; pinned base oleans reused'}
(dest / 'result.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record))
print((dest / 'lean.log').read_text())
raise SystemExit(result.returncode)
