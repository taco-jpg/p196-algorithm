#!/usr/bin/env python3
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parent
inputs=json.loads((root/'CANONICAL_BINDING_INPUT.json').read_text())
identity=json.loads((root/'source/proofs/contributions/agent-1/periodic-nine-cycle-20261017/review/final-source-identity.json').read_text())
refs={k:{e['path']:e for e in v['selected']} for k,v in inputs['refs'].items()}
assert len(identity['sources'])==34
rows=[]
for s in identity['sources']:
    row={'module':s['module'],'path':s['path'],'reviewed_git_blob':s['git_blob']}
    for k in ['H','R','P','B']:
        e=refs[k][s['path']]
        row[k]={'sha':e.get('sha'),'mode':e.get('mode'),'absent':e.get('absent',False)}
    assert row['H']['sha']==row['R']['sha']==s['git_blob']
    assert row['H']['mode']==row['R']['mode']=='100644'
    if s['module'] not in identity['new_modules']:
        assert row['P']['sha']==s['git_blob'] and row['P']['mode']=='100644'
    else: assert row['P']['absent']
    if not row['B']['absent']:
        assert row['B']['sha']==s['git_blob'] and row['B']['mode']=='100644'
    rows.append(row)
registry='proofs/Agent1PeriodicNinesCycle.registry.json'
raw=(root/'source'/registry).read_bytes()
assert hashlib.sha256(raw).hexdigest()==identity['registry_sha256']
blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
assert refs['H'][registry]['sha']==refs['R'][registry]['sha']==blob
assert refs['P'][registry].get('absent') and refs['B'][registry].get('absent')
verifier='proofs/verify_project__214bf7673efe116b.py'
assert len({refs[k][verifier]['sha'] for k in refs})==1
result={'status':'PASS_CANONICAL_SOURCE_BINDING','refs':{k:v['commit'] for k,v in inputs['refs'].items()},'modules_equal_H_R':34,'inherited_equal_P':32,'base_modules_present_equal':sum(not r['B']['absent'] for r in rows),'base_modules_missing':[r['module'] for r in rows if r['B']['absent']],'registry_git_blob':blob,'registry_sha256':hashlib.sha256(raw).hexdigest(),'verifier_git_blob':refs['H'][verifier]['sha'],'rows':rows,'fresh_lean_execution':False,'scope':'Metadata and byte identity only; does not claim prerequisite integration or main acceptance.'}
(root/'CANONICAL_BINDING_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
