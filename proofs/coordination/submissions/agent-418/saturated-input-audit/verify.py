#!/usr/bin/env python3
"""Clean-build the five research modules and audit every declared theorem.
Usage: python verify.py /absolute/path/to/Lean-4.19.0/bin/lean
No external service, stale project .olean, or native_decide is used.
"""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

MODULES = [
 'Agent418SaturatedInputAudit',
 'Agent418ArbitraryOddControls',
 'Agent418FiniteDecimalWitness',
 'Agent418AllPatternsRealizable',
 'Agent418BalancedResetFailure',
]

def run(lean: str) -> int:
    here=Path(__file__).resolve().parent
    out=here/'evidence'/'clean-build'
    out.mkdir(parents=True,exist_ok=True)
    lean_path=Path(lean).expanduser().resolve()
    if not lean_path.is_file(): raise FileNotFoundError(f'Lean executable not found: {lean_path}')
    version=subprocess.check_output([str(lean_path),'--version'],text=True).strip()
    if 'version 4.19.0,' not in version: raise RuntimeError(f'Wrong Lean version: {version}')
    audit_roots=[]; sources={}
    for module in MODULES:
        p=here/(module+'.lean'); s=p.read_text()
        namespace=re.search(r'^namespace\s+(\S+)',s,re.M).group(1)
        audit_roots.extend(namespace+'.'+name for name in re.findall(r'^theorem\s+(\w+)',s,re.M))
        sources[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
    audit='import Agent418BalancedResetFailure\n\n'+''.join('#print axioms '+r+'\n' for r in audit_roots)
    (here/'Agent418AxiomAudit.lean').write_text(audit)
    sources['Agent418AxiomAudit.lean']=hashlib.sha256(audit.encode()).hexdigest()
    report={'status':'INCOMPLETE','started_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
      'lean_version':version,'sources_sha256':sources,'steps':[],'audited_roots':audit_roots,
      'verification_scope':'Clean local rebuild of standalone exact-definition audit; not full repository build or independent reviewer.'}
    env=dict(os.environ)
    try:
        with tempfile.TemporaryDirectory(prefix='agent418-clean-') as tmp:
            root=Path(tmp); env['LEAN_PATH']=str(root)
            for name in sources:shutil.copy2(here/name,root/name)
            for module in MODULES+['Agent418AxiomAudit']:
                cmd=[str(lean_path),'-o',module+'.olean',module+'.lean']
                p=subprocess.run(cmd,cwd=root,env=env,text=True,stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,timeout=45,check=False)
                (out/(module+'.log')).write_text(p.stdout)
                report['steps'].append({'module':module,'command':cmd,'exit_code':p.returncode})
                if p.returncode:raise RuntimeError(f'Build failed: {module}; see retained log')
            text=(out/'Agent418AxiomAudit.log').read_text()
            for forbidden in ['sorryAx','Lean.ofReduceBool','Lean.trustCompiler']:
                if forbidden in text:raise RuntimeError(f'Excluded dependency {forbidden}')
            axiom_lines=[line for line in text.splitlines() if 'depends on axioms:' in line]
            allowed={'propext','Quot.sound','Classical.choice'}
            for line in axiom_lines:
                names=set(re.search(r'\[([^\]]*)\]',line).group(1).split(', '))
                if names-allowed:raise RuntimeError(f'Unexpected axioms: {names-allowed}')
            if sum(('depends on axioms:' in x or 'does not depend on any axioms' in x)
                   for x in text.splitlines())!=len(audit_roots):
                raise RuntimeError('Incomplete audit-root output')
            report['status']='LEAN-CHECKED'
            report['standard_axiom_roots']=len(axiom_lines)
            report['empty_axiom_roots']=len(audit_roots)-len(axiom_lines)
    except Exception as exc:
        report['error']=str(exc)
        raise
    finally:
        report['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
        (here/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','lean_version','standard_axiom_roots','empty_axiom_roots']},indent=2))
    return 0

if __name__=='__main__':
    if len(sys.argv)!=2:
        raise SystemExit('Usage: python verify.py /absolute/path/to/lean')
    raise SystemExit(run(sys.argv[1]))
