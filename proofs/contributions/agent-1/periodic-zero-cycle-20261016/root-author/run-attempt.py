from pathlib import Path
import sys,json,hashlib,subprocess,shutil,os,time
root=Path(__file__).resolve().parents[5];base=Path(__file__).resolve().parent
module=sys.argv[1];attempt=base/(module+'-'+sys.argv[2]);attempt.mkdir()
build=Path('/workspace/p196-agent1-session-20261016/periodic-zero-root-build');build.mkdir(exist_ok=True)
prior=Path('/workspace/p196-agent1-session-20261016/periodic-validity-review-clean-001')
mods=json.loads((root/'proofs/Agent1PeriodicValidity.registry.json').read_text())['projects']['agent1-periodic-validity']['modules']
for n,m in mods.items():
 assert hashlib.sha256((root/m['path']).read_bytes()).hexdigest()==m['sha256'];assert (root/m['path']).read_bytes()==(prior/(n+'.lean')).read_bytes();shutil.copy2(prior/(n+'.olean'),build/(n+'.olean'))
extra={'Agent1PeriodicZeroPeriod':Path('/workspace/p196-agent1-session-20261016/periodic-zero-period-author-build/Agent1PeriodicZeroPeriod.olean'),'Agent1PeriodicZeroState':root/'proofs/contributions/agent-1/periodic-zero-cycle-20261016/state-author/attempt-001/Agent1PeriodicZeroState.olean'}
for n,p in extra.items():shutil.copy2(p,build/(n+'.olean'))
# Extra accepted new module objects may be placed here explicitly by the parent.
src=root/'proofs'/(module+'.lean');shutil.copy2(src,build/src.name);shutil.copy2(src,attempt/src.name)
cmd=['/workspace/p196-tools/lean-4.19.0-linux/bin/lean','--trust=0','-j1','-DElab.async=false','-o',module+'.olean',src.name];t=time.monotonic();r=subprocess.run(cmd,cwd=build,env=dict(os.environ,LEAN_PATH=str(build)),capture_output=True,text=True,timeout=600)
(attempt/'stdout.log').write_text(r.stdout);(attempt/'stderr.log').write_text(r.stderr);(attempt/'result.json').write_text(json.dumps({'command':cmd,'cwd':str(build),'exit_code':r.returncode,'seconds':time.monotonic()-t,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'dependency_policy':'Authorincrement uses pinned17previouslyreviewedobjects plus frozencheckednewmoduleobjects; finalfreshcombinedclosure required.'},indent=2)+'\n');print(r.stdout);print(r.stderr);print('EXIT',r.returncode);sys.exit(r.returncode)
