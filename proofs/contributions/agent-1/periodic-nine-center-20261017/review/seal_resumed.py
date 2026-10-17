#!/usr/bin/env python3
"""Seal actual resumed reviewer execution, preserving prior preparation and math."""
from pathlib import Path
import hashlib,json,re,subprocess,datetime
p=Path(__file__).resolve().parent
root=p.parents[4]
sha=lambda b:hashlib.sha256(b).hexdigest()
identity=json.loads((p/'resumed-source-identity.json').read_text())
prep=json.loads((p/'resumed-preparation.json').read_text())
v=json.loads((p/'clean-001/verification.json').read_text())
results=json.loads((p/'clean-001/results.json').read_text())
inv=json.loads((p/'clean-001/implementation-inventory.json').read_text())
execution=json.loads((p/'execution-receipt.json').read_text())
log=(p/'clean-001/ReviewAudit.log').read_text()
assert identity['source_commit']=='54e1e58b320dfdbe8dc7d2a3ca9e141df9b8ffe2'
assert identity['registry_sha256']=='d76263fe94ddaa93ea5ae364e39c8d3577faa6f6cc7c8b8422428b73b2c4a813'
assert v['status']=='PASS' and inv['status']=='PASS' and v['source_modules']==17
assert execution['exit_code']==0 and len(results)==18 and all(x['exit_code']==0 and not x['timed_out'] for x in results)
assert v['reviewer']=='Agent #1 specialist center_review_resume'
assert len(identity['new_module_theorems'])==4 and not identity['new_module_definitions']
for name,expected in prep['existing_files_sha256'].items():
 assert sha((p/name).read_bytes())==expected,'Prepared evidence changed: '+name
for e in identity['sources']:
 data=(root/e['path']).read_bytes()
 assert sha(data)==e['sha256']
 assert data==subprocess.check_output(['git','show',identity['source_commit']+':'+e['path']],cwd=root)
 assert data==(p/'clean-001/compiled-sources'/f"{e['module']}.lean").read_bytes()
 assert sha((p/'clean-001'/f"{e['module']}.log").read_bytes())==next(r['log_sha256'] for r in results if r['module']==e['module'])
registry=(root/identity['registry_path']).read_bytes()
assert sha(registry)==identity['registry_sha256']
assert registry==subprocess.check_output(['git','show',identity['source_commit']+':'+identity['registry_path']],cwd=root)
assert (p/'clean-001/replay.py').read_bytes()==(p/'replay_resumed.py').read_bytes()
assert sha((p/'clean-001/ReviewAudit.log').read_bytes())==results[-1]['log_sha256']
new={}
for mod in identity['new_modules']:
 new[mod]={}
 for label,token in [('theorems','AUDIT_THEOREM'),('safe_definitions','AUDIT_SAFE_DEFINITION')]:
  entries=re.findall(r'^'+token+' '+mod+r' (\S+) : \[([^\]]*)\]',log,re.M)
  new[mod][label]=[{'name':n,'axioms':[] if not ax else re.split(r'\s*,\s*',ax.strip())} for n,ax in entries]
 new[mod]['runtime_definitions']=re.findall(r'^NONSAFE_DEFINITION '+mod+r' (\S+)',log,re.M)
assert len(new['Agent1PeriodicCenterWrap']['theorems'])==6
assert len(new['Agent1PeriodicNinesCenter']['theorems'])==12
assert not any(e['safe_definitions'] or e['runtime_definitions'] for e in new.values())
for name in identity['new_module_theorems']:
 assert name+' ' in log
 assert f"'{name}' depends on axioms:" in log or f"'{name}' does not depend on any axioms" in log
assert set(v['axiom_union'])=={'propext','Classical.choice','Quot.sound'}
assert set(v['safe_definition_axiom_union']) <= {'propext','Classical.choice','Quot.sound'}
for filename in ['new-module-origin-audit.json','semantic-review.md','README.md','frozen-receipt.json','FILES.json']:
 assert not (p/filename).exists(),'Do not overwrite sealed evidence: '+filename
