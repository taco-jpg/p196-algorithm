#!/usr/bin/env python3
"""Clean Lean 4.19.0 source rebuild and transitive axiom audit for Agent123."""
from pathlib import Path
import hashlib,json,os,re,subprocess,sys,tempfile,time
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
EVIDENCE=BASE/'evidence'
EVIDENCE.mkdir(exist_ok=True)
SOURCES=[
 'proofs/research/continuation/LychrelDigitSums.lean',
 'proofs/research/main_existence_attempt/renewal_pass/lean/incoming_carry/IncomingCarrySensitivity.lean',
 'proofs/research/main_existence_attempt/renewal_pass/lean/raw_symmetry/RawSymmetryObstruction.lean',
 'proofs/research/main_existence_attempt/continuation_pass/lean/IntrinsicSeam.lean',
 'proofs/contributions/agent-123/seam-mask-realizability/SeamMaskRealizability.lean',
 'proofs/contributions/agent-123/seam-mask-realizability/SeamMaskMass.lean',
]
lean=str(Path(sys.argv[1]).resolve())
version=subprocess.check_output([lean,'--version'],text=True).strip()
if 'version 4.19.0' not in version: raise SystemExit('Wrong Lean version: '+version)
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
records={'agent':123,'commit':commit,'lean':version,'status':'WIP','sources':{},'commands':[]}
print('SOURCE_COMMIT',commit,'LEAN',version,flush=True)
for rel in SOURCES:
 p=ROOT/rel
 records['sources'][rel]=hashlib.sha256(p.read_bytes()).hexdigest()
 print('SOURCE',rel,records['sources'][rel],flush=True)
exports=[]
for rel in SOURCES[4:]:
 exports+=re.findall(r'^theorem\s+([A-Za-z0-9_]+)',(ROOT/rel).read_text(),re.M)
audit='import SeamMaskMass\n'+''.join('#print axioms Agent123.SeamMasks.'+x+'\n' for x in exports)
(EVIDENCE/'Audit.lean').write_text(audit)
try:
 with tempfile.TemporaryDirectory(prefix='agent123-clean-') as tmp:
  build=Path(tmp)
  env=dict(os.environ,LEAN_PATH=tmp)
  for rel in SOURCES:
   src=ROOT/rel
   (build/src.name).write_bytes(src.read_bytes())
  (build/'Audit.lean').write_text(audit)
  for name in [Path(p).name for p in SOURCES]+['Audit.lean']:
   cmd=[lean,'-o',name[:-5]+'.olean',name]
   start=time.time()
   cp=subprocess.run(cmd,cwd=build,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=240)
   (EVIDENCE/(name+'.log')).write_text(cp.stdout)
   print('COMPILE',name,'EXIT',cp.returncode,'SECONDS',round(time.time()-start,3),flush=True)
   print(cp.stdout,flush=True)
   records['commands'].append({'command':cmd,'exit_status':cp.returncode})
   if cp.returncode: raise RuntimeError('Lean compile failed: '+name)
   if name=='Audit.lean':
    reports=re.findall(r"(?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)",cp.stdout)
    if len(reports)!=len(exports): raise RuntimeError('Missing axiom audit output')
    for report in reports:
     axioms={x.strip() for x in report.split(',') if x.strip()}
     if not axioms <= {'propext','Classical.choice','Quot.sound'}:
      raise RuntimeError('Unapproved transitive axioms: '+str(axioms))
  records['status']='LEAN-CHECKED'
  records['exports']=['Agent123.SeamMasks.'+x for x in exports]
finally:
 (EVIDENCE/'verification.json').write_text(json.dumps(records,indent=2)+'\n')
print('RESULT',records['status'],flush=True)
