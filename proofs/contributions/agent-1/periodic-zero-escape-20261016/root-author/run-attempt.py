from pathlib import Path
import sys,json,hashlib,subprocess,os,time
root=Path(__file__).resolve().parents[5];base=Path(__file__).resolve().parent
build=Path('/workspace/p196-agent1-session-20261016/periodic-zero-escape-author-build');name='Agent1PeriodicZeroEscape';attempt=base/sys.argv[1];attempt.mkdir()
src=root/'proofs'/(name+'.lean');data=src.read_bytes();(attempt/src.name).write_bytes(data);(build/src.name).write_bytes(data)
cmd=['/workspace/p196-tools/lean-4.19.0-linux/bin/lean','--trust=0','-j1','-DElab.async=false','-o',name+'.olean',src.name];start=time.monotonic();r=subprocess.run(cmd,cwd=build,env=dict(os.environ,LEAN_PATH=str(build)),capture_output=True,text=True,timeout=600)
(attempt/'stdout.log').write_text(r.stdout);(attempt/'stderr.log').write_text(r.stderr);(attempt/'result.json').write_text(json.dumps({'command':cmd,'cwd':str(build),'exit_code':r.returncode,'seconds':time.monotonic()-start,'source_sha256':hashlib.sha256(data).hexdigest(),'reuse_policy':'Explicit pinned author increment; final fresh independent closure pending.'},indent=2)+'\n');print(r.stdout);print(r.stderr);print('EXIT',r.returncode);sys.exit(r.returncode)
