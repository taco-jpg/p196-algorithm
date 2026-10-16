#!/usr/bin/env python3
"""Rebuild the complete Agent #108 proof chain from source in a fresh directory."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('lean', type=Path, help='absolute Lean 4.19.0 executable')
p.add_argument('--build-root', type=Path, required=True)
p.add_argument('--preload', type=Path, help='optional documented PID-namespace adapter')
p.add_argument('--phase', default='complete-package')
a = p.parse_args()
base = Path(__file__).resolve().parent
repo = base.parents[3]
modules = ['AutonomyDefs', 'AutonomyBasic', 'DigitPerturbation', 'LeadingWitness',
           'Necessity', 'ModularAutonomy', 'CounterexampleBound']
manifest = json.loads((base / 'SOURCE_MANIFEST.json').read_text())
for rel, expected in manifest['source_sha256'].items():
    actual = hashlib.sha256((repo / rel).read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(f'Source mismatch: {rel}: {actual} != {expected}')
lean = a.lean.resolve()
cmd = [sys.executable, str(base / 'review/clean/clean_rebuild.py'),
       '--repo', str(repo), '--lean-root', str(lean.parent.parent),
       '--build-root', str(a.build_root.resolve()), '--phase', a.phase,
       '--modules', *modules]
if a.preload:
    cmd += ['--preload', str(a.preload.resolve())]
env = dict(os.environ)
env.pop('LD_PRELOAD', None)
raise SystemExit(subprocess.call(cmd, env=env))
