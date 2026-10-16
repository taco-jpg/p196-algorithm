from pathlib import Path
import sys,json,hashlib,subprocess,os,time,shutil,resource
root=Path(__file__).resolve().parents[5];base=Path(__file__).resolve().parent
attempt=base/sys.argv[1];attempt.mkdir();shutil.copy2(__file__,attempt/'run-driver.py');build=attempt/'build';build.mkdir()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
phase=Path('/workspace/p196-agent1-session-20261016/periodic-phase-parent-clean-001/agent1-periodic-phase-catalog/source')
reg=json.loads((root/'proofs/Agent1PeriodicPhaseCatalog.registry.json').read_text());mods=next(iter(reg['projects'].values()))['modules'];pins=[]
for name,v in mods.items():
 src=root/v['path'];old=phase/(name+'.lean');obj=phase/(name+'.olean')
 assert sha(src)==v['sha256']==sha(old)
 shutil.copy2(old,build/old.name);shutil.copy2(obj,build/obj.name)
 pins.append({'module':name,'source':str(src),'source_sha256':sha(src),'object':str(obj),'object_sha256':sha(obj)})
extra=[('Agent1PeriodicSafetyAlphabet',Path('/workspace/p196-agent1-session-20261016/periodic-safety-review-clean-001')),('Agent1PeriodicOuter',base.parent/'outer-author/attempt-001'),('Agent1PeriodicOuterChoices',base.parent/'choices-author/attempt-002'),('Agent1PeriodicCatalogOrder',Path('/workspace/p196-agent1-session-20261016/catalog-order-author/attempt-003'))]
for name,oldroot in extra:
 src=root/'proofs'/(name+'.lean');old=oldroot/(name+'.lean');obj=oldroot/(name+'.olean')
 assert sha(src)==sha(old),(name,'source mismatch')
 shutil.copy2(old,build/old.name);shutil.copy2(obj,build/obj.name)
 pins.append({'module':name,'source':str(src),'source_sha256':sha(src),'object':str(obj),'object_sha256':sha(obj)})
(attempt/'dependencies.json').write_text(json.dumps(pins,indent=2)+'\n')
name='Agent1PeriodicOuterCatalog';src=root/'proofs'/(name+'.lean');shutil.copy2(src,build/src.name);shutil.copy2(src,attempt/src.name)
cmd=['/workspace/p196-tools/lean-4.19.0-linux/bin/lean','--trust=0','-s','131072','-j1','-DElab.async=false','-o',name+'.olean',src.name]
start=time.monotonic()
with (attempt/'stdout.log').open('w') as out,(attempt/'stderr.log').open('w') as err:
 def limits(): resource.setrlimit(resource.RLIMIT_AS,(6*1024**3,6*1024**3))
 try:r=subprocess.run(cmd,preexec_fn=limits,cwd=build,env=dict(os.environ,LEAN_PATH=str(build)),stdout=out,stderr=err,text=True,timeout=600);code=r.returncode
 except subprocess.TimeoutExpired:code=124
receipt={'command':cmd,'cwd':str(build),'exit_code':code,'seconds':time.monotonic()-start,'source_sha256':sha(src),'compiled_snapshot_sha256':sha(build/src.name),'dependency_count':len(pins),'reuse_policy':'Explicit hash-pinned author increment; combined fresh independent gate pending.'}
(attempt/'result.json').write_text(json.dumps(receipt,indent=2)+'\n')
print((attempt/'stdout.log').read_text());print((attempt/'stderr.log').read_text());print(json.dumps(receipt));sys.exit(code)
