#!/usr/bin/env python3
"""Different-author rebuild from source into a previously absent directory."""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import time

ROOT = Path('/workspace/scratch/50e90e07524e/p196-agent106')
REVIEW = ROOT / 'proofs/contributions/agent-106/run-births/review/allbase-reviewer'
BUILD = REVIEW / 'fresh-build-001'
LEAN = Path('/workspace/scratch/50e90e07524e/runtime/lean-4.19.0-linux/bin/lean')
PRELOAD = Path('/workspace/scratch/50e90e07524e/runtime/readlink_self.so')
SOURCES = [
    'proofs/contributions/2026-10-14-base-uniqueness-formal/SignedDigitUniqueness.lean',
    *[f'proofs/contributions/2026-10-15-base-reflection-formal/{name}.lean'
      for name in ['BaseReflection', 'ResetNormalization', 'PhysicalWidth', 'SeamSafety']],
    'proofs/contributions/2026-10-15-base-reverse-add-formal/ReverseAdd.lean',
    'proofs/contributions/agent-106/run-births/BaseBirths.lean',
    'proofs/contributions/agent-106/run-births/ActualBaseBirths.lean',
]

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

assert not BUILD.exists(), 'Do not reuse a build directory'
BUILD.mkdir()
report = {
    'reviewer': 'overflow_births',
    'reviewed_source_authorship': 'different author',
    'initially_empty': not any(BUILD.iterdir()),
    'build_directory': str(BUILD.relative_to(ROOT)),
    'olean_policy': 'Only newly rebuilt modules plus official Lean runtime',
    'lean_sha256': sha(LEAN), 'preload_sha256': sha(PRELOAD),
    'script_sha256': sha(__file__), 'modules': [],
}
env = dict(os.environ, LD_PRELOAD=str(PRELOAD), LEAN_PATH=str(BUILD))
env.pop('LEAN_SRC_PATH', None)
env.pop('LEAN_SYSROOT', None)
report['environment_overrides'] = {k: env[k] for k in ['LD_PRELOAD', 'LEAN_PATH']}
report['version'] = subprocess.check_output([str(LEAN), '--version'], env=env, text=True).strip()
assert 'version 4.19.0,' in report['version']

def save():
    (REVIEW / 'rebuild.json').write_text(json.dumps(report, indent=2) + '\n')

def compile_source(name, original):
    snapshot = BUILD / (name + '.lean')
    if original != snapshot:
        shutil.copyfile(original, snapshot)
    before = sha(snapshot)
    cmd = [str(LEAN), '-j1', '-DElab.async=false', '-o', name + '.olean', name + '.lean']
    start = time.monotonic()
    result = subprocess.run(cmd, cwd=BUILD, env=env, text=True, capture_output=True)
    log = REVIEW / (name + '.log')
    log.write_text(result.stdout + result.stderr)
    entry = {
        'module': name, 'source_path': str(original.relative_to(ROOT)),
        'source_sha256': before, 'source_unchanged_after_compile': sha(original) == before,
        'snapshot_sha256': sha(snapshot), 'command': cmd,
        'cwd': str(BUILD), 'exit_code': result.returncode,
        'elapsed_seconds': time.monotonic() - start, 'log_sha256': sha(log),
    }
    output = BUILD / (name + '.olean')
    if output.exists():
        entry['olean_sha256'] = sha(output)
    report['modules'].append(entry)
    save()
    print(name, 'exit', result.returncode, before, flush=True)
    assert entry['source_unchanged_after_compile'], 'Source changed while building'
    assert result.returncode == 0, 'See preserved module log'
    assert not any(t in log.read_text() for t in ['sorryAx', 'error:', 'Lean.ofReduceBool', 'Lean.trustCompiler'])

theorems = []
for relative in SOURCES:
    source = ROOT / relative
    name = source.stem
    compile_source(name, source)
    namespaces = re.findall(r'^namespace\s+(\w+)\s*$', source.read_text(), re.M)
    assert namespaces == [name], (name, namespaces)
    exports = re.findall(r'^theorem\s+([\w\']+)', source.read_text(), re.M)
    theorems.extend(name + '.' + th for th in exports)

audit = BUILD / 'AllAxioms.lean'
audit.write_text('import ActualBaseBirths\n\n' +
                 '\n'.join('#print axioms ' + th for th in theorems) + '\n')
report['exported_theorem_count'] = len(theorems)
report['audited_theorems'] = theorems
compile_source('AllAxioms', audit)
for item in report['modules']:
    assert sha(ROOT / item['source_path']) == item['source_sha256'], 'Reviewed source changed'
report['status'] = 'PASS'
save()
print('PASS all', len(theorems), 'exported theorem axioms', flush=True)
