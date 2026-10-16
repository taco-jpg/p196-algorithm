import datetime,hashlib,json,os,pathlib,shutil,subprocess,sys
base=pathlib.Path(__file__).resolve().parent.parent
run=base/'complete-dev'/sys.argv[1];run.mkdir(exist_ok=False)
source=run/'source';source.mkdir()
lean=pathlib.Path('/workspace/scratch/aaafdd394dd6/agent7-runtime/lean-4.19.0-linux/bin/lean')
for origin in [base/'sharp-dev/attempt-001/source',base/'output-dev/attempt-001/source']:
 for p in origin.iterdir():
  if p.suffix in ('.lean','.olean'):
   target=source/p.name
   if target.exists() and p.suffix=='.lean': assert target.read_bytes()==p.read_bytes(),p.name
   shutil.copy2(p,target)
shutil.copy2(base/'OddComplete.lean',source/'OddComplete.lean')
env=os.environ.copy();env['LEAN_PATH']=str(source)
cmd=[str(lean),'--trust=0','-j1','-DElab.async=false','-o','OddComplete.olean','OddComplete.lean']
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
p=subprocess.run(cmd,cwd=source,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(run/'OddComplete.log').write_bytes(p.stdout)
record={'agent':7,'status':'incremental development; final fresh import closure pending','command':cmd,'cwd':str(source),'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode,'source_sha256':hashlib.sha256((source/'OddComplete.lean').read_bytes()).hexdigest(),'log_sha256':hashlib.sha256(p.stdout).hexdigest(),'lean_sha256':hashlib.sha256(lean.read_bytes()).hexdigest(),'dependency_sources':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source.glob('*.lean')},'dependency_objects_from':['sharp-dev/attempt-001/source','output-dev/attempt-001/source']}
(run/'verification.json').write_text(json.dumps(record,indent=2)+'\n')
print(p.stdout.decode());print(json.dumps({'exit_code':p.returncode,'source_sha256':record['source_sha256']}));sys.exit(p.returncode)
