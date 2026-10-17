import datetime,hashlib,json,os,resource,stat,subprocess,sys
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS,(256*1024*1024,256*1024*1024))
repo=Path('/workspace/scratch/d4d5258160f7/agent5/repo')
root=repo/'proofs/contributions/agent-5/pr164-replay-evidence-repair-20261017'
review=Path('/workspace/scratch/d4d5258160f7/agent5/pr164-repair-review')
out=review/'run-001'
review.mkdir(parents=True,exist_ok=True)
assert not out.exists(), str(out)
def digest(b): return hashlib.sha256(b).hexdigest()
def inventory():
 rows=[]
 for p in sorted(root.rglob('*')):
  if p.is_file() or p.is_symlink():
   s=p.lstat(); b=p.read_bytes()
   assert stat.S_ISREG(s.st_mode) and not stat.S_ISLNK(s.st_mode),str(p)
   rows.append({'path':str(p.relative_to(root)),'bytes':len(b),'sha256':digest(b),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),'mode':'100755' if s.st_mode&0o111 else '100644'})
 return rows
before=inventory()
assert len(before)==7
assert next(r['sha256'] for r in before if r['path']=='check_selection.py')=='fb9ccd199ae387a83980d92df3c671b4df93decd8a7f5c5dc0c34aec9c2ba357'
env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);env['GIT_NO_LAZY_FETCH']='1';env['GIT_OPTIONAL_LOCKS']='0';env['GIT_TERMINAL_PROMPT']='0';env['GIT_PAGER']='cat';env['PYTHONDONTWRITEBYTECODE']='1'
argv=[sys.executable,str(root/'check_selection.py'),'--repo',str(repo),'--output',str(out),'--source','fa2683e489acc7c85e08764450550f7e463041da','--baseline','10a173cb635fa8d03e357f454232816fc3e77609']
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
p=subprocess.run(argv,capture_output=True,env=env)
finished=datetime.datetime.now(datetime.timezone.utc).isoformat()
if not out.exists():out.mkdir()
(out/'stdout.log').write_bytes(p.stdout);(out/'stderr.log').write_bytes(p.stderr)
after=inventory()
record={'schema_version':1,'reviewer':'Agent #5 independent nonauthor specialist /root/pr164_repair_review','argv':argv,'started_at_utc':started,'finished_at_utc':finished,'exit_code':p.returncode,'assertions_enabled':True,'python_version':sys.version,'environment_overrides':{k:env[k] for k in ('GIT_NO_LAZY_FETCH','GIT_OPTIONAL_LOCKS','GIT_TERMINAL_PROMPT','GIT_PAGER','PYTHONDONTWRITEBYTECODE')},'PYTHONOPTIMIZE':'unset','address_space_limit_bytes':256*1024*1024,'maximum_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'candidate_inventory':before,'candidate_bytes_and_modes_unchanged_after_run':before==after,'stdout_sha256':digest(p.stdout),'stderr_sha256':digest(p.stderr)}
for name in ('actual-map-selection-uses.reverified.json','commands.json','stdout.log','stderr.log'):
 f=out/name
 record.setdefault('original_author_run_comparison',{})[name]={'independent_bytes':len(f.read_bytes()) if f.exists() else None,'independent_sha256':digest(f.read_bytes()) if f.exists() else None,'byte_equal':f.exists() and f.read_bytes()==(root/'run'/name).read_bytes()}
(out/'independent-execution.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
assert p.returncode==0,(p.returncode,p.stderr.decode())
assert before==after
assert all(v['byte_equal'] for v in record['original_author_run_comparison'].values())
