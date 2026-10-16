#!/usr/bin/env python3
"""Independent fresh source-closure build with explicit and module-origin audits."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import subprocess
import time

PACKAGE = Path(__file__).resolve().parents[1]
REPO = PACKAGE.parents[3]
LEAN = Path('/workspace/scratch/aaafdd394dd6/agent7-runtime/lean-4.19.0-linux/bin/lean')
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', action='append', required=True)
    ap.add_argument('--expect', action='append', default=[])
    ap.add_argument('--fixture', type=Path, action='append', default=[])
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    out=args.output.resolve(); out.mkdir(parents=True,exist_ok=False)
    src=out/'source'; src.mkdir(); logs=out/'logs'; logs.mkdir()
    verifier=runpy.run_path(str(REPO/'proofs/verify_project__214bf7673efe116b.py'),run_name='review_reference')
    code_only=verifier['code_only']
    sources={p.stem:p for p in (PACKAGE/'dependencies').glob('*.lean')}
    sources.update({p.stem:p for p in PACKAGE.glob('*.lean')})
    sources.update({p.stem:p.resolve() for p in args.fixture})
    expected=dict(s.split('=',1) for s in args.expect)
    pins={p['module']:p['sha256'] for p in json.loads((PACKAGE/'dependencies/SOURCE_PINS.json').read_text())['dependencies']}
    expected.update(pins)
    roots=[*args.root,*[p.stem for p in args.fixture]]
    order=[]; records={}; active=set()
    def visit(module):
        if module in records: return
        if module not in sources:
            if module.split('.')[0] in {'Std','Lean','Init'}: return
            raise ValueError('Missing source: '+module)
        if module in active: raise ValueError('Import cycle: '+module)
        active.add(module)
        original=sources[module]; data=original.read_bytes(); code=code_only(data.decode())
        digest=hashlib.sha256(data).hexdigest()
        if module in expected and digest!=expected[module]: raise ValueError('Source pin changed: '+module)
        if re.search(r'\b(?:sorry|admit|axiom|sorryAx|native_decide|ofReduceBool|skipKernelTC)\b',code): raise ValueError('Forbidden source token: '+module)
        imports=[d for line in re.findall(r'^\s*import\s+([^\n]+)',code,re.M) for d in line.split()]
        for dependency in imports: visit(dependency)
        spaces=re.findall(r'^namespace\s+(\S+)',code,re.M)
        if len(spaces)!=1: raise ValueError('Inspect namespace structure manually: '+module)
        names=re.findall(r'^(?:@\[[^\n]*\]\s*)?(?:theorem|lemma)\s+([A-Za-z_][\w.]*)',code,re.M)
        public=[spaces[0]+'.'+name for name in names]
        (src/(module+'.lean')).write_bytes(data)
        records[module]={'original':str(original),'sha256':digest,'git_blob':hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest(),'imports':imports,'public_theorems':public}
        active.remove(module); order.append(module)
    for module in roots: visit(module)
    version=subprocess.check_output([str(LEAN),'--version'],text=True).strip()
    assert 'version 4.19.0,' in version and 'commit 6caaee842e94, Release' in version
    report={'reviewer':'Agent #7 /root/runtime','started_at':datetime.now(timezone.utc).isoformat(),'status':'RUNNING','roots':roots,'source_records':records,'build_order':order,'commands':[],'fresh_project_objects':True,'lean_version':version,'lean_sha256':sha(LEAN)}
    def save(): (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    env=dict(os.environ); env['LEAN_PATH']=str(src)
    def run(module,compile_object=True):
        command=[str(LEAN),'--trust=0','-j1','-DElab.async=false']
        if compile_object: command+=['-o',module+'.olean']
        command+=[module+'.lean']; start=time.monotonic()
        with (logs/(module+'.log')).open('wb') as stream:
            p=subprocess.run(command,cwd=src,env=env,stdout=stream,stderr=subprocess.STDOUT)
        report['commands'].append({'module':module,'command':command,'cwd':str(src),'exit_code':p.returncode,'elapsed_seconds':time.monotonic()-start,'log_sha256':sha(logs/(module+'.log'))}); save()
        print(module+' exit='+str(p.returncode),flush=True)
        if p.returncode: raise RuntimeError((logs/(module+'.log')).read_text())
    try:
        save()
        for module in order: run(module)
        public=[name for module in order for name in records[module]['public_theorems']]
        assert len(public)==len(set(public))
        audit='\n'.join('import '+m for m in roots)+'\nimport Lean\nopen Lean Elab Command\nset_option maxRecDepth 100000\nset_option maxHeartbeats 0\n'
        audit+='\n'.join('#print axioms '+name for name in public)+'\n'
        audit+='run_cmd do\n  let env ← getEnv\n  let selected : List String := '+json.dumps(order)+'''\n  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        match info with
        | .axiomInfo v =>
          if v.isUnsafe then logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {mod} {name}"
          else throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          let axs ← liftCoreM (Lean.collectAxioms name)
          if axs.toList.any (fun a => !(allowed.contains a)) then throwError m!"DISALLOWED_AXIOMS {mod} {name}: {axs.toList}"
          count := count + 1
          logInfo m!"AUDIT_THEOREM {mod} {name}: {axs.toList}"
        | _ => pure ()
  logInfo m!"FULL_MODULE_AUDIT theorems={count}"
'''
        (src/'PublicAudit.lean').write_text(audit); run('PublicAudit',False)
        text=(logs/'PublicAudit.log').read_text()
        printed=re.findall(r"^'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)$",text,re.M)
        assert set(n for n,a in printed)==set(public) and len(printed)==len(public)
        for name,axes in printed: assert set(axes.split(', ') if axes else [])<=ALLOWED
        constants=re.findall(r'^AUDIT_THEOREM (\S+) (\S+): (.*)$',text,re.M)
        count=re.findall(r'^FULL_MODULE_AUDIT theorems=(\d+)$',text,re.M)
        assert len(count)==1 and int(count[0])==len(constants) and len({n for m,n,a in constants})==len(constants)
        for module,record in records.items():
            assert sha(sources[module])==record['sha256'] and sha(src/(module+'.lean'))==record['sha256']
            record['object_sha256']=sha(src/(module+'.olean'))
        report.update(status='PASS',public_theorem_count=len(public),module_origin_theorem_count=len(constants),allowed_axioms=sorted(ALLOWED),unsafe_implementation_axioms=re.findall(r'^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$',text,re.M))
    except Exception as e:
        report['status']='FAIL'; report['error']=str(e); print(str(e),flush=True)
    report['finished_at']=datetime.now(timezone.utc).isoformat(); save()
    raise SystemExit(0 if report['status']=='PASS' else 1)

if __name__=='__main__': main()
