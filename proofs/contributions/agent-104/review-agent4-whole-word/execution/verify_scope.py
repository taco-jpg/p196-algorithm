#!/usr/bin/env python3
"""Compile frozen review-scope illustrations after the independently rebuilt closure.
The existing five local objects must be the exact independently audited attempt01
objects. This script starts one compiler at a time and records every outcome.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

WITNESS_COMMIT='c8fb8bca4160f3dfdb577b17405d2845bf6dbb12'
WITNESS_PATH='proofs/contributions/agent-104/review-agent4-whole-word/semantic/ReviewScopeWitnesses.lean'
WITNESS_PIN='0a070699854fcace3d623101a7c7bedf3f89be3b743deeaacc123646561089d2'
ALLOWED={'propext','Classical.choice','Quot.sound'}
EXPECTED={'decimalDigits_bounded','canonical_89870','canonical_179745797','canonical_770','canonical_176176','orbit_89870_eight','orbit_770_seven','saturated_return_89870','nonsaturated_return_770'}


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()


def save(path, value):
    Path(path).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--build',type=Path,required=True)
    p.add_argument('--closure-evidence',type=Path,required=True)
    p.add_argument('--evidence',type=Path,required=True)
    p.add_argument('--lean',type=Path,required=True)
    args=p.parse_args()
    repo,build,evidence=args.repo.resolve(),args.build.resolve(),args.evidence.resolve()
    snapshot=build/'snapshot'
    closure_file=args.closure_evidence.resolve()/'verification.json'
    closure=json.loads(closure_file.read_text())
    if closure['status']!='PASS':raise ValueError('Full original closure is not independently accepted')
    if (snapshot/'ReviewScopeWitnesses.olean').exists():raise ValueError('Pre-existing witness object; retain and use fresh attempt')
    evidence.mkdir(parents=True,exist_ok=False)
    env=dict(os.environ)
    for key in ('LEAN_PATH','LEAN_SRC_PATH','LEAN_SYSROOT','LD_PRELOAD','LD_LIBRARY_PATH'):env.pop(key,None)
    env['LEAN_PATH']=str(snapshot)
    report={'status':'IN_PROGRESS','scope':'Review illustrations, no new main-theorem ownership or P196 claim.',
        'source_commit':WITNESS_COMMIT,'source_path':WITNESS_PATH,'source_sha256':WITNESS_PIN,
        'closure_evidence':str(closure_file),'closure_evidence_sha256':sha(closure_file),
        'local_compiler_processes':1,'compiler_threads':1,'asynchronous_elaboration':False,
        'builds':[],'allowed_axioms':sorted(ALLOWED),'runner_sha256':sha(__file__)}
    reportfile=evidence/'verification.json'
    save(reportfile,report)
    def run(label,command):
        log=evidence/(label+'.log');start=time.monotonic()
        with log.open('w') as stream:
            proc=subprocess.Popen(command,cwd=snapshot,env=env,stdout=stream,stderr=subprocess.STDOUT)
            _,status,usage=os.wait4(proc.pid,0);proc.returncode=os.waitstatus_to_exitcode(status)
        rec={'label':label,'command':command,'cwd':str(snapshot),'exit_code':proc.returncode,
            'seconds':round(time.monotonic()-start,3),'log':log.name,'log_sha256':sha(log),
            'resources':{key:getattr(usage,key) for key in ('ru_utime','ru_stime','ru_maxrss','ru_minflt','ru_majflt','ru_nswap')}}
        report['builds'].append(rec);save(reportfile,report);print(json.dumps(rec),flush=True)
        if proc.returncode:raise ValueError(f'{label}: compiler exited {proc.returncode}')
        return log.read_text()
    try:
        for module,rec in closure['sources'].items():
            if sha(snapshot/(module+'.lean'))!=rec['sha256']:raise ValueError('Original closure source changed '+module)
            if sha(snapshot/(module+'.olean'))!=rec['object_sha256']:raise ValueError('Original closure object changed '+module)
        for path,digest in closure['compiler_fingerprints'].items():
            if sha(path)!=digest:raise ValueError('Compiler changed since closure audit '+path)
        blob=subprocess.check_output(['git','show',WITNESS_COMMIT+':'+WITNESS_PATH],cwd=repo)
        if hashlib.sha256(blob).hexdigest()!=WITNESS_PIN:raise ValueError('Witness source pin mismatch')
        report['source_bytes']=len(blob)
        source=snapshot/'ReviewScopeWitnesses.lean';source.write_bytes(blob)
        report['source_snapshot']=str(source)
        run('ReviewScopeWitnesses',[str(args.lean),'-j1','-DElab.async=false','-o','ReviewScopeWitnesses.olean',source.name])
        report['object_sha256']=sha(snapshot/'ReviewScopeWitnesses.olean')
        audit='''import ReviewScopeWitnesses
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  for mod in env.allImportedModuleNames do
    logInfo m!"AUDIT_IMPORT {mod}"
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if mod.toString == "ReviewScopeWitnesses" then
        match info with
        | .axiomInfo v =>
          if v.isUnsafe then
            logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {mod} {name}"
          else
            throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          logInfo m!"AUDIT_THEOREM {mod} {name}"
          elabCommand (← `(command| #print axioms $(mkIdent name)))
        | _ => pure ()
'''
        auditpath=snapshot/'ScopeTheoremAudit.lean';auditpath.write_text(audit)
        (evidence/'ScopeTheoremAudit.lean').write_text(audit)
        report['audit_source_sha256']=sha(auditpath)
        output=run('ScopeTheoremAudit',[str(args.lean),'-j1','-DElab.async=false',auditpath.name])
        declared=re.findall(r'^AUDIT_THEOREM (\S+) (\S+)$',output,re.MULTILINE)
        names={n:m for m,n in declared}
        if not names or len(names)!=len(declared):raise ValueError('Empty/duplicate environment theorem enumeration')
        audited={}
        for n,ax in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",output):
            if n in audited:raise ValueError('Duplicate axiom record')
            audited[n]=sorted(a.strip() for a in ax.split(',') if a.strip())
        for n in re.findall(r"'([^']+)' does not depend on any axioms",output):
            if n in audited:raise ValueError('Duplicate empty axiom record')
            audited[n]=[]
        if set(audited)!=set(names):raise ValueError('Incomplete compiled-theorem audit')
        bad={n:a for n,a in audited.items() if set(a)-ALLOWED}
        report['forbidden_transitive_axioms']=bad
        if bad:raise ValueError('Forbidden transitive axioms')
        required={'P196.Agent104.Agent4Review.'+n for n in EXPECTED}
        if not required<=set(names):raise ValueError('Missing named scope theorem')
        report['theorem_count']=len(names)
        report['theorems']={n:{'module':names[n],'axioms':audited[n]} for n in sorted(names)}
        report['unsafe_implementation_axioms']=re.findall(r'^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$',output,re.MULTILINE)
        imported=set(re.findall(r'^AUDIT_IMPORT (\S+)$',output,re.MULTILINE))
        expected_imports=set(closure['imported_object_fingerprints'])|{'ReviewScopeWitnesses'}
        if imported!=expected_imports:raise ValueError('Unexpected witness/audit import closure')
        for module,rec in closure['imported_object_fingerprints'].items():
            if sha(rec['path'])!=rec['sha256']:raise ValueError('Dependency object changed '+module)
        for module,rec in closure['sources'].items():
            if sha(snapshot/(module+'.lean'))!=rec['sha256']:raise ValueError('Original closure source changed '+module)
        if sha(source)!=WITNESS_PIN:raise ValueError('Witness snapshot changed')
        if sha(repo/WITNESS_PATH)!=WITNESS_PIN:raise ValueError('Working witness changed')
        for path,digest in closure['compiler_fingerprints'].items():
            if sha(path)!=digest:raise ValueError('Compiler changed during scope check '+path)
        report['imported_object_pins_unchanged']=True
        report['source_pins_unchanged']=True
        report['status']='PASS';save(reportfile,report)
        print(f'PASS: {len(names)} compiled scope theorem constants exhaustively audited',flush=True)
        return 0
    except Exception as exc:
        report['status']='FAIL';report['failure']=str(exc);save(reportfile,report)
        print('FAIL: '+str(exc),flush=True);return 1

if __name__=='__main__':raise SystemExit(main())
