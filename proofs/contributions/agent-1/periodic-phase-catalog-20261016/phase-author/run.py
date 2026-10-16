#!/usr/bin/env python3
"""Incremental Phase compilation using ten unchanged pinned parent-clean objects."""
from pathlib import Path
import hashlib, json, os, re, shutil, subprocess, sys, time

ROOT = Path('/workspace/p196-agent1-phase-20261016')
OUT = ROOT/'proofs/contributions/agent-1/periodic-phase-catalog-20261016/phase-author'
BASE = Path('/workspace/p196-agent1-session-20261016/periodic-zero-escape-parent-clean-001')
DEPS = BASE/'agent1-periodic-zero-escape/source'
LEAN = Path('/workspace/p196-tools/lean-4.19.0-linux/bin/lean')
MODULE = 'Agent1PeriodicPhase'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

attempt = OUT/sys.argv[1]
attempt.mkdir(parents=True, exist_ok=False)
shutil.copy2(Path(__file__), attempt/'run-driver.py')
receipt = json.loads((BASE/'verification.json').read_text())
assert receipt['status'] == 'PASS'
project = receipt['projects']['agent1-periodic-zero-escape']
assert project['status'] == 'PASS'
assert sha(LEAN) == '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
seen = set()
order = []
def visit(name):
    if name in ('Std', 'Init', 'Lean') or name in seen: return
    seen.add(name)
    for dep in project['sources'][name]['imports']: visit(dep)
    order.append(name)
visit('Agent1PeriodicGuard')
assert len(order) == 10
deps = []
for name in order:
    entry = project['sources'][name]
    assert entry['adapter'] is None
    assert sha(ROOT/entry['path']) == entry['sha256']
    assert sha(DEPS/(name+'.lean')) == entry['build_sha256'] == entry['sha256']
    assert (DEPS/(name+'.olean')).is_file()
    deps.append(dict(module=name, path=entry['path'], source_sha256=entry['sha256'],
                     olean_sha256=sha(DEPS/(name+'.olean')), imports=entry['imports']))
(attempt/'dependencies.json').write_text(json.dumps(dict(
    receipt=str(BASE/'verification.json'), receipt_sha256=sha(BASE/'verification.json'),
    source_commit=receipt['source_commit'], object_origin=str(DEPS),
    qualification='Author increment reusing ten unchanged dependency objects; not a fresh or independent rebuild.',
    modules=deps), indent=2)+'\n')
source = ROOT/'proofs'/(MODULE+'.lean')
assert not re.search(r'\b(sorry|admit|sorryAx|native_decide|axiom)\b', source.read_text())
shutil.copy2(source, attempt/source.name)
argv = [str(LEAN),'--trust=0','-j1','-DElab.async=false','-o',MODULE+'.olean',MODULE+'.lean']
lean_path = str(attempt)+':'+str(DEPS)
record = dict(command=argv, cwd=str(attempt), LEAN_PATH=lean_path,
    source_sha256=sha(source), compiler_sha256=sha(LEAN), started_at_epoch=time.time(),
    independent_clean_rebuild=False)
(attempt/'run.json').write_text(json.dumps(record,indent=2)+'\n')
start=time.monotonic()
with (attempt/'compile.log').open('w') as log:
    rc=subprocess.run(argv,cwd=attempt,env=dict(os.environ,LEAN_PATH=lean_path),
                      stdout=log,stderr=subprocess.STDOUT).returncode
record.update(exit_code=rc, seconds=time.monotonic()-start, finished_at_epoch=time.time(),
              log_sha256=sha(attempt/'compile.log'))
if rc == 0: record['olean_sha256'] = sha(attempt/(MODULE+'.olean'))
(attempt/'run.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
print((attempt/'compile.log').read_text())
raise SystemExit(rc)
