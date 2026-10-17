#!/usr/bin/env python3
"""Seal text evidence only after the independent and parent local checks pass."""
from pathlib import Path
import collections, hashlib, json, re, shutil, subprocess
review=Path(__file__).resolve().parent
root=review.parents[4]
package=review.parent
clean=review/'clean-001'
build=Path('/workspace/p196-agent1-session-20261016/periodic-upper-gap-review-clean-001')
parent=Path('/workspace/p196-agent1-session-20261016/upper-gap-parent-clean-001')
project='agent1-periodic-return-upper-gap'
sha=lambda b:hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,j):p.write_text(json.dumps(j,indent=2)+'\n')
def gitdata(commit,p):return subprocess.check_output(['git','show',commit+':'+p],cwd=root)
def manifest(d,name):
 j={str(p.relative_to(d)):{'bytes':len(p.read_bytes()),'sha256':sha(p.read_bytes())} for p in sorted(d.rglob('*')) if p.is_file() and p!=d/name and p.suffix not in ['.olean','.ilean','.pyc'] and '__pycache__' not in p.parts}
 write(d/name,j)
 for p,x in j.items():
  b=(d/p).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256']
 return j
identity=read(review/'final-source-identity.json');commit=identity['source_commit']
v=read(clean/'verification.json');results=read(clean/'results.json');inv=read(clean/'implementation-inventory.json')
assert v['status']=='PASS' and inv['status']=='PASS' and len(results)==42 and len(identity['sources'])==41
assert len(v['audited_named_exports'])==172 and all(x['exit_code']==0 and '--trust=0' in x['command'] for x in results)
pv=read(parent/'verification.json');pp=pv['projects'][project]
assert pv['status']==pp['status']=='PASS' and pv['source_commit']==commit and pp['theorem_count']==v['theorems_audited']
checks=[]
for x in identity['sources']:
 data=(root/x['path']).read_bytes();assert sha(data)==x['sha256'];assert data==gitdata(commit,x['path'])==(build/(x['module']+'.lean')).read_bytes()==(clean/'compiled-sources'/(x['module']+'.lean')).read_bytes()
 pb=parent/project/'source'/(x['module']+'.lean');assert data==pb.read_bytes()
 checks.append({'module':x['module'],'sha256':x['sha256'],'local_commit_worktree_build_archive_parent_equal':True})
reg=(root/identity['registry_path']).read_bytes();assert sha(reg)==identity['registry_sha256'] and reg==gitdata(commit,identity['registry_path'])
for x in results:assert sha((clean/(x['module']+'.log')).read_bytes())==x['log_sha256']
assert (review/'replay.py').read_bytes()==(clean/'replay.py').read_bytes()
assert (clean/'ReviewAudit.lean').read_bytes()==(build/'ReviewAudit.lean').read_bytes()
log=(clean/'ReviewAudit.log').read_text();tc=collections.Counter(re.findall(r'AUDIT_THEOREM (\S+) ',log));dc=collections.Counter(re.findall(r'AUDIT_SAFE_(?:DEFINITION|OPAQUE) (\S+) ',log))
new=[]
for x in identity['sources']:
 if x['module'] in identity['new_modules']:
  new += ['Agent1.Periodic.'+n for n in re.findall(r'^theorem\s+(\w+)',(root/x['path']).read_text(),re.M)]
assert len(new)==5 and all(x in v['audited_named_exports'] for x in new)
source_receipt={'status':'PASS_LOCAL_FROZEN_SOURCE_IDENTITY','source_commit':commit,'remote_publication_at_verification':'PENDING_AUTHENTICATION_FAILURE','registry_sha256':identity['registry_sha256'],'sources':checks,'all_command_log_hashes_checked':True,'executed_driver_exact_match':True,'audit_source_exact_match':True,'source_tree_status_after_build':subprocess.check_output(['git','status','--short'],cwd=root,text=True).splitlines()}
write(clean/'local-source-receipt.json',source_receipt)
summary={'status':'PASS','source_commit':commit,'remote_publication':'Pending; local verification does not assert a successful push.','modules':41,'lean_commands':42,'failed_lean_commands':[],'failed_wrapper_runs':[],'seconds':sum(x['seconds'] for x in results),'theorems':v['theorems_audited'],'safe_definitions':v['safe_definitions_audited'],'public_named_theorem_exports':len(v['audited_named_exports']),'new_public_exports':new,'prior_public_count':len(v['audited_named_exports'])-len(new),'per_module':{x['module']:{'theorems':tc[x['module']],'safe_definitions':dc[x['module']]} for x in identity['sources']},'axiom_union':v['axiom_union'],'safe_definition_axiom_union':v['safe_definition_axiom_union'],'unsafe_implementation_axioms':len(inv['unsafe_axioms']),'nonsafe_generated_definitions':inv['nonsafe_count'],'cstage_helpers':inv['cstage_helpers'],'unsafe_rec_helpers':inv['unsafe_rec_helpers'],'unsafe_opaque_count':len(inv['unsafe_opaques']),'unclassified_nonsafe_count':len(inv['unclassified_nonsafe'])}
write(review/'audit-summary.json',summary)
# Preserve the parent's existing manifest/report/flags exactly; additions have a separate manifest.
dest=package/'verification/parent-clean-001';dest.mkdir(parents=True,exist_ok=False)
original=read(parent/'FILES.json')
for rel,x in original.items():
 source=parent/rel;data=source.read_bytes();assert len(data)==x['bytes'] and sha(data)==x['sha256'];target=dest/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
