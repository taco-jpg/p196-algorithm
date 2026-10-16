from pathlib import Path
import subprocess,os,json,hashlib,time,sys,shutil
root=Path(__file__).resolve().parents[5]
base=Path(__file__).resolve().parent
attempt=base/('attempt-'+sys.argv[1]);attempt.mkdir()
build=Path('/workspace/p196-agent1-session-20261016/periodic-safety-boundary-build');build.mkdir(exist_ok=True)
prior=Path('/workspace/p196-agent1-session-20261016/periodic-validity-review-clean-001')
mods=json.loads((root/'proofs/Agent1PeriodicValidity.registry.json').read_text())['projects']['agent1-periodic-validity']['modules']
for name,m in mods.items():
 s=root/m['path']; assert hashlib.sha256(s.read_bytes()).hexdigest()==m['sha256']; assert (prior/(name+'.lean')).read_bytes()==s.read_bytes()
 shutil.copy2(prior/(name+'.olean'),build/(name+'.olean'))
source=root/'proofs/Agent1PeriodicSafetyBoundary.lean';target=build/source.name;shutil.copy2(source,target);shutil.copy2(source,attempt/source.name)
for name in ['Agent1PeriodicSafetyAlphabet','Agent1PeriodicSafety']:
 extra=Path('/workspace/p196-agent1-session-20261016/periodic-safety-author-build')/(name+'.olean')
 if extra.exists():shutil.copy2(extra,build/extra.name)
cmd=['/workspace/p196-tools/lean-4.19.0-linux/bin/lean','--trust=0','-j1','-DElab.async=false','-o','Agent1PeriodicSafetyBoundary.olean',target.name]
env=dict(os.environ,LEAN_PATH=str(build));start=time.monotonic();r=subprocess.run(cmd,cwd=build,env=env,capture_output=True,text=True,timeout=300)
(attempt/'stdout.log').write_text(r.stdout);(attempt/'stderr.log').write_text(r.stderr)
(attempt/'result.json').write_text(json.dumps({'command':cmd,'cwd':str(build),'exit_code':r.returncode,'seconds':time.monotonic()-start,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'dependency_policy':'Incremental author compile reuses exact pinned independently fresh-verified 17module objects; final combined freshbuild required.'},indent=2)+'\n')
print(r.stdout);print(r.stderr);print('EXIT',r.returncode);sys.exit(r.returncode)
