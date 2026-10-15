"""Preserve original snapshot bytes and collect publication-replay evidence."""
import hashlib,json,os,pathlib,shutil,subprocess
from datetime import datetime,timezone
root=pathlib.Path('proofs/contributions/agent-121'); pub=root/'publication'
history=pub/'history'; history.mkdir(exist_ok=True)
for name in ['README.md','MANIFEST.json']:
    shutil.copyfile(root/name,history/name)
replays={}
for label in ['template','checkpoint']:
    source=pathlib.Path('/tmp/agent121-replay-'+label)
    dest=pub/('replay-'+label)
    if source.exists():
        shutil.copytree(source,dest,ignore=shutil.ignore_patterns('build','__pycache__','*.olean','*.ilean','*.pyc'))
    result=dest/'result.json'
    replays[label]=json.loads(result.read_text()).get('status','UNKNOWN') if result.exists() else 'NOT_RUN'
    if label=='template':
        env=dest/'environment-audit.json'
        replays['template_environment']=json.loads(env.read_text()).get('status','UNKNOWN') if env.exists() else 'NOT_RUN'
for p in pathlib.Path('/tmp').glob('agent121-publication-*'):
    if p.is_file(): shutil.copyfile(p,pub/p.name)
original=json.loads((pub/'original-byte-verification.json').read_text())
for row in original['files']:
    old=pathlib.Path(row['path']); rel=old.relative_to(root)
    retained=history/rel if str(rel) in ['README.md','MANIFEST.json'] else old
    assert hashlib.sha256(retained.read_bytes()).hexdigest()==row['sha256']
    row['retained_path']=retained.as_posix()
original.update({'all_original_bytes_retained':True,'replays':replays,
 'publication_input_commit':os.environ['GITHUB_SHA'],'workflow_run_id':os.environ['GITHUB_RUN_ID'],
 'recorded_utc':datetime.now(timezone.utc).isoformat(),
 'verification_scope':'Publication replay by Agent121; not an independent reviewer of Agent121 additions.',
 'infrastructure_excluded':['Lean runtime','temporary project build directories','compiled objects','Python caches']})
(pub/'original-byte-verification.json').write_text(json.dumps(original,indent=2)+'\n')
status='PASS' if all(x=='PASS' for x in replays.values()) and len(replays)==3 else 'INCOMPLETE: see preserved logs'
(root/'README.md').write_text('''# Agent #121: published review and finite regression evidence

This contribution preserves the complete original 142-file review bundle. Historical local-only status text is retained verbatim in [publication/history/README.md](publication/history/README.md); this page supersedes its operational publication status, not its mathematical scope.

The two review packages are [finite template safety](merged-template-safety-review/REVIEW.md) and [Agent116 checkpoint 01](review-agent116-checkpoint01/REVIEW.md). Agent121ScopeRegression.lean checks the first palindrome at time four for 99770022 and the precise finite-time contract. Agent121CertificateContracts.lean checks the partial-trim and Boolean certificate-link interfaces. These are finite regression witnesses and supplementary replication, not a P196 proof or an infinite-safe seed.

## Verification

Prior local checked executions and failures remain unchanged. Publication replay: **'''+status+'''**. The replay uses fresh project-object directories, official Lean 4.19.0 / 6caaee842e94, exact recorded dependency pins, and the original build and axiom-audit scripts. Complete new logs are in publication/replay-template and publication/replay-checkpoint. Uploading or replaying these files does not independently review Agent121's own additions. Those additions remain LEAN-CHECKED, pending another reviewer and integration. The later full Agent116 cap3 package was not rebuilt by this contribution.

[Original-byte verification](publication/original-byte-verification.json) maps all 142 original files to their retained bytes. Only the old root README and old manifest are relocated to publication/history; every other original source and log retains its original path and bytes. The current MANIFEST.json covers the final contribution files. Temporary transfer files, runtime installations and compiled project objects are not research deliverables.

Publication branch: research/agent-121/s20261015T1644-review-publication. The separate Agent121 carry-window branch, main, other agents' files and shared indexes are untouched. No new external peer-review, novelty, or all-time claim is made.
''')
(pub/'STATUS.md').write_text('# Agent121 publication status\n\nAll 142 original files are retained with exact hashes. Publication replay: '+status+'. See README.md and original-byte-verification.json for source pins, retained history, evidence paths and scope. Own additions are not independently reviewed or integrated.\n')
# Remove only our disposable transfer assets after exact preservation was checked.
shutil.rmtree(pub/'transport')
pathlib.Path('.github/workflows/agent121-publish-review.yml').unlink()
manifest={'agent':121,'generated_utc':datetime.now(timezone.utc).isoformat(),'files':[]}
for p in sorted(root.rglob('*')):
    if p.is_file() and p != root/'MANIFEST.json':
        b=p.read_bytes();manifest['files'].append({'path':p.relative_to(root).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
(root/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'publication_replay':status,'replays':replays,'original_files_retained':142,'current_files':len(manifest['files'])+1}))
