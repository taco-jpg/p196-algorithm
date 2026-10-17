#!/usr/bin/env python3
"""Seal the completed independent review without running Lean or editing sources."""
from pathlib import Path
import hashlib,json,re,subprocess
p=Path(__file__).resolve().parent
root=p.parents[4]
sha=lambda b:hashlib.sha256(b).hexdigest()
identity=json.loads((p/'final-source-identity.json').read_text())
v=json.loads((p/'clean-001/verification.json').read_text())
r=json.loads((p/'clean-001/results.json').read_text())
inventory=json.loads((p/'clean-001/implementation-inventory.json').read_text())
log=(p/'clean-001/ReviewAudit.log').read_text()
assert v['status']=='PASS' and inventory['status']=='PASS'
assert len(r)==31 and all(x['exit_code']==0 for x in r)
assert v['source_modules']==30 and v['theorems_audited']==1506 and v['safe_definitions_audited']==243
for e in identity['sources']:
 data=(root/e['path']).read_bytes()
 assert sha(data)==e['sha256']
 assert data==subprocess.check_output(['git','show',identity['source_commit']+':'+e['path']],cwd=root)
new={}
for m in identity['new_modules']:
 new[m]={}
 for label,token in [('theorems','AUDIT_THEOREM'),('safe_definitions','AUDIT_SAFE_DEFINITION')]:
  entries=re.findall(r'^'+token+' '+m+r' (\S+) : \[([^\]]*)\]',log,re.M)
  new[m][label]=[{'name':n,'axioms':[] if not ax else ax.split(', ')} for n,ax in entries]
 new[m]['compiler_runtime_definitions']=re.findall(r'^NONSAFE_DEFINITION '+m+r' (\S+)',log,re.M)
 for name in [x for x in identity['new_module_exports'] if x in log]: pass
