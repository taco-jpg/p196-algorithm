#!/usr/bin/env python3
"""Author increment: unchanged seventeen validity objects plus reviewed Alphabet."""
from pathlib import Path
import hashlib,json,os,re,shutil,subprocess,sys,time

ROOT=Path('/workspace/p196-agent1-outer-20261016')
OUT=ROOT/'proofs/contributions/agent-1/periodic-outer-catalog-20261016/outer-author'
BASE=Path('/workspace/p196-agent1-session-20261016/periodic-phase-parent-clean-001')
DEPS=BASE/'agent1-periodic-phase-catalog/source'
ALPHABET=Path('/workspace/p196-agent1-session-20261016/periodic-safety-review-clean-001')
REVIEW=ROOT/'proofs/contributions/agent-1/periodic-safety-20261016/review/clean-001'
LEAN=Path('/workspace/p196-tools/lean-4.19.0-linux/bin/lean')
MODULE='Agent1PeriodicOuter'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

attempt=OUT/sys.argv[1]
attempt.mkdir(parents=True,exist_ok=False)
shutil.copy2(Path(__file__),attempt/'run-driver.py')
receipt=json.loads((BASE/'verification.json').read_text())
assert receipt['status']=='PASS'
project=receipt['projects']['agent1-periodic-phase-catalog']
assert project['status']=='PASS'
assert json.loads((REVIEW/'verification.json').read_text())['status']=='PASS'
assert sha(LEAN)=='92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
seen=set();order=[]
def visit(name):
    if name in ('Std','Lean','Init') or name in seen:return
    seen.add(name)
    for dep in project['sources'][name]['imports']:visit(dep)
    order.append(name)
visit('Agent1PeriodicValidity')
assert len(order)==17
old_sources={x['module']:x for x in json.loads((REVIEW/'sources.json').read_text())}
deps=[]
for name in order:
    e=project['sources'][name]
    assert e['adapter'] is None
    assert sha(ROOT/e['path'])==e['sha256']==e['build_sha256']
    assert sha(DEPS/(name+'.lean'))==e['sha256']==old_sources[name]['sha256']
    assert sha(ALPHABET/(name+'.lean'))==e['sha256']
    deps.append(dict(module=name,path=e['path'],source_sha256=e['sha256'],
        object_origin=str(DEPS),olean_sha256=sha(DEPS/(name+'.olean')),imports=e['imports']))
entry=old_sources['Agent1PeriodicSafetyAlphabet']
assert entry['sha256']=='ec2632bcdfc630947844098f09f54161e2bd4ab3473f0e4a139ec6bc2d56912c'
assert sha(ROOT/entry['path'])==sha(ALPHABET/'Agent1PeriodicSafetyAlphabet.lean')==entry['sha256']
deps.append(dict(entry,object_origin=str(ALPHABET),
    olean_sha256=sha(ALPHABET/'Agent1PeriodicSafetyAlphabet.olean')))
(attempt/'dependencies.json').write_text(json.dumps(dict(
    phase_parent_receipt=str(BASE/'verification.json'),phase_parent_receipt_sha256=sha(BASE/'verification.json'),
    phase_parent_commit=receipt['source_commit'],alphabet_review_receipt=str(REVIEW/'verification.json'),
    alphabet_review_receipt_sha256=sha(REVIEW/'verification.json'),
    qualification='Author incremental reuse of eighteen unchanged objects from two prior PASS clean builds; shared source pins are identical. Not a fresh independent rebuild.',
    modules=deps),indent=2)+'\n')
source=ROOT/'proofs'/(MODULE+'.lean')
assert not re.search(r'\b(sorry|admit|sorryAx|native_decide|axiom)\b',source.read_text())
shutil.copy2(source,attempt/source.name)
argv=[str(LEAN),'--trust=0','-j1','-DElab.async=false','-o',MODULE+'.olean',MODULE+'.lean']
lean_path=':'.join(map(str,[attempt,DEPS,ALPHABET]))
record=dict(command=argv,cwd=str(attempt),LEAN_PATH=lean_path,source_sha256=sha(source),
    compiler_sha256=sha(LEAN),started_at_epoch=time.time(),independent_clean_rebuild=False)
(attempt/'run.json').write_text(json.dumps(record,indent=2)+'\n')
start=time.monotonic()
with (attempt/'compile.log').open('w') as log:
    rc=subprocess.run(argv,cwd=attempt,env=dict(os.environ,LEAN_PATH=lean_path),
        stdout=log,stderr=subprocess.STDOUT).returncode
record.update(exit_code=rc,seconds=time.monotonic()-start,finished_at_epoch=time.time(),
    log_sha256=sha(attempt/'compile.log'))
if rc==0:record['olean_sha256']=sha(attempt/(MODULE+'.olean'))
(attempt/'run.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2));print((attempt/'compile.log').read_text())
raise SystemExit(rc)
