#!/usr/bin/env python3
"""Seal completed independent center review; no Lean execution or proof edits."""
from pathlib import Path
import hashlib,json,re,subprocess
p=Path(__file__).resolve().parent;root=p.parents[4];sha=lambda b:hashlib.sha256(b).hexdigest()
id=json.loads((p/'final-source-identity.json').read_text());v=json.loads((p/'clean-001/verification.json').read_text());r=json.loads((p/'clean-001/results.json').read_text());inv=json.loads((p/'clean-001/implementation-inventory.json').read_text());log=(p/'clean-001/ReviewAudit.log').read_text()
assert v['status']=='PASS' and inv['status']=='PASS' and v['source_modules']==17
assert len(r)==18 and all(x['exit_code']==0 for x in r)
assert len(id['new_module_theorems'])==4 and not id['new_module_definitions']
for e in id['sources']:
 b=(root/e['path']).read_bytes();assert sha(b)==e['sha256'] and b==subprocess.check_output(['git','show',id['source_commit']+':'+e['path']],cwd=root)
new={}
for m in id['new_modules']:
 new[m]={}
 for label,token in [('theorems','AUDIT_THEOREM'),('safe_definitions','AUDIT_SAFE_DEFINITION')]:
  entries=re.findall(r'^'+token+' '+m+r' (\S+) : \[([^\]]*)\]',log,re.M)
  new[m][label]=[{'name':n,'axioms':[] if not ax else re.split(r'\s*,\s*',ax.strip())} for n,ax in entries]
 new[m]['compiler_runtime_definitions']=re.findall(r'^NONSAFE_DEFINITION '+m+r' (\S+)',log,re.M)
