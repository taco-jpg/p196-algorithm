#!/usr/bin/env python3
"""Fresh foundation + frozen scope checks and unproved specification typechecking.

Requires a PASS from the independent original temporal-strip execution. It
reuses only that exact freshly built strip object, builds the foundation anew,
and audits all compiled theorem constants from all five selected local modules.
The two bridge Prop definitions are explicitly *not* accepted as proved results.
Version 2 selects the explicit-application ExactTypesApplied fixture.
The frozen original ExactTypes draft and version-1 runner remain unexecuted.
A manifest pins the semantic author's frozen source files before any compilation.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import subprocess
import time

BASE_COMMIT='5bd98567b259659fd3195f5aa61617422aa80914'
BASE_PATH='proofs/research/continuation/LychrelDigitSums.lean'
BASE_SHA='ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57'
MODULES=['NoAlternatingReturn','LychrelDigitSums','ScopeTests','ExactTypesApplied','ActualMapObligations']
CONTRACTS=['Agent104.TemporalStripObligations.ActualPrefixTransportObligation','Agent104.TemporalStripObligations.UniformBandTailObligation']


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for key in ['repo','build','original-evidence','evidence','lean','semantic-manifest']:
        parser.add_argument('--'+key,type=Path,required=True)
    parser.add_argument('--slot-authorization',required=True)
    args=parser.parse_args()
    helper_path=Path(__file__).with_name('review.py')
    helper=runpy.run_path(str(helper_path))
    sha,save,code_only=helper['sha'],helper['save'],helper['code_only']
    repo,build,evidence=args.repo.resolve(),args.build.resolve(),args.evidence.resolve()
    snapshot=build/'snapshot'
    original_file=args.original_evidence.resolve()/'verification.json'
    original=json.loads(original_file.read_text())
    if original['status']!='PASS':raise ValueError('Original single-module review must pass first')
    if original['source']['source_commit']!=BASE_COMMIT:raise ValueError('Unexpected original strip source commit')
    if any((snapshot/(m+'.olean')).exists() for m in MODULES[1:]):raise ValueError('Pre-existing auxiliary objects; preserve attempt and use fresh directory')
    manifest=json.loads(args.semantic_manifest.read_text())
    if set(manifest['modules'])!={'ScopeTests','ExactTypesApplied','ActualMapObligations'}:raise ValueError('Semantic manifest module mismatch')
    evidence.mkdir(parents=True,exist_ok=False)
    report={'status':'IN_PROGRESS','slot_authorization':args.slot_authorization,
        'runner_sha256':sha(__file__),'helper_runner_sha256':sha(helper_path),
        'original_evidence':str(original_file),'original_evidence_sha256':sha(original_file),
        'semantic_manifest':str(args.semantic_manifest.resolve()),'semantic_manifest_sha256':sha(args.semantic_manifest),
        'foundation_rebuilt_from_source':True,'reused_only_independently_rebuilt_strip_object':True,
        'local_compiler_processes':1,'compiler_threads':1,'asynchronous_elaboration':False,
        'memory_cap':None,'timeout':None,'allowed_axioms':sorted(helper['ALLOWED']),
        'sources':{'NoAlternatingReturn':original['source']},'builds':[],
        'scope':'Original abstract strip theorem plus independent hypothesis fixtures. ActualMapObligations contains unproved Prop contracts; typechecking is not a proof of either contract.'}
    reportfile=evidence/'verification.json';save(reportfile,report)
    env=dict(os.environ)
    for key in ['LEAN_PATH','LEAN_SRC_PATH','LEAN_SYSROOT','LD_PRELOAD','LD_LIBRARY_PATH']:env.pop(key,None)
    env['LEAN_PATH']=str(snapshot)
    def run(label,command):
        log=evidence/(label+'.log');start=time.monotonic()
        with log.open('w') as stream:
            proc=subprocess.Popen(command,cwd=snapshot,env=env,stdout=stream,stderr=subprocess.STDOUT)
            _,status,usage=os.wait4(proc.pid,0);proc.returncode=os.waitstatus_to_exitcode(status)
        rec={'label':label,'command':command,'cwd':str(snapshot),'exit_code':proc.returncode,
            'seconds':round(time.monotonic()-start,3),'log':log.name,'log_sha256':sha(log),
            'resources':{key:getattr(usage,key) for key in ['ru_utime','ru_stime','ru_maxrss','ru_minflt','ru_majflt','ru_nswap']}}
        report['builds'].append(rec);save(reportfile,report);print(json.dumps(rec),flush=True)
        if proc.returncode:raise ValueError(f'{label}: compiler exit {proc.returncode}')
        return log.read_text()
    try:
        for module,rec in original['imported_object_fingerprints'].items():
            if sha(rec['path'])!=rec['sha256']:raise ValueError('Original imported object changed '+module)
        for path,digest in original['compiler_fingerprints'].items():
            if sha(path)!=digest:raise ValueError('Compiler changed since original audit '+path)
        if sha(snapshot/'NoAlternatingReturn.lean')!=original['source']['sha256']:raise ValueError('Original strip source changed')
        records={'LychrelDigitSums':{'source_commit':BASE_COMMIT,'path':BASE_PATH,'sha256':BASE_SHA},**manifest['modules']}
        for module,rec in records.items():
            if rec.get('source_commit'):
                blob=subprocess.check_output(['git','show',rec['source_commit']+':'+rec['path']],cwd=repo)
            else:
                blob=(repo/rec['path']).read_bytes()
            if hashlib.sha256(blob).hexdigest()!=rec['sha256']:raise ValueError('Frozen auxiliary source mismatch '+module)
            code=code_only(blob.decode())
            hits=[{'line':code.count('\n',0,m.start())+1,'token':m.group()} for m in helper['FORBIDDEN'].finditer(code)]
            if hits:raise ValueError('Excluded source trust dependencies '+module+': '+str(hits))
            imports=[m for clause in re.findall(r'^\s*import\s+(.+)$',code,re.MULTILINE) for m in clause.split()]
            expected={'LychrelDigitSums':['Std'],'ScopeTests':['NoAlternatingReturn'],'ExactTypesApplied':['NoAlternatingReturn'],'ActualMapObligations':['NoAlternatingReturn','LychrelDigitSums']}[module]
            if imports!=expected:raise ValueError('Unexpected auxiliary import closure '+module)
            theorem_names=re.findall(r'^\s*(?:private\s+)?theorem\s+(\S+)',code,re.MULTILINE)
            examples=len(re.findall(r'^\s*example\b',code,re.MULTILINE))
            if module=='ActualMapObligations' and (theorem_names or examples):raise ValueError('Specification file unexpectedly asserts theorem/example')
            if module=='ScopeTests' and examples:raise ValueError('Scope fixtures need stable theorem names for exhaustive dependency audit')
            if (snapshot/(module+'.lean')).exists() and (snapshot/(module+'.lean')).read_bytes()!=blob:raise ValueError('Conflicting source snapshot')
            (snapshot/(module+'.lean')).write_bytes(blob)
            report['sources'][module]={**rec,'bytes':len(blob),'git_blob_sha1':hashlib.sha1(f'blob {len(blob)}\0'.encode()+blob).hexdigest(),'imports':imports,'explicit_theorems':theorem_names,'source_trust_escape_scan':hits}
        save(evidence/'source-pins.json',report['sources']);save(reportfile,report)
        for module in ['ExactTypesApplied','LychrelDigitSums','ScopeTests','ActualMapObligations']:
            run(module,[str(args.lean),'-j1','-DElab.async=false','-o',module+'.olean',module+'.lean'])
            report['sources'][module]['object_sha256']=sha(snapshot/(module+'.olean'));save(reportfile,report)
        audit=helper['audit_source']().replace('import NoAlternatingReturn','import ScopeTests\nimport ExactTypesApplied\nimport ActualMapObligations')
        audit=audit.replace('if mod.toString == "NoAlternatingReturn" then','if (["NoAlternatingReturn", "LychrelDigitSums", "ScopeTests", "ExactTypesApplied", "ActualMapObligations"] : List String).contains mod.toString then')
        audit+='''\nrun_cmd do
  let env ← getEnv
  let names : List Name := [`Agent104.TemporalStripObligations.ActualPrefixTransportObligation, `Agent104.TemporalStripObligations.UniformBandTailObligation]
  for name in names do
    let some info := env.find? name | throwError m!"MISSING_CONTRACT {name}"
    match info with
    | .defnInfo v =>
      logInfo m!"UNPROVED_PROP_CONTRACT {name}"
      logInfo m!"CONTRACT_TYPE {name} {v.type}"
    | _ => throwError m!"CONTRACT_IS_NOT_DEF {name}"
'''
        (evidence/'AllFiveModulesAudit.lean').write_text(audit)
        (snapshot/'AllFiveModulesAudit.lean').write_text(audit)
        report['audit_source_sha256']=sha(evidence/'AllFiveModulesAudit.lean')
        output=run('AllFiveModulesAudit',[str(args.lean),'-j1','-DElab.async=false','AllFiveModulesAudit.lean'])
        rows=re.findall(r'^AUDIT_THEOREM (\S+) (\S+)$',output,re.MULTILINE)
        names={name:module for module,name in rows}
        if not names or len(rows)!=len(names):raise ValueError('Empty/duplicate environment theorem inventory')
        audits={}
        for name,ax in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",output):
            if name in audits:raise ValueError('Duplicate axiom record')
            audits[name]=sorted(a.strip() for a in ax.split(',') if a.strip())
        for name in re.findall(r"'([^']+)' does not depend on any axioms",output):
            if name in audits:raise ValueError('Duplicate empty axiom record')
            audits[name]=[]
        if set(audits)!=set(names):raise ValueError('Incomplete transitive audit')
        bad={name:ax for name,ax in audits.items() if set(ax)-helper['ALLOWED']}
        report['forbidden_transitive_axioms']=bad
        if bad:raise ValueError('Forbidden theorem dependency')
        report['theorems']={name:{'module':names[name],'axioms':audits[name]} for name in sorted(names)}
        report['theorem_count']=len(names)
        report['theorems_per_module']={m:sum(v==m for v in names.values()) for m in MODULES}
        report['unsafe_implementation_axioms']=re.findall(r'^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$',output,re.MULTILINE)
        for name,rec in original['theorems'].items():
            if name not in audits or audits[name]!=rec['axioms']:raise ValueError('Original theorem axiom set differs')
        reported_contracts=re.findall(r'^UNPROVED_PROP_CONTRACT (\S+)$',output,re.MULTILINE)
        if reported_contracts!=CONTRACTS:raise ValueError('Missing/extra Prop contract status record')
        for name in CONTRACTS:
            if name in names:raise ValueError('Contract incorrectly inventoried as theorem')
        report['unproved_prop_contracts']=reported_contracts
        report['contracts_proved']=False
        official_path=repo/helper['INHERITED']/'official-archive-member-pins.json'
        official=json.loads(official_path.read_text())
        prefix=args.lean.resolve().parent/'lean-4.19.0-linux'
        report['imported_object_fingerprints']={}
        for module in sorted(set(re.findall(r'^AUDIT_IMPORT (\S+)$',output,re.MULTILINE))):
            rel=module.replace('.','/')+'.olean'
            p=snapshot/rel if module in MODULES else prefix/'lib/lean'/rel
            digest=sha(p)
            if module not in MODULES and official.get('lib/lean/'+rel)!=digest:raise ValueError('Official imported object mismatch '+module)
            report['imported_object_fingerprints'][module]={'path':str(p),'sha256':digest,'local_rebuilt':module in MODULES,'official_manifest_match':None if module in MODULES else True}
        for module,rec in report['sources'].items():
            if sha(snapshot/(module+'.lean'))!=rec['sha256']:raise ValueError('Source snapshot changed '+module)
            if module in manifest['modules'] and sha(repo/rec['path'])!=rec['sha256']:raise ValueError('Frozen authored source changed '+module)
        for path,digest in original['compiler_fingerprints'].items():
            if sha(path)!=digest:raise ValueError('Compiler changed during auxiliary execution')
        report['source_and_compiler_pins_unchanged']=True
        report['status']='PASS';save(reportfile,report)
        print(f'PASS: {len(names)} theorem constants audited across five local modules; two contracts TYPECHECKED_BUT_UNPROVED',flush=True)
        return 0
    except Exception as exc:
        report['status']='FAIL';report['failure']=str(exc);save(reportfile,report)
        print('FAIL: '+str(exc),flush=True);return 1

if __name__=='__main__':raise SystemExit(main())
