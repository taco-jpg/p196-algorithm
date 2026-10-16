#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]
WORKSPACE=REPO.parent
RUNTIME=WORKSPACE/'agent107-runtime'
BUILD=Path('/tmp/agent107-runtime/reachability-build')
BUILD.mkdir(parents=True,exist_ok=True)
SOURCE=REPO/'proofs/Agent107TransducerReachable.lean'
data=SOURCE.read_bytes()
(BUILD/SOURCE.name).write_bytes(data)
env=os.environ.copy()
for key in ['LEAN_PATH','LEAN_SRC_PATH','LEAN_SYSROOT','LD_PRELOAD','LD_LIBRARY_PATH']: env.pop(key,None)
env['LEAN_PATH']=':'.join(map(str,[BUILD,Path('/tmp/agent107-runtime/table-build'),WORKSPACE/'agent107-build',RUNTIME/'baseline']))
attempt=len(list(HERE.glob('attempt-*.json')))+1
name=f'attempt-{attempt:02d}'
command=[str(RUNTIME/'lean-4.19.0-linux/bin/lean'),'--trust=0','-j1','-DElab.async=false',
         '-o',str(BUILD/'Agent107TransducerReachable.olean'),str(BUILD/SOURCE.name)]
start=time.time()
p=subprocess.run(command,cwd=BUILD,env=env,text=True,capture_output=True)
(HERE/(name+'.stdout.log')).write_text(p.stdout)
(HERE/(name+'.stderr.log')).write_text(p.stderr)
record=dict(command=command,exit_code=p.returncode,elapsed_seconds=time.time()-start,
            source_sha256=hashlib.sha256(data).hexdigest(),lean_path=env['LEAN_PATH'],
            stdout_log=name+'.stdout.log',stderr_log=name+'.stderr.log')
if p.returncode==0:
    clean=re.sub(r'/\-.*?\-/', '', data.decode(), flags=re.S)
    for token in ['sorry','admit','sorryAx','axiom','native_decide','unsafe','ofReduceBool']:
        assert not re.search(r'\b'+token+r'\b',clean),(token,)
    names=['Agent107.FoldedTransducer.'+v for v in re.findall(r'^theorem\s+(\w+)\b',clean,re.M)]
    axioms={}
    for target in names:
        match=re.search("'"+re.escape(target)+"' (?:depends on axioms: \\[([^\\]]*)\\]|does not depend on any axioms)",p.stdout)
        assert match,target
        deps=[] if match.group(1) is None else [x.strip() for x in match.group(1).split(',')]
        assert set(deps)<={'propext','Quot.sound','Classical.choice'},(target,deps)
        axioms[target]=deps
    record['axioms']=axioms
    record['theorem_count']=len(names)
    record['olean_sha256']=hashlib.sha256((BUILD/'Agent107TransducerReachable.olean').read_bytes()).hexdigest()
(HERE/(name+'.json')).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k!='axioms'}),flush=True)
print(p.stdout,flush=True)
print(p.stderr,flush=True)
raise SystemExit(p.returncode)
