#!/usr/bin/env python3
"""Retain exact source snapshots, commands and logs for a scoped development run."""
from pathlib import Path
import argparse, datetime, hashlib, json, os, shutil, subprocess, time

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--lean', type=Path, required=True)
parser.add_argument('--module', choices=['Agent14SpectralInjectivity', 'Agent14SpectralDecimal'], required=True)
args = parser.parse_args()
here = Path(__file__).resolve().parent
repo = here.parents[3]
modules = {'Agent14SpectralWeights': repo / 'proofs/Agent14SpectralWeights.lean',
           'Agent14SpectralInjectivity': repo / 'proofs/Agent14SpectralInjectivity.lean'}
if args.module == 'Agent14SpectralDecimal':
    modules = {'LychrelDigitSums': repo / 'proofs/LychrelDigitSums__0810ace083af80c5.lean', **modules,
               'Agent14SpectralDecimal': repo / 'proofs/Agent14SpectralDecimal.lean'}
root = here / 'development' / args.module
root.mkdir(parents=True, exist_ok=True)
index = 1
while (root / f'attempt-{index:03d}').exists():
    index += 1
out = root / f'attempt-{index:03d}'
out.mkdir()
source = out / 'source'
source.mkdir()
report = {'status': 'RUNNING', 'started_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'toolchain': str(args.lean), 'sources': {}, 'commands': [],
          'scope': 'Author development only; not independent acceptance.'}
def sha(data):
    return hashlib.sha256(data).hexdigest()
def save():
    (out / 'receipt.json').write_text(json.dumps(report, indent=2) + '\n')
for name, path in modules.items():
    data = path.read_bytes()
    (source / (name + '.lean')).write_bytes(data)
    report['sources'][name] = {'path': str(path.relative_to(repo)), 'sha256': sha(data)}
save()
environment = os.environ.copy()
environment['LEAN_PATH'] = str(source)
for name in modules:
    command = [str(args.lean), '--trust=0', '-j1', '-DElab.async=false',
               '-o', name + '.olean', name + '.lean']
    start = time.monotonic()
    logfile = out / (name + '.log')
    with logfile.open('wb') as log:
        result = subprocess.run(command, cwd=source, env=environment,
                                stdout=log, stderr=subprocess.STDOUT, timeout=300)
    report['commands'].append({'argv': command, 'exit_code': result.returncode,
                               'elapsed_seconds': time.monotonic()-start,
                               'log': logfile.name, 'log_sha256': sha(logfile.read_bytes())})
    save()
    print(name, 'exit=' + str(result.returncode), flush=True)
    if result.returncode:
        report['status'] = 'FAILED'
        save()
        print(logfile.read_text(), flush=True)
        raise SystemExit(result.returncode)
report['status'] = 'LEAN_CHECKED_AUTHOR'
save()
print('Evidence:', out, flush=True)
