#!/usr/bin/env python3
"""Seal exact completed Nine review evidence; no Lean execution or math edits."""
from pathlib import Path
import hashlib,json,re,subprocess
p=Path(__file__).resolve().parent;root=p.parents[4];sha=lambda b:hashlib.sha256(b).hexdigest()
identity=json.loads((p/'final-source-identity.json').read_text());v=json.loads((p/'clean-001/verification.json').read_text());r=json.loads((p/'clean-001/results.json').read_text());inv=json.loads((p/'clean-001/implementation-inventory.json').read_text());log=(p/'clean-001/ReviewAudit.log').read_text()
assert v['status']=='PASS' and inv['status']=='PASS'
assert v['source_modules']==34 and len(r)==35 and all(x['exit_code']==0 for x in r)
assert len(identity['new_module_theorems'])==5 and not identity['new_module_definitions']
for e in identity['sources']:
 b=(root/e['path']).read_bytes();assert sha(b)==e['sha256'] and b==subprocess.check_output(['git','show',identity['source_commit']+':'+e['path']],cwd=root)
new={}
for m in identity['new_modules']:
 new[m]={}
 for label,token in [('theorems','AUDIT_THEOREM'),('safe_definitions','AUDIT_SAFE_DEFINITION')]:
  entries=re.findall(r'^'+token+' '+m+r' (\S+) : \[([^\]]*)\]',log,re.M)
  new[m][label]=[{'name':n,'axioms':[] if not ax else re.split(r'\s*,\s*',ax.strip())} for n,ax in entries]
 new[m]['compiler_runtime_definitions']=re.findall(r'^NONSAFE_DEFINITION '+m+r' (\S+)',log,re.M)
