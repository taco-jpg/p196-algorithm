from pathlib import Path
import subprocess,json,os
root=Path(__file__).resolve().parent
tool='/workspace/scratch/aaafdd394dd6/agent7-runtime/lean-4.19.0-linux/bin/lean'
env=dict(os.environ,LEAN_PATH=str(root))
version=subprocess.run([tool,'--version'],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(root/'compiler-version.log').write_text(version.stdout)
results=[]
for mod in ['OddWords','BoundaryControls']:
    command=[tool,'-o',str(root/(mod+'.olean')),str(root/(mod+'.lean'))]
    proc=subprocess.run(command,cwd=root,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (root/(mod+'.log')).write_text(proc.stdout)
    results.append({'module':mod,'command':command,'exit_code':proc.returncode})
    print(mod, 'PASS' if proc.returncode==0 else 'FAIL',flush=True)
    if proc.returncode:
        print(proc.stdout,flush=True)
        break
(root/'results.json').write_text(json.dumps(results,indent=2)+'\n')
raise SystemExit(results[-1]['exit_code'])
