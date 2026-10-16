from pathlib import Path
import subprocess, shutil, os, hashlib, json, sys
root=Path(__file__).resolve().parent.parent
tool=Path('/workspace/scratch/aaafdd394dd6/agent7-runtime/lean-4.19.0-linux/bin/lean')
name=sys.argv[1] if len(sys.argv)>1 else 'attempt-001'
build=root/'center-dev'/name
build.mkdir(exist_ok=False)
modules=['InverseFibers','PathCounts','WordBridge','OddCenter']
manifest={}
for mod in modules:
    src=root/'dependencies'/(mod+'.lean') if mod!='OddCenter' else root/'OddCenter.lean'
    shutil.copy2(src,build/(mod+'.lean'))
    manifest[mod]=hashlib.sha256(src.read_bytes()).hexdigest()
(build/'source-sha256.json').write_text(json.dumps(manifest,indent=2)+'\n')
env=dict(os.environ,LEAN_PATH=str(build))
results=[]
for mod in modules:
    cmd=[str(tool),'-o',str(build/(mod+'.olean')),str(build/(mod+'.lean'))]
    proc=subprocess.run(cmd,cwd=build,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (build/(mod+'.log')).write_text(proc.stdout)
    results.append({'module':mod,'command':cmd,'exit_code':proc.returncode})
    print(mod, 'PASS' if proc.returncode==0 else 'FAIL',flush=True)
    if proc.returncode:
        print(proc.stdout,flush=True)
        break
(build/'results.json').write_text(json.dumps(results,indent=2)+'\n')
raise SystemExit(results[-1]['exit_code'])
