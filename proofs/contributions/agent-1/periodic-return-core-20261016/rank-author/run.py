#!/usr/bin/env python3
"""Retain single-core, RSS-bounded author checks against pinned Outer objects."""
from pathlib import Path
import hashlib,json,re,resource,subprocess,sys,time
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
DEP=Path('/workspace/p196-agent1-session-20261016/periodic-outer-parent-clean-001/agent1-periodic-outer-catalog/source')
LEAN=Path('/workspace/p196-tools/lean-4.19.0-linux/bin/lean')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write_json(p,r): p.write_text(json.dumps(r,indent=2)+'\n')
def run(command, folder, env, label):
    started = time.monotonic()
    observed_rss = 0
    observed_virtual = 0
    stop = None
    with (folder / (label + '.log')).open('wb') as output:
        process = subprocess.Popen(command, cwd=folder, env=env, stdout=output,
                                   stderr=subprocess.STDOUT)
        while process.poll() is None:
            try:
                status = Path(f'/proc/{process.pid}/status').read_text()
                rss = re.search(r'^VmRSS:\s+(\d+) kB$', status, re.M)
                virt = re.search(r'^VmSize:\s+(\d+) kB$', status, re.M)
                if rss:
                    observed_rss = max(observed_rss, int(rss.group(1)))
                if virt:
                    observed_virtual = max(observed_virtual, int(virt.group(1)))
                if observed_rss > 1500 * 1024:
                    stop = 'RSS exceeded 1500 MiB stop threshold'
                    process.kill()
                elif time.monotonic() - started > 600:
                    stop = '600 second timeout'
                    process.kill()
            except FileNotFoundError:
                pass
            time.sleep(0.01)
        rc = process.wait()
    receipt = {'status': 'PASS' if rc == 0 and stop is None else 'FAIL',
               'exit_code': rc, 'seconds': time.monotonic() - started,
               'command': command, 'environment': env,
               'observed_peak_rss_kib': observed_rss,
               'observed_peak_virtual_kib': observed_virtual,
               'kernel_children_peak_rss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
               'rss_watchdog_stop_threshold_mib': 1500,
               'rss_poll_interval_seconds': 0.01, 'address_space_limit_mib': None,
               'watchdog_reason': stop}
    write_json(folder / (label + '-receipt.json'), receipt)
    print(json.dumps({'phase': label, **receipt}), flush=True)
    return receipt

def main():
 label,source_arg=sys.argv[1:3]
 source=Path(source_arg).resolve()
 out=HERE/label;out.mkdir(exist_ok=False)
 raw=source.read_bytes();(out/source.name).write_bytes(raw)
 registry_path=ROOT/'proofs/Agent1PeriodicOuterCatalog.registry.json'
 registry=json.loads(registry_path.read_text())['projects']['agent1-periodic-outer-catalog']['modules']
 report_path=DEP.parents[1]/'verification.json'
 report=json.loads(report_path.read_text())
 assert report['status']=='PASS' and len(registry)==25
 pins={}
 for name,rec in registry.items():
  sp=DEP/(name+'.lean');obj=DEP/(name+'.olean');data=sp.read_bytes()
  assert sha(sp)==rec['sha256']==report['projects']['agent1-periodic-outer-catalog']['sources'][name]['sha256']
  assert (ROOT/rec['path']).read_bytes()==data
  assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==rec['git_blob']
  assert re.findall(r'^import\s+(\S+)',data.decode(),re.M)==rec['imports']
  pins[name]={**rec,'source':str(sp),'object':str(obj),'object_sha256':sha(obj)}
 version=subprocess.check_output([str(LEAN),'--version'],text=True).strip()
 assert 'version 4.19.0,' in version and 'commit 6caaee842e94' in version
 assert sha(LEAN)==report['compiler']['files'][str(LEAN)]
 own_imports=[]
 for name in re.findall(r'^import\s+(\S+)',raw.decode(),re.M):
  if name=='Agent1PeriodicOuterRank':
   accepted=HERE/'attempt-001'
   rr=json.loads((accepted/'receipt.json').read_text());assert rr['status']=='PASS'
   assert sha(ROOT/'proofs/Agent1PeriodicOuterRank.lean')==rr['source_sha256']
   assert sha(accepted/'Agent1PeriodicOuterRank.olean')==rr['object_sha256']
   own_imports.append(str(accepted))
 env={'PATH':str(LEAN.parent)+':/usr/bin:/bin','LANG':'C.UTF-8','LEAN_PATH':':'.join([str(out)]+own_imports+[str(DEP)])}
 manifest={'source':str(source),'source_sha256':sha(source),'source_git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),'compiler_version':version,'compiler_sha256':sha(LEAN),'dependencies':pins,'dependency_registry':str(registry_path),'registry_sha256':sha(registry_path),'reused_build_report':str(report_path),'reused_build_report_sha256':sha(report_path),'fresh_dependency_build':False,'dependency_count':25}
 write_json(out/'source-and-dependencies.json',manifest)
 command=[str(LEAN),'--trust=0','-j1','-DElab.async=false','-o',source.stem+'.olean',source.name]
 receipt=run(command,out,env,'lean')
 unchanged=source.read_bytes()==raw and all(sha(Path(p['source']))==p['sha256'] and sha(Path(p['object']))==p['object_sha256'] and sha(ROOT/p['path'])==p['sha256'] for p in pins.values())
 receipt.update({'source_sha256':sha(source),'source_git_blob':manifest['source_git_blob'],'source_and_dependencies_unchanged':unchanged,'fresh_dependency_build':False,'dependency_count':25})
 if not unchanged:receipt['status']='FAIL'
 if (out/(source.stem+'.olean')).exists():receipt['object_sha256']=sha(out/(source.stem+'.olean'))
 write_json(out/'receipt.json',receipt)
 print(json.dumps({k:receipt[k] for k in ['status','source_sha256','source_and_dependencies_unchanged','seconds']}),flush=True)
 return 0 if receipt['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
