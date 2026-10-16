import sys, pathlib, subprocess, json, hashlib, time, os
source=pathlib.Path(sys.argv[1]); evidence=pathlib.Path(sys.argv[2]); evidence.mkdir(parents=True,exist_ok=True)
build=pathlib.Path('/workspace/scratch/2a8a87fd78df/agent101-runtime/profile-width-dev')
base=pathlib.Path('/workspace/scratch/2a8a87fd78df/agent101-generic-closure-bbbcc857/agent101-nonpalindromic-fibers/source')
attempt=len(list(evidence.glob('attempt-*.json')))+1
stem=f'attempt-{attempt:03d}'; data=source.read_bytes()
(evidence/(stem+'.lean.txt')).write_bytes(data)
dest=build/source.name
if source!=dest: dest.write_bytes(data)
cmd=['/workspace/scratch/2a8a87fd78df/agent101-runtime/toolchain/lean-4.19.0-linux/bin/lean','--trust=0','-j1','-DElab.async=false','-o',str(dest.with_suffix('.olean')),str(dest)]
env=dict(os.environ,LEAN_PATH=str(build)+':'+str(base)); start=time.monotonic()
r=subprocess.run(cmd,capture_output=True,text=True,env=env,cwd=build)
(evidence/(stem+'.log')).write_text(r.stdout+r.stderr)
record={'command':cmd,'LEAN_PATH':env['LEAN_PATH'],'source_sha256':hashlib.sha256(data).hexdigest(),'exit_code':r.returncode,'seconds':time.monotonic()-start}
(evidence/(stem+'.json')).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2)); print(r.stdout+r.stderr); sys.exit(r.returncode)
