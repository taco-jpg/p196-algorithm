from pathlib import Path
import subprocess,resource,time,os,json,hashlib,sys
base=Path(__file__).resolve().parent
repo=Path('/workspace/p196-agent1-prefix-saturation-20261016')
periodic=Path('/workspace/p196-agent1-session-20261016/periodic-clock-parent-clean-001/agent1-periodic-return-clock/source')
saturation=Path('/workspace/p196-agent1-onboarding/saturated-profile-build/agent2-saturated-profile/source')
lean=Path('/workspace/p196-tools/lean-4.19.0-linux/bin/lean')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
registries=[('proofs/Agent1PeriodicReturnClock.registry.json','agent1-periodic-return-clock',periodic),('proofs/Agent2SaturatedProfile.registry.json','agent2-saturated-profile',saturation)]
entries={};origins={}
for path,project,origin in registries:
 for name,spec in json.loads((repo/path).read_text())['projects'][project]['modules'].items():
  if name in entries:assert entries[name]['sha256']==spec['sha256'],name
  else:entries[name]=spec;origins[name]=origin
needed=set()
def visit(name):
 if name in needed or name=='Std' or name.startswith('Lean.'):return
 assert name in entries,name
 for imp in entries[name]['imports']:visit(imp)
 needed.add(name)
for name in ['Agent1PeriodicOuter','SaturationTheorem']:visit(name)
deps=[]
for name in sorted(needed):
 spec=entries[name];source=origins[name]/(name+'.lean');obj=origins[name]/(name+'.olean')
 assert sha(source)==sha(repo/spec['path'])==spec['sha256'],name
 assert obj.is_file(),name
 deps.append({'module':name,'source':str(source),'source_sha256':sha(source),'object':str(obj),'object_sha256':sha(obj)})
(base/'dependencies.json').write_text(json.dumps(deps,indent=2)+'\n')
env=os.environ.copy();env['LEAN_PATH']=str(base)+':'+str(periodic)+':'+str(saturation)
command=[str(lean),'--trust=0','-j1','-DElab.async=false','-o','Agent1PeriodicPrefix.olean','Agent1PeriodicPrefix.lean']
record={'claim':'8a8e6b9d748cbd25892e4836ff1a25fc55a78ca2','command':command,'cwd':str(base),'LEAN_PATH':env['LEAN_PATH'],'compiler_sha256':sha(lean),'source_sha256':sha(base/'Agent1PeriodicPrefix.lean'),'address_space_limit_bytes':4*1024**3,'dependency_count':len(deps),'independent_clean_rebuild':False}
(base/'command.json').write_text(json.dumps(record,indent=2)+'\n')
(base/'lean-version.txt').write_text(subprocess.check_output([str(lean),'--version'],text=True))
def limits():resource.setrlimit(resource.RLIMIT_AS,(4*1024**3,4*1024**3))
start=time.monotonic()
with (base/'compile.log').open('w') as out:
 result=subprocess.run(command,cwd=base,env=env,stdout=out,stderr=subprocess.STDOUT,preexec_fn=limits)
r=resource.getrusage(resource.RUSAGE_CHILDREN)
record.update(elapsed_seconds=time.monotonic()-start,max_rss_kib=r.ru_maxrss,exit_code=result.returncode)
if result.returncode==0:record['object_sha256']=sha(base/'Agent1PeriodicPrefix.olean')
(base/'result.json').write_text(json.dumps(record,indent=2)+'\n')
(base/'exit-code.txt').write_text(str(result.returncode)+'\n')
(base/'evidence.sha256').write_text(''.join(sha(p)+'  '+p.name+'\n' for p in sorted(base.iterdir()) if p.is_file() and p.name!='evidence.sha256'))
print((base/'compile.log').read_text(),end='')
print(json.dumps({k:record[k] for k in ['elapsed_seconds','max_rss_kib','exit_code','dependency_count']},indent=2))
sys.exit(result.returncode)