assert sum(len(x['theorems']) for x in new.values())==31
assert sum(len(x['safe_definitions']) for x in new.values())==2
(p/'new-module-origin-audit.json').write_text(json.dumps({'status':'PASS','modules':new,'public_theorems':identity['new_module_theorems'],'public_definitions':identity['new_module_definitions'],'public_types_checked_in':'clean-001/ReviewAudit.log','runtime_inventory_separate':True},indent=2)+'\n')
source_report=(p/'source-interpretation-prepublication.md').read_text()
final_report=source_report.replace('# Independent source interpretation before publication','# Independent semantic and fresh-build review',1)
old='Status: source-only inspection complete with no semantic finding at the observed source hashes below. This is not an execution result, a frozen publication check, or a claim that a qualifying cycle exists. Independent fresh compilation waits for the parent-confirmed published source and registry.'
new_status='Status: independent review PASS at published commit `'+identity['source_commit']+'`. The three reviewed source hashes were unchanged at final publication and after the fresh build. All 30 source modules plus the full origin audit compiled from source with official Lean 4.19.0 and explicit `--trust=0`; no precompiled project objects were reused. No semantic finding or reviewer compile failure occurred. This review does not claim that a qualifying cycle exists.'
assert old in final_report
final_report=final_report.replace(old,new_status,1)
final_report+='''
## Execution and audit

The exact registry SHA is `239a98f425775ffa41298e1776e7618aed4793f064115f8571f4a29bc0dabac7`. The reviewer independently read back the published remote branch at the pinned commit and checked every registered source byte and Git blob against that commit. Literal imports give exactly the 30 registered modules. All 31 commands (30 modules and ReviewAudit) returned zero in the first reviewer attempt. Original raw sources, commands, compiler hash, resource limits, output logs, and all inventories are retained in `clean-001/`.

The origin audit checked all 1,506 theorem constants and 243 safe definitions in the closure. The theorem axiom union is exactly `propext`, `Classical.choice`, and `Quot.sound`; safe definitions use only `propext`. The three new modules contribute 31 theorem constants and two safe definitions. Their ten public theorem declarations and two public definitions have complete checked types and axiom output; the larger count includes private/generated proof constants. The audit also type-checked all 124 top-level public Agent1 theorem declarations in the closure.

The separate compiler inventory records 976 generated non-safe runtime definitions: 945 compilation-stage helpers and 31 unsafe-recursion implementation helpers whose safe bases were all audited. It also records 13 compiler implementation axioms inherited from `LychrelDigitSums`, zero unsafe opaques, and no unclassified runtime definition. None of these implementation entries appears in the checked theorem/safe-definition axiom dependencies. They are not erased from the inventory or described as additional accepted proof axioms.

The parent's separate canonical run also passed all 30 modules and its ProjectAudit. Its 63 original manifest files are copied byte-for-byte under `../verification/parent-clean-001/`; a separate package manifest adds identity metadata and the exact checker snapshot. Its original report says `source_tree_clean=true` under the checker’s tracked-file status rule, and its Lean commands contain no explicit trust override. Those historical fields are unchanged and are distinct from this reviewer’s explicit trust-zero commands. This is a review of the pinned closure, not a repository-wide acceptance claim.
'''
(p/'semantic-review.md').write_text(final_report)
readme='''# Independent cycle-adapter review

PASS for published source commit `'''+identity['source_commit']+'''`; root `Agent1PeriodicCycleNumeric`, registry project `agent1-periodic-cycle-adapter`.

Reviewer Agent #1 specialist `symbolic_scope` authored none of the three new modules. Prior authorship of some frozen dependency modules is disclosed; all dependencies were nevertheless rebuilt afresh. The separate complementary source review is attributed under `../complementary-review/`.

`clean-001/` is the sole reviewer execution attempt: 30 source compiles plus ReviewAudit all returned zero. No project objects were reused. Commands use official Lean 4.19.0, `--trust=0 -j1 -DElab.async=false`, an 8 GiB per-process address-space cap and a 600-second per-command timeout. Exact elapsed times and compiler bytes are recorded, not inferred. There were no failed or interrupted reviewer commands. Author attempts remain separately preserved in their owned evidence directories.

The full origin audit covers 1,506 theorem constants and 243 safe definitions; the three new modules contain 31 theorem constants and two safe definitions. There are ten new public theorem declarations and two public definitions, all with checked complete types and axiom output. The standard three axioms are the only theorem dependencies. Runtime/compiler helper inventory is separate and complete; see `semantic-review.md` for the exact counts and scope boundaries.

Replay into new, empty directories:

```bash
python3 proofs/contributions/agent-1/periodic-cycle-adapter-20261017/review/replay.py \\
  --source-root /workspace/p196-agent1-cycle-adapter-20261017 \\
  --build-dir /tmp/cycle-review-fresh-build \\
  --evidence-dir /tmp/cycle-review-fresh-evidence \\
  --lean /workspace/p196-tools/lean-4.19.0-linux/bin/lean
```

The driver verifies exact source bytes against `final-source-identity.json` and the published commit. Its lexical scanner masks nested comments and strings before the auxiliary forbidden-token check; logical trust is established by the kernel checks and axiom audit. `pin_published.py` is the independent publication/closure pinning driver, and `package_parent.py` preserves the separate canonical parent run without changing historical flags.

The full source-only evidence manifest excludes disposable `fresh-build-001/` binary objects. All executed sources and logs are retained separately under `clean-001/compiled-sources/`. The prepublication reports are immutable historical records; `frozen-receipt.json` and this README state the final result. The mathematical result remains conditional on a supplied positive complete quotient cycle and explicit safety for every finite-cycle state. It supplies no qualifying cycle or result for a particular decimal seed.
'''
(p/'README.md').write_text(readme)
package=p.parent/'verification/parent-clean-001'
meta=json.loads((package/'PACKAGE.json').read_text())
assert meta['status']=='UNCHANGED_PARENT_EVIDENCE_PACKAGE_PASS'
receipt={'status':'INDEPENDENT_REVIEW_PASS','source_commit':identity['source_commit'],'new_source_sha256':{e['module']:e['sha256'] for e in identity['sources'] if e['module'] in identity['new_modules']},'registry_sha256':identity['registry_sha256'],'reviewer':'Agent #1 specialist symbolic_scope','authored_new_modules':False,'prior_frozen_dependency_authorship_disclosed':True,'accepted_run':'clean-001','failed_or_interrupted_reviewer_runs':[],'source_modules_rebuilt':30,'reused_objects':False,'trust':0,'all_compilation_and_audit_commands_passed':True,'theorem_constants_audited':1506,'safe_definitions_audited':243,'new_module_theorem_constants_audited':31,'new_module_safe_definitions_audited':2,'new_public_theorems':identity['new_module_theorems'],'new_public_definitions':identity['new_module_definitions'],'theorem_axiom_union':v['axiom_union'],'safe_definition_axiom_union':v['safe_definition_axiom_union'],'semantic_findings':[],'compiler_implementation_inventory_separate':True,'source_bytes_equal_published_commit':True,'sources_unchanged_at_finish':True,'review_evidence':{},'parent_evidence_package':'../verification/parent-clean-001','parent_source_tree_clean_original':meta['original_source_tree_clean'],'parent_explicit_trust_override':meta['original_explicit_trust_override'],'repository_wide_acceptance_claimed':False}
for rel in ['final-source-identity.json','semantic-review.md','clean-001/verification.json','clean-001/implementation-inventory.json','clean-001/ReviewAudit.log','new-module-origin-audit.json','README.md','replay.py','pin_published.py','package_parent.py','seal_review.py']:
 receipt['review_evidence'][rel]=sha((p/rel).read_bytes())
(p/'frozen-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
files={str(f.relative_to(p)):{'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in sorted(p.rglob('*')) if f.is_file() and f.name!='evidence-files.json' and not any(q.startswith('fresh-build-') for q in f.relative_to(p).parts)}
(p/'evidence-files.json').write_text(json.dumps(files,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'receipt_sha256':sha((p/'frozen-receipt.json').read_bytes()),'review_file_count':len(files),'review_manifest_sha256':sha((p/'evidence-files.json').read_bytes()),'parent_original_files':meta['original_file_count'],'parent_package_files':len(json.loads((package/'PACKAGE_FILES.json').read_text())),'parent_package_sha256':sha((package/'PACKAGE.json').read_bytes())},indent=2))