assert len(new['Agent1PeriodicNinesPath']['theorems'])==16
assert len(new['Agent1PeriodicNinesCycle']['theorems'])==7
assert not any(x['safe_definitions'] or x['compiler_runtime_definitions'] for x in new.values())
(p/'new-module-origin-audit.json').write_text(json.dumps({'status':'PASS','modules':new,'public_theorems':identity['new_module_theorems'],'public_definitions':[],'public_types_checked_in':'clean-001/ReviewAudit.log','runtime_inventory_separate':True},indent=2)+'\n')
report=f'''# Independent semantic and fresh-build review

PASS at published source `{identity['source_commit']}`, registry SHA256 `{identity['registry_sha256']}`. Reviewer Agent #1 specialist `symbolic_scope` authored neither new module. Some frozen dependencies have prior reviewer authorship; the entire dependency closure was rebuilt afresh. No new mathematical source or registry was modified during review.

## Exact five public interfaces

`quotient_path_nines_phase` takes the unchanged literal `QuotientPath B H w N` and only the initial and final period equalities to `[9,9,9,9]`. It concludes that every period at i≤N is four nines. It includes N=0. It has no original-validity, positive-length, complete-tuple return, safety, exponent, or catalog premise. The two private phase facts retain the actual arithmetic: the nine update has only zero, nine, or eighteen outputs because the computed left/right entries are bits, and eighteen absorption specializes the original phaseImage formula with the actual bounded rawGamma. Zero absorption is reused unchanged. Forward trichotomy and backward endpoint exclusion use coefficient bounds only at used sources i<N. No path premise is applied at the terminal index.

`quotient_path_nines_entry_sum` retains those same phase-return hypotheses and i<N. It concludes that the two original actual entry scans sum to one. This does not assign independent bits or equate their sum with the complete-word rawGamma. Unconditional nine persistence is not claimed: original-valid tuples can leave nine for zero or eighteen in one step, but a phase path doing so cannot return to nine.

`periodic_nines_input_nonpalindrome` assumes k>0, the original `DecimalDigits.Canonical` representation at the exact periodic-word length, and full in-range `columnSum` equality. It extracts a real in-range coefficient nine using positive repetition. Original `palindrome_value_iff` makes reflected canonical digits equal under the palindrome assumption; their pair sum would be twice a natural digit and cannot equal nine. The helper therefore excludes a palindrome at the represented input, including time zero. Canonical preserves bounded digits, positive leading digit, and exact value. No separate validity, exterior nonemptiness, arbitrary extension of columns outside the width, or stronger adjacent-high-coefficient premise is inserted.

`quotient_cycle_nines_safe` takes a positive-length exact quotient path, original initial validity, initial period nine, and full literal B/H/w return. It derives the original Boolean safety test at every used finite state, without a separate safety hypothesis. It first obtains one original same-seed all-time realization and then uses the successor residue `(i+1)%N` to prove the next integer nonpalindromic. At the final edge this residue is zero; positive N makes the modulus bound valid. Applying `safePeriodic_iff_next_not_palindrome` at i is therefore correctly timed. An arbitrary current nine state is not asserted to be automatically safe. The supplied path's three updates and the full return remain explicit; a phase-only or projected graph loop would not suffice.

`quotient_cycle_nines_positive_seed` has exactly the same full-cycle hypotheses and concludes `∃ n, 0<n ∧ Lychrel196.IsLychrel n`. It supplies the derived finite safety premise to the inherited conditional cycle criterion. That original criterion chooses a single seed before all time indices and returns its positive successor, so IsLychrel includes time zero correctly via `orbit_from_step`. No horizon-dependent witnesses are exchanged for one all-time witness. The package constructs no qualifying cycle, proves no unconditional decimal existence theorem, supplies no nine-center obstruction or generic nine-run ancestry theorem, and concludes nothing about 196.

No source-level semantic finding remains at the final frozen hashes. The two new source files are exactly the previously inspected final author snapshots and the published Git bytes.

## Fresh execution and complete origin audit

The literal import closure is exactly34 modules. All 34 were copied from the published commit into a new empty build directory and compiled with official Lean 4.19.0, compiler SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`, explicit `--trust=0 -j1 -DElab.async=false`, an 8 GiB per-process address-space cap and a 600-second per-command timeout. No author or other project objects were reused. All 35 commands, including the complete origin audit, passed in reviewer attempt `clean-001`. No failed or interrupted reviewer Lean command occurred. Exact argv, source snapshots, logs, timing, and compiler bytes are retained. Author attempts remain separately preserved in their owned directories; this statement does not relabel those earlier attempts.

The complete audit covers {v['theorems_audited']} theorem constants and {v['safe_definitions_audited']} safe definitions. The theorem axiom union is `{', '.join(v['axiom_union'])}`; safe-definition union is `{', '.join(v['safe_definition_axiom_union'])}`. Only the standard three axioms are permitted. The two new modules contribute 23 theorem constants (Path 16, Cycle 7), no safe definitions, and no runtime compiler definitions. All five public theorem types are checked exactly. The larger origin count includes private/generated proof constants; the full audit additionally checks {len(v['audited_named_exports'])} top-level public Agent1 theorem declarations in the closure.

The separate compiler inventory records {inv['nonsafe_count']} generated non-safe definitions: {inv['cstage_helpers']} compilation-stage helpers and {inv['unsafe_rec_helpers']} unsafe-recursion helpers whose safe bases were all audited. It records {len(inv['unsafe_axioms'])} inherited compiler implementation axioms, zero unsafe opaques and no unclassified runtime definitions. These implementation entries do not appear among accepted theorem/safe-definition axiom dependencies. All declaration scans mask nested comments and strings; the historical documentation false-positive from another package is covered by the preparation controls and did not recur here.

This review establishes the exact pinned dependency closure, not repository-wide acceptance or existence of a full cycle. Any separate parent checker run and its historical flags are distinct evidence.
'''
(p/'semantic-review.md').write_text(report)
(p/'README.md').write_text(f'''# Independent nine-cycle review: PASS

Published source `{identity['source_commit']}`; exact 34-module root `Agent1PeriodicNinesCycle`, project `agent1-periodic-nine-cycle`. The reviewer authored neither new module and discloses earlier frozen dependency authorship.

`clean-001` is the sole reviewer execution attempt: 34 source compiles and the full origin audit all passed. No project objects were reused. Explicit trust zero is used. Complete audit: {v['theorems_audited']} theorem constants and {v['safe_definitions_audited']} safe definitions; new modules 23 theorem constants, five public theorems, no definitions. Standard-three theorem dependencies only. Runtime inventory is separate. See `semantic-review.md` for all public interfaces, input/output safety timing, N=0 persistence, and full-cycle conditions.

To reproduce, run `replay.py --source-root /workspace/p196-agent1-nine-cycle-20261017 --build-dir NEW_EMPTY_BUILD --evidence-dir NEW_EMPTY_EVIDENCE --lean /workspace/p196-tools/lean-4.19.0-linux/bin/lean`. The driver refuses existing output directories and compares each source to the published identity. `pin_published.py` independently checks source bytes, Git blobs, imports, closure and public endpoint registration. Nested comments and strings are masked before every declaration scan and auxiliary token scan.

All executed sources and logs are retained. The source-only manifest excludes disposable fresh-build objects. Prepublication reports and driver preparation records remain historical; this README and the frozen receipt record the final result. Mathematical sources and registry were not changed. No actual cycle or result for 196 is supplied.
''')
receipt={'status':'INDEPENDENT_REVIEW_PASS','source_commit':identity['source_commit'],'registry_sha256':identity['registry_sha256'],'reviewer':'Agent #1 specialist symbolic_scope','authored_new_modules':False,'prior_frozen_dependency_authorship_disclosed':True,'accepted_run':'clean-001','failed_or_interrupted_reviewer_lean_runs':[],'source_modules_rebuilt':34,'external_project_objects_reused':False,'trust':0,'all35_compilation_and_audit_commands_passed':True,'theorem_constants_audited':v['theorems_audited'],'safe_definitions_audited':v['safe_definitions_audited'],'new_module_theorem_constants_audited':23,'new_module_safe_definitions_audited':0,'new_public_theorems':identity['new_module_theorems'],'new_public_definitions':[],'theorem_axiom_union':v['axiom_union'],'safe_definition_axiom_union':v['safe_definition_axiom_union'],'semantic_findings':[],'compiler_implementation_inventory_separate':True,'source_bytes_equal_published_commit':True,'sources_unchanged_at_finish':True,'repository_wide_acceptance_claimed':False,'review_evidence':{}}
for rel in ['final-source-identity.json','semantic-review.md','clean-001/verification.json','clean-001/implementation-inventory.json','clean-001/ReviewAudit.log','new-module-origin-audit.json','README.md','replay.py','pin_published.py','seal_review.py']:
 receipt['review_evidence'][rel]=sha((p/rel).read_bytes())
(p/'frozen-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
files={str(f.relative_to(p)):{'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in sorted(p.rglob('*')) if f.is_file() and f.name!='FILES.json' and not any(x.startswith('fresh-build-') for x in f.relative_to(p).parts)}
(p/'FILES.json').write_text(json.dumps(files,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'receipt_sha256':sha((p/'frozen-receipt.json').read_bytes()),'review_files':len(files),'manifest_sha256':sha((p/'FILES.json').read_bytes()),'semantic_review_sha256':sha((p/'semantic-review.md').read_bytes()),'theorem_constants':v['theorems_audited'],'safe_definitions':v['safe_definitions_audited']},indent=2))
