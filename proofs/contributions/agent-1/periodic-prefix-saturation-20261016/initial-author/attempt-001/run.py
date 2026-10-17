from pathlib import Path
import json,subprocess,hashlib,os,resource,time,shutil,sys
here=Path(__file__).resolve().parent;root=here.parents[4];name='Agent1PeriodicInitialUnsaturated'
attempt=here/sys.argv[1];attempt.mkdir(exist_ok=False)
lean=Path('/workspace/p196-tools/lean-4.19.0-linux/bin/lean')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
shutil.copyfile(__file__,attempt/'run.py')
shutil.copyfile(root/'proofs'/(name+'.lean'),attempt/(name+'.lean'))
shutil.copyfile(here/'InitialAudit.lean',attempt/'InitialAudit.lean')
sat=here.parent/'saturation-author/attempt-001'
paths=[Path(p) for p in json.loads((sat/'commands.json').read_text())[0]['LEAN_PATH'].split(':')]
paths.append(Path('/workspace/p196-agent1-session-20261016/periodic-return-parent-clean-001/agent1-periodic-return-core/source'))
r=json.loads((root/'proofs/Agent1PeriodicInitialUnsaturated.registry.json').read_text());mods=next(iter(r['projects'].values()))['modules'];pins=[]
for m,v in mods.items():
 if m==name:continue
 p=next(p for p in paths if (p/(m+'.olean')).exists())
 assert sha(root/v['path'])==v['sha256']==sha(p/(m+'.lean')),m
 pins.append({'module':m,'source':str(p/(m+'.lean')),'source_sha256':v['sha256'],'object':str(p/(m+'.olean')),'object_sha256':sha(p/(m+'.olean'))})
(attempt/'dependencies.json').write_text(json.dumps(pins,indent=2)+'\n')
(attempt/'lean-version.txt').write_text(subprocess.check_output([str(lean),'--version'],text=True))
env=os.environ.copy();env['LEAN_PATH']=':'.join(str(p) for p in [attempt,*paths]);commands=[]
def limits():resource.setrlimit(resource.RLIMIT_AS,(6*1024**3,6*1024**3))
rc=0
for label,args in [('compile',['-o',name+'.olean',name+'.lean']),('audit',['InitialAudit.lean'])]:
 cmd=[str(lean),'--trust=0','-j1','-DElab.async=false',*args];start=time.monotonic()
 with (attempt/(label+'.log')).open('w') as f:p=subprocess.run(cmd,cwd=attempt,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=600,preexec_fn=limits)
 commands.append({'name':label,'command':cmd,'cwd':str(attempt),'LEAN_PATH':env['LEAN_PATH'],'compiler_sha256':sha(lean),'exit_code':p.returncode,'seconds':time.monotonic()-start,'address_space_limit_bytes':6*1024**3})
 (attempt/'commands.json').write_text(json.dumps(commands,indent=2)+'\n');print((attempt/(label+'.log')).read_text());rc=p.returncode
 if rc:break
result={'status':'PASS' if rc==0 else 'FAILED','exit_code':rc,'source_sha256':sha(attempt/(name+'.lean')),'dependency_count':len(pins),'dependency_objects_reused':True,'fresh_full_closure':False,'independent_review':False,'source_unchanged':sha(root/'proofs'/(name+'.lean'))==sha(attempt/(name+'.lean'))}
(attempt/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));sys.exit(rc)
