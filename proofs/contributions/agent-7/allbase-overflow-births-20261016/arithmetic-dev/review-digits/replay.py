#!/usr/bin/env python3
"""Independent clean replay of the frozen OverflowDigits source and controls."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent
CONTRIB = ROOT.parent.parent
LEAN = Path('/workspace/scratch/aaafdd394dd6/agent7-runtime/lean-4.19.0-linux/bin/lean')
EXPECTED = '37926723ba9d0d95b567f27607a810ea40d4fc622d60571d79228a5d33f33f8f'
attempt = 1
while (ROOT/f'attempt-{attempt:03d}').exists():
    attempt += 1
OUT = ROOT/f'attempt-{attempt:03d}'
SRC = OUT/'source'
SRC.mkdir(parents=True)
pins_path = CONTRIB/'dependencies/SOURCE_PINS.json'
pins = {p['module']: p for p in json.loads(pins_path.read_text())['dependencies']}
dependencies = ['SignedDigitUniqueness', 'BaseReflection', 'ResetNormalization',
                'PhysicalWidth', 'SeamSafety', 'ReverseAdd', 'BaseBirths', 'ActualBaseBirths']
modules = dependencies + ['OverflowDigits']
sources = {}
for module in modules:
    original = (CONTRIB/'dependencies'/f'{module}.lean' if module in dependencies
                else CONTRIB/'digits-dev/attempt-002/source/OverflowDigits.lean')
    dest = SRC/f'{module}.lean'
    shutil.copyfile(original, dest)
    sha = hashlib.sha256(dest.read_bytes()).hexdigest()
    assert sha == (pins[module]['sha256'] if module in dependencies else EXPECTED), module
    sources[module] = {'original': str(original), 'snapshot': str(dest), 'sha256': sha}
exports = re.findall(r'^theorem\s+(\w+)', (SRC/'OverflowDigits.lean').read_text(), re.M)
audit = SRC/'AllExportsAudit.lean'
audit.write_text('import OverflowDigits\n\n'+''.join(
    '#print axioms P196.Agent7.AllBaseOverflow.'+name+'\n' for name in exports))
sources['AllExportsAudit'] = {'snapshot': str(audit), 'sha256': hashlib.sha256(audit.read_bytes()).hexdigest()}
shutil.copyfile(ROOT/'BoundaryControls.lean', SRC/'BoundaryControls.lean')
sources['BoundaryControls'] = {'original': str(ROOT/'BoundaryControls.lean'),
                              'snapshot': str(SRC/'BoundaryControls.lean'),
                              'sha256': hashlib.sha256((SRC/'BoundaryControls.lean').read_bytes()).hexdigest()}
modules += ['AllExportsAudit', 'BoundaryControls']
env = dict(os.environ)
env['LEAN_PATH'] = str(SRC)
records = []
for module in modules:
    command = [str(LEAN), '--trust=0', '-j1', '-DElab.async=false', '-o', f'{module}.olean', f'{module}.lean']
    started = datetime.now(timezone.utc).isoformat()
    result = subprocess.run(command, cwd=SRC, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log = OUT/f'{module}.log'
    log.write_text(result.stdout)
    records.append({'module': module, 'command': command, 'cwd': str(SRC), 'started_at': started,
                    'exit_code': result.returncode, 'log': str(log), 'log_sha256': hashlib.sha256(log.read_bytes()).hexdigest()})
    print(f'{module}: exit {result.returncode}', flush=True)
    print(result.stdout, end='', flush=True)
    if result.returncode:
        break
passed = len(records) == len(modules) and all(r['exit_code'] == 0 for r in records)
axioms = {}
if passed:
    allowed = {'propext', 'Quot.sound', 'Classical.choice'}
    for name, raw in re.findall(r"^'([^']+)' depends on axioms: \[([^\]]*)\]", (OUT/'AllExportsAudit.log').read_text(), re.M):
        found = [a.strip() for a in raw.split(',') if a.strip()]
        axioms[name] = found
        assert set(found) <= allowed, (name, found)
    for name in re.findall(r"^'([^']+)' does not depend on any axioms", (OUT/'AllExportsAudit.log').read_text(), re.M):
        axioms[name] = []
    assert set(axioms) == {'P196.Agent7.AllBaseOverflow.'+name for name in exports}
report = {'timestamp': datetime.now(timezone.utc).isoformat(), 'lean': str(LEAN),
          'lean_sha256': hashlib.sha256(LEAN.read_bytes()).hexdigest(),
          'source_snapshots': sources, 'records': records, 'all_passed': passed,
          'dependency_pins_sha256': hashlib.sha256(pins_path.read_bytes()).hexdigest(),
          'public_theorem_exports': exports, 'public_axiom_audit': axioms,
          'independence': 'Reviewer copied the author-frozen source by pinned hash and freshly compiled every dependency; no author objects were reused.'}
(OUT/'verification.json').write_text(json.dumps(report, indent=2)+'\n')
print('REPORT '+str(OUT/'verification.json'), flush=True)
raise SystemExit(0 if passed else 1)
