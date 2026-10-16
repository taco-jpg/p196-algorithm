#!/usr/bin/env python3
"""Independent Boundary rebuild: fresh Defs and Boundary, own previously rebuilt baseline only."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]
WORKSPACE=REPO.parent
RUNTIME=WORKSPACE/'agent107-runtime'
LEAN=RUNTIME/'lean-4.19.0-linux/bin/lean'
BASE=RUNTIME/'baseline'
BASE_MANIFEST=json.loads((BASE/'manifest.json').read_text())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(BASE/'Lychrel196Research.lean')==BASE_MANIFEST['source_sha256']
assert sha(BASE/'Lychrel196Research.olean')==BASE_MANIFEST['olean_sha256']
assert sha(REPO/BASE_MANIFEST['source_file'])==BASE_MANIFEST['source_sha256']
BUILD=Path(tempfile.mkdtemp(prefix='boundary-independent-',dir='/tmp/agent107-runtime'))
assert not list(BUILD.iterdir())

def lean_code(text):
    result=[]; i=0; depth=0; string=False
    while i<len(text):
        pair=text[i:i+2]
        if depth:
            if pair=='/-': depth+=1; i+=2
            elif pair=='-/': depth-=1; i+=2
            else: i+=1
        elif string:
            if text[i]=='\\': i+=2
            elif text[i]=='"': string=False; i+=1
            else: i+=1
        elif pair=='/-': depth=1; result.append(' '); i+=2
        elif pair=='--':
            n=text.find('\n',i); i=len(text) if n<0 else n
        elif text[i]=='"': string=True; result.append(' '); i+=1
        else: result.append(text[i]); i+=1
    assert depth==0 and not string
    return ''.join(result)

env=os.environ.copy()
for key in ['LEAN_PATH','LEAN_SRC_PATH','LEAN_SYSROOT','LD_PRELOAD','LD_LIBRARY_PATH']: env.pop(key,None)
env['LEAN_PATH']=str(BUILD)+':'+str(BASE)
sources=[]
for module in ['Agent107TransducerDefs','Agent107TransducerBoundary']:
    source=REPO/('proofs/'+module+'.lean')
    clean=lean_code(source.read_text())
    assert not re.search(r'\b(sorry|admit|sorryAx|axiom|native_decide|unsafe|ofReduceBool|ofReduceNat)\b',clean)
    copy=BUILD/(module+'.lean'); copy.write_bytes(source.read_bytes())
    sources.append(dict(module=module,source=str(source.relative_to(REPO)),sha256=sha(source),copy_sha256=sha(copy),
                        computed_git_blob=subprocess.check_output(['git','-C',str(REPO),'hash-object',str(source)],text=True).strip()))
manifest=dict(status='IN_PROGRESS',review_scope='Boundary only; author semantic_review, independent reviewer lean_runtime',
              build_dir=str(BUILD),build_dir_initially_empty=True,lean_path=env['LEAN_PATH'],
              baseline_reused=dict(source_commit=BASE_MANIFEST['source_commit'],source_git_blob=BASE_MANIFEST['source_git_blob'],
                  source_sha256=BASE_MANIFEST['source_sha256'],olean_sha256=BASE_MANIFEST['olean_sha256'],
                  origin='Previously rebuilt independently by this same reviewer from exact original repository source with --trust=0; baseline/manifest.json'),
              source_files=sources,path_semantics_source_sha256=sha(REPO/'proofs/Agent107TransducerPath.lean'),executions=[])
def save(): (HERE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
def run(name,args):
    command=[str(LEAN),'--trust=0','-j1','-DElab.async=false',*args]
    start=time.time()
    p=subprocess.run(command,cwd=BUILD,env=env,text=True,capture_output=True)
    (HERE/(name+'.stdout.log')).write_text(p.stdout)
    (HERE/(name+'.stderr.log')).write_text(p.stderr)
    record=dict(name=name,command=command,exit_code=p.returncode,elapsed_seconds=time.time()-start,
                stdout_log=name+'.stdout.log',stderr_log=name+'.stderr.log')
    manifest['executions'].append(record); save()
    print(json.dumps(record),flush=True)
    assert p.returncode==0,p.stdout+p.stderr
    return p.stdout

try:
    save()
    for s in sources:
        module=s['module']
        run('build-'+module,['-o',str(BUILD/(module+'.olean')),str(BUILD/(module+'.lean'))])
        s['olean_sha256']=sha(BUILD/(module+'.olean'))
    audit='''import Lean
import Agent107TransducerBoundary

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let mut count := 0
  for (name, info) in env.constants do
    let origin : Name := match env.getModuleIdxFor? name with
      | none => Name.anonymous
      | some idx => env.allImportedModuleNames[idx.toNat]!
    if origin == `Agent107TransducerBoundary then
      if let .axiomInfo _ := info then
        throwError "Boundary introduces an axiom: {name}"
      if let .thmInfo _ := info then
        count := count + 1
        logInfo m!"BOUNDARY_MODULE_ORIGIN {name}"
        elabCommand (← `(command| #print axioms $(mkIdent name)))
        let axioms ← collectAxioms name
        for ax in axioms do
          unless #[``propext, ``Quot.sound, ``Classical.choice].contains ax do
            throwError "Disallowed transitive axiom: {name} uses {ax}"
  logInfo m!"BOUNDARY_MODULE_ORIGIN_COUNT {count}"
'''
    (HERE/'BoundaryModuleOriginAudit.lean').write_text(audit)
    (BUILD/'BoundaryModuleOriginAudit.lean').write_text(audit)
    output=run('module-origin-audit',[str(BUILD/'BoundaryModuleOriginAudit.lean')])
    match=re.search(r'BOUNDARY_MODULE_ORIGIN_COUNT (\d+)',output)
    assert match
    axioms={}
    for name,no,yes in re.findall(r"^'(.+)' (does not depend on any axioms|depends on axioms: \[([^\]]*)\])$",output,re.M):
        axioms[name]=[] if no=='does not depend on any axioms' else [x.strip() for x in yes.split(',')]
    assert len(axioms)==int(match.group(1))
    public=['Agent107.FoldedTransducer.Boundary.'+name for name in re.findall(r'^theorem\s+(\w+)\b',lean_code((REPO/'proofs/Agent107TransducerBoundary.lean').read_text()),re.M)]
    assert len(public)==15 and set(public)<=set(axioms)
    for s in sources: assert sha(REPO/s['source'])==s['sha256']
    manifest.update(status='INDEPENDENT_BOUNDARY_REBUILD_AND_AXIOM_AUDIT_PASS',
                    module_origin_theorem_count=len(axioms),public_endpoint_count=len(public),
                    audited_axioms=axioms,audit_source_sha256=sha(HERE/'BoundaryModuleOriginAudit.lean'))
    save()
    print(json.dumps(dict(status=manifest['status'],public_endpoint_count=len(public),module_origin_theorem_count=len(axioms))),flush=True)
except Exception as error:
    manifest.update(status='FAILED',error=repr(error));save();raise
