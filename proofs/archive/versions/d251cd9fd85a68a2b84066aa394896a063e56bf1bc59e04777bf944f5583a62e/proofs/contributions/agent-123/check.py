#!/usr/bin/env python3
"""Clean, source-pinned Lean 4.19.0 rebuild and transitive axiom audit."""
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
 'proofs/contributions/agent-123/seam-mask-realizability/SeamMaskMinimalCuts.lean',
 'proofs/contributions/agent-123/seam-mask-realizability/Agent123All.lean',
]
DEPENDENCY_HASHES=[
 'ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57',
 '52850d75999a8fdad298e2e9da638965472ab6507f88630bf428698576ac631f',
 '922b660e5b3ac42389cd6ea00885075327d4b44fb315b9cc496e1323890e9c87',
 'de764dffc4d72b3060c3648339116adc4cfeb3d425a2edd5ef4e42056ec36b20',
]
def without_comments(text):
 out=[];i=0;depth=0
 while i<len(text):
  if text[i:i+2]=='/-': depth+=1;i+=2
  elif depth and text[i:i+2]=='-/':depth-=1;i+=2
  elif depth:i+=1
  elif text[i:i+2]=='--':
   j=text.find('\n',i);i=len(text) if j<0 else j
  else:out.append(text[i]);i+=1
 return re.sub(r'"(?:\\.|[^"\\])*"','""',''.join(out))
lean=str(Path(sys.argv[1]).resolve())
version=subprocess.check_output([lean,'--version'],text=True).strip()
if 'version 4.19.0' not in version or '6caaee842e94' not in version:
 raise SystemExit('Wrong Lean version: '+version)
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
records={'agent':123,'commit':commit,'source_base':'eec3d5f3646cab50abad6e610ea19626cd249070',
 'lean':version,'status':'WIP','review_level':'author execution, not independent review',
 'build_isolation':'new empty temporary directory; no reused project objects','sources':{},'commands':[]}
print('SOURCE_COMMIT',commit,'LEAN',version,flush=True)
for index,rel in enumerate(SOURCES):
 p=ROOT/rel
 digest=hashlib.sha256(p.read_bytes()).hexdigest()
 if index<4 and digest!=DEPENDENCY_HASHES[index]:raise SystemExit('Dependency source drift: '+rel)
 code=without_comments(p.read_text())
 bad=re.search(r'\b(sorry|admit|sorryAx|native_decide|axiom|unsafe|implemented_by|extern)\b',code)
 if bad:raise SystemExit('Excluded source token '+bad.group()+' in '+rel)
 records['sources'][rel]=digest
 print('SOURCE',rel,digest,flush=True)
exports=[]
for rel in SOURCES[4:]:
 exports+=re.findall(r'^(?:theorem|def)\s+([A-Za-z0-9_]+)',(ROOT/rel).read_text(),re.M)
audit='import Agent123All\n'+''.join('#print axioms Agent123.SeamMasks.'+x+'\n' for x in exports)
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
   if cp.returncode:raise RuntimeError('Lean compile failed: '+name)
   if name=='Audit.lean':
    reports=re.findall(r"(?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)",cp.stdout)
    if len(reports)!=len(exports):raise RuntimeError('Missing axiom audit output')
    for report in reports:
     axioms={x.strip() for x in report.split(',') if x.strip()}
     if not axioms <= {'propext','Classical.choice','Quot.sound'}:
      raise RuntimeError('Unapproved transitive axioms: '+str(axioms))
  records['status']='LEAN-CHECKED'
  records['exports']=['Agent123.SeamMasks.'+x for x in exports]
finally:
 (EVIDENCE/'verification.json').write_text(json.dumps(records,indent=2)+'\n')
control=BASE/'exact_controls.py'
records['controls_source_sha256']=hashlib.sha256(control.read_bytes()).hexdigest()
cp=subprocess.run([sys.executable,str(control)],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=180)
(EVIDENCE/'exact-controls.log').write_text(cp.stdout)
print(cp.stdout,flush=True)
if cp.returncode:raise SystemExit(cp.returncode)
(EVIDENCE/'verification.json').write_text(json.dumps(records,indent=2)+'\n')
print('RESULT',records['status'],flush=True)
