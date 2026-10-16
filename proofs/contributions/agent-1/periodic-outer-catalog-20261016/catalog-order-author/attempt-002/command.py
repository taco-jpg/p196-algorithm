from pathlib import Path
import subprocess,resource,time,os,json,hashlib,sys
base=Path(__file__).resolve().parent
os.chdir(base)
lean='/workspace/p196-tools/lean-4.19.0-linux/bin/lean'
env=os.environ.copy()
env['LEAN_PATH']='/workspace/p196-agent1-outer-20261016/proofs/contributions/agent-1/periodic-outer-catalog-20261016/choices-author/attempt-002:/workspace/p196-agent1-session-20261016/periodic-phase-parent-clean-001/agent1-periodic-phase-catalog/source'
command=[lean,'--trust=0','-j1','-DElab.async=false','-o','Agent1PeriodicCatalogOrder.olean','Agent1PeriodicCatalogOrder.lean']
(base/'command.json').write_text(json.dumps({'cwd':str(base),'command':command,'LEAN_PATH':env['LEAN_PATH'],'address_space_limit_bytes':1800000*1024},indent=2)+'\n')
(base/'lean-version.txt').write_text(subprocess.check_output([lean,'--version'],text=True))
def limits():resource.setrlimit(resource.RLIMIT_AS,(1800000*1024,1800000*1024))
start=time.monotonic()
with (base/'compile.log').open('w') as out:
 result=subprocess.run(command,env=env,stdout=out,stderr=subprocess.STDOUT,preexec_fn=limits)
r=resource.getrusage(resource.RUSAGE_CHILDREN)
(base/'resource.json').write_text(json.dumps({'elapsed_seconds':time.monotonic()-start,'max_rss_kib':r.ru_maxrss,'exit_code':result.returncode},indent=2)+'\n')
(base/'exit-code.txt').write_text(str(result.returncode)+'\n')
(base/'evidence.sha256').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in sorted(base.iterdir()) if p.is_file() and p.name!='evidence.sha256'))
print((base/'compile.log').read_text(),end='')
print((base/'resource.json').read_text(),end='')
sys.exit(result.returncode)
