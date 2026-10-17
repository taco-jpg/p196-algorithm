#!/usr/bin/env python3
"""Seal completed staged independent review; no Lean execution or source edits."""
from pathlib import Path
import hashlib,json,re,subprocess
p=Path(__file__).resolve().parent;root=p.parents[4];sha=lambda b:hashlib.sha256(b).hexdigest()
id=json.loads((p/'final-source-identity.json').read_text());v=json.loads((p/'final-002/verification.json').read_text());inv=json.loads((p/'final-002/implementation-inventory.json').read_text());log=(p/'final-002/ReviewAudit.log').read_text()
assert v['status']=='PASS' and v['source_modules']==31 and v['theorems_audited']==1699 and v['safe_definitions_audited']==248 and inv['status']=='PASS'
base=json.loads((p/'baseline-001/results.json').read_text());first=json.loads((p/'final-001/results.json').read_text());last=json.loads((p/'final-002/results.json').read_text())
assert len(base)==28 and all(x['exit_code']==0 for x in base)
assert len(first)==5 and all(x['exit_code']==0 for x in first[:4]) and first[-1]['exit_code']==1
assert len(last)==1 and last[0]['module']=='ReviewAudit' and last[0]['exit_code']==0
for e in id['sources']:
 b=(root/e['path']).read_bytes();assert sha(b)==e['sha256'] and b==subprocess.check_output(['git','show',id['source_commit']+':'+e['path']],cwd=root)
for rel,e in json.loads((p/'baseline-files.json').read_text()).items():
 b=(p/rel).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'],rel
new={}
for m in id['new_modules']:
 new[m]={}
 for label,token in [('theorems','AUDIT_THEOREM'),('safe_definitions','AUDIT_SAFE_DEFINITION')]:
  entries=re.findall(r'^'+token+' '+m+r' (\S+) : \[([^\]]*)\]',log,re.M)
  new[m][label]=[{'name':n,'axioms':[] if not ax else re.split(r'\s*,\s*',ax.strip())} for n,ax in entries]
 new[m]['compiler_runtime_definitions']=re.findall(r'^NONSAFE_DEFINITION '+m+r' (\S+)',log,re.M)
