#!/usr/bin/env python3
"""Seal actual fresh sharp-excursion review after successful source-pinned execution."""
from pathlib import Path
import hashlib,json,re,subprocess,datetime
p=Path(__file__).resolve().parent; root=p.parents[4]
sha=lambda b:hashlib.sha256(b).hexdigest()
identity=json.loads((p/'source-identity.json').read_text())
v=json.loads((p/'clean-001/verification.json').read_text())
results=json.loads((p/'clean-001/results.json').read_text())
inv=json.loads((p/'clean-001/implementation-inventory.json').read_text())
execution=json.loads((p/'execution-receipt.json').read_text())
log=(p/'clean-001/ReviewAudit.log').read_text()
assert v['status']=='PASS' and inv['status']=='PASS' and v['source_modules']==32
assert execution['exit_code']==0 and len(results)==33 and all(r['exit_code']==0 and not r['timed_out'] for r in results)
assert v['reviewer']=='Agent #1 specialist center_review_resume'
assert len(identity['new_module_theorems'])==5 and not identity['new_module_definitions']
for e in identity['sources']:
 data=(root/e['path']).read_bytes()
 assert sha(data)==e['sha256'] and data==subprocess.check_output(['git','show',identity['source_commit']+':'+e['path']],cwd=root)
 assert data==(p/'clean-001/compiled-sources'/f"{e['module']}.lean").read_bytes()
 assert sha((p/'clean-001'/f"{e['module']}.log").read_bytes())==next(r['log_sha256'] for r in results if r['module']==e['module'])
registry=(root/identity['registry_path']).read_bytes()
assert sha(registry)==identity['registry_sha256'] and registry==subprocess.check_output(['git','show',identity['source_commit']+':'+identity['registry_path']],cwd=root)
assert (p/'clean-001/replay.py').read_bytes()==(p/'replay.py').read_bytes()
assert sha((p/'clean-001/ReviewAudit.log').read_bytes())==results[-1]['log_sha256']
pre=json.loads((p/'prepublication-source-review.json').read_text())
for mod in identity['new_modules']:
 assert pre['observed_sources'][mod]==next(e['sha256'] for e in identity['sources'] if e['module']==mod)
new={}
for mod in identity['new_modules']:
 new[mod]={}
 for label,token in [('theorems','AUDIT_THEOREM'),('safe_definitions','AUDIT_SAFE_DEFINITION')]:
  entries=re.findall(r'^'+token+' '+mod+r' (\S+) : \[([^\]]*)\]',log,re.M)
  new[mod][label]=[{'name':n,'axioms':[] if not ax else re.split(r'\s*,\s*',ax.strip())} for n,ax in entries]
 new[mod]['runtime_definitions']=re.findall(r'^NONSAFE_DEFINITION '+mod+r' (\S+)',log,re.M)
assert len(new['Agent1PeriodicNinesClockStrip']['theorems'])==16
assert len(new['Agent1PeriodicCenterNormalPath']['theorems'])==5
assert len(new['Agent1PeriodicNinesSharpExcursion']['theorems'])==9
assert all(not e['safe_definitions'] and not e['runtime_definitions'] for e in new.values())
for name in identity['new_module_exports']:
 assert f"'{name}' depends on axioms:" in log or f"'{name}' does not depend on any axioms" in log
assert set(v['axiom_union'])=={'propext','Classical.choice','Quot.sound'}
assert set(v['safe_definition_axiom_union']) <= {'propext','Classical.choice','Quot.sound'}
for filename in ['new-module-origin-audit.json','semantic-review.md','README.md','frozen-receipt.json','FILES.json']:
 assert not (p/filename).exists(),'Do not overwrite sealed evidence: '+filename
