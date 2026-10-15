#!/usr/bin/env python3
"""Audit every public declaration in the two independently reviewed modules."""
from pathlib import Path
import hashlib, json, os, re, subprocess
REPO = Path('/workspace/scratch/50e90e07524e/p196-agent106')
CONTRIB = REPO/'proofs/contributions/agent-106/run-births'
EVIDENCE = CONTRIB/'review/nooverflow-reviewer'
BUILD = Path('/workspace/scratch/50e90e07524e/review106-nooverflow-fresh')
LEAN = '/workspace/scratch/50e90e07524e/runtime/lean-4.19.0-linux/bin/lean'
def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()
report = json.loads((EVIDENCE/'rebuild.json').read_text())
names=[]
for module in ['BaseBirths', 'PopulationObstructions']:
    entry = next(item for item in report['modules'] if item['module']==module)
    assert entry['exit_code']==0
    source=BUILD/(module+'.lean')
    assert digest(source)==entry['source_sha256']==digest(CONTRIB/(module+'.lean'))
    text=source.read_text()
    ns=re.findall(r'^namespace ([A-Za-z0-9_.]+)$',text,re.M)
    assert len(ns)==1
    names.extend(ns[0]+'.'+n for n in re.findall(r'^(?:def|theorem) ([A-Za-z0-9_]+)',text,re.M))
audit='import BaseBirths\nimport PopulationObstructions\n\n'
audit+='\n'.join('#print axioms '+n for n in names)+'\n'
(EVIDENCE/'ExportedAxioms.lean').write_text(audit)
(BUILD/'ExportedAxioms.lean').write_text(audit)
env=dict(os.environ, LEAN_PATH=str(BUILD), LD_PRELOAD='/workspace/scratch/50e90e07524e/runtime/readlink_self.so')
env.pop('LEAN_SRC_PATH',None)
env.pop('LEAN_SYSROOT',None)
cmd=[LEAN,'-j1','-DElab.async=false','ExportedAxioms.lean']
proc=subprocess.run(cmd,cwd=BUILD,env=env,text=True,capture_output=True)
output=proc.stdout+proc.stderr
(EVIDENCE/'ExportedAxioms.log').write_text(output)
assert proc.returncode==0
found={}
for n, aa in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",output):
    found[n]=[a.strip() for a in aa.split(',') if a.strip()]
for n in re.findall(r"'([^']+)' does not depend on any axioms",output):
    found[n]=[]
assert set(names)==set(found)
allowed={'propext','Classical.choice','Quot.sound'}
assert all(set(aa)<=allowed for aa in found.values())
result=dict(status='PASS',public_declarations=len(names),axioms=found,
    source_sha256=digest(EVIDENCE/'ExportedAxioms.lean'),
    log_sha256=digest(EVIDENCE/'ExportedAxioms.log'),script_sha256=digest(__file__),
    command=cmd,exit_code=proc.returncode)
(EVIDENCE/'axioms.json').write_text(json.dumps(result,indent=2)+'\n')
print('Public declaration axiom audit PASS:',len(names))