(p/'new-module-origin-audit.json').write_text(json.dumps({'status':'PASS','reviewer':v['reviewer'],'modules':new,'public_theorems':identity['new_module_theorems'],'public_definitions':[],'literal_public_axioms_and_types':'clean-001/ReviewAudit.log','runtime_inventory_separate':True},indent=2)+'\n')
report=f'''# Independent semantic and fresh-build review

PASS for published source `{identity['source_commit']}`, registry SHA256 `{identity['registry_sha256']}`. Current reviewer: Agent #1 specialist `center_review_resume`. I authored none of the new modules or frozen dependency math. Earlier specialist `symbolic_scope` prepared the source interpretation and verification helpers and disclosed prior authorship of some frozen dependencies. That preparation did not execute Lean. All original preparation files remain byte-identical; `resumed-preparation.json` records their hashes. This report describes my new source inspection and actual fresh execution, not execution by the earlier preparer.

## Statement and semantic review

`stripPeriodCenter_wrap w K hw` assumes only `w ≠ []` and returns exact pair equality: the maximal residual of `w ++ K ++ w.reverse` is the residual of `K`, and the count is the count for `K` plus one. `K` may be empty, asymmetric, or already wrapped; `w` need not be primitive. The original empty-period convention remains unchanged and is correctly excluded from this theorem.

The private sufficient-fuel identity uses `H.length ≤ fuel`. At zero fuel, `H=[]`, and a nonempty period cannot pass the reconstruction test. At a successful successor step, the original strict length-decrease lemma yields the induction hypothesis's predecessor fuel bound. At an unsuccessful test both calls stop identically. The public wrapper has length `K.length + (2*w.length-1) + 1`, with the natural subtraction justified by positivity of `w.length`. After its first guaranteed removal, the sufficient-fuel identity equates the remaining call to the original length-fuel call on `K`. Thus the theorem compares literal algorithm results, including the exact count, without a hidden irreducibility or fuel assumption on the public interface.

For the three mixed-nine results let `W9=[9,9,9,9]`, `e=leftEntry B`, `f=rightEntry B H W9`, and `g=rawGamma B H W9`. The assumptions are exactly `Bounded B 18`, `Bounded H 18`, and `e+f=1`. `e` and `f` are the actual original scans; the all-nine blocks transmit these bits. `g` is the actual whole-word terminal carry of `periodicWord B H W9 3`, bounded by the existing scan theorem. It is neither a freely chosen bit nor the outgoing carry of `H`.

The raw result is exactly `W9 ++ R ++ W9`, where `R=pair (fixedDigits H e ++ List.replicate g (9*e))`. Existing `raw_blocks_eq_zipper` identifies the original literal raw center slice. The private zipper proof handles all four combinations of the two mixed orientations and the two possible clocks:

| Actual e/f | Left/right fixed nine digits | g=0 middle | g=1 middle |
| --- | --- | --- | --- |
| 0/1 | nines / zeros | fixedDigits H 0 | fixedDigits H 0 ++ [0] |
| 1/0 | zeros / nines | fixedDigits H 1 | fixedDigits H 1 ++ [9] |

`pair_three_parts` then produces the nine wrapper in each case. The fixed digits deliberately omit `H`'s outgoing carry; the separate pad belongs to the actual full-word clock. This is not a formula for `stepWord H` or standalone normalization of `H`.

No symmetry, even-middle, positivity, minimum length, initial irreducibility, or full `ValidPeriodic` premise is added for `H` or `B`. Empty or all-nine `H` makes the mixed-entry premise impossible because it transmits the same carry; this does not add an unstated exclusion. Small centers and centers with additional nine boundaries remain covered conditionally by the same statements.

The private simultaneous identity derives actual `rawPeriod B H W9=W9` from unchanged `rawPeriod_nines` and the mixed equality, then uses the generic wrapper result. `quotientCenter_nines_mixed` and `centerPeriods_nines_mixed` are precisely the unchanged first and second projections of maximal stripping by actual rawPeriod. All additional removals within `R` remain represented: `centerPeriods` is `stripPeriodCenter W9 R`'s count plus one, with no claim that the total equals one or is bounded above.

No semantic gap was found in these four statements. These are local arithmetic identities. They establish no temporal center descent, no-return theorem, actual cycle, ordinary positive witness, or result about 196. The exact closure imports existing Nines and Quotient with the two new modules; no phase graph, CycleNumeric, or RunAncestry enters this 17-module review.

## Actual verification

The new empty object directory was `/workspace/p196-agent1-session-20261016/nine-center-review-build-001`, outside the Git worktree. All 17 published sources were copied there and rebuilt; no external project objects were reused. The sole reviewer run `clean-001` passed 17 module compilation commands and one full-origin audit command. No reviewer Lean command failed, timed out, or was interrupted. Commands, original source snapshots, logs, resource limits and compiler identity are preserved. Earlier author attempts remain separate with their original outcomes.

Official Lean 4.19.0 binary SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023` was invoked with `--trust=0 -j1 -DElab.async=false`, 8 GiB per-command address-space limit, and 600-second per-command timeout. The current driver is `replay_resumed.py`, copied from the preserved prepared driver with explicit reviewer attribution and four additional literal public `#print axioms` commands. Its exact executed bytes are also retained in `clean-001/replay.py`.

The full module-origin audit checked {v['theorems_audited']} theorem constants and {v['safe_definitions_audited']} safe definitions. The theorem axiom union is exactly `{', '.join(v['axiom_union'])}`; the safe-definition union is `{', '.join(v['safe_definition_axiom_union'])}`. Only the standard three axioms are accepted. The two new modules contain 18 theorem constants (CenterWrap 6; NinesCenter 12), four public theorems, zero safe definitions and zero runtime definitions. All four public types and literal axiom outputs appear in `clean-001/ReviewAudit.log`; all {len(v['audited_named_exports'])} top-level public Agent1 theorems in this closure were also type-checked. The source scan of all 17 modules masks nested comments and strings and found no `sorry`, `admit`, `native_decide`, `sorryAx`, `axiom` declaration, or `Lean.ofReduceBool`.

The separate implementation inventory records {inv['nonsafe_count']} generated non-safe runtime definitions: {inv['cstage_helpers']} compilation-stage helpers and {inv['unsafe_rec_helpers']} unsafe-recursion helpers whose corresponding safe definitions were audited. It records {len(inv['unsafe_axioms'])} inherited compiler implementation axioms, zero unsafe opaques, and no unclassified runtime definitions. No such implementation entry occurs among accepted theorem or safe-definition axiom dependencies. This inventory is not a proof shortcut or repository-wide acceptance.

The exact registry, imports, minimal closure, published source bytes, and evidence source snapshots were checked again while sealing. The initial source pin records the source-only stage honestly; this report and the execution receipt record the later completed execution. Coordination check-in 6228459948 was POSTed and GET-read back successfully. The initial unsupported `gh --slurp` attempt was a coordination-tooling failure, corrected with supported `gh api --paginate`; it was not a Lean failure and is preserved in the coordination record. No math source, registry, or Git state was written by this reviewer.
'''
(p/'semantic-review.md').write_text(report)
(p/'README.md').write_text(f'''# Nine-center independent review: PASS

Current reviewer `center_review_resume` independently checked published source `{identity['source_commit']}` and rebuilt its exact 17-module closure with official Lean 4.19.0, explicit trust zero, and no reused project objects. All 18 actual compile/audit commands passed. Full origin audit: {v['theorems_audited']} theorem constants and {v['safe_definitions_audited']} safe definitions; only standard theorem axioms. New modules: 18 theorem constants and four public interfaces, with no definitions or runtime entries.

Read `semantic-review.md`, `frozen-receipt.json`, and `clean-001/ReviewAudit.log` for scope and execution evidence. `resumed-preparation.json` preserves the earlier `symbolic_scope` preparation hashes and discloses the actual new executor; earlier source-only artifacts remain historical, not Lean-run claims.

Reproduce with `replay_resumed.py --source-root /workspace/p196-agent1-nine-center-20261017 --build-dir NEW_EMPTY_DIRECTORY_OUTSIDE_WORKTREE --evidence-dir NEW_EMPTY_EVIDENCE --lean /workspace/p196-tools/lean-4.19.0-linux/bin/lean --memory-mib 8192 --module-timeout-seconds 600`. `pin_resumed.py` produced the separate immutable current source pin. Build directories must be new; do not overwrite old runs. All sources/logs are retained; object files stay outside the Git worktree. No mathematical source or registry was changed, and no temporal descent, return obstruction, cycle, or 196 conclusion is claimed.
''')
receipt={'status':'INDEPENDENT_REVIEW_PASS','reviewer':v['reviewer'],'source_commit':identity['source_commit'],'registry_sha256':identity['registry_sha256'],'authored_any_math':False,'prior_preparer':'Agent #1 specialist symbolic_scope','prior_preparer_authored_some_dependencies':True,'prepared_files_preserved_byte_identical':True,'accepted_run':'clean-001','failed_or_interrupted_reviewer_lean_runs':[],'source_modules_rebuilt':17,'external_project_objects_reused':False,'trust':0,'all18_compilation_and_audit_commands_passed':True,'theorem_constants_audited':v['theorems_audited'],'safe_definitions_audited':v['safe_definitions_audited'],'new_module_theorem_constants_audited':18,'new_module_safe_definitions_audited':0,'new_public_theorems':identity['new_module_theorems'],'new_public_definitions':[],'literal_public_axioms_printed':True,'theorem_axiom_union':v['axiom_union'],'safe_definition_axiom_union':v['safe_definition_axiom_union'],'semantic_findings':[],'compiler_implementation_inventory_separate':True,'source_bytes_equal_published_commit':True,'sources_unchanged_at_finish':True,'disposable_build_outside_git_worktree':True,'repository_wide_acceptance_claimed':False,'formal_pr_review_posted':False,'sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'review_evidence':{}}
for rel in ['.gitignore','final-source-identity.json','resumed-source-identity.json','resumed-preparation.json','semantic-review.md','clean-001/verification.json','clean-001/implementation-inventory.json','clean-001/ReviewAudit.log','new-module-origin-audit.json','README.md','replay.py','replay_resumed.py','pin_published.py','pin_resumed.py','seal_review.py','seal_resumed.py','execution-receipt.json','resumed-console.log']:
 receipt['review_evidence'][rel]=sha((p/rel).read_bytes())
(p/'frozen-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
files={str(f.relative_to(p)):{'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in sorted(p.rglob('*')) if f.is_file() and f.name!='FILES.json'}
assert not any(Path(x).suffix in ['.olean','.ilean','.o','.c'] for x in files)
(p/'FILES.json').write_text(json.dumps(files,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'receipt_sha256':sha((p/'frozen-receipt.json').read_bytes()),'review_files':len(files),'manifest_sha256':sha((p/'FILES.json').read_bytes()),'semantic_review_sha256':sha((p/'semantic-review.md').read_bytes()),'audit_log_sha256':sha((p/'clean-001/ReviewAudit.log').read_bytes()),'theorem_constants':v['theorems_audited'],'safe_definitions':v['safe_definitions_audited']},indent=2))
