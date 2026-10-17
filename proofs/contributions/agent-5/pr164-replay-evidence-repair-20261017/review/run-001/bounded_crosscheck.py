import hashlib,json,os,resource,subprocess
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS,(256*1024*1024,256*1024*1024))
repo='/workspace/scratch/d4d5258160f7/agent5/repo';out=Path('/workspace/scratch/d4d5258160f7/agent5/pr164-repair-review/run-001')
env=os.environ.copy();env.update(GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0',GIT_TERMINAL_PROMPT='0',GIT_PAGER='cat')
H='fa2683e489acc7c85e08764450550f7e463041da';P='10a173cb635fa8d03e357f454232816fc3e77609'
cmds=[]
def git(*args):
 p=subprocess.run(['git','-C',repo,*args],capture_output=True,env=env);cmds.append({'argv':p.args,'exit_code':p.returncode,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr':p.stderr.decode()});assert p.returncode==0;return p.stdout
def unique(pairs):
 d={}
 for k,v in pairs:assert k not in d,k;d[k]=v
 return d
orig=json.loads(git('show',P+':proofs/SOURCE_MAP.json'),object_pairs_hook=unique)
new=json.loads(git('show',H+':proofs/SOURCE_MAP.json'),object_pairs_hook=unique)
deltas=[]
def diff(a,b,path):
 if type(a) is not type(b):deltas.append([path,a,b]);return
 if isinstance(a,dict):
  assert a.keys()==b.keys(),path
  for k in a:diff(a[k],b[k],path+[k])
 elif isinstance(a,list):
  assert len(a)==len(b),path
  for i in range(len(a)):diff(a[i],b[i],path+[i])
 elif a!=b:deltas.append([path,a,b])
diff(orig,new,[])
expected=[[["paths",doc,"current"],doc,None] for doc in ('proofs/CONSOLIDATION.md','proofs/FINDINGS.md')]
assert sorted(deltas,key=lambda x:str(x[0]))==sorted(expected,key=lambda x:str(x[0]))
rows=[]
for ref in (P,H):
 tree={}
 for item in git('ls-tree','-rz','--full-tree',ref).split(b'\0'):
  if not item:continue
  raw,path=item.split(b'\t',1);mode,kind,oid=raw.decode().split();tree[path.decode()]=(mode,kind,oid)
 rows.append(tree)
verified=[]
for key,row in orig['paths'].items():
 left=rows[0][row['current'] or row['preserved']]
 right=rows[1][new['paths'][key]['current'] or new['paths'][key]['preserved']]
 assert left==right and right==(row['mode'],'blob',row['oid']),key
 verified.append(key)
assert len(verified)==9161
search_old=Path('/workspace/scratch/d4d5258160f7/agent5/pr164-evidence/recovery-search.json').read_bytes()
search_new=Path(repo+'/proofs/contributions/agent-5/pr164-replay-evidence-repair-20261017/ORIGINAL_RECEIPT_SEARCH.json').read_bytes()
assert search_old==search_new
receipt={'status':'PASS_BOUNDED_REVIEWER_CROSSCHECK','duplicate_json_keys_present':False,'type_sensitive_exact_differences':deltas,'effective_git_entries_verified_as_blobs':len(verified),'retained_search_record_byte_equal':True,'retained_search_record_sha256':hashlib.sha256(search_new).hexdigest(),'commands':cmds,'notes':'This is a fresh bounded reviewer object/type crosscheck; the historical search itself was reused, not repeated.'}
(out/'bounded-crosscheck.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
