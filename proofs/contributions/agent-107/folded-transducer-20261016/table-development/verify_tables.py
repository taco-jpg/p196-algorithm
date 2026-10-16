#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
WORKSPACE = REPO.parent
RUNTIME = WORKSPACE / 'agent107-runtime'
BUILD = Path('/tmp/agent107-runtime/table-build')
BUILD.mkdir(parents=True, exist_ok=True)
parser=argparse.ArgumentParser()
parser.add_argument('--reuse-checked',action='store_true')
args=parser.parse_args()
attempt = len(list(HERE.glob('attempt-*.json'))) + 1
env = os.environ.copy()
for key in ['LEAN_PATH', 'LEAN_SRC_PATH', 'LEAN_SYSROOT', 'LD_PRELOAD', 'LD_LIBRARY_PATH']:
    env.pop(key, None)
env['LEAN_PATH'] = ':'.join(map(str,[BUILD,WORKSPACE/'agent107-build',RUNTIME/'baseline']))
records=[]
prior_changed=False
modules=['Agent107TransducerTablesData','Agent107TransducerTablesChecks','Agent107TransducerTables']
for module in modules:
    source = REPO / ('proofs/'+module+'.lean')
    data = source.read_bytes()
    source_hash=hashlib.sha256(data).hexdigest()
    cache=BUILD/(module+'.checked.json')
    obj=BUILD/(module+'.olean')
    if args.reuse_checked and not prior_changed and cache.exists() and obj.exists():
        old=json.loads(cache.read_text())
        if old['source_sha256']==source_hash and old['olean_sha256']==hashlib.sha256(obj.read_bytes()).hexdigest():
            record=dict(module=module,status='REUSED_CHECKED',source_sha256=source_hash,olean_sha256=old['olean_sha256'])
            records.append(record)
            print(json.dumps(record),flush=True)
            continue
    prior_changed=True
    (BUILD / (module+'.lean')).write_bytes(data)
    command = [str(RUNTIME/'lean-4.19.0-linux/bin/lean'),'--trust=0','-j1','-DElab.async=false',
               '-o',str(obj),str(BUILD/(module+'.lean'))]
    start=time.time()
    p=subprocess.run(command,cwd=BUILD,env=env,text=True,capture_output=True)
    name=f'attempt-{attempt:02d}-{module}'
    (HERE/(name+'.stdout.log')).write_text(p.stdout)
    (HERE/(name+'.stderr.log')).write_text(p.stderr)
    record=dict(module=module,command=command,exit_code=p.returncode,elapsed_seconds=time.time()-start,
                source_sha256=source_hash,lean_path=env['LEAN_PATH'],
                stdout_log=name+'.stdout.log',stderr_log=name+'.stderr.log')
    if p.returncode==0:
        record['olean_sha256']=hashlib.sha256(obj.read_bytes()).hexdigest()
        cache.write_text(json.dumps(record,indent=2)+'\n')
    records.append(record)
    (HERE/(f'attempt-{attempt:02d}.json')).write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps(record),flush=True)
    print(p.stdout,flush=True)
    print(p.stderr,flush=True)
    if p.returncode:
        raise SystemExit(p.returncode)

names=[]
for module in modules:
    text=(REPO/('proofs/'+module+'.lean')).read_text()
    clean=re.sub(r'/\-.*?\-/', '', text, flags=re.S)
    for token in ['sorry','admit','sorryAx','axiom','native_decide','unsafe','ofReduceBool']:
        assert not re.search(r'\b'+token+r'\b',clean), (module,token)
    names.extend('Agent107.FoldedTransducer.Table.'+name for name in re.findall(r'^theorem\s+(\w+)\b',clean,re.M))
assert len(names)==len(set(names))
audit='import Agent107TransducerTables\n\n'+'\n'.join('#print axioms '+name for name in names)+'\n'
(HERE/'AuditTables.lean').write_text(audit)
(BUILD/'AuditTables.lean').write_text(audit)
command=[str(RUNTIME/'lean-4.19.0-linux/bin/lean'),'--trust=0','-j1','-DElab.async=false',str(BUILD/'AuditTables.lean')]
start=time.time()
p=subprocess.run(command,cwd=BUILD,env=env,text=True,capture_output=True)
name=f'attempt-{attempt:02d}-audit'
(HERE/(name+'.stdout.log')).write_text(p.stdout)
(HERE/(name+'.stderr.log')).write_text(p.stderr)
assert p.returncode==0, p.stdout+p.stderr
axioms={}
for target in names:
    match=re.search("'"+re.escape(target)+"' (?:depends on axioms: \\[([^\\]]*)\\]|does not depend on any axioms)",p.stdout)
    assert match, target
    dependencies=[] if match.group(1) is None else [v.strip() for v in match.group(1).split(',')]
    assert set(dependencies) <= {'propext','Quot.sound','Classical.choice'}, (target,dependencies)
    axioms[target]=dependencies
record=dict(module='AuditTables',command=command,exit_code=p.returncode,elapsed_seconds=time.time()-start,
            source_sha256=hashlib.sha256(audit.encode()).hexdigest(),theorem_count=len(names),axioms=axioms,
            stdout_log=name+'.stdout.log',stderr_log=name+'.stderr.log')
records.append(record)
(HERE/(f'attempt-{attempt:02d}.json')).write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k!='axioms'}),flush=True)
print('FULL_TABLE_AUDIT_PASSED',flush=True)
