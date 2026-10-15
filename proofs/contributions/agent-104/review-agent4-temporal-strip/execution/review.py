#!/usr/bin/env python3
"""Immutable-source fresh Lean rebuild, exhaustive axiom audit, and exact type dump.

Without --execute this only extracts and inspects pinned source, and prepares
review programs. Compiler execution requires a recorded coordinator slot grant.
All local .olean files must be absent initially; failed attempts are preserved.
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

SOURCE_COMMIT='5bd98567b259659fd3195f5aa61617422aa80914'
SOURCE_PATH='proofs/agent4/temporal_strip/NoAlternatingReturn.lean'
SOURCE_SHA='49b1065166c02c2efd1bf58c3391c5166b44106f12e82af371304e9fe3ae7ba0'
MODULE='NoAlternatingReturn'
NAMESPACE='P196.Agent4.TemporalStrip'
EXPORTS=['left_scalar','right_scalar','left_backward','right_backward','cyclic_successor_onto','no_alternating_six_twelve_strip','no_finite_alternating_six_twelve_strip']
ALLOWED={'propext','Classical.choice','Quot.sound'}
INHERITED='proofs/contributions/agent-104/seven-column-kernel/review-final-clean/preflight-01'
FORBIDDEN=re.compile(r"(?<![\w'])\b(?:sorry|admit|axiom|newaxiom|native_decide|sorryAx|ofReduceBool|ofReduceNat|unsafe|implemented_by|extern|run_cmd|elab|macro|initialize|unsafeCast)\b(?![\w'])|#(?:eval|reduce)|debug\.skipKernelTC")


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    return h.hexdigest()


def save(path,value):Path(path).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')


def code_only(text):
    out,i,depth,string=[],0,0,False
    while i<len(text):
        pair=text[i:i+2]
        if depth:
            if pair=='/-':depth+=1;out.extend('  ');i+=2
            elif pair=='-/':depth-=1;out.extend('  ');i+=2
            else:out.append('\n' if text[i]=='\n' else ' ');i+=1
        elif string:
            if text[i]=='\\':out.extend('  ');i+=2
            else:string=text[i]!='"';out.append('\n' if text[i]=='\n' else ' ');i+=1
        elif pair=='/-':depth=1;out.extend('  ');i+=2
        elif pair=='--':
            end=text.find('\n',i);end=len(text) if end<0 else end
            out.extend(' '*(end-i));i=end
        elif text[i]=='"':string=True;out.append(' ');i+=1
        else:out.append(text[i]);i+=1
    if depth or string:raise ValueError('Unterminated source comment/string')
    return ''.join(out)


def audit_source():
    return '''import NoAlternatingReturn
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
      if mod.toString == "NoAlternatingReturn" then
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


def statement_source():
    # Both readable full-detail elaborated types and raw Expr values are retained.
    # Raw Expr is a compiler data structure, not a new trusted proof inference.
    names=', '.join('`'+NAMESPACE+'.'+name for name in EXPORTS)
    return '''import NoAlternatingReturn
import Lean
open Lean Elab Command
set_option pp.all true
set_option pp.universes true
set_option pp.proofs true
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let names : List Name := ['''+names+''']
  for name in names do
    let some info := env.find? name | throwError m!"MISSING_EXPORT {name}"
    logInfo m!"STATEMENT_BEGIN {name}"
    logInfo m!"{info.type}"
    logInfo m!"STATEMENT_RAW {name} {repr info.type}"
    logInfo m!"STATEMENT_END {name}"
'''


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for flag in ['repo','build','evidence','lean']:parser.add_argument('--'+flag,type=Path,required=True)
    parser.add_argument('--execute',action='store_true')
    parser.add_argument('--slot-authorization',default='')
    args=parser.parse_args()
    repo,build,evidence=(getattr(args,k).resolve() for k in ['repo','build','evidence'])
    evidence.mkdir(parents=True,exist_ok=True)
    snapshot=build/'snapshot';snapshot.mkdir(parents=True,exist_ok=True)
    if list(snapshot.rglob('*.olean')):raise ValueError('Pre-existing local .olean: retain attempt and use new directory')
    blob=subprocess.check_output(['git','show',SOURCE_COMMIT+':'+SOURCE_PATH],cwd=repo)
    if hashlib.sha256(blob).hexdigest()!=SOURCE_SHA:raise ValueError('Source pin mismatch')
    source=snapshot/(MODULE+'.lean')
    if source.exists() and source.read_bytes()!=blob:raise ValueError('Snapshot differs; preserve before new attempt')
    source.write_bytes(blob)
    code=code_only(blob.decode())
    imports=[m for clause in re.findall(r'^\s*import\s+(.+)$',code,re.MULTILINE) for m in clause.split()]
    if imports!=['Lean.Elab.Tactic.Omega']:raise ValueError('Unexpected local or nonlocal source dependency')
    hits=[{'line':code.count('\n',0,m.start())+1,'token':m.group()} for m in FORBIDDEN.finditer(code)]
    declarations=re.findall(r'^\s*(?:private\s+)?theorem\s+(\S+)',code,re.MULTILINE)
    if set(declarations)!=set(EXPORTS):raise ValueError('Unexpected source theorem inventory')
    source_record={'source_commit':SOURCE_COMMIT,'path':SOURCE_PATH,'sha256':SOURCE_SHA,
        'git_blob_sha1':hashlib.sha1(f'blob {len(blob)}\0'.encode()+blob).hexdigest(),
        'bytes':len(blob),'imports':imports,'explicit_theorems':declarations,'snapshot':str(source)}
    save(evidence/'source-pins.json',source_record)
    for name,text in [('AllLocalTheorems.lean',audit_source()),('StatementDump.lean',statement_source())]:
        (evidence/name).write_text(text)
    inherited_file=repo/INHERITED/'independent-preflight.json'
    official_file=repo/INHERITED/'official-archive-member-pins.json'
    inherited=json.loads(inherited_file.read_text());official=json.loads(official_file.read_text())
    preflight={'status':'PREPARED_NOT_EXECUTED','compiler_started':False,
        'source':source_record,'source_trust_escape_scan':hits,
        'source_closure_local_modules':[MODULE],'build_dir':str(build),'runner_sha256':sha(__file__),
        'inherited_toolchain_evidence':{str(inherited_file.relative_to(repo)):sha(inherited_file),str(official_file.relative_to(repo)):sha(official_file)},
        'official_archive_sha256':inherited['official_archive_sha256'],
        'official_archive_members_in_inherited_manifest':len(official),
        'toolchain_provenance':'Inherited published official Lean 4.19.0 archive-member comparison; no new archive download or independent provenance claim.',
        'inherited_LD_PRELOAD':os.environ.get('LD_PRELOAD',''),'inherited_LD_LIBRARY_PATH':os.environ.get('LD_LIBRARY_PATH',''),
        'scope':'Abstract temporal-strip implications only. No ordinary-integer bridge, P196 result, or new ownership claim.'}
    save(evidence/'preflight.json',preflight)
    if hits:raise ValueError('Excluded source trust dependency: '+str(hits))
    if any(os.environ.get(k) for k in ['LD_PRELOAD','LD_LIBRARY_PATH']):raise ValueError('Unreviewed inherited dynamic-library override')
    if not args.execute:print(json.dumps(preflight,indent=2));return 0
    if not args.slot_authorization:raise ValueError('Compiler slot authorization must be recorded')
    logdir=evidence/'logs';logdir.mkdir(exist_ok=False)
    report={'status':'IN_PROGRESS','source':source_record,'slot_authorization':args.slot_authorization,
        'runner_sha256':sha(__file__),'fresh_local_source_rebuild':True,'reused_local_objects':False,
        'local_compiler_processes':1,'compiler_threads':1,'asynchronous_elaboration':False,
        'memory_cap':None,'timeout':None,'allowed_axioms':sorted(ALLOWED),'builds':[],
        'audit_scope':'Every local compiled theorem constant, including private/generated constants, and complete transitive axiom sets.',
        'mathematical_scope':'Abstract temporal-strip implications only; ordinary-integer realization and bridge are not established.'}
    reportfile=evidence/'verification.json';save(reportfile,report)
    env=dict(os.environ)
    for key in ['LEAN_PATH','LEAN_SRC_PATH','LEAN_SYSROOT','LD_PRELOAD','LD_LIBRARY_PATH']:env.pop(key,None)
    env['LEAN_PATH']=str(snapshot)
    report['compiler_environment']={k:env.get(k,'') for k in ['LEAN_PATH','LEAN_SRC_PATH','LEAN_SYSROOT','LD_PRELOAD','LD_LIBRARY_PATH']}
    def run(label,command):
        log=logdir/(label+'.log');start=time.monotonic()
        with log.open('w') as stream:
            proc=subprocess.Popen(command,cwd=snapshot,env=env,stdout=stream,stderr=subprocess.STDOUT)
            _,status,usage=os.wait4(proc.pid,0);proc.returncode=os.waitstatus_to_exitcode(status)
        rec={'label':label,'command':command,'cwd':str(snapshot),'exit_code':proc.returncode,
            'seconds':round(time.monotonic()-start,3),'log':str(log.relative_to(evidence)),
            'log_sha256':sha(log),'resources':{key:getattr(usage,key) for key in ['ru_utime','ru_stime','ru_maxrss','ru_minflt','ru_majflt','ru_nswap']}}
        report['builds'].append(rec);save(reportfile,report);print(json.dumps(rec),flush=True)
        if proc.returncode:raise ValueError(f'{label}: compiler exit {proc.returncode}')
        return log.read_text()
    try:
        version=run('version',[str(args.lean),'--version']).strip()
        if version!='Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)':raise ValueError('Wrong Lean version')
        tc=args.lean.resolve().parent;prefix=tc/'lean-4.19.0-linux'
        actual_prefix=Path(run('prefix',[str(args.lean),'--print-prefix']).strip()).resolve()
        if actual_prefix!=prefix:raise ValueError('Unexpected toolchain installation')
        paths=[args.lean.resolve(),prefix/'bin/lean',tc/'proc-self-compat.c',tc/'proc-self-compat.so',prefix/'src/lean/Lean/Util/CollectAxioms.lean']
        paths+=sorted((prefix/'lib/lean').glob('*.so'))
        report['compiler_fingerprints']={str(p):sha(p) for p in paths}
        for p in paths:
            if p.is_relative_to(prefix) and str(p.relative_to(prefix)) in official:
                expected=official[str(p.relative_to(prefix))]
            elif str(p) in inherited['support_file_pins']:expected=inherited['support_file_pins'][str(p)]
            else:raise ValueError('Unpinned compiler component '+str(p))
            if sha(p)!=expected:raise ValueError('Toolchain fingerprint mismatch '+str(p))
        report['compiler_version']=version;report['official_manifest_sha256']=sha(official_file)
        save(reportfile,report)
        run(MODULE,[str(args.lean),'-j1','-DElab.async=false','-o',MODULE+'.olean',source.name])
        report['local_object_sha256']=sha(source.with_suffix('.olean'))
        for name,body in [('AllLocalTheorems.lean',audit_source()),('StatementDump.lean',statement_source())]:(snapshot/name).write_text(body)
        output=run('AllLocalTheorems',[str(args.lean),'-j1','-DElab.async=false','AllLocalTheorems.lean'])
        rows=re.findall(r'^AUDIT_THEOREM (\S+) (\S+)$',output,re.MULTILINE)
        names={name:module for module,name in rows}
        if not names or len(names)!=len(rows):raise ValueError('Empty/duplicate compiled theorem enumeration')
        audits={}
        for name,axioms in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",output):
            if name in audits:raise ValueError('Duplicate axiom record')
            audits[name]=sorted(a.strip() for a in axioms.split(',') if a.strip())
        for name in re.findall(r"'([^']+)' does not depend on any axioms",output):
            if name in audits:raise ValueError('Duplicate empty axiom record')
            audits[name]=[]
        if set(audits)!=set(names):raise ValueError('Incomplete compiled-theorem transitive audit')
        bad={name:ax for name,ax in audits.items() if set(ax)-ALLOWED}
        report['forbidden_transitive_axioms']=bad
        if bad:raise ValueError('Forbidden transitive axiom dependency')
        required={NAMESPACE+'.'+name for name in EXPORTS}
        if not required<=set(names):raise ValueError('Missing named theorem export')
        report['theorem_count']=len(names)
        report['theorems']={name:{'module':names[name],'axioms':audits[name]} for name in sorted(names)}
        report['seven_export_axioms']={name:audits[name] for name in sorted(required)}
        report['unsafe_implementation_axioms']=re.findall(r'^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$',output,re.MULTILINE)
        report['imported_object_fingerprints']={}
        for module in sorted(set(re.findall(r'^AUDIT_IMPORT (\S+)$',output,re.MULTILINE))):
            relative=module.replace('.','/')+'.olean'
            p=snapshot/relative if module==MODULE else prefix/'lib/lean'/relative
            digest=sha(p);rec={'path':str(p),'sha256':digest,'local_rebuilt':module==MODULE}
            if module!=MODULE:
                key='lib/lean/'+relative
                if key not in official or digest!=official[key]:raise ValueError('Official imported object mismatch '+module)
                rec['official_manifest_match']=True
            report['imported_object_fingerprints'][module]=rec
        statement_log=run('StatementDump',[str(args.lean),'-j1','-DElab.async=false','StatementDump.lean'])
        beginnings=re.findall(r'^STATEMENT_BEGIN (\S+)$',statement_log,re.MULTILINE)
        endings=re.findall(r'^STATEMENT_END (\S+)$',statement_log,re.MULTILINE)
        raw=re.findall(r'^STATEMENT_RAW (\S+) ',statement_log,re.MULTILINE)
        if len(beginnings)!=7 or set(beginnings)!=required or endings!=beginnings or raw!=beginnings:raise ValueError('Missing/ambiguous elaborated statement output')
        report['exact_elaborated_statement_count']=len(beginnings)
        report['statement_representation']='pp.all=true typed expression plus raw Expr repr, one begin/end block per named export'
        for path,digest in report['compiler_fingerprints'].items():
            if sha(path)!=digest:raise ValueError('Compiler component changed during execution')
        for module,rec in report['imported_object_fingerprints'].items():
            if sha(rec['path'])!=rec['sha256']:raise ValueError('Imported object changed during execution '+module)
        if sha(source)!=SOURCE_SHA:raise ValueError('Snapshot source changed')
        if hashlib.sha256(subprocess.check_output(['git','show',SOURCE_COMMIT+':'+SOURCE_PATH],cwd=repo)).hexdigest()!=SOURCE_SHA:raise ValueError('Pinned source no longer matches')
        report['official_imported_object_count']=sum(not r['local_rebuilt'] for r in report['imported_object_fingerprints'].values())
        report['all_source_object_compiler_pins_unchanged']=True
        report['status']='PASS';save(reportfile,report)
        print(f'PASS: one fresh local module; {len(names)} theorem constants audited; seven exact statements retained',flush=True)
        return 0
    except Exception as exc:
        report['status']='FAIL';report['failure']=str(exc);save(reportfile,report)
        print('FAIL: '+str(exc),flush=True);return 1

if __name__=='__main__':raise SystemExit(main())