assert len(new['Agent1PeriodicCenterWrap']['theorems'])==6 and len(new['Agent1PeriodicNinesCenter']['theorems'])==12
assert not any(x['safe_definitions'] or x['compiler_runtime_definitions'] for x in new.values())
(p/'new-module-origin-audit.json').write_text(json.dumps({'status':'PASS','modules':new,'public_theorems':id['new_module_theorems'],'public_definitions':[],'public_types_checked_in':'clean-001/ReviewAudit.log','runtime_inventory_separate':True},indent=2)+'\n')
report=(p/'source-interpretation-prepublication.md').read_text()
report=report.replace('# Source-only interpretation of both frozen author modules','# Independent semantic and fresh-build review',1)
old='No semantic gap was found in the two source hashes recorded in the companion JSON. This is source interpretation, not an independent compilation or published-source pin claim. The reviewer authored neither new module; prior frozen dependency authorship is disclosed.'
newstatus=f'PASS at published source `{id["source_commit"]}`, registry SHA256 `{id["registry_sha256"]}`. Both author source hashes were checked against publication and remained unchanged after the independent fresh build. The reviewer authored neither new module; prior frozen dependency authorship is disclosed. No semantic finding or failed reviewer Lean command remains.'
assert old in report;report=report.replace(old,newstatus,1)
report=report.replace('Fresh full-closure verification and publication byte comparison remain pending.','The actual import closure and published byte identity were independently verified, and the complete fresh closure passed as recorded below.')
report=report.replace('for196','for 196').replace('is0','is 0').replace('is9','is 9').replace('bounds18','bounds 18')
report+=f'''

## Exact execution and origin audit

The reviewed closure contains exactly 17 modules, all copied from the published source commit into the new empty build directory `/workspace/p196-agent1-session-20261016/nine-center-review-build-001` outside the Git worktree. No author or external project objects were reused. All 17 module compilation commands and the full-origin ReviewAudit command passed in the single reviewer run `clean-001`. There were no failed or interrupted reviewer Lean commands. Original source snapshots, commands, logs, compiler identity and resource limits are preserved. Author attempts remain distinct evidence and retain their original outcomes.

Official Lean 4.19.0, binary SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`, was invoked with `--trust=0 -j1 -DElab.async=false`, an 8 GiB per-process address-space cap and a 600-second per-command timeout. A local ignore file was installed before execution to exclude disposable objects; the actual object directory is outside the worktree. All declaration discovery masks nested comments and strings; the preparation controls cover documentation/string false positives.

The complete origin audit checks {v['theorems_audited']} theorem constants and {v['safe_definitions_audited']} safe definitions. The theorem axiom union is exactly `{', '.join(v['axiom_union'])}`; safe definitions use `{', '.join(v['safe_definition_axiom_union'])}`. Only the standard three axioms are permitted. The two new modules contribute 18 theorem constants (CenterWrap 6, NinesCenter 12), no definitions and no compiler runtime entries. All four public theorem types were checked; the complete audit also checks all {len(v['audited_named_exports'])} top-level public Agent1 theorem declarations in this closure.

The separate compiler inventory contains {inv['nonsafe_count']} generated non-safe runtime definitions: {inv['cstage_helpers']} compilation-stage helpers and {inv['unsafe_rec_helpers']} unsafe-recursion helpers whose safe bases were all audited. It records {len(inv['unsafe_axioms'])} inherited compiler implementation axioms, zero unsafe opaques and no unclassified runtime entries. None of those implementation entries occurs among the accepted theorem/safe-definition axiom dependencies. This is a review of the pinned closure, not repository-wide acceptance. Any separate parent run and its exact historical trust/clean flags remain distinct evidence.
'''
(p/'semantic-review.md').write_text(report)
(p/'README.md').write_text(f'''# Independent nine-center review: PASS

Published source `{id['source_commit']}`; exact 17-module root `Agent1PeriodicNinesCenter`, project `agent1-periodic-nine-center`. The reviewer authored neither new module; earlier frozen dependency authorship is disclosed.

The sole reviewer run `clean-001` passed all 17 source compiles and the full-origin audit, with explicit trust zero and no reused project objects. Full audit: {v['theorems_audited']} theorem constants, {v['safe_definitions_audited']} safe definitions. New modules: 18 theorem constants, four public theorems, no definitions or runtime helpers. Only the standard three theorem axioms occur. See `semantic-review.md` for exact assumptions, empty/small-center treatment, both entry/clock cases, sufficient-fuel equality and scope limits.

Replay with `replay.py --source-root /workspace/p196-agent1-nine-center-20261017 --build-dir NEW_EMPTY_DIRECTORY_OUTSIDE_WORKTREE --evidence-dir NEW_EMPTY_EVIDENCE --lean /workspace/p196-tools/lean-4.19.0-linux/bin/lean`. The driver requires empty output directories, exact published source bytes and no external project objects. `pin_published.py` independently checks the registry, imports, closure and public endpoint inventory. Every executed source/log is retained; disposable objects stay outside the worktree and are also covered by the local ignore file. Prepublication reports remain historical records, not final execution claims.

No mathematical source or registry was changed during review. These local identities establish neither temporal center descent nor a return obstruction, cycle, ordinary seed, or result about 196.
''')
receipt={'status':'INDEPENDENT_REVIEW_PASS','source_commit':id['source_commit'],'registry_sha256':id['registry_sha256'],'reviewer':'Agent #1 specialist symbolic_scope','authored_new_modules':False,'prior_frozen_dependency_authorship_disclosed':True,'accepted_run':'clean-001','failed_or_interrupted_reviewer_lean_runs':[],'source_modules_rebuilt':17,'external_project_objects_reused':False,'trust':0,'all18_compilation_and_audit_commands_passed':True,'theorem_constants_audited':v['theorems_audited'],'safe_definitions_audited':v['safe_definitions_audited'],'new_module_theorem_constants_audited':18,'new_module_safe_definitions_audited':0,'new_public_theorems':id['new_module_theorems'],'new_public_definitions':[],'theorem_axiom_union':v['axiom_union'],'safe_definition_axiom_union':v['safe_definition_axiom_union'],'semantic_findings':[],'compiler_implementation_inventory_separate':True,'source_bytes_equal_published_commit':True,'sources_unchanged_at_finish':True,'disposable_build_outside_git_worktree':True,'repository_wide_acceptance_claimed':False,'review_evidence':{}}
for rel in ['.gitignore','final-source-identity.json','semantic-review.md','clean-001/verification.json','clean-001/implementation-inventory.json','clean-001/ReviewAudit.log','new-module-origin-audit.json','README.md','replay.py','pin_published.py','seal_review.py']:
 receipt['review_evidence'][rel]=sha((p/rel).read_bytes())
(p/'frozen-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
files={str(f.relative_to(p)):{'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in sorted(p.rglob('*')) if f.is_file() and f.name!='FILES.json' and not any(x.startswith('fresh-build-') for x in f.relative_to(p).parts)}
assert not any(Path(x).suffix in ['.olean','.ilean','.o','.c'] for x in files)
(p/'FILES.json').write_text(json.dumps(files,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'receipt_sha256':sha((p/'frozen-receipt.json').read_bytes()),'review_files':len(files),'manifest_sha256':sha((p/'FILES.json').read_bytes()),'semantic_review_sha256':sha((p/'semantic-review.md').read_bytes()),'theorem_constants':v['theorems_audited'],'safe_definitions':v['safe_definitions_audited']},indent=2))
