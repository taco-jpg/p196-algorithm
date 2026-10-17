import ast, hashlib, json, subprocess
from pathlib import Path
R=Path('.')
H='056e6e9256ef446b372354c911e2be3d3c006dd1'
BASE='10a173cb635fa8d03e357f454232816fc3e77609'
B='74a1c3922eb7af438fe40b23d2105ad07556e3f5'
REVIEW='6f191168a6175879276d397a3ce99859c994f982'
TREE='a01aee0be2a6045ad6b8560a135230eb37a16e00'
D='proofs/contributions/agent-62/residual-five-guide/'
def git(*a): return subprocess.check_output(['git',*a])
def obj(ref,path): return git('show',ref+':'+path)
def oid(ref,path): return git('rev-parse',ref+':'+path).decode().strip()
paths=git('diff','--name-only',BASE,H).decode().splitlines()
assert len(paths)==17
assert all(s.startswith('A\t') for s in git('diff','--name-status',BASE,H).decode().splitlines())
entries=git('ls-tree','-r',H,'--',*paths).decode().splitlines()
assert all(e.startswith('100644 blob ') for e in entries)
print('ADDED_FILE_IDENTITIES')
for path in paths:
 data=obj(H,path)
 assert (R/path).read_bytes()==data
 assert obj(TREE,path)==data
 print(json.dumps({'path':path,'blob':oid(H,path),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'mode':'100644'}))
hist=[('history/ResidualFiveFibersGuide.initial.md','ab1d8216f2acf87f4bce4a2961efc4727df09418','proofs/ResidualFiveFibersGuide.md'),('history/README.initial.md','ab1d8216f2acf87f4bce4a2961efc4727df09418',D+'README.md'),('history/ResidualFiveFibersGuide.replay.md','81508fbee30e0eed2affd43e4e8ec735dc9a53de','proofs/ResidualFiveFibersGuide.md'),('history/README.replay.md',REVIEW,D+'README.md'),('history/README.index-initial.md',REVIEW,D+'history/README.md')]
for dst,ref,src in hist:
 assert obj(H,D+dst)==obj(ref,src)
 print('HISTORICAL_BYTE_MATCH',dst,ref,src,oid(ref,src))
run=json.loads(obj(H,D+'validation-execution.json'))
receipt=json.loads(obj(H,D+'retained-evidence-validation.json'))
assert run['complete_retained_evidence_inspection']['argv'][:3]==['python3','-B','-c']
assert run['complete_retained_evidence_inspection']['argv'][-1].encode()==obj(H,D+'verify_retained_evidence.py')
assert json.loads(run['complete_retained_evidence_inspection']['stdout'])==receipt
for key in ['preliminary_archive_inspection','complete_retained_evidence_inspection']:
 assert run[key]['exit_code']==0
 ast.parse(run[key]['argv'][-1])
print('SCRIPT_AND_EXECUTION_RECEIPT_IDENTITIES_PASS')
sb=json.loads(obj(H,D+'source-boundary-validation.json'))
pkg=sb['package']
entries={}
for line in git('ls-tree',BASE+':'+pkg).decode().splitlines():
 mode,typ,rest=line.split(' ',2)
 sha,name=rest.split('\t',1)
 entries[name]={'name':name,'type':'dir' if typ=='tree' else 'file','sha':sha}
assert len(entries)==sb['compared_immediate_entries']==24
assert entries=={e['name']:e for e in sb['package_entries']}
assert oid(BASE,pkg)==oid(B,pkg)==oid(H,pkg)==oid(TREE,pkg)
reviewed_paths=git('diff','--name-status',BASE,REVIEW).decode().splitlines()
assert len(reviewed_paths)==11
assert all(x.startswith('A\t') for x in reviewed_paths)
assert {x.split('\t',1)[1] for x in reviewed_paths}=={x['path'] for x in sb['changed_paths']}
for e in sb['changed_paths']: assert oid(REVIEW,e['path'])==e['git_blob']
assert oid(H,'proofs/ResidualFiveFibersGuide.md')==oid(REVIEW,'proofs/ResidualFiveFibersGuide.md')==sb['reviewed_guide_blob']
assert int(git('rev-list','--count',BASE+'..'+REVIEW))==sb['documentation_commit_count']==3
oc=json.loads(obj(H,D+'occurrence-bound-clarification.json'))
assert oid(oc['source_commit'],oc['source_path'])==oc['source_git_blob']
ri=json.loads(obj(H,D+'reproduction-inspection.json'))
assert oid(BASE,ri['package']['path'])==ri['package']['git_blob']
assert oid(BASE,ri['source_import_route']['path'])==ri['source_import_route']['git_blob']
for path in paths:
 if path.endswith('.json'): json.loads(obj(H,path))
print('SOURCE_BOUNDARY_JSON_PASS',oid(BASE,pkg))
print('COMBINATION_DELTA',git('diff','--name-status',B,TREE).decode())
assert git('diff','--name-status',B,TREE)==git('diff','--name-status',BASE,H)
assert not git('status','--porcelain')
print('ALL_BOUNDED_LOCAL_IDENTITY_CHECKS_PASS')
