#!/usr/bin/env python3
"""One fixed fresh16 service run, stopping at the first nonzero/timeout/signal."""
from pathlib import Path
import hashlib,json,os,re,resource,shutil,subprocess,time
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BUILD=Path('/workspace/p196-agent1-session-20261016/agent104-monitor-fresh-001')
LEAN=Path('/workspace/p196-tools/lean-4.19.0-linux/bin/lean')
COMMIT='e67807e6d3d7a0cbd43d26257f37d1dd66e43ae6'
CLAIM='31fa126cea0382edcf3eff9303482d40fbf15432'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def limits():resource.setrlimit(resource.RLIMIT_AS,(4*1024**3,4*1024**3))
pins=json.loads((HERE/'source-pins.json').read_text());assert pins['source_commit']==COMMIT
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==COMMIT
assert sha(LEAN)=='92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
assert len(pins['order'])==16
RUN=HERE/'fresh-001';RUN.mkdir(exist_ok=False);BUILD.mkdir(exist_ok=False);(RUN/'source').mkdir();(RUN/'logs').mkdir()
shutil.copyfile(__file__,RUN/'run.py');shutil.copyfile(HERE/'source-pins.json',RUN/'source-pins.json');shutil.copyfile(HERE/'ProjectAudit.lean',RUN/'ProjectAudit.lean')
for name in pins['order']:
 rec=pins['modules'][name];source=ROOT/rec['path'];data=source.read_bytes()
 assert sha(source)==rec['sha256'],name
 assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==rec['git_blob'],name
 assert re.findall(r'^import\s+(\S+)',data.decode(),re.M)==rec['imports'],name
 for dest in [RUN/'source'/(name+'.lean'),BUILD/(name+'.lean')]:dest.write_bytes(data)
assert not list(BUILD.glob('*.olean'))
shutil.copyfile(HERE/'ProjectAudit.lean',BUILD/'ProjectAudit.lean')
env=os.environ.copy();env['LEAN_PATH']=str(BUILD)
compiler_files={str(p):sha(p) for p in [LEAN,*sorted((LEAN.parents[1]/'lib/lean').glob('*.so'))]}
dump(RUN/'compiler-pins.json',{'version_from_published_pin':'Lean 4.19.0 / 6caaee842e94','files':compiler_files})
started=time.monotonic();started_epoch=time.time();deadline=started+1200;commands=[];failed=None
flags=[str(LEAN),'--trust=0','-j1','-DElab.async=false']
labels=pins['order']+['ProjectAudit']
for label in labels:
 remaining=deadline-time.monotonic()
 if remaining<=0:
  failed={'label':label,'outcome':'NOT_RUN_OVERALL_DEADLINE'};break
 args=flags+(['ProjectAudit.lean'] if label=='ProjectAudit' else ['-o',label+'.olean',label+'.lean'])
 timeout=min(600,remaining);start=time.monotonic();print('START '+label,flush=True);stdout=RUN/'logs'/(label+'.stdout.log');stderr=RUN/'logs'/(label+'.stderr.log');exit_code=None;timed_out=False
 with stdout.open('wb') as out,stderr.open('wb') as err:
  try:
   r=subprocess.run(args,cwd=BUILD,env=env,stdout=out,stderr=err,timeout=timeout,preexec_fn=limits)
   exit_code=r.returncode
  except subprocess.TimeoutExpired:timed_out=True
 command={'label':label,'argv':args,'cwd':str(BUILD),'LEAN_PATH':str(BUILD),'exit_code':exit_code,'timed_out':timed_out,'signal':-exit_code if exit_code is not None and exit_code<0 else None,'elapsed_seconds':time.monotonic()-start,'timeout_seconds':timeout,'address_space_limit_bytes':4*1024**3,'stdout_sha256':sha(stdout),'stderr_sha256':sha(stderr),'child_max_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
 commands.append(command);dump(RUN/'commands.json',commands);print(label+' exit='+str(exit_code)+' timeout='+str(timed_out),flush=True)
 if exit_code!=0 or timed_out:
  failed=command;print(stdout.read_text(errors='replace'),end='',flush=True);print(stderr.read_text(errors='replace'),end='',flush=True);break
objects={p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(BUILD.glob('*.olean'))}
compile_commands=[c for c in commands if c['label']!='ProjectAudit'];audit_commands=[c for c in commands if c['label']=='ProjectAudit'];attempted={c['label'] for c in commands}
result={'status':'PASS' if failed is None and len(commands)==17 else 'FAIL','executor':'Agent #1 specialist center_parent_receipt; independent compiler-service executor, no authorship of Agent104 or inherited Agent107 modules','claim_commit':CLAIM,'source_commit':COMMIT,'target_source_sha256':pins['modules']['Agent104DFABadMonitor']['sha256'],'source_tree_tracked_clean_at_completion':subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,text=True).strip()=='','started_at_epoch':started_epoch,'finished_at_epoch':time.time(),'elapsed_seconds':time.monotonic()-started,'module_count':16,'compile_commands_attempted':len(compile_commands),'compile_commands_passed':sum(c['exit_code']==0 and not c['timed_out'] for c in compile_commands),'audit_status':'PASS' if audit_commands and audit_commands[-1]['exit_code']==0 else ('FAIL' if audit_commands else 'NOT_RUN'),'not_run_labels':[n for n in labels if n not in attempted],'first_failure':failed,'no_source_edits':True,'dependency_objects_reused':False,'fresh_build_initially_object_empty':True,'overall_deadline_seconds':1200,'compiled_objects':objects,'compiled_objects_packaged':False,'later_author_sources_tested':False,'unproved_proposition_targets':['Agent104.DFASafety.monitorBadWordCorrespondence','Agent104.DFASafety.safetyRowsSound']}
dump(RUN/'result.json',result)
print(json.dumps({k:v for k,v in result.items() if k not in ['compiled_objects','first_failure']},indent=2),flush=True)
raise SystemExit(0 if result['status']=='PASS' else 1)
