#!/usr/bin/env python3
"""Build manifest-listed split row proofs, then their unchanged-target wrappers."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('--lean', required=True)
p.add_argument('--build', required=True)
p.add_argument('--inverse-build', required=True)
p.add_argument('--tag', default='split01')
p.add_argument('batches', nargs='*')
a = p.parse_args()
here = Path(__file__).resolve().parent
manifest = json.loads((here / 'split-batches.json').read_text())
for name in a.batches or sorted(manifest):
    cmd = [sys.executable, str(here / 'build_checks.py'), '--lean', a.lean,
           '--build', a.build, '--inverse-build', a.inverse_build,
           '--seconds', '240', '--tag', a.tag, *manifest[name], name]
    result = subprocess.run(cmd)
    if result.returncode:
        raise SystemExit(result.returncode)