shutil.copyfile(parent/'FILES.json',dest/'FILES.json')
checker='proofs/verify_project__214bf7673efe116b.py';data=(root/checker).read_bytes();assert data==gitdata(commit,checker);(dest/'canonical-checker.py').write_bytes(data)
parent_receipt={'status':'PASS_EXACT_PARENT_TEXT_PACKAGE','executor':'Parent /root; not this specialist','source_commit':commit,'remote_publication_at_verification':'PENDING_AUTHENTICATION_FAILURE','original_report_sha256':sha((parent/'verification.json').read_bytes()),'original_files_sha256':sha((parent/'FILES.json').read_bytes()),'original_files_count':len(original),'original_source_tree_clean':pv['source_tree_clean'],'original_command_flags_preserved':True,'all_commands_explicit_trust_zero':all('--trust=0' in c['argv'] for c in pp['commands']),'canonical_checker_path':checker,'canonical_checker_sha256':sha(data),'source_pins':checks,'no_project_objects_copied':True}
write(dest/'source-identity-receipt.json',parent_receipt);pm=manifest(dest,'PACKAGE-FILES.json')
text=(review/'semantic-review.md').read_text()
text=text.replace('The independent fresh rebuild is in progress against frozen local commit','The independent fresh rebuild passed against frozen local commit')
text=text.replace('Fresh compilation, full-origin/safe-definition dependency checks, public type prints, and parent evidence packaging remain in progress.','Fresh compilation, full-origin/safe-definition dependency checks, public type prints, and separate parent evidence packaging are now complete.')
text += f'''

## Independent fresh execution

All 41 source compilations and ReviewAudit passed on the first attempt in {summary['seconds']:.3f} seconds. The exact executed replay driver is archived in clean-001, SHA256 `{sha((review/'replay.py').read_bytes())}`. Every command uses official Lean 4.19.0, explicit `--trust=0 -j1 -DElab.async=false`, default stack, an 8-GiB address-space cap and a 600-second timeout. LEAN_PATH points only to the newly created build directory. No project objects were reused.

The complete actual-origin audit checked {summary['theorems']:,} theorem constants and {summary['safe_definitions']:,} safe definitions/opaques. The theorem axiom union is `propext`, `Classical.choice`, and `Quot.sound`; safe definitions use only `propext` and `Quot.sound`. All 172 named public theorem types and their source axiom prints were checked: five new and 167 prior. InitialIncoming contributes {tc['Agent1PeriodicInitialIncoming']} actual-origin theorem constants; ReturnUpper contributes {tc['Agent1PeriodicReturnUpper']}; neither new module contains safe definitions.

The separate implementation inventory records {summary['unsafe_implementation_axioms']} unsafe compiler implementation axioms and {summary['nonsafe_generated_definitions']:,} nonsafe generated definitions ({summary['cstage_helpers']:,} cstage helpers and {summary['unsafe_rec_helpers']} unsafe recursion implementations whose safe bases were audited). There are zero unsafe opaques and zero unclassified implementations. These runtime entries do not enlarge the logical dependency sets. The comment-aware forbidden-token postcheck passed; all source inputs and log hashes, the generated audit source, and the archived replay driver were rechecked. No failed Lean command, wrapper failure, timeout or source drift occurred.

The source and registry identity receipt records agreement among the frozen LOCAL commit, worktree, compiled inputs and archived full-source snapshots. It does not assert successful remote publication. The accepted claim is unchanged; the authentication failure is a publication limitation, not a failed proof check.

## Separate parent canonical execution

The parent independently completed its canonical fresh 41-module check, with {pp['theorem_count']:,} theorem constants. This specialist verified and copied only its text evidence into ../verification/parent-clean-001. All {len(original)} original manifest entries and the original FILES.json are preserved byte-for-byte. The actual original source_tree_clean value is `{str(pv['source_tree_clean']).lower()}`. Original command flags are unchanged and do not explicitly include --trust=0; every command in this specialist's own run does. All 41 parent source inputs match the frozen local sources.

The exact canonical checker and a separate source-identity receipt are additional files, covered by a separate {len(pm)}-entry PACKAGE-FILES.json. No compiled objects are packaged. Parent execution is not attributed to this reviewer.

No unresolved semantic defect remains. The proven endpoint is a necessary condition for positive exact complete-tuple returns at the specified initial phase: N+2≤4C, and positive G with C=8G, signed delta G, 16G≤N and N+2≤32G. This package does not include the separate strict lower bound, prove a return exists, classify generic equality cycles, lift an arbitrary graph path, assert safety or an infinite ordinary trajectory, or prove a statement about 196.
'''
(review/'semantic-review.md').write_text(text)
(review/'README.md').write_text(f'''# Independent UpperGap review

Fresh LOCAL source commit `{commit}` passed independent verification: 41 modules plus ReviewAudit, {summary['theorems']:,} theorem constants, {summary['safe_definitions']:,} safe definitions, and 172 named public theorem interfaces (five new). Remote publication was pending because GitHub authentication failed after environment reconnect; this receipt makes no successful-push claim.

The reviewer is the separate same-session/account specialist `/root/research_status`, with no mathematical source authorship in this closure. ReturnUpper was authored by a separate child specialist. Parent canonical execution is separately attributed in verification/parent-clean-001.

Run from any checkout containing these exact files with the official Lean 4.19.0 binary:

```sh
python3 proofs/contributions/agent-1/periodic-return-upper-gap-20261017/review/replay.py \\
  --source-root /absolute/checkout \\
  --build-dir /absolute/new-empty-build-path \\
  --evidence-dir /absolute/new-empty-evidence-path \\
  --lean /absolute/lean-4.19.0-linux/bin/lean
```

The build and evidence paths must not exist. The driver verifies the pinned compiler and source hashes, copies every source into a fresh build, archives itself and all compiled sources, compiles with explicit --trust=0, and audits all module-origin theorems and safe definitions. Its generated-implementation inventory is separate from logical dependency checking. The default resource limits are 8 GiB address space and 600 seconds per command, default Lean stack. No prior project objects are reused.

`semantic-review.md` explains the exact premises, edge cases and limits. `audit-summary.json`, `final-review-receipt.json`, and `clean-001/local-source-receipt.json` record the completed run. `clean-001/replay.py` is byte-identical to the executed driver. The full compiled source snapshots, logs, results and generated audit source are included. The initial source-only preparation snapshots are historical and were not executed. `seal-evidence.py` is the text-evidence sealing script; it is separate from the Lean replay.

`FILES.json` covers this review's text evidence and excludes itself and generated runtime objects. The parent package preserves its original FILES/report/flags and has a separate PACKAGE-FILES manifest. Retained author attempt001 failed on unknown Nat.cast_zero; attempt002 passed a smaller partial source; attempt003 passed the final source. These author increments reused dependencies and are not this independent fresh build.
''')
final={'status':'PASS','reviewer':'Separate same-session/account nonauthor specialist /root/research_status; ReturnUpper author is a separate child specialist.','source_commit':commit,'remote_publication':'Pending authentication recovery at verification time','source_modules':41,'strict_lean_commands':42,'failed_lean_commands':0,'failed_wrapper_runs':0,'project_objects_reused':False,'theorems':summary['theorems'],'safe_definitions':summary['safe_definitions'],'named_public_theorem_types_and_axiom_prints':172,'new_public_theorems':5,'prior_public_theorems':167,'axiom_union':v['axiom_union'],'safe_definition_axiom_union':v['safe_definition_axiom_union'],'unsafe_implementation_axioms_separately_inventoried':summary['unsafe_implementation_axioms'],'nonsafe_compiler_definitions_separately_inventoried':summary['nonsafe_generated_definitions'],'unsafe_opaque_count':0,'unclassified_nonsafe_count':0,'executed_driver_sha256':sha((review/'replay.py').read_bytes()),'archived_driver_exact_match':True,'verification_sha256':sha((clean/'verification.json').read_bytes()),'semantic_review_sha256':sha((review/'semantic-review.md').read_bytes()),'parent_canonical_execution_separate':True,'parent_original_source_tree_clean':pv['source_tree_clean'],'parent_packaging_receipt_sha256':sha((dest/'source-identity-receipt.json').read_bytes()),'parent_package_manifest_sha256':sha((dest/'PACKAGE-FILES.json').read_bytes()),'remaining_semantic_flaw':None,'scope_limits':'Positive exact full B/H/w return at initial period14,14,4,4 implies actual last clock1,N+2<=4C,and positiveG with C=8G,signedDelta=G,16G<=N,N+2<=32G. No strict lower bound imported, existence,generic equality classifier,ordinary lift,safety,infinite orbit or196 claim.'}
write(review/'final-review-receipt.json',final);rm=manifest(review,'FILES.json')
print(json.dumps({'status':'SEALED','source_commit':commit,'review_files':len(rm),'parent_original_files':len(original),'parent_package_files':len(pm),'counts':{k:summary[k] for k in ['modules','theorems','safe_definitions','public_named_theorem_exports']},'review_manifest_sha256':sha((review/'FILES.json').read_bytes()),'semantic_review_sha256':final['semantic_review_sha256'],'final_receipt_sha256':sha((review/'final-review-receipt.json').read_bytes()),'parent_package_sha256':final['parent_package_manifest_sha256']},indent=2))
