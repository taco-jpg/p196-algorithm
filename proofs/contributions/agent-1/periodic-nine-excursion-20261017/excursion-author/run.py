from pathlib import Path
import json, hashlib, subprocess, sys, os, time, resource, shutil, re
root=Path(__file__).resolve().parents[5]
evidence=Path(__file__).resolve().parent
out=evidence/('attempt-'+sys.argv[1]); out.mkdir()
compiler=Path('/workspace/p196-tools/lean-4.19.0-linux/bin/lean')
ledger=Path('/workspace/p196-agent1-session-20261016/nine-ledger-author-build/attempt-001')
cycle=Path('/workspace/p196-agent1-session-20261016/nine-cycle-parent-clean-001/agent1-periodic-nine-cycle/source')
center=Path('/workspace/p196-agent1-session-20261016/nine-center-parent-clean-001/agent1-periodic-nine-center/source')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
reg={}
for suffix in ['NinesCycle','NinesCenter']:
 d=json.loads((root/f'proofs/Agent1Periodic{suffix}.registry.json').read_text())
 for k,v in next(iter(d['projects'].values()))['modules'].items():
  if k in reg:assert reg[k]['sha256']==v['sha256']
  reg[k]=v
reg['Agent1PeriodicNinesLedger']={'path':'proofs/Agent1PeriodicNinesLedger.lean','sha256':'f3cbfad8fc013e88d5337f51e4f43d8d4e459460f677b065b336876b2069af4a','imports':['Agent1PeriodicNinesCenter','Agent1PeriodicNinesPath']}
seen=set()
def visit(n):
 if n in seen:return
 seen.add(n)
 for i in reg[n]['imports']:
  if i in reg:visit(i)
for n in ['Agent1PeriodicNinesLedger','Agent1PeriodicReturnClock']:visit(n)
pins={}
for n in sorted(seen):
 s=root/reg[n]['path']; assert sha(s)==reg[n]['sha256'],n
 candidates=[d for d in [ledger,cycle,center] if (d/(n+'.olean')).exists() and (d/(n+'.lean')).exists() and sha(d/(n+'.lean'))==sha(s)]
 assert candidates,n
 dep=candidates[0]; o=dep/(n+'.olean')
 pins[n]={'source_path':str(s),'source_sha256':sha(s),'build_source':str(dep/(n+'.lean')),'object':str(o),'object_sha256':sha(o),'reused':True}
(out/'dependencies.json').write_text(json.dumps({'fresh_closure':False,'role':'author incremental; objects reused from pinned prior author/fresh builds','modules':pins},indent=2)+'\n')
source=root/'proofs/Agent1PeriodicNinesExcursion.lean';shutil.copyfile(source,out/source.name);shutil.copyfile(__file__,out/'run.py')
audit='''import Agent1PeriodicNinesExcursion
import Lean.Elab.BuiltinEvalCommand
import Lean.Util.CollectAxioms
open Lean Elab Command
#check Agent1.Periodic.quotient_return_nines_center_excursion
#check Agent1.Periodic.quotient_path_nines_small_centers_no_return
#print axioms Agent1.Periodic.quotient_return_nines_center_excursion
#print axioms Agent1.Periodic.quotient_path_nines_small_centers_no_return
run_cmd do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      if env.allImportedModuleNames[idx.toNat]!.toString == "Agent1PeriodicNinesExcursion" then
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
for name,args in [('compile',['-o','Agent1PeriodicNinesExcursion.olean',source.name]),('audit',['ExcursionAudit.lean'])]:
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
