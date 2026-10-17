#!/usr/bin/env python3
"""Copy original parent source/log evidence byte-for-byte; add separate metadata."""
import hashlib,json,subprocess
from pathlib import Path
root=Path('/workspace/p196-agent1-zero-width-loop-20261016')
origin=Path('/workspace/p196-agent1-session-20261016/zero-width-loop-parent-clean-001')
dest=root/'proofs/contributions/agent-1/zero-width-loop-20261016/verification/parent-clean-001'
review=root/'proofs/contributions/agent-1/zero-width-loop-20261016/review'
sha=lambda b:hashlib.sha256(b).hexdigest()
manifest_bytes=(origin/'FILES.json').read_bytes(); manifest=json.loads(manifest_bytes)
dest.mkdir(parents=True,exist_ok=False)
for rel,record in manifest.items():
 assert not Path(rel).is_absolute() and '..' not in Path(rel).parts
 assert Path(rel).suffix in ('.lean','.log','.json'),rel
 data=(origin/rel).read_bytes()
 assert len(data)==record['bytes'] and sha(data)==record['sha256'],rel
 out=dest/rel;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data)
 assert out.read_bytes()==data
(dest/'FILES.json').write_bytes(manifest_bytes)
identity=json.loads((review/'final-source-identity.json').read_text())
parent=json.loads((dest/'verification.json').read_text())
assert parent['status']=='PASS' and parent['source_commit']==identity['source_commit']
assert parent['registry_sha256']==identity['registry_sha256']
project=parent['projects']['agent1-periodic-zero-width-loop']
assert project['status']=='PASS'
for command in project['commands']:
 assert command['exit_code']==0
 assert not any(arg.startswith('--trust') or arg=='-t' for arg in command['argv'])
 data=(dest/command['log']).read_bytes();assert sha(data)==command['log_sha256']
for entry in identity['sources']:
 data=(dest/'agent1-periodic-zero-width-loop/source'/f"{entry['module']}.lean").read_bytes()
 assert sha(data)==entry['sha256']
 assert data==subprocess.check_output(['git','show',identity['source_commit']+':'+entry['path']],cwd=root)
(dest/'SOURCE_IDENTITY.json').write_bytes((review/'final-source-identity.json').read_bytes())
meta={'status':'UNCHANGED_PARENT_EVIDENCE_PACKAGE_PASS','origin':str(origin),'source_commit':parent['source_commit'],'original_manifest_sha256':sha(manifest_bytes),'original_manifest_unchanged':True,'original_file_count':len(manifest),'source_modules':len(identity['sources']),'source_bytes_equal_published_commit':True,'original_source_tree_clean':parent['source_tree_clean'],'original_tracked_clean_semantics':'git status --porcelain --untracked-files=no, as recorded by parent checker','original_explicit_trust_override':False,'independent_review_explicit_trust_override':'--trust=0','parent_command_count':len(project['commands']),'parent_theorem_count':project['theorem_count'],'original_registry_status_fields_preserved':True,'objects_excluded':True,'new_lean_execution_performed_by_packaging':False,'note':'Original manifest, verification report, generated audit, logs, and source bytes are unchanged. Added package metadata does not amend the historical report.'}
(dest/'PACKAGE.json').write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps(meta,indent=2))