assert sum(len(x['theorems']) for x in new.values())==73 and sum(len(x['safe_definitions']) for x in new.values())==4
(p/'new-module-origin-audit.json').write_text(json.dumps({'status':'PASS','modules':new,'public_theorems':id['new_module_theorems'],'public_definitions':id['new_module_definitions'],'public_types_checked_in':'final-002/ReviewAudit.log','runtime_inventory_separate':True},indent=2)+'\n')
semantic='''# Independent semantic and staged fresh-build review

PASS at published source commit `1c65552f079e1ce4061c69be5488573c59e5a207`, registry SHA256 `a425319d71d007104942a2a7010d985ef6fd3f82bb645d75cc8913fb73fe1718`. Reviewer: Agent #1 specialist `symbolic_scope`, nonauthor of all four new modules. Some frozen dependencies have prior reviewer authorship; the entire dependency closure was nevertheless rebuilt from source in this review.

## Exact result and interpretation

The checked public endpoint is exactly:

```lean
quotient_path_eighteen_no_return
  (B H w : Nat → Agent8.Word) (N : Nat)
  (hp : QuotientPath B H w N)
  (hv : ValidPeriodic (B 0) (H 0) (w 0))
  (hw : w 0 = [18,18,18,18]) (hN : 0 < N) :
  ¬ (B N = B 0 ∧ H N = H 0 ∧ w N = w 0)
```

No extra safety, nonempty exterior/center, phase-catalog membership, or chosen-clock assumption is hidden in this type. Positivity of N matters: a zero-length path returns trivially. The theorem excludes the complete literal quotient tuple return, not an abstract phase/width graph edge or a single repeated coefficient. It asserts neither whole-population extinction nor a result for an ordinary numeric seed or 196. A downstream reduction of the retained component set is a separate package.

## All eight public interfaces

`periodic_eighteen_band_run` constructs one maximal run covering the entire nonempty left eighteen band. It uses only the literal word and positive exponent, not original validity. Its private least-natural-number helper selects the least permitted left boundary and the first right obstruction or physical end. The proof explicitly bounds the right endpoint by the whole word length. The result allows the run to extend into B, through H, across both bands, and up to the physical end. Empty B/H and all-eighteen B/H remain included.

`periodic_eighteen_band_left_eq` compares two maximal runs meeting one shared position in the two left bands. It uses equality of the prefix up to that position, then each run's left maximality condition. It does not assume the runs start at B.length, does not require the centers to agree, and does not assert the proposed suffix-length formula from the scout. Its band inequalities themselves force positive band lengths. This direct comparison is sufficient for the final contradiction and avoids a generic maximal-interval API.

`quotientEighteenTrack` is the literal recursive descendant of one supplied initial run. `quotient_eighteen_track` retains that same ancestry. Its endpoint estimates show the left endpoint advances by at most one and the right endpoint retreats by at most one per step; the actual carry contributes a lower bound on left advance. The fixed anchor and its N-position margins prove the descendant nonempty before invoking the unchanged original `RunAncestry.descendant_step` maximality result. Original admissibility comes from propagated `ValidPeriodic` and the positive guarded exponent at every used source. Neither population coverage nor an assumption that every intermediate period is eighteen is used. N=0 is retained in this helper.

The private stepWord transport uses only the existing in-range list/index bridge. Run positions and the predecessor are inside the next width; the right boundary uses equality only when it lies strictly below that width and otherwise retains the endpoint disjunction. It never asserts global function equality. This addresses the source-review warning that list getD and original nextColumns can differ outside the physical width (for example at index2 after W=[18]). Whole-word maximality is supplied by the original theorem, not inferred from matching values inside the old interval alone.

`periodicWord_carry_eq_rawGamma` rewrites the actual indexed carry through the existing list-carry bridge, then uses stable carry at positive exponents. `quotient_path_actual_carry_step` and `quotient_path_actual_carry_sum` retain every source index and the literal actual cumulative recurrence, including horizon zero. No arbitrary abstract clock bit is substituted. The main endpoint uses the step adapter directly with C=quotientClockSum.

`quotient_path_eighteen_no_return` begins with the inherited finite schedule k0=2*N+3. Every source guard is proved before applying literal word updates or converting natural subtraction into signed accounting. Under the assumed full return, the existing return-clock theorem supplies a positive natural G, total actual clock 8*G, and signed gain G. Guarded accounting gives kN=k0+G. The chosen anchor |B0|+N remains inside the tracked descendant throughout the path because the initial band has 4*k0 positions. At N it is also inside the final left band. Full B/H/w return permits the static left-boundary comparison even though kN differs from k0 and the full words need not be equal. The same descendant's left boundary is forced both to equal the initial boundary and to exceed it by the positive actual clock, giving the contradiction. No ancestry is silently replaced by a newly born run.

No semantic finding remains at the final source hashes. The proof uses the original admissibility, carry, maximality and quotient definitions unchanged. The private existence helper is a least-natural witness; there is no generic run population partition, unique founder theorem, or all-run disappearance claim.

## Exact staged execution and retained failure

The independent review first compiled 27 pinned existing modules from published baseline `7f23ce839fcc88acb235b1816c2c57dc12e16a33` into an empty build directory. All 27 compiles and the baseline audit passed. This includes original RunAncestry, with all 140 of its theorem constants and three safe definitions audited. After final publication, every baseline source byte and object hash was checked; the four frozen new modules were then compiled into that same review build. No author or external project objects were imported. This is a staged fresh closure, not a claim that all 31 modules were compiled in one command or at one time.

All four new-module compilation commands passed. The first full audit attempt, `final-001`, failed only because the reviewer driver's unmasked public-declaration regex read a documentation line beginning `theorem through` as an identifier. The original generated audit, full error log, exact driver, and sources remain intact. The fix applies the existing nested-comment/string masker to all declaration discovery. A control checks real declarations versus documentation. The only repeated Lean execution was the full audit in `final-002`, after revalidating all 31 original object/source pins. It passed. No mathematical source was edited and no failed command was relabeled successful.

Commands use official Lean 4.19.0, binary SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`, explicit `--trust=0 -j1 -DElab.async=false`, an 8 GiB address-space cap per command and a 600-second timeout. Raw inputs, argv, resource limits and output logs are retained in all three stage directories.

## Full audit and compiler inventory

The accepted complete origin audit covers 1,699 theorem constants and 248 safe definitions. The theorem axiom union is exactly `propext`, `Classical.choice`, and `Quot.sound`; safe definitions use only `propext`. The new four modules contribute 73 theorem constants and four safe definitions: Band26/0, Track27/4, Clock6/0, Return14/0. The larger origin count includes private/generated proof constants and differs from the seven public theorems and one public definition. All eight public types are checked exactly; the audit additionally checks all 121 top-level public Agent1 theorems in this closure.

The separate compiler inventory contains 980 generated non-safe runtime definitions: 948 compilation-stage helpers and 32 unsafe-recursion helpers with audited safe bases. Thirteen compiler implementation axioms are inherited from LychrelDigitSums. There are no unsafe opaques or unclassified runtime entries. The four new modules contribute eight generated runtime helpers, all from Track. None of these implementation entries occurs in the accepted theorem/safe-definition axiom dependencies.

## Parent evidence provenance

The parent's separate fresh31 run passed 32 commands and audited 1,699 theorem constants. Its original report recorded HEAD `7208d7314afe8391db964980f094374c866f9114`, when Band, Return, and the final registry were still untracked. That commit alone does not contain the full built package. Its `source_tree_clean=true` used `git status --porcelain --untracked-files=no` and must not be read as all build inputs already committed. Its argv contains no explicit trust override. These original values are retained unchanged.

The parent addendum, independently checked here, establishes that all 31 executed source snapshots and the registry equal published `1c65552f079e1ce4061c69be5488573c59e5a207` byte-for-byte. All 65 original manifest files and the 69-file package manifest were independently validated. This review's own final-stage pin and explicit trust-zero execution are bound to the published commit. No repository-wide acceptance is claimed.
'''
(p/'semantic-review.md').write_text(semantic)
readme='''# Independent eighteen-return review: PASS

Reviewed published sources `1c65552f079e1ce4061c69be5488573c59e5a207`; project `agent1-periodic-eighteen-return`, root `Agent1PeriodicEighteenReturn`. The reviewer authored none of the four new modules; prior frozen dependency authorship is disclosed.

The fresh closure was staged: 27 pinned dependencies in `baseline-001`, then four frozen new modules in `final-001`, all compiled successfully. No external project objects were reused. The first final audit failed on a documentation line misread by the reviewer declaration scanner. The exact failed driver/audit/logs are preserved. After masking comments and strings consistently, an audit-only retry `final-002` passed on the same hash-pinned fresh objects. This is not a single-command rebuild claim.

Full audit: 1,699 theorem constants and 248 safe definitions, standard-three theorem axioms only. New modules: 73 theorem constants, four safe definitions, seven public theorems and one public definition. All eight public types are checked. Runtime/compiler implementation inventory is separate. Read `semantic-review.md` for the proof interpretation, endpoint cases, and exact parent provenance caveat.

`baseline-README.md`, `baseline-files.json`, and all stage directories are immutable historical evidence. `baseline-objects.json` and `compiled-frozen-objects.json` record the original generated object hashes; `.olean` files themselves are disposable and excluded from the source-only manifest. All exact Lean source bytes and logs are retained.

For a new replay, run `baseline_replay.py` into new empty directories using its recorded baseline identity. Generate a new object receipt for that new build, then use corrected `append_frozen.py` without `--resume-compiled` to compile the four new modules and run the full audit. The optional resume mode exists solely to replay the preserved audit-only correction against the recorded original objects. Both drivers expose source/build/evidence/compiler arguments and refuse unpinned preexisting new-module objects. `pin_published.py` independently verifies final publication, import closure, and public endpoint inventory.

Official Lean4.19.0 commands use `--trust=0 -j1 -DElab.async=false`. The parent’s separately preserved checker commands do not add explicit trust zero; its earlier recorded HEAD and tracked-only clean flag remain unchanged, with a separate byte-identity addendum to the published sources. No proof sources were changed during review.
'''
(p/'README.md').write_text(readme)
parent=json.loads((p/'parent-package-validation.json').read_text());assert parent['status']=='PARENT_PACKAGE_INDEPENDENT_VALIDATION_PASS'
receipt={'status':'INDEPENDENT_REVIEW_PASS','source_commit':id['source_commit'],'registry_sha256':id['registry_sha256'],'reviewer':'Agent #1 specialist symbolic_scope','authored_new_modules':False,'prior_frozen_dependency_authorship_disclosed':True,'staged_fresh_closure':True,'baseline_modules':27,'frozen_appended_modules':4,'external_project_objects_reused':False,'accepted_full_audit':'final-002','failed_audit_preserved':'final-001','failure_was_reviewer_declaration_scanner':True,'source_compilation_failures':[],'all31_source_compilation_commands_passed':True,'trust':0,'theorem_constants_audited':1699,'safe_definitions_audited':248,'new_module_theorem_constants_audited':73,'new_module_safe_definitions_audited':4,'new_public_theorems':id['new_module_theorems'],'new_public_definitions':id['new_module_definitions'],'theorem_axiom_union':v['axiom_union'],'safe_definition_axiom_union':v['safe_definition_axiom_union'],'semantic_findings':[],'compiler_implementation_inventory_separate':True,'source_bytes_equal_published_commit':True,'sources_unchanged_at_finish':True,'parent_original_recorded_source_commit':parent['original_parent_recorded_commit'],'parent_tracked_only_source_tree_clean_original':True,'parent_actual_snapshots_equal_published_commit':True,'parent_explicit_trust_override':False,'parent_package_manifest_sha256':parent['package_manifest_sha256'],'review_evidence':{},'repository_wide_acceptance_claimed':False}
for rel in ['final-source-identity.json','semantic-review.md','baseline-files.json','baseline-objects.json','compiled-frozen-objects.json','declaration-scanner-correction.json','final-001/ReviewAudit.log','final-002/verification.json','final-002/implementation-inventory.json','final-002/ReviewAudit.log','new-module-origin-audit.json','parent-package-validation.json','README.md','baseline_replay.py','append_frozen.py','pin_published.py','seal_review.py']:
 receipt['review_evidence'][rel]=sha((p/rel).read_bytes())
(p/'frozen-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
files={str(f.relative_to(p)):{'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in sorted(p.rglob('*')) if f.is_file() and f.name!='FILES.json' and not any(x.startswith('fresh-build-') for x in f.relative_to(p).parts)}
(p/'FILES.json').write_text(json.dumps(files,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'receipt_sha256':sha((p/'frozen-receipt.json').read_bytes()),'review_files':len(files),'manifest_sha256':sha((p/'FILES.json').read_bytes()),'semantic_review_sha256':sha((p/'semantic-review.md').read_bytes()),'math_sources_changed':False},indent=2))
