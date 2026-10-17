python3 -B - <<'PY'
from pathlib import Path
import hashlib, json, difflib
root=Path('/workspace/scratch/2e594544e72c/agent8-pr157')
source=root/'source'
m=json.loads((root/'SOURCE_MANIFEST.json').read_text())
checked=[]
for entry in m['files']:
    data=(source/entry['path']).read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    digest=hashlib.sha256(data).hexdigest()
    assert (len(data),blob,digest)==(entry['bytes'],entry['git_blob'],entry['sha256']), entry['path']
    checked.append(entry['path'])
assert set(checked)=={str(p.relative_to(source)) for p in source.rglob('*') if p.is_file()}
base=source/'proofs/contributions/agent-62/residual-five-guide'
json_paths=[p for p in source.rglob('*.json')]
for p in json_paths:
    json.loads(p.read_text())
record=json.loads((base/'validation-execution.json').read_text())
program=record['complete_retained_evidence_inspection']['argv'][-1]
assert program.encode()==(base/'verify_retained_evidence.py').read_bytes()
assert json.loads(record['complete_retained_evidence_inspection']['stdout'])==json.loads((base/'retained-evidence-validation.json').read_text())
boundary=json.loads((base/'source-boundary-validation.json').read_text())
old={e['path']:e['git_blob'] for e in boundary['changed_paths']}
new={e['path']:e['git_blob'] for e in m['files']}
changed=[p for p in old if old[p]!=new[p]]
added=[p for p in new if p not in old]
assert len(changed)==2 and len(added)==6
preserved={
 'history/README.replay.md':'proofs/contributions/agent-62/residual-five-guide/README.md',
 'history/README.index-initial.md':'proofs/contributions/agent-62/residual-five-guide/history/README.md'
}
for p, prior in preserved.items():
    data=(base/p).read_bytes()
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==old[prior]
print(json.dumps({'head':m['head'],'file_count':len(checked),'total_bytes':sum(e['bytes'] for e in m['files']),'identity_checks':'PASS: bytes, Git blob SHA-1, SHA-256, exact file inventory','json_parse_count':len(json_paths),'embedded_program_matches_published_program':True,'embedded_stdout_matches_validation_receipt':True,'reviewed_head':boundary['documentation_reviewed_head'],'guide_unchanged_from_reviewed_head':old['proofs/ResidualFiveFibersGuide.md']==new['proofs/ResidualFiveFibersGuide.md'],'later_delta_modified_paths':changed,'later_delta_added_paths':added,'overwritten_reviewed_documents_preserved':True},indent=2))
for p,q in [('history/README.replay.md','README.md'),('history/README.index-initial.md','history/README.md')]:
    print(''.join(difflib.unified_diff((base/p).read_text().splitlines(True),(base/q).read_text().splitlines(True),fromfile=p,tofile=q)))
PY
