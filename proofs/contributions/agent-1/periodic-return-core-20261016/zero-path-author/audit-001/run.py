from pathlib import Path
import subprocess,resource,time,os,json,hashlib,sys
base=Path(__file__).resolve().parent
repo=Path('/workspace/p196-agent1-return-20261016')
zero=Path('/workspace/p196-agent1-session-20261016/periodic-zero-parent-clean-001/agent1-periodic-zero-cycle/source')
width=Path('/workspace/p196-agent1-width-20261016/proofs/contributions/agent-1/periodic-width-projection-20261016/width-path-author/attempt-002')
lean=Path('/workspace/p196-tools/lean-4.19.0-linux/bin/lean')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
reg=json.loads((repo/'proofs/Agent1PeriodicZeroCycle.registry.json').read_text())['projects']['agent1-periodic-zero-cycle']['modules']
deps=[]
for name,spec in reg.items():
 source=zero/(name+'.lean'); obj=zero/(name+'.olean')
 assert sha(source)==sha(repo/spec['path'])==spec['sha256']
 assert obj.is_file()
 deps.append({'module':name,'source':str(source),'source_sha256':sha(source),'object':str(obj),'object_sha256':sha(obj)})
name='Agent1PeriodicWidthPath';source=width/(name+'.lean');obj=width/(name+'.olean')
assert sha(source)==sha(repo/'proofs'/source.name)
assert obj.is_file()
deps.append({'module':name,'source':str(source),'source_sha256':sha(source),'object':str(obj),'object_sha256':sha(obj)})
(base/'dependencies.json').write_text(json.dumps(deps,indent=2)+'\n')
env=os.environ.copy();env['LEAN_PATH']=str(base)+':'+str(base.parent/'attempt-001')+':'+str(width)+':'+str(zero)
command=[str(lean),'--trust=0','-j1','-DElab.async=false','-o','ZeroPathAudit.olean','ZeroPathAudit.lean']
record={'claim':'efe6d4b95f53ad8fbcebf113f8da0616dfa67b22','command':command,'cwd':str(base),'LEAN_PATH':env['LEAN_PATH'],'compiler_sha256':sha(lean),'source_sha256':sha(base/'ZeroPathAudit.lean'),'address_space_limit_bytes':1800000*1024,'independent_clean_rebuild':False}
(base/'command.json').write_text(json.dumps(record,indent=2)+'\n')
(base/'lean-version.txt').write_text(subprocess.check_output([str(lean),'--version'],text=True))
def limits():resource.setrlimit(resource.RLIMIT_AS,(1800000*1024,1800000*1024))
start=time.monotonic()
with (base/'compile.log').open('w') as out:
 result=subprocess.run(command,cwd=base,env=env,stdout=out,stderr=subprocess.STDOUT,preexec_fn=limits)
r=resource.getrusage(resource.RUSAGE_CHILDREN)
record.update(elapsed_seconds=time.monotonic()-start,max_rss_kib=r.ru_maxrss,exit_code=result.returncode)
if result.returncode==0:record['object_sha256']=sha(base/'ZeroPathAudit.olean')
(base/'result.json').write_text(json.dumps(record,indent=2)+'\n')
(base/'exit-code.txt').write_text(str(result.returncode)+'\n')
(base/'evidence.sha256').write_text(''.join(sha(p)+'  '+p.name+'\n' for p in sorted(base.iterdir()) if p.is_file() and p.name!='evidence.sha256'))
print((base/'compile.log').read_text(),end='')
print(json.dumps({k:record[k] for k in ['elapsed_seconds','max_rss_kib','exit_code']},indent=2))
sys.exit(result.returncode)
