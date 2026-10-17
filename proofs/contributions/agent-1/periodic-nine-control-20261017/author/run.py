from pathlib import Path
import json,hashlib,subprocess,sys,os,time,resource,shutil
root=Path(__file__).resolve().parents[5]
evidence=Path(__file__).resolve().parent
out=evidence/('attempt-'+sys.argv[1]);out.mkdir()
compiler=Path('/workspace/p196-tools/lean-4.19.0-linux/bin/lean')
deps=Path('/workspace/p196-agent1-session-20261016/nine-cycle-parent-clean-001/agent1-periodic-nine-cycle/source')
reg=json.loads((root/'proofs/Agent1PeriodicNinesCycle.registry.json').read_text())['projects']['agent1-periodic-nine-cycle']['modules']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
seen=set()
def visit(n):
 if n in seen:return
 seen.add(n)
 for i in reg[n]['imports']:
  if i in reg:visit(i)
visit('Agent1PeriodicQuotient')
pins={}
for n in sorted(seen):
 s=root/reg[n]['path'];b=deps/(n+'.lean');o=deps/(n+'.olean')
 assert sha(s)==reg[n]['sha256']==sha(b) and o.exists(),n
 pins[n]={'source_path':str(s),'source_sha256':sha(s),'build_source':str(b),'object':str(o),'object_sha256':sha(o)}
(out/'dependencies.json').write_text(json.dumps({'role':'author incremental compile; projectobjects reused from prior parentfresh34; notfreshclosure','modules':pins},indent=2)+'\n')
source=root/'proofs/Agent1PeriodicNinesExtraStrip.lean';shutil.copyfile(source,out/source.name);shutil.copyfile(__file__,out/'run.py')
audit='''import Agent1PeriodicNinesExtraStrip
import Lean.Elab.BuiltinEvalCommand
import Lean.Util.CollectAxioms
open Lean Elab Command
#check Agent1.Periodic.nines_extra_strip_control
#print axioms Agent1.Periodic.nines_extra_strip_control
run_cmd do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  let mut found := false
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      if env.allImportedModuleNames[idx.toNat]!.toString == "Agent1PeriodicNinesExtraStrip" then
        match info with
        | .thmInfo _ =>
          count := count + 1
          if name == ``Agent1.Periodic.nines_extra_strip_control then found := true
          let axs ← liftCoreM (Lean.collectAxioms name)
          if axs.toList.any (fun ax => !(allowed.contains ax)) then
            throwError m!"DISALLOWED_AXIOMS {name} : {axs.toList}"
          logInfo m!"AUDIT_THEOREM {name} : {axs.toList}"
        | _ => throwError m!"UNEXPECTED_NEW_CONSTANT {name}"
  if !found then throwError "MISSING_ENDPOINT"
  logInfo m!"MODULE_AUDIT theorem_constants={count} safe_defs=0 runtime=0 custom_axioms=0"
'''
(out/'ControlAudit.lean').write_text(audit)
env=dict(os.environ,LEAN_PATH=str(out)+':'+str(deps))
records=[]
def limits():resource.setrlimit(resource.RLIMIT_AS,(8*1024**3,8*1024**3))
for name,args in [('compile',['-o','Agent1PeriodicNinesExtraStrip.olean',source.name]),('audit',['ControlAudit.lean'])]:
 argv=[str(compiler),'--trust=0','-j1','-DElab.async=false',*args];start=time.time()
 r=subprocess.run(argv,cwd=out,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=600,preexec_fn=limits)
 (out/(name+'.log')).write_bytes(r.stdout)
 records.append({'name':name,'argv':argv,'cwd':str(out),'LEAN_PATH':env['LEAN_PATH'],'exit_code':r.returncode,'started_at_epoch':start,'finished_at_epoch':time.time(),'log_sha256':sha(out/(name+'.log'))})
 (out/'commands.json').write_text(json.dumps(records,indent=2)+'\n')
 if r.returncode:break
result={'status':'PASS' if len(records)==2 and all(x['exit_code']==0 for x in records) else 'FAIL','source_sha256':sha(source),'compiler_sha256':sha(compiler),'dependency_count':len(pins),'fresh_closure':False,'commands':records}
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result));print((out/(records[-1]['name']+'.log')).read_text())
sys.exit(0 if result['status']=='PASS' else 1)