(p/'new-module-origin-audit.json').write_text(json.dumps({'status':'PASS','reviewer':v['reviewer'],'modules':new,'public_theorems':identity['new_module_theorems'],'public_definitions':identity['new_module_definitions'],'literal_public_axioms_and_types':'clean-001/ReviewAudit.log','runtime_inventory_separate':True},indent=2)+'\n')
report=f'''# Independent clock-strip and sharp-excursion review

PASS for published source `{identity['source_commit']}`, registry SHA256 `{identity['registry_sha256']}`. Reviewer: Agent #1 specialist `center_review_resume`, author of none of the new or inherited mathematical modules. I performed the actual fresh execution and semantic inspection. All three new modules match the earlier source-only snapshots and frozen published bytes. Preparation records retain their historical unexecuted status; the replay helper's provenance from my prior excursion review is recorded. Earlier PR173/175 review and execution evidence remain separate.

## Mathematical review

`centerPeriods_nines_clock_one` retains original ValidPeriodic for B/H/W9, literal input normalization `stripPeriodCenter W9 H=(H,0)`, actual mixed entries and actual `rawGamma=1`. It proves the original centerPeriods count is exactly one; it does not assume a further nine transition or choose a carry independently. The local normalized-center premise belongs to this local API and is subsequently proved from the closed path for the sharp return theorem.

The private clock-pad peel argument is exact. With bit e, coefficient bound 18, symmetry, and the actual mixed terminal-carry equation, the first paired boundary digit being nine forces the first input coefficient to be nine: e=0 gives a mod 10=9, and e=1 gives (a+1) mod 10=0; the bound excludes any alternative. Symmetry forces the final coefficient to be nine. Empty and singleton-nine cases contradict the mixed equation. Removing those two nines preserves symmetry, coefficient bounds, and the same mixed carry equation, because nine transmits the carry bit. The fixed-digit decomposition and `pair_three_parts` identify the residual pair with precisely the same clock pad. Four iterations therefore show that a residual W9 wrapper requires an original W9 wrapper. Original maximality contradicts the latter, so the residual strip count is zero and the actual full count is one.

No even-center parity field is used in that private ancestry argument. The public theorem correctly retains original ValidPeriodic, including its original fields; the earlier issue61 assertion that parity was necessary was explicitly corrected in comment 6228673931. This review neither repeats that necessity claim nor treats exploratory computational samples as a proof. The actual clock is the original rawGamma, not H's outgoing carry or a freely selected bit.

`stripPeriodCenter_of_maximal` retracts the unchanged algorithm on a word with no complete mirrored-period wrapper. Its empty-period branch uses the original total empty-period convention. In the nonempty branch, the reconstruction test fails, and either length-fuel case returns (H,0). It introduces no definition or global rewrite.

`quotient_path_return_centers_normal` assumes only original QuotientPath, N>0, center return and period return. Every positive index receives a literal quotient output, so the existing `quotient_irreducible` theorem gives maximality with respect to its actual successor period. Retraction gives exact pair equality. Index zero inherits that equality from the returned endpoint. No original validity, exterior return, nine phase, or initial-normalization premise is added. Endpoint and zero-index handling are explicit.

`quotient_return_nines_center_drop_eight` retains original QuotientPath, original initial ValidPeriodic, initial nine phase, N>0, and full B/H/w return. The previous excursion theorem supplies all-state nonemptiness and a used drop of at least seven. At the same actual index, phase persistence and validity propagation give the original valid nine state, and the new closed-path result gives its literal normalization. If its actual clock were one, the local clock-one theorem and the unchanged count formula would force the additional-strip count to zero. The exact natural ledger would then say the center length increases by one, contradicting the selected drop. The actual bit bound therefore forces clock zero. The natural ledger and selected drop force at least one additional strip, hence the center drops by at least eight.

`quotient_path_nines_centers_le_eight_no_return` bounds only used source-center lengths by eight. A hypothetical full return supplies the drop-eight event and a nonempty next center, including when the next index is the endpoint N. The source length must then be at least nine, contradicting that bound. The final theorem assumes no initial normalization, nonempty center, supplied safety, freely assigned carry, or global descent condition.

No semantic gap was found in these five public interfaces. The result is a necessary existential excursion and precisely the cap-eight exclusion. It does not assert monotonic decrease at every step, a general nine no-return theorem, a qualifying cycle, a positive ordinary seed, or a conclusion about 196.

## Actual verification

The exact minimal import closure contains 32 modules. Each published source was copied to the new empty directory `/workspace/p196-agent1-session-20261016/nine-clock-strip-review-build-001` outside the Git worktree. No project objects were reused. The independent `clean-001` run passed all 32 source compilations and one full-origin audit, 33 commands total. No reviewer Lean command failed, timed out or was interrupted. The preserved author failures, including ClockStrip's intermediate helper-only checkpoint and SharpExcursion's failed first attempt, retain their actual outcomes and are not relabeled by this fresh review.

Official Lean 4.19.0 binary SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023` used `--trust=0 -j1 -DElab.async=false`, an 8 GiB address-space cap, and a 600-second per-command timeout. Executed sources, commands, logs, timestamps, tool identity, limits and exact helper bytes are retained. No mathematical source, registry or Git state was written by this reviewer.

The complete module-origin audit checked {v['theorems_audited']} theorem constants and {v['safe_definitions_audited']} safe definitions. The theorem axiom union is exactly `{', '.join(v['axiom_union'])}`; safe-definition union is `{', '.join(v['safe_definition_axiom_union'])}`. Only the standard foundational axioms are accepted. The three new modules contribute 30 theorem constants: ClockStrip 16, CenterNormalPath 5, SharpExcursion 9. They add no safe definition, runtime definition, or custom axiom. All five public theorem types and literal axiom outputs appear in `clean-001/ReviewAudit.log`. All {len(v['audited_named_exports'])} top-level public Agent1 theorems in the closure were also type-checked.

The separate inherited runtime inventory records {inv['nonsafe_count']} generated non-safe definitions: {inv['cstage_helpers']} compilation-stage helpers and {inv['unsafe_rec_helpers']} recursion helpers with audited safe bases. It records {len(inv['unsafe_axioms'])} inherited compiler implementation axioms, no unsafe opaque and no unclassified runtime definition. None is accepted as a theorem/safe-definition axiom dependency. Every source passed the comment/string-aware scan rejecting sorry, admit, native_decide, sorryAx, custom source axiom declarations and Lean.ofReduceBool. This is acceptance of the pinned contribution closure, not repository-wide acceptance.

The exact registry, actual import closure, published source bytes, retained compiled-source snapshots, and log hashes were rechecked while sealing. Objects remain outside tracked evidence. The actual issue61 role check-in and GET readback are retained in coordination/. Formal PR review and final publication-head comparison are separate subsequent actions, not claimed by this execution seal.
'''
(p/'semantic-review.md').write_text(report)
(p/'README.md').write_text(f'''# Independent sharp-excursion review: PASS

Published source `{identity['source_commit']}`; registry SHA256 `{identity['registry_sha256']}`. Reviewer `center_review_resume` authored none of the mathematical modules and independently rebuilt the exact 32-module closure with official Lean 4.19.0, explicit trust zero, and no reused project objects. All 33 compile/audit commands passed. Full origin audit: {v['theorems_audited']} theorem constants and {v['safe_definitions_audited']} safe definitions. New modules: 30 theorem constants, five public theorems, no new definitions/runtime. Literal public types/axioms and separate inherited runtime inventory are retained.

Read `semantic-review.md`, `frozen-receipt.json`, and `clean-001/ReviewAudit.log`. Normalization is derived from the positive returned path; the actual clock-one local restriction strengthens the necessary drop to eight and excludes only the source-cap-eight class. No general no-return, cycle, positive seed or 196 result is claimed. Earlier author failures remain preserved separately.

Reproduce with `replay.py --source-root /workspace/p196-agent1-nine-clock-strip-20261017 --build-dir NEW_EMPTY_DIRECTORY_OUTSIDE_WORKTREE --evidence-dir NEW_EMPTY_EVIDENCE --lean /workspace/p196-tools/lean-4.19.0-linux/bin/lean --memory-mib 8192 --module-timeout-seconds 600`. Every run requires new directories. `pin_published.py` generated the immutable source identity. Earlier source-only/preparation artifacts retain their historical status. No math source, registry, or Git state was changed by this reviewer.
''')
receipt={'status':'INDEPENDENT_REVIEW_PASS','reviewer':v['reviewer'],'source_commit':identity['source_commit'],'registry_sha256':identity['registry_sha256'],'authored_any_math':False,'accepted_run':'clean-001','failed_or_interrupted_reviewer_lean_runs':[],'source_modules_rebuilt':32,'external_project_objects_reused':False,'trust':0,'all33_compilation_and_audit_commands_passed':True,'theorem_constants_audited':v['theorems_audited'],'safe_definitions_audited':v['safe_definitions_audited'],'new_module_theorem_constants_audited':30,'new_module_safe_definitions_audited':0,'new_module_runtime_definitions':0,'new_public_theorems':identity['new_module_theorems'],'new_public_definitions':identity['new_module_definitions'],'literal_public_axioms_printed':True,'theorem_axiom_union':v['axiom_union'],'safe_definition_axiom_union':v['safe_definition_axiom_union'],'new_safe_definitions_axiom_free':True,'semantic_findings':[],'compiler_implementation_inventory_separate':True,'source_bytes_equal_published_commit':True,'sources_unchanged_at_finish':True,'disposable_build_outside_git_worktree':True,'repository_wide_acceptance_claimed':False,'formal_pr_review_posted':False,'sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'review_evidence':{}}
for rel in ['.gitignore','source-identity.json','driver-preparation.json','semantic-review.md','clean-001/verification.json','clean-001/implementation-inventory.json','clean-001/ReviewAudit.log','new-module-origin-audit.json','README.md','replay.py','pin_published.py','seal_review.py','execution-receipt.json','console.log','prepublication-source-review.json']:
 receipt['review_evidence'][rel]=sha((p/rel).read_bytes())
(p/'frozen-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
files={str(f.relative_to(p)):{'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in sorted(p.rglob('*')) if f.is_file() and f.name!='FILES.json'}
assert not any(Path(x).suffix in ['.olean','.ilean','.o','.c'] for x in files)
(p/'FILES.json').write_text(json.dumps(files,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'receipt_sha256':sha((p/'frozen-receipt.json').read_bytes()),'review_files':len(files),'manifest_sha256':sha((p/'FILES.json').read_bytes()),'semantic_review_sha256':sha((p/'semantic-review.md').read_bytes()),'audit_log_sha256':sha((p/'clean-001/ReviewAudit.log').read_bytes()),'theorem_constants':v['theorems_audited'],'safe_definitions':v['safe_definitions_audited']},indent=2))
