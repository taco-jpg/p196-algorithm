#!/usr/bin/env python3
"""Preserve exact author attempts; reuse explicitly identified checked dependencies."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,shutil,subprocess,time
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--module',required=True)
p.add_argument('--lean',type=Path,required=True)
a=p.parse_args()
here=Path(__file__).resolve().parent
root=here.parents[3]
deps=root/'dependencies'
base=here/'development'/a.module
base.mkdir(parents=True,exist_ok=True)
k=1
while (base/f'attempt-{k:03d}').exists():k+=1
out=base/f'attempt-{k:03d}'
source=out/'source'
source.mkdir(parents=True)
main=root/'proofs'/f'{a.module}.lean'
shutil.copy2(main,source/main.name)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
report={'status':'RUNNING','author':'Agent14/root','started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'module':a.module,'source_sha256':digest(main),'dependency_reuse':'Author development only. Dependency objects came from identified successful earlier builds; final independent acceptance recompiles source.','dependency_objects':{x.name:{'bytes':x.stat().st_size,'sha256':digest(x)} for x in sorted(deps.glob('*.olean'))},'dependency_sources':{x.name:digest(x) for x in sorted(deps.glob('*.lean'))}}
cmd=[str(a.lean),'--trust=0','-j1','-DElab.async=false','-o',a.module+'.olean',a.module+'.lean']
report['argv']=cmd
report['cwd']=str(source)
env=os.environ.copy();env['LEAN_PATH']=str(source)+os.pathsep+str(deps)
report['LEAN_PATH']=env['LEAN_PATH']
def save(): (out/'receipt.json').write_text(json.dumps(report,indent=2)+'\n')
save();start=time.monotonic()
try:
 with (out/'compiler.log').open('wb') as log:
  r=subprocess.run(cmd,cwd=source,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=1800)
 report['exit_code']=r.returncode
 report['status']='LEAN_CHECKED_AUTHOR' if r.returncode==0 else 'FAILED'
except subprocess.TimeoutExpired as e:
 report['exit_code']=124;report['status']='TIMEOUT';report['exception']=str(e)
report['elapsed_seconds']=time.monotonic()-start
report['log_sha256']=digest(out/'compiler.log')
save()
print(json.dumps({'status':report['status'],'exit_code':report['exit_code'],'elapsed_seconds':report['elapsed_seconds'],'receipt':str(out/'receipt.json')}),flush=True)
print((out/'compiler.log').read_text(),flush=True)
if report['exit_code']==0:
 shutil.copy2(main,deps/main.name)
 shutil.copy2(source/(a.module+'.olean'),deps/(a.module+'.olean'))
raise SystemExit(report['exit_code'])
