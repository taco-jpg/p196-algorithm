#!/usr/bin/env python3
"""Seal actual fresh excursion review after successful source-pinned execution."""
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
assert v['status']=='PASS' and inv['status']=='PASS' and v['source_modules']==29
assert execution['exit_code']==0 and len(results)==30 and all(r['exit_code']==0 and not r['timed_out'] for r in results)
assert v['reviewer']=='Agent #1 specialist center_review_resume'
assert len(identity['new_module_theorems'])==4 and len(identity['new_module_definitions'])==2
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
assert len(new['Agent1PeriodicNinesLedger']['theorems'])==11
assert len(new['Agent1PeriodicNinesLedger']['safe_definitions'])==5
assert len(new['Agent1PeriodicNinesLedger']['runtime_definitions'])==13
assert len(new['Agent1PeriodicNinesExcursion']['theorems'])==15
assert not new['Agent1PeriodicNinesExcursion']['safe_definitions'] and not new['Agent1PeriodicNinesExcursion']['runtime_definitions']
for name in identity['new_module_exports']:
 assert f"'{name}' depends on axioms:" in log or f"'{name}' does not depend on any axioms" in log
assert set(v['axiom_union'])=={'propext','Classical.choice','Quot.sound'}
assert set(v['safe_definition_axiom_union']) <= {'propext','Classical.choice','Quot.sound'}
for filename in ['new-module-origin-audit.json','semantic-review.md','README.md','frozen-receipt.json','FILES.json']:
 assert not (p/filename).exists(),'Do not overwrite sealed evidence: '+filename
