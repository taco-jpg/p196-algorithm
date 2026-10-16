import hashlib,json,subprocess,time,sys,shutil
from pathlib import Path
ROOT=Path('/workspace/p196-agent1-handoff-20261016')
BUILD=Path('/workspace/p196-agent1-session-20261016/handoff-author-build')
EVIDENCE=ROOT/'proofs/contributions/agent-1/groupIII-handoff-20261016/author'
LEAN=Path('/workspace/p196-tools/lean-4.19.0-linux/bin/lean')
ENV={'PATH':str(LEAN.parent)+':/usr/bin:/bin','LANG':'C.UTF-8','LEAN_PATH':str(BUILD)}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(label,modules):
 out=EVIDENCE/label;out.mkdir(parents=True,exist_ok=False);BUILD.mkdir(parents=True,exist_ok=True)
 record={'label':label,'compiler':subprocess.check_output([str(LEAN),'--version'],text=True).strip(),'compiler_sha256':digest(LEAN),'cwd':str(BUILD),'environment':ENV,'commands':[],'status':'RUNNING'}
 def save():(out/'run.json').write_text(json.dumps(record,indent=2)+'\n')
 for name,path in modules:
  b=path.read_bytes();(out/(name+'.lean')).write_bytes(b);(BUILD/(name+'.lean')).write_bytes(b)
  obj=BUILD/(name+'.olean')
  if obj.exists():obj.unlink()
  cmd=[str(LEAN),'--trust=0','-j1','-DElab.async=false','-o',name+'.olean',name+'.lean'];start=time.monotonic()
  with (out/(name+'.log')).open('wb') as f:
   result=subprocess.run(cmd,cwd=BUILD,env=ENV,stdout=f,stderr=subprocess.STDOUT,timeout=1800)
  row={'module':name,'source':str(path),'source_sha256':hashlib.sha256(b).hexdigest(),'argv':cmd,'exit_code':result.returncode,'elapsed_seconds':round(time.monotonic()-start,6),'log_sha256':digest(out/(name+'.log'))};record['commands'].append(row);save();print(json.dumps(row),flush=True)
  if result.returncode:record['status']='FAIL';save();return result.returncode
 record['status']='PASS';save();return 0
if __name__=='__main__':
 label=sys.argv[1]
 if label=='baseline':
  mapping=json.loads((ROOT/'proofs/SOURCE_MAP.json').read_text())['paths']
  pairs=[('LychrelDigitSums','proofs/research/continuation/LychrelDigitSums.lean')]+[(n,'proofs/research/main_existence_attempt/correlation_pass/lean/'+n+'.lean') for n in ['SafeDelay','DecimalSafeRuns','DecimalDelayBridge','PairDelayBridge']]+[('DelayedOverlapGate','proofs/research/main_existence_attempt/renewal_pass/lean/DelayedOverlapGate.lean')]
  modules=[]
  for n,p in pairs:
   info=mapping[p];path=ROOT/(info.get('current') or info['preserved']);assert digest(path)==info['sha256'];modules.append((n,path))
 else:modules=[(n,ROOT/'proofs'/(n+'.lean')) for n in sys.argv[2:]]
 sys.exit(run(label,modules))
