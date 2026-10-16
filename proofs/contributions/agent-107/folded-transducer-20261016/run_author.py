#!/usr/bin/env python3
"""Retain one exact development attempt; this is not the release verifier."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parents[4]
parser = argparse.ArgumentParser()
parser.add_argument('--lean', type=Path, required=True)
parser.add_argument('--module', required=True)
parser.add_argument('--build', type=Path, required=True)
parser.add_argument('--dependency', type=Path, action='append', default=[])
parser.add_argument('--evidence', type=Path, required=True)
args = parser.parse_args()
if not args.module.replace('_', '').isalnum():
    raise SystemExit('Invalid module')
args.evidence.mkdir(parents=True, exist_ok=False)
args.build.mkdir(parents=True, exist_ok=True)
source = ROOT / 'proofs' / (args.module + '.lean')
data = source.read_bytes()
(args.evidence / (args.module + '.lean')).write_bytes(data)
target = args.build / (args.module + '.lean')
target.write_bytes(data)
command = [str(args.lean.resolve()), '--trust=0', '-j1', '-DElab.async=false',
           '-o', args.module + '.olean', args.module + '.lean']
env = os.environ.copy()
env['LEAN_PATH'] = ':'.join(str(p.resolve()) for p in [args.build, *args.dependency])
started = time.monotonic()
out = subprocess.run(command, cwd=args.build, env=env, capture_output=True)
(args.evidence / 'compiler.stdout.log').write_bytes(out.stdout)
(args.evidence / 'compiler.stderr.log').write_bytes(out.stderr)
record = {'executor': 'Agent #107 root author', 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'command': command, 'cwd': str(args.build.resolve()), 'lean_path': env['LEAN_PATH'],
          'source': str(source.relative_to(ROOT)), 'source_sha256': hashlib.sha256(data).hexdigest(),
          'source_git_blob': hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest(),
          'exit_code': out.returncode, 'seconds': round(time.monotonic() - started, 6),
          'source_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()}
(args.evidence / 'execution.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, ensure_ascii=False))
print(out.stdout.decode(), end='')
print(out.stderr.decode(), end='')
raise SystemExit(out.returncode)
