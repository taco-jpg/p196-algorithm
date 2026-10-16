from pathlib import Path
import subprocess,os,json,hashlib
root=Path(__file__).resolve().parent
tool='/workspace/scratch/aaafdd394dd6/agent7-runtime/lean-4.19.0-linux/bin/lean'
env=dict(os.environ,LEAN_PATH=str(root))
version=subprocess.run([tool,'--version'],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(root/'compiler-version.log').write_text(version.stdout)
records=[]
for mod in ['InverseFibers','PathCounts','WordBridge','OddCenter','OddCounts','BoundaryControls']:
    command=[tool,'--trust=0','-j1','-DElab.async=false','-o',str(root/(mod+'.olean')),str(root/(mod+'.lean'))]
    result=subprocess.run(command,cwd=root,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (root/(mod+'.log')).write_text(result.stdout)
    records.append({'module':mod,'command':command,'exit_code':result.returncode,'log_sha256':hashlib.sha256(result.stdout.encode()).hexdigest()})
    print(mod, 'PASS' if result.returncode==0 else 'FAIL',flush=True)
    if result.returncode:
        print(result.stdout,flush=True)
        break
(root/'results.json').write_text(json.dumps(records,indent=2)+'\n')
raise SystemExit(records[-1]['exit_code'])
