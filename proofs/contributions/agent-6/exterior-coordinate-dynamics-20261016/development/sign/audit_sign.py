#!/usr/bin/env python3
"""Check every exported signature and kernel axiom dependency of CoordinateSign."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = Path('/workspace/scratch/f8aedc6d7adf')
WORK = ROOT / 'landscape-agent6'
BUILD = WORK / 'sign-build'
SOURCE = ROOT / 'agent6-work/proofs/contributions/agent-6/exterior-coordinate-dynamics-20261016/CoordinateSign.lean'
LEAN = ROOT / 'runtime-agent6/lean-4.19.0-linux/bin/lean'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

index = 1
while (WORK / ('sign-audit-%03d' % index)).exists():
    index += 1
out = WORK / ('sign-audit-%03d' % index)
out.mkdir()
latest = sorted((WORK / 'sign-attempts').glob('attempt-*'))[-1]
compilation = json.loads((latest / 'verification.json').read_text())[-1]
if compilation['exit_code'] != 0 or compilation['source_sha256'] != sha(SOURCE):
    raise RuntimeError('No successful compilation of current source')
if compilation['object_sha256'] != sha(BUILD / 'CoordinateSign.olean'):
    raise RuntimeError('Compiled object mismatch')
if sha(SOURCE) != sha(BUILD / 'CoordinateSign.lean'):
    raise RuntimeError('Build source mismatch')

names = re.findall(r'^theorem\s+(\w+)', SOURCE.read_text(), flags=re.M)
audit = 'import CoordinateSign\n\n'
for name in names:
    full = 'Agent6.ExteriorCoordinates.' + name
    audit += '#check @' + full + '\n#print axioms ' + full + '\n'
path = BUILD / 'SignAudit.lean'
path.write_text(audit)
(out / path.name).write_text(audit)
command = [str(LEAN), '--trust=0', '-j1', '-DElab.async=false', '-o', 'SignAudit.olean', 'SignAudit.lean']
run = subprocess.run(command, cwd=BUILD, env=dict(os.environ, LEAN_PATH=str(BUILD)),
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=240)
log = out / 'SignAudit.log'
log.write_bytes(run.stdout)
output = run.stdout.decode('utf-8', errors='replace')
reports = re.findall(r"'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)", output)
allowed = {'propext', 'Classical.choice', 'Quot.sound'}
unexpected = sorted({a.strip() for _, raw in reports for a in raw.split(',') if a.strip()} - allowed)
expected = {'Agent6.ExteriorCoordinates.' + name for name in names}
actual = {name for name, _ in reports}
forbidden = re.findall(r'\b(?:sorry|admit|axiom|native_decide|unsafe)\b', SOURCE.read_text())
receipt = {'exit_code': run.returncode, 'command': command, 'cwd': str(BUILD),
           'source': str(SOURCE), 'source_sha256': sha(SOURCE),
           'object_sha256': sha(BUILD / 'CoordinateSign.olean'),
           'compiler_sha256': sha(LEAN), 'audit_source_sha256': sha(path),
           'audit_log_sha256': sha(log), 'exported_theorems': sorted(expected),
           'reported_count': len(reports), 'missing_reports': sorted(expected - actual),
           'extra_reports': sorted(actual - expected), 'unexpected_axioms': unexpected,
           'forbidden_token_matches': forbidden,
           'axioms': {name: [a.strip() for a in raw.split(',') if a.strip()] for name, raw in reports},
           'dependencies': str(WORK / 'sign-dependencies.json'),
           'compilation': str(latest / 'verification.json')}
receipt['pass'] = run.returncode == 0 and expected == actual and not unexpected and not forbidden
(out / 'verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(output)
print(json.dumps({'pass': receipt['pass'], 'exports': len(names), 'receipt': str(out / 'verification.json')}))
sys.exit(0 if receipt['pass'] else 1)
