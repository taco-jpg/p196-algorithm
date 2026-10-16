#!/usr/bin/env python3
"""Strict author increment with pinned outer-clean and WidthPath objects."""
from pathlib import Path
import hashlib,json,os,re,resource,shutil,subprocess,sys,time

ROOT=Path('/workspace/p196-agent1-return-20261016')
OUT=ROOT/'proofs/contributions/agent-1/periodic-return-core-20261016/path-author'
BASE=Path('/workspace/p196-agent1-session-20261016/periodic-outer-parent-clean-001')
DEPS=BASE/'agent1-periodic-outer-catalog/source'
WIDTH=Path('/workspace/p196-agent1-width-20261016/proofs/contributions/agent-1/periodic-width-projection-20261016/width-path-author')
WOBJ=WIDTH/'attempt-002'
LEAN=Path('/workspace/p196-tools/lean-4.19.0-linux/bin/lean')
MODULE='Agent1PeriodicQuotientPath'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
attempt=OUT/sys.argv[1]
attempt.mkdir(parents=True,exist_ok=False)
shutil.copy2(Path(__file__),attempt/'run-driver.py')
receipt=json.loads((BASE/'verification.json').read_text())
assert receipt['status']=='PASS'
project=receipt['projects']['agent1-periodic-outer-catalog']
assert project['status']=='PASS'
assert sha(LEAN)=='92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
seen=set();order=[]
def visit(name):
    if name in ('Std','Init','Lean') or name in seen:return
    seen.add(name)
    for dep in project['sources'][name]['imports']:visit(dep)
    order.append(name)
visit('Agent1PeriodicOuterCatalog')
assert len(order)==25
deps=[]
for name in order:
    e=project['sources'][name]
    assert e['adapter'] is None
    assert sha(ROOT/e['path'])==sha(DEPS/(name+'.lean'))==e['sha256']==e['build_sha256']
    deps.append(dict(module=name,path=e['path'],source_sha256=e['sha256'],
        object_path=str(DEPS/(name+'.olean')),olean_sha256=sha(DEPS/(name+'.olean')),imports=e['imports']))
wr=json.loads((WOBJ/'run.json').read_text())
wa=json.loads((WIDTH/'audit-006/run.json').read_text())
assert wr['exit_code']==0 and wa['status']=='PASS'
wsrc=ROOT/'proofs/Agent1PeriodicWidthPath.lean'
assert sha(wsrc)==wr['source_sha256']==wa['source_sha256']==sha(WOBJ/wsrc.name)
assert sha(WOBJ/'Agent1PeriodicWidthPath.olean')==wr['olean_sha256']==wa['object_sha256']
for e in json.loads((WOBJ/'dependencies.json').read_text())['modules']:
    assert project['sources'][e['module']]['sha256']==e['source_sha256']
deps.append(dict(module='Agent1PeriodicWidthPath',path=str(wsrc.relative_to(ROOT)),
    source_sha256=sha(wsrc),object_path=str(WOBJ/'Agent1PeriodicWidthPath.olean'),
    olean_sha256=wr['olean_sha256'],imports=['Agent1PeriodicQuotient']))
(attempt/'dependencies.json').write_text(json.dumps(dict(
    outer_receipt=str(BASE/'verification.json'),outer_receipt_sha256=sha(BASE/'verification.json'),
    outer_source_commit=receipt['source_commit'],
    width_compile_receipt=str(WOBJ/'run.json'),width_compile_receipt_sha256=sha(WOBJ/'run.json'),
    width_audit_receipt=str(WIDTH/'audit-006/run.json'),width_audit_receipt_sha256=sha(WIDTH/'audit-006/run.json'),
    qualification='Author increment reuses 25 outer-clean objects and one audited WidthPath author object; not a fresh independent build.',
    modules=deps),indent=2)+'\n')
source=ROOT/'proofs'/(MODULE+'.lean')
assert not re.search(r'\b(sorry|admit|sorryAx|native_decide|axiom)\b',source.read_text())
shutil.copy2(source,attempt/source.name)
argv=[str(LEAN),'--trust=0','-j1','-DElab.async=false','-o',MODULE+'.olean',MODULE+'.lean']
lean_path=':'.join(map(str,[attempt,WOBJ,DEPS]))
record=dict(command=argv,cwd=str(attempt),LEAN_PATH=lean_path,source_sha256=sha(source),
    compiler_sha256=sha(LEAN),started_at_epoch=time.time(),independent_clean_rebuild=False)
cpu=min(os.sched_getaffinity(0));rss_cap_kib=1500*1024
def limits():
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    os.sched_setaffinity(0,{cpu})
record.update(cpu_affinity=[cpu],rss_watchdog_limit_kib=rss_cap_kib,rss_watchdog_poll_seconds=0.01)
(attempt/'run.json').write_text(json.dumps(record,indent=2)+'\n')
start=time.monotonic();sampled_peak=0;triggered=False
with (attempt/'compile.log').open('w') as log:
    proc=subprocess.Popen(argv,cwd=attempt,env=dict(os.environ,LEAN_PATH=lean_path),stdout=log,stderr=subprocess.STDOUT,preexec_fn=limits)
    while proc.poll() is None:
        try:
            stat=Path(f'/proc/{proc.pid}/status').read_text()
            vals=re.findall(r'^Vm(?:RSS|HWM):\s+(\d+) kB$',stat,re.M)
            sampled_peak=max([sampled_peak]+list(map(int,vals)))
            if sampled_peak>rss_cap_kib:triggered=True;proc.kill();break
        except FileNotFoundError:pass
        time.sleep(0.01)
    rc=proc.wait()
record.update(status='PASS' if rc==0 and not triggered else 'FAIL',exit_code=rc,
    seconds=time.monotonic()-start,finished_at_epoch=time.time(),log_sha256=sha(attempt/'compile.log'),
    peak_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
    sampled_peak_rss_kib=sampled_peak,rss_watchdog_triggered=triggered)
if rc==0:record['olean_sha256']=sha(attempt/(MODULE+'.olean'))
(attempt/'run.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2));print((attempt/'compile.log').read_text())
raise SystemExit(0 if record['status']=='PASS' else 1)
