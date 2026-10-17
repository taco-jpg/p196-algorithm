from pathlib import Path
import json, hashlib, subprocess, sys, os, time, resource, shutil, re
root=Path(__file__).resolve().parents[5]
evidence=Path(__file__).resolve().parent
out=evidence/('attempt-'+sys.argv[1]); out.mkdir()
compiler=Path('/workspace/p196-tools/lean-4.19.0-linux/bin/lean')
ledger=Path('/workspace/p196-agent1-session-20261016/nine-center-normal-author-build/attempt-001')
cycle=Path('/workspace/p196-agent1-session-20261016/nine-excursion-parent-clean-001/agent1-periodic-nine-excursion/source')
center=Path('/workspace/p196-agent1-nine-excursion-20261017/proofs/contributions/agent-1/periodic-nine-excursion-20261017/sharpness/attempt-006')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
reg=json.loads((root/'proofs/Agent1PeriodicNinesExcursion.registry.json').read_text())['projects']['agent1-periodic-nine-excursion']['modules']
reg['Agent1PeriodicCenterNormalPath']={'path':'proofs/Agent1PeriodicCenterNormalPath.lean','sha256':'fbf8ff955a238d4f3257073e9a936391df7203ad822e4cd5da2c427803ad59b4','imports':['Agent1PeriodicWidthPath']}
reg['Agent1PeriodicNinesClockStrip']={'path':'proofs/Agent1PeriodicNinesClockStrip.lean','sha256':'cf78db242e666ffaeb85444ee2347b97dac629a2dc6835c2ebf62b07f3a022d5','imports':['Agent1PeriodicNinesCenter']}
seen=set()
def visit(n):
 if n in seen:return
 seen.add(n)
 for i in reg[n]['imports']:
  if i in reg:visit(i)
for n in ['Agent1PeriodicNinesExcursion','Agent1PeriodicCenterNormalPath','Agent1PeriodicNinesClockStrip']:visit(n)
pins={}
for n in sorted(seen):
 s=root/reg[n]['path']; assert sha(s)==reg[n]['sha256'],n
 candidates=[d for d in [ledger,cycle,center] if (d/(n+'.olean')).exists() and (d/(n+'.lean')).exists() and sha(d/(n+'.lean'))==sha(s)]
 assert candidates,n
 dep=candidates[0]; o=dep/(n+'.olean')
 pins[n]={'source_path':str(s),'source_sha256':sha(s),'build_source':str(dep/(n+'.lean')),'object':str(o),'object_sha256':sha(o),'reused':True}
(out/'dependencies.json').write_text(json.dumps({'fresh_closure':False,'role':'author incremental; objects reused from pinned prior author/fresh builds','modules':pins},indent=2)+'\n')
source=root/'proofs/Agent1PeriodicNinesSharpExcursion.lean';shutil.copyfile(source,out/source.name);shutil.copyfile(__file__,out/'run.py')
audit='''import Agent1PeriodicNinesSharpExcursion
import Lean.Elab.BuiltinEvalCommand
import Lean.Util.CollectAxioms
open Lean Elab Command
#check Agent1.Periodic.quotient_return_nines_center_drop_eight
#check Agent1.Periodic.quotient_path_nines_centers_le_eight_no_return
#print axioms Agent1.Periodic.quotient_return_nines_center_drop_eight
#print axioms Agent1.Periodic.quotient_path_nines_centers_le_eight_no_return
run_cmd do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      if env.allImportedModuleNames[idx.toNat]!.toString == "Agent1PeriodicNinesSharpExcursion" then
        match info with
        | .thmInfo _ =>
          count := count + 1
          let axs ← liftCoreM (Lean.collectAxioms name)
          if axs.toList.any (fun ax => !(allowed.contains ax)) then
            throwError m!"DISALLOWED_AXIOMS {name} : {axs.toList}"
          logInfo m!"AUDIT_THEOREM {name} : {axs.toList}"
        | _ => throwError m!"UNEXPECTED_NEW_CONSTANT {name}"
  logInfo m!"MODULE_AUDIT theorem_constants={count} safe_defs=0 runtime=0 custom_axioms=0"
'''
(out/'ExcursionAudit.lean').write_text(audit)
env=dict(os.environ,LEAN_PATH=':'.join(map(str,[out,ledger,cycle,center])))
records=[]
def limits():resource.setrlimit(resource.RLIMIT_AS,(8*1024**3,8*1024**3))
for name,args in [('compile',['-o','Agent1PeriodicNinesSharpExcursion.olean',source.name]),('audit',['ExcursionAudit.lean'])]:
 argv=[str(compiler),'--trust=0','-j1','-DElab.async=false',*args];start=time.time()
 p=subprocess.run(argv,cwd=out,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=600,preexec_fn=limits)
 (out/(name+'.log')).write_bytes(p.stdout)
 records.append({'name':name,'argv':argv,'cwd':str(out),'LEAN_PATH':env['LEAN_PATH'],'exit_code':p.returncode,'started_at_epoch':start,'finished_at_epoch':time.time(),'log_sha256':sha(out/(name+'.log'))})
 (out/'commands.json').write_text(json.dumps(records,indent=2)+'\n')
 if p.returncode:break
result={'status':'PASS' if len(records)==2 and all(x['exit_code']==0 for x in records) else 'FAIL','source_sha256':sha(source),'compiler_sha256':sha(compiler),'dependency_count':len(pins),'fresh_closure':False,'commands':records}
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='commands'}));print((out/(records[-1]['name']+'.log')).read_text())
sys.exit(0 if result['status']=='PASS' else 1)
