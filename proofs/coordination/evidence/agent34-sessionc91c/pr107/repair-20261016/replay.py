#!/usr/bin/env python3
"""Agent34 scoped strict replay. Never downloads or imports prebuilt project oleans."""
import datetime,hashlib,json,os,pathlib,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parent
LEAN=pathlib.Path('/tmp/p196-agent5-lean/lean-4.19.0-linux/bin/lean')
ORDER=['OuterFinite','TARGET','ExteriorFactorizationProof','ExteriorObservationInjective','CoordinateThreshold','ExteriorUpdateLaw','CoordinateDynamics','CoordinateSign','CoordinateCycle','RhoCycleTargets','RhoCycleLemmas']
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
stage=sys.argv[1] if len(sys.argv)>1 else 'original'
if stage not in ('original','comment-fix'): raise SystemExit('Unknown stage')
build=ROOT/'build-original'
logdir=ROOT/'logs'/stage
logdir.mkdir(parents=True,exist_ok=False)
env=os.environ.copy()
env['LEAN_PATH']=str(build)
env['PATH']=str(LEAN.parent)+os.pathsep+env.get('PATH','')
version=subprocess.run([str(LEAN),'--version'],capture_output=True,text=True,env=env,timeout=30)
(logdir/'version.stdout.log').write_text(version.stdout)
(logdir/'version.stderr.log').write_text(version.stderr)
if version.returncode or 'version 4.19.0' not in version.stdout or '6caaee842e94' not in version.stdout:
    raise SystemExit('Wrong Lean version')
if sha(LEAN)!='92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023':
    raise SystemExit('Wrong Lean binary hash')
if stage=='original' and list(build.glob('*.olean')):
    raise SystemExit('Original replay requires an empty project build')
ledger={'stage':stage,'started_at':now(),'source_head':'254b4bc6b545aa9dd027c7bb46e7c4022b5d2f27','lean_binary':str(LEAN),'lean_binary_sha256':sha(LEAN),'lean_version':version.stdout.strip(),'strict_flags':['--trust=0','-j1','-DElab.async=false'],'build_directory':str(build),'compilation_reuse':'none; all eleven project sources recompiled' if stage=='original' else 'ten exact imported modules compiled in the original stage; only the repaired helper source is recompiled','status':'RUNNING','steps':[]}
selected=ORDER if stage=='original' else ['RhoCycleLemmas']
for index,module in enumerate(selected,1):
    source=build/(module+'.lean')
    command=[str(LEAN),'--trust=0','-j1','-DElab.async=false','-o',module+'.olean',module+'.lean']
    out=logdir/(module+'.stdout.log');err=logdir/(module+'.stderr.log')
    started=now();tic=time.monotonic()
    with out.open('wb') as stdout,err.open('wb') as stderr:
        proc=subprocess.run(command,cwd=build,env=env,stdout=stdout,stderr=stderr,timeout=180)
    step={'module':module,'source_sha256':sha(source),'command':command,'cwd':str(build),'started_at':started,'seconds':round(time.monotonic()-tic,6),'exit_code':proc.returncode,'stdout':str(out.relative_to(ROOT)),'stdout_sha256':sha(out),'stderr':str(err.relative_to(ROOT)),'stderr_sha256':sha(err)}
    if (build/(module+'.olean')).exists(): step['olean_sha256']=sha(build/(module+'.olean'))
    ledger['steps'].append(step)
    (logdir/'execution.json').write_text(json.dumps(ledger,indent=2)+'\n')
    print(module+' exit '+str(proc.returncode),flush=True)
    total=sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file())
    if total>512*1024*1024: raise SystemExit('Private workspace exceeded its 512 MiB cap')
    if proc.returncode:
        ledger['status']='FAIL'
        ledger['completed_at']=now()
        (logdir/'execution.json').write_text(json.dumps(ledger,indent=2)+'\n')
        print(out.read_text(),end='',flush=True)
        print(err.read_text(),end='',flush=True)
        raise SystemExit(proc.returncode)
ledger['status']='PASS'
ledger['completed_at']=now()
(logdir/'execution.json').write_text(json.dumps(ledger,indent=2)+'\n')
print(json.dumps({'stage':stage,'status':ledger['status'],'compiled':len(ledger['steps'])}),flush=True)
