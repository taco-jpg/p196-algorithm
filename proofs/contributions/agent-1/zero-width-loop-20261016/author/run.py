#!/usr/bin/env python3
"""Retained bounded author increments; dependency objects are explicitly reused."""
from pathlib import Path
import hashlib,json,re,resource,subprocess,sys,time
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
LEAN=Path('/workspace/p196-tools/lean-4.19.0-linux/bin/lean')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def blob(data):return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,indent=2)+'\n')

def main():
 label,source_arg=sys.argv[1:3]
 source=Path(source_arg).resolve();raw=source.read_bytes()
 out=HERE/label;out.mkdir(exist_ok=False)
 (out/source.name).write_bytes(raw)
 (out/'run.py').write_bytes(Path(__file__).read_bytes())
 allmods={};origins={};reports=[]
 for scope,regname,project in [
   ('return','Agent1PeriodicReturnCore','agent1-periodic-return-core'),
   ('width','Agent1PeriodicWidthLift','agent1-periodic-width-projection')]:
  regpath=ROOT/'proofs'/(regname+'.registry.json')
  reg=json.loads(regpath.read_text())['projects'][project]['modules']
  build=Path('/workspace/p196-agent1-session-20261016/periodic-'+scope+'-parent-clean-001')
  reportpath=build/'verification.json';report=json.loads(reportpath.read_text())
  assert report['status']=='PASS' and report['projects'][project]['status']=='PASS'
  assert sha(LEAN)==report['compiler']['files'][str(LEAN)]
  reports.append({'registry':str(regpath),'registry_sha256':sha(regpath),'build_report':str(reportpath),'build_report_sha256':sha(reportpath)})
  for name,rec in reg.items():
   if name in allmods:assert allmods[name]==rec
   else:
    allmods[name]=rec
    origins[name]=(build/project/'source',report['projects'][project]['sources'][name])
 order=[];seen=set()
 def dfs(name):
  if name in seen:return
  seen.add(name)
  for dep in allmods[name]['imports']:
   if dep in allmods:dfs(dep)
   else:assert dep in ['Std','Lean'] or dep.startswith('Lean.')
  order.append(name)
 for name in ['Agent1PeriodicWidthLift','Agent1PeriodicZeroPath']:dfs(name)
 assert len(order)==36
 deps=HERE/'dependencies';deps.mkdir(exist_ok=True)
 pins={}
 for name in order:
  rec=allmods[name];base,rrec=origins[name]
  sp=base/(name+'.lean');obj=base/(name+'.olean');data=sp.read_bytes()
  assert sha(sp)==rec['sha256']==rrec['sha256']
  assert (ROOT/rec['path']).read_bytes()==data
  assert blob(data)==rec['git_blob']
  assert re.findall(r'^import\s+(\S+)',data.decode(),re.M)==rec['imports']
  for p in [sp,obj]:
   dest=deps/p.name
   if dest.exists():assert dest.read_bytes()==p.read_bytes()
   else:dest.write_bytes(p.read_bytes())
  pins[name]={**rec,'reused_source':str(sp),'reused_object':str(obj),'object_sha256':sha(obj)}
 version=subprocess.check_output([str(LEAN),'--version'],text=True).strip()
 assert 'version 4.19.0,' in version and 'commit 6caaee842e94' in version
 own=[]
 if 'import Agent1PeriodicZeroWidthLoop' in raw.decode():
  accepted=HERE/sys.argv[3]
  rr=json.loads((accepted/'receipt.json').read_text());assert rr['status']=='PASS'
  assert sha(ROOT/'proofs/Agent1PeriodicZeroWidthLoop.lean')==rr['source_sha256']
  assert sha(accepted/'Agent1PeriodicZeroWidthLoop.olean')==rr['object_sha256']
  own=[str(accepted)]
 env={'PATH':str(LEAN.parent)+':/usr/bin:/bin','LANG':'C.UTF-8','LEAN_PATH':':'.join([str(out)]+own+[str(deps)])}
 manifest={'source':str(source),'source_sha256':sha(source),'source_git_blob':blob(raw),'compiler_version':version,'compiler_sha256':sha(LEAN),'dependencies':pins,'reused_builds':reports,'fresh_dependency_build':False,'dependency_count':36,'dependency_order':order,'author_object_paths':own}
 dump(out/'source-and-dependencies.json',manifest)
 command=[str(LEAN),'--trust=0','-j1','-DElab.async=false','-o',source.stem+'.olean',source.name]
 started=time.monotonic();observed_rss=0;observed_virtual=0;stop=None
 with (out/'lean.log').open('wb') as output:
  process=subprocess.Popen(command,cwd=out,env=env,stdout=output,stderr=subprocess.STDOUT)
  while process.poll() is None:
   try:
    status=Path(f'/proc/{process.pid}/status').read_text()
    rss=re.search(r'^VmRSS:\s+(\d+) kB$',status,re.M);virt=re.search(r'^VmSize:\s+(\d+) kB$',status,re.M)
    if rss:observed_rss=max(observed_rss,int(rss.group(1)))
    if virt:observed_virtual=max(observed_virtual,int(virt.group(1)))
    if observed_rss>1500*1024:stop='RSS exceeded 1500 MiB threshold';process.kill()
    elif time.monotonic()-started>600:stop='600 second timeout';process.kill()
   except FileNotFoundError:pass
   time.sleep(0.01)
  rc=process.wait()
 unchanged=source.read_bytes()==raw and all(sha(Path(p['reused_source']))==p['sha256'] and sha(Path(p['reused_object']))==p['object_sha256'] and sha(ROOT/p['path'])==p['sha256'] and sha(deps/(n+'.olean'))==p['object_sha256'] for n,p in pins.items())
 receipt={'status':'PASS' if rc==0 and stop is None and unchanged else 'FAIL','exit_code':rc,'seconds':time.monotonic()-started,'command':command,'environment':env,'source_sha256':sha(source),'source_git_blob':blob(raw),'source_and_dependencies_unchanged':unchanged,'fresh_dependency_build':False,'dependency_count':36,'observed_peak_rss_kib':observed_rss,'observed_peak_virtual_kib':observed_virtual,'kernel_children_peak_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'rss_watchdog_stop_threshold_mib':1500,'rss_poll_interval_seconds':0.01,'address_space_limit_mib':None,'watchdog_reason':stop}
 if (out/(source.stem+'.olean')).exists():receipt['object_sha256']=sha(out/(source.stem+'.olean'))
 dump(out/'receipt.json',receipt);print(json.dumps(receipt),flush=True)
 return 0 if receipt['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
