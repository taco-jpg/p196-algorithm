#!/usr/bin/env python3
"""Retain isolated actual-bridge development builds and exact command evidence."""
from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument('--attempt', required=True)
parser.add_argument('--reuse', help='Reuse only pinned dependency objects from this previous attempt')
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent
out = root / 'actual-dev' / args.attempt
out.mkdir(exist_ok=False)
source = out / 'source'
source.mkdir()
logs = out / 'logs'
logs.mkdir()
lean = Path('/workspace/scratch/aaafdd394dd6/agent7-runtime/lean-4.19.0-linux/bin/lean')
order = ['InverseFibers', 'PathCounts', 'WordBridge', 'PeriodObstructions', 'ActualWords', 'OddCenter', 'OddActual']
records = []
sha = lambda data: hashlib.sha256(data).hexdigest()
pins = {p['file']: p for p in json.loads((root / 'dependencies/SOURCE_PINS.json').read_text())}
for module in order:
    original = root / (module + '.lean') if module in {'OddCenter', 'OddActual'} else root / 'dependencies' / (module + '.lean')
    data = original.read_bytes()
    if original.name in pins:
        assert sha(data) == pins[original.name]['sha256']
    (source / original.name).write_bytes(data)
    records.append({'module': module, 'original': str(original), 'sha256': sha(data)})

report = {
    'agent': 7,
    'role': 'odd actual arithmetic bridge specialist',
    'started_at': datetime.now(timezone.utc).isoformat(),
    'status': 'RUNNING',
    'lean': str(lean),
    'lean_sha256': sha(lean.read_bytes()),
    'source_records': records,
    'commands': [],
    'reuse_attempt': args.reuse,
}
def save():
    (out / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')

if args.reuse:
    previous = root / 'actual-dev' / args.reuse
    old = json.loads((previous / 'verification.json').read_text())
    if old['lean_sha256'] != report['lean_sha256']:
        raise SystemExit('Compiler mismatch in requested development dependency reuse')
    previous_records = {rec['module']: rec for rec in old['source_records']}
    for rec in records[:-1]:
        module = rec['module']
        if previous_records[module]['sha256'] != rec['sha256']:
            raise SystemExit('Source mismatch in requested dependency reuse: ' + module)
        old_object = previous / 'source' / (module + '.olean')
        shutil.copyfile(old_object, source / old_object.name)
        rec['reused_object_sha256'] = sha(old_object.read_bytes())

env = dict(os.environ)
env['LEAN_PATH'] = str(source)
env['PATH'] = str(lean.parent) + ':/usr/bin:/bin'
save()
for module in (order[-1:] if args.reuse else order):
    command = [str(lean), '--trust=0', '-j1', '-DElab.async=false', '-o', module + '.olean', module + '.lean']
    log = logs / (module + '.log')
    start = time.monotonic()
    with log.open('wb') as stream:
        result = subprocess.run(command, cwd=source, env=env, stdout=stream, stderr=subprocess.STDOUT)
    report['commands'].append({'module': module, 'command': command, 'cwd': str(source), 'exit_code': result.returncode,
        'elapsed_seconds': time.monotonic() - start, 'log': str(log), 'log_sha256': sha(log.read_bytes())})
    save()
    print(module + ' exit=' + str(result.returncode), flush=True)
    if result.returncode:
        report['status'] = 'FAIL'
        report['failed_module'] = module
        report['finished_at'] = datetime.now(timezone.utc).isoformat()
        save()
        print(log.read_text(), flush=True)
        raise SystemExit(result.returncode)
report['status'] = 'PASS'
report['finished_at'] = datetime.now(timezone.utc).isoformat()
for rec in records:
    rec['object_sha256'] = sha((source / (rec['module'] + '.olean')).read_bytes())
save()
print((logs / 'OddActual.log').read_text(), flush=True)
