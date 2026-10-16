import datetime, hashlib, json, os, pathlib, shutil, subprocess, sys
base=pathlib.Path(__file__).resolve().parent.parent
run=base/'canonical-dev'/sys.argv[1]
run.mkdir(exist_ok=False)
source=run/'source'; source.mkdir()
lean=pathlib.Path('/workspace/scratch/aaafdd394dd6/agent7-runtime/lean-4.19.0-linux/bin/lean')
deps=base/'actual-dev'/'clean-004'/'source'
for p in deps.iterdir():
    if p.suffix in ('.lean','.olean'): shutil.copy2(p,source/p.name)
for name in ['OddWords','OddCanonical']:
    shutil.copy2(base/(name+'.lean'),source/(name+'.lean'))
env=os.environ.copy(); env['LEAN_PATH']=str(source)
record={'agent':7,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'build_scope':'Incremental development build; dependency oleans copied from independently recorded actual-dev/clean-004; final clean full closure audit required.','lean':str(lean),'lean_sha256':hashlib.sha256(lean.read_bytes()).hexdigest(),'modules':[]}
for name in ['OddWords','OddCanonical']:
    cmd=[str(lean),'--trust=0','-j1','-DElab.async=false','-o',name+'.olean',name+'.lean']
    p=subprocess.run(cmd,cwd=source,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    log=run/(name+'.log'); log.write_bytes(p.stdout)
    record['modules'].append({'module':name,'command':cmd,'cwd':str(source),'exit_code':p.returncode,'source_sha256':hashlib.sha256((source/(name+'.lean')).read_bytes()).hexdigest(),'log_sha256':hashlib.sha256(p.stdout).hexdigest()})
    print(name,p.returncode,p.stdout.decode(),flush=True)
    if p.returncode: break
record['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
record['success']=len(record['modules'])==2 and all(x['exit_code']==0 for x in record['modules'])
(run/'verification.json').write_text(json.dumps(record,indent=2)+'\n')
sys.exit(0 if record['success'] else 1)
