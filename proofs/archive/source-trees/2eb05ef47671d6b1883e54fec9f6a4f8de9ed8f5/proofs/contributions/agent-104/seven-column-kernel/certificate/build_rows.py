#!/usr/bin/env python3
"""Run independent finite-row modules with at most two single-worker compilers."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import json
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('--lean', required=True)
p.add_argument('--build', required=True)
p.add_argument('--inverse-build', required=True)
p.add_argument('--workers', type=int, choices=[1, 2], default=2)
p.add_argument('--start', type=int, default=0)
p.add_argument('--stop', type=int, default=256)
p.add_argument('--tag', default='kernel01')
a = p.parse_args()
here = Path(__file__).resolve().parent
build = Path(a.build).resolve()

def run(i):
    name = f'Rows739_{i:03d}'
    cmd = [sys.executable, str(here / 'run_lean.py'), '--lean', a.lean,
           '--lean-path', str(build) + ':' + a.inverse_build,
           '--seconds', '300', '--output', str(build / (name + '.olean')),
           '--log', str(here / (name + '-' + a.tag + '.log')),
           str(here / (name + '.lean'))]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {'module': name, 'exit_code': result.returncode,
            'resources': result.stdout.strip(), 'stderr': result.stderr.strip()}

failed = []
with ThreadPoolExecutor(max_workers=a.workers) as pool:
    futures = [pool.submit(run, i) for i in range(a.start, a.stop)]
    for future in as_completed(futures):
        record = future.result()
        print(json.dumps(record), flush=True)
        if record['exit_code']:
            failed.append(record['module'])
if failed:
    print(json.dumps({'failed': failed}), flush=True)
    raise SystemExit(1)
