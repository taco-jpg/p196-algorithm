#!/usr/bin/env python3
"""Record a real incremental Lean author attempt without replacing older evidence."""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument('attempt')
args = parser.parse_args()
evidence = Path(__file__).resolve().parent
attempt = evidence / args.attempt
source = attempt / 'BinaryBlockCounts.lean'
if (attempt / 'verification.json').exists():
    raise SystemExit('Refusing to overwrite an executed attempt')
workspace = Path('/workspace/scratch/4ce7c54d31f6')
lean = workspace / 'lean-runtime/lean-4.19.0-linux/bin/lean'
cache = workspace / 'agent3-depth-canonical-build-001/modules'
build = workspace / 'agent3-prefix-counting-build'
build.mkdir(exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
source_hash = sha(source)
shutil.copy2(source, build / source.name)
env = dict(os.environ)
for key in ['LEAN_PATH', 'LEAN_SRC_PATH', 'LEAN_SYSROOT', 'LEAN_OPTS']:
    env.pop(key, None)
env['LEAN_PATH'] = str(build) + ':' + str(cache)
command = [str(lean), '--trust=0', '-o', 'BinaryBlockCounts.olean', source.name]
start = time.monotonic()
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
result = subprocess.run(command, cwd=build, env=env, stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT, text=True, timeout=180)
(attempt / 'compile.log').write_text(result.stdout)
decls = re.findall(r'^(?:def|theorem)\s+([A-Za-z0-9_]+)', source.read_text(), re.M)
audited = re.findall(r"^'([^']+)' (?:depends on axioms:|does not depend on any axioms)", result.stdout, re.M)
axioms = sorted({a.strip() for group in re.findall(r'depends on axioms: \[([^\]]*)\]', result.stdout) for a in group.split(',') if a.strip()})
expected = ['P196.Agent3.PrefixContraction.BinaryCount.' + n for n in decls]
record = {'stage': 'incremental author check with explicitly inherited dependency objects',
          'started_utc': started, 'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'source': str(source), 'source_sha256': source_hash,
          'source_unchanged': source_hash == sha(source),
          'lean': str(lean), 'lean_sha256': sha(lean),
          'dependency_cache': str(cache),
          'dependency_source_commit': '8a67ea8204757cc4f80bf5f576e2cc8024bea97b',
          'dependency_pin_manifest': str(workspace / 'p196-prefix/proofs/contributions/agent-3/three-layer-prefix-20261016/verification/source-pins.json'),
          'command': command, 'cwd': str(build), 'LEAN_PATH': env['LEAN_PATH'],
          'exit_code': result.returncode, 'elapsed_seconds': time.monotonic() - start,
          'explicit_declarations': expected, 'printed_declarations': audited,
          'axiom_union': axioms, 'full_explicit_audit': sorted(expected) == sorted(audited),
          'log_sha256': sha(attempt / 'compile.log')}
ok = result.returncode == 0 and record['source_unchanged'] and record['full_explicit_audit']
ok = ok and set(axioms) <= {'Classical.choice', 'Quot.sound', 'propext'}
ok = ok and 'sorryAx' not in result.stdout and 'Lean.ofReduceBool' not in result.stdout
record['status'] = 'LEAN-CHECKED' if ok else 'FAILED'
(attempt / 'verification.json').write_text(json.dumps(record, indent=2) + '\n')
print(result.stdout, end='')
print(json.dumps({k: record[k] for k in ['status', 'exit_code', 'elapsed_seconds', 'full_explicit_audit', 'axiom_union']}))
raise SystemExit(0 if ok else result.returncode or 1)