(p/'new-module-origin-audit.json').write_text(json.dumps({'status':'PASS','reviewer':v['reviewer'],'modules':new,'public_theorems':identity['new_module_theorems'],'public_definitions':identity['new_module_definitions'],'literal_public_axioms_and_types':'clean-001/ReviewAudit.log','runtime_inventory_separate':True},indent=2)+'\n')
report=f'''# Independent nine-excursion review

PASS for published source `{identity['source_commit']}`, registry SHA256 `{identity['registry_sha256']}`. Reviewer: Agent #1 specialist `center_review_resume`. I authored none of the new or inherited math modules. I performed this actual fresh execution and semantic review. The two new source hashes match both the earlier source-only snapshots and the frozen published bytes; the preparation artifacts remain explicitly labeled as unexecuted at their original stage. The replay helper was adapted from my completed center review, with exact prior and current helper hashes in `driver-preparation.json`. Earlier PR173 evidence and formal review remain separate.

## Exact statements and argument

Let W9=[9,9,9,9]. `ninesExtraStrips B H` is the original maximal-strip count for the paired fixed center digits plus the actual whole-word clock pad: pair(fixedDigits H (leftEntry B) ++ replicate (rawGamma B H W9) (9*leftEntry B)). No extra removal is discarded. `ninesExtraSum B H N` is the natural sum over exactly source indices i<N, defined recursively with zero base. Both definitions preserve computed entries and clock; neither introduces an independent bit trajectory.

`quotientCenter_nines_length_balance` assumes only the original coefficient bounds on B/H and actual mixed entry sum one. It proves the natural identity length(quotientCenter B H W9)+8*ninesExtraStrips B H=length(H)+rawGamma B H W9. The proof uses the literal residual formula and original strip length identity. Pairing preserves the digit-word length here; the actual pad contributes exactly the actual clock. All arithmetic is exact, with no signed or truncated count substituted.

`quotient_path_nines_center_balance` assumes an original bounded exact QuotientPath and initial/final nine phases. It yields length(H N)+8*ninesExtraSum B H N=length(H 0)+quotientClockSum B H w N. Its zero-length case is retained. The inductive step derives the actual intermediate nine phase and mixed-entry equality, uses the original next-center equality, and rewrites the actual clock contribution of that step. Neither full validity nor full center/exterior return nor positive clock is assumed at this ledger layer.

`quotient_return_nines_center_excursion` retains original QuotientPath, original initial ValidPeriodic, initial W9, positive N, and full B/H/w endpoint equality. Every used source has actual mixed entries. If a source center were empty, rightEntry_nines would make its outgoing entry equal its incoming entry, contradicting their sum one. The endpoint center is nonempty by H N=H 0 and N>0. Thus all states through N are covered, without a new nonempty premise.

The full center return and exact ledger identify total clock with eight times the natural additional-strip sum. Existing `quotient_return_clock_gain`, with its original validity and full return assumptions unchanged, supplies a positive clock gain. This forces a positive extra-strip sum; finite natural-sum induction selects an actual index i<N with at least one extra pair. The local ledger and actual rawGamma<=1 then give length(H(i+1))+7<=length(H i). The theorem states existence of a decreasing transition; it makes no claim that all transitions decrease or that center length is monotone.

`quotient_path_nines_small_centers_no_return` assumes only that every used source center has length at most seven. A hypothetical full return supplies the excursion. The next center is nonempty, including when i+1=N. Hence the drop inequality forces source length at least eight, contradicting the source cap. No cap on unused states or extra endpoint assumption is introduced. Positive N, original full validity, exact tuple return, and actual carry/clock semantics are all essential inputs to the invoked statements and are retained.

No semantic finding was identified. There is no initial maximal-normalization premise, supplied safety premise, hidden nonempty premise, independently chosen carry, or generic center-descent assumption. This proves a necessary excursion condition and the precise source-cap-seven exclusion only. It does not exclude arbitrary full nine returns, construct a cycle or positive ordinary seed, claim a result about 196, or depend on the separate local sharpness investigation. That investigation and the extra-strip control are not new roots of this exact closure.

## Actual strict verification and evidence

The exact minimal closure has 29 source modules. Each was copied from the pinned publication to the new empty directory `/workspace/p196-agent1-session-20261016/nine-excursion-review-build-001`, outside the Git worktree. No project objects were reused. The single reviewer run `clean-001` passed all 29 source compilations and the full-origin audit, 30 commands total. No reviewer Lean command failed, timed out, or was interrupted. Author increments and any separate parent run retain their own execution semantics and are not relabeled as this independent fresh run.

Official Lean 4.19.0 binary SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023` ran with `--trust=0 -j1 -DElab.async=false`, an 8 GiB address-space cap, and a 600-second timeout for each command. Commands, execution timestamps, sources, logs, resource settings, and exact helper bytes are retained. No mathematical source or registry was changed by this reviewer.

The full module-origin audit checked {v['theorems_audited']} theorem constants and {v['safe_definitions_audited']} safe definitions. The theorem axiom union is exactly `{', '.join(v['axiom_union'])}`; safe-definition union is `{', '.join(v['safe_definition_axiom_union'])}`. Only the standard foundational axioms are permitted. The two new modules contribute 26 theorem constants (Ledger 11; Excursion 15), five safe definitions, and 13 generated Ledger runtime definitions. Every new safe definition is axiom-free. All six public interfaces (four theorems and two definitions) have literal type and axiom output in `clean-001/ReviewAudit.log`. All {len(v['audited_named_exports'])} top-level public Agent1 theorems in the closure were also type-checked.

The separate runtime inventory records {inv['nonsafe_count']} non-safe generated definitions: {inv['cstage_helpers']} compilation-stage helpers and {inv['unsafe_rec_helpers']} recursion helpers with individually audited safe bases. It records {len(inv['unsafe_axioms'])} inherited compiler implementation axioms, no unsafe opaque, and no unclassified runtime definition. No runtime implementation entry is accepted as a theorem or safe-definition axiom dependency. The comment/string-aware scan of every source rejects sorry, admit, native_decide, sorryAx, custom source axiom declarations, and Lean.ofReduceBool. This is a review of the pinned contribution closure, not repository-wide acceptance.

The registry, actual import closure, published source bytes, retained compiled-source snapshots, and all log hashes were rechecked while sealing. Objects remain outside tracked evidence. The accepted issue61 check-in and GET readback are preserved in `coordination/`. A formal PR review is separate and is not claimed by this prepublication evidence seal.
'''
assert all(not e['axioms'] for e in new['Agent1PeriodicNinesLedger']['safe_definitions'])
(p/'semantic-review.md').write_text(report)
(p/'README.md').write_text(f'''# Independent nine-excursion review: PASS

Published source `{identity['source_commit']}`; registry SHA256 `{identity['registry_sha256']}`. Reviewer `center_review_resume` authored none of the mathematical modules and independently rebuilt the exact 29-module closure with official Lean 4.19.0, explicit trust zero, and no reused project objects. All 30 compile/audit commands passed. Full origin audit: {v['theorems_audited']} theorem constants, {v['safe_definitions_audited']} safe definitions. New modules: 26 theorem constants, five safe definitions, four public theorems and two public definitions. Literal public types/axioms and separate runtime inventory are retained.

See `semantic-review.md`, `frozen-receipt.json`, and `clean-001/ReviewAudit.log`. This establishes an actual additional-strip ledger, a necessary at-least-seven center drop on a positive original-valid full nine return, and the restricted source-cap-seven no-return consequence. It establishes no general nonreturn, cycle, positive seed, or result about 196.

To reproduce, run `replay.py --source-root /workspace/p196-agent1-nine-excursion-20261017 --build-dir NEW_EMPTY_DIRECTORY_OUTSIDE_WORKTREE --evidence-dir NEW_EMPTY_EVIDENCE --lean /workspace/p196-tools/lean-4.19.0-linux/bin/lean --memory-mib 8192 --module-timeout-seconds 600`. Every run requires new directories. `pin_published.py` generated the immutable source identity. Source-only preflight and preparation records retain their historical status. No math source, registry, or Git state was written by this reviewer.
''')
receipt={'status':'INDEPENDENT_REVIEW_PASS','reviewer':v['reviewer'],'source_commit':identity['source_commit'],'registry_sha256':identity['registry_sha256'],'authored_any_math':False,'accepted_run':'clean-001','failed_or_interrupted_reviewer_lean_runs':[],'source_modules_rebuilt':29,'external_project_objects_reused':False,'trust':0,'all30_compilation_and_audit_commands_passed':True,'theorem_constants_audited':v['theorems_audited'],'safe_definitions_audited':v['safe_definitions_audited'],'new_module_theorem_constants_audited':26,'new_module_safe_definitions_audited':5,'new_module_runtime_definitions':13,'new_public_theorems':identity['new_module_theorems'],'new_public_definitions':identity['new_module_definitions'],'literal_public_axioms_printed':True,'theorem_axiom_union':v['axiom_union'],'safe_definition_axiom_union':v['safe_definition_axiom_union'],'new_safe_definitions_axiom_free':True,'semantic_findings':[],'compiler_implementation_inventory_separate':True,'source_bytes_equal_published_commit':True,'sources_unchanged_at_finish':True,'disposable_build_outside_git_worktree':True,'repository_wide_acceptance_claimed':False,'formal_pr_review_posted':False,'sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'review_evidence':{}}
for rel in ['.gitignore','source-identity.json','driver-preparation.json','semantic-review.md','clean-001/verification.json','clean-001/implementation-inventory.json','clean-001/ReviewAudit.log','new-module-origin-audit.json','README.md','replay.py','pin_published.py','seal_review.py','execution-receipt.json','console.log','prepublication-source-review.json','scope-preflight.md']:
 receipt['review_evidence'][rel]=sha((p/rel).read_bytes())
(p/'frozen-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
files={str(f.relative_to(p)):{'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in sorted(p.rglob('*')) if f.is_file() and f.name!='FILES.json'}
assert not any(Path(x).suffix in ['.olean','.ilean','.o','.c'] for x in files)
(p/'FILES.json').write_text(json.dumps(files,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'receipt_sha256':sha((p/'frozen-receipt.json').read_bytes()),'review_files':len(files),'manifest_sha256':sha((p/'FILES.json').read_bytes()),'semantic_review_sha256':sha((p/'semantic-review.md').read_bytes()),'audit_log_sha256':sha((p/'clean-001/ReviewAudit.log').read_bytes()),'theorem_constants':v['theorems_audited'],'safe_definitions':v['safe_definitions_audited']},indent=2))
