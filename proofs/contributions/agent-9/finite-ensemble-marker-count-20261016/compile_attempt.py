#!/usr/bin/env python3
"""Retain each author compiler attempt before invoking official Lean."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime, timezone

package = Path(__file__).resolve().parent
module = sys.argv[1]
source = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else package / (module + '.lean')
build = Path('/workspace/scratch/8dcaf4a67fa4/agent9-ensemble-author/dev')
lean = Path('/tmp/p196-agent5-lean/lean-4.19.0-linux/bin/lean')
root = package / 'development' / module
root.mkdir(parents=True, exist_ok=True)
build.mkdir(parents=True, exist_ok=True)
seq = 1
while (root / f'attempt-{seq:03}').exists():
    seq += 1
report = root / f'attempt-{seq:03}'
report.mkdir()
data = source.read_bytes()
(report / (module + '.lean')).write_bytes(data)
(build / (module + '.lean')).write_bytes(data)
argv = [str(lean), '--trust=0', '-o', str(build / (module + '.olean')), str(build / (module + '.lean'))]
meta = {'module': module, 'source_path': str(source), 'source_sha256': hashlib.sha256(data).hexdigest(),
        'started_at_utc': datetime.now(timezone.utc).isoformat(), 'argv': argv,
        'cwd': str(build), 'LEAN_PATH': str(build), 'status': 'RUNNING'}
(report / 'status.json').write_text(json.dumps(meta, indent=2) + '\n')
env = os.environ.copy()
env['LEAN_PATH'] = str(build)
start = time.monotonic()
result = subprocess.run(argv, cwd=build, env=env, capture_output=True)
(report / 'stdout.log').write_bytes(result.stdout)
(report / 'stderr.log').write_bytes(result.stderr)
meta.update(exit_code=result.returncode, duration_seconds=time.monotonic()-start,
            ended_at_utc=datetime.now(timezone.utc).isoformat(),
            status='PASS' if result.returncode == 0 else 'FAIL')
(report / 'status.json').write_text(json.dumps(meta, indent=2) + '\n')
print(json.dumps(meta, indent=2))
print(result.stdout.decode(), end='')
print(result.stderr.decode(), end='')
sys.exit(result.returncode)
