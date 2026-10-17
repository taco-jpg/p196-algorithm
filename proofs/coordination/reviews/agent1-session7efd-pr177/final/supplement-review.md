# Independent review of the PR #177 supplemental audit

Reviewer: Agent #1 independent review specialist, not the author of the audit runner.

## Pre-execution decision

**APPROVED for the authorized isolated audit** at runner SHA-256:

`a96fb1f93b13eed7a733cf871d875c5d5c0ef878cf7d7072fc3e4196cfbfe3c9`

Runner: `/workspace/scratch/7efd48098de6/pr177-evidence/run_supplement.py`.

This is approval of the reviewed audit implementation, not a claim of successful execution. Actual results are to be appended separately.

## Review and corrections

I read the runner and its generated Lean programs in full. I checked the referenced APIs against the installed Lean 4.19.0 source: `ConstantInfo.isUnsafe`, `ConstantInfo.isPartial`, `Lean.Compiler.getImplementedBy?`, `Lean.getExternAttrData?`, and the existing use of `Lean.collectAxioms` have the required signatures.

The first draft had two concrete evidence issues, both fixed before execution:

1. The supplied Lean CLI argument was not tied to the retained compiler-file map, although stored compiler paths were rehashed. The accepted revision requires the actual resolved executable path to belong to that map and rechecks every mapped compiler hash before and after the audit.
2. Concatenating generated private theorem names into textual `#print axioms` commands is unsafe for Lean Name values with numeric components, such as `_private.Agent107DFABoolean.0._proof_3`. The accepted revision enumerates the original Name values and calls the real command elaborator with `elabCommand (← \`(#print axioms $(mkIdent name)))`. This preserves exact private identifiers and still executes the actual `#print axioms` command. The resulting printed-name set and a command-count marker must match the independent prior name list exactly.

At my request the revision also rechecks all selected source-snapshot hashes after execution, alongside object, compiler, and prior-report stability.

## Coverage and safeguards

The runner requires the repaired verifier's PASS at exact H, 19 selected modules, 20 successful explicit-trust-zero invocations, the retained compiler identity, and unchanged source snapshots. It pins all 19 freshly built object files and does not rebuild modules or borrow project objects from an unrelated execution.

The first generated audit traverses declarations by their actual selected module origin. It rejects non-unsafe project axioms; collects transitive axioms for every safe theorem, definition, and opaque declaration; enforces the exact foundational whitelist; rejects project `implemented_by` and `extern` attributes on those audited declarations; and separately lists unsafe/partial implementation declarations. It checks unique declaration names and summary/category counts, requires the theorem count to equal the successful prior audit, and requires nonempty safe-definition coverage.

The second audit invokes actual `#print axioms` on every theorem constant from the seven new modules and retains literal `#check` commands for all nine advertised endpoints. It does not substitute a handpicked endpoint subset for the module-origin traversal. The original all-source scan found no source-written unsafe/partial declarations or executable overrides; compiler-generated unsafe placeholders will be reviewed separately against the retained list and the safe declaration dependency results.

Each audit uses `--trust=0 -j1 -DElab.async=false`, records its source/log hashes and exit status, and fails on nonzero exit or missing/duplicate output. Fresh evidence directories are required, so prior attempts remain preserved. The allowed foundational set and all prior verifier evidence remain unchanged.

## Already inspected repaired-verifier results

I separately read the repaired-verifier report and endpoint output, then recomputed all 20 command-log hashes and 19 source-snapshot hashes: zero mismatches. All 20 invocations explicitly include `--trust=0`. Current results are 1,453 theorem constants, 115 from the seven new modules, and 20 separately reported unsafe implementation axioms. The theorem axiom union is `Classical.choice`, `Quot.sound`, and `propext`.

These are the fresh execution counts. They differ from the historical reported 20-module/1,445-theorem/128-new-theorem summary whose raw bundle remains unavailable. The fresh result must be reported on its own provenance rather than claimed as recovery or confirmation of that absent historical execution.

## First execution and scoped follow-up repair

Actual `supplement-001` executed the safe-definition audit successfully (exit 0). Its literal stage printed all 115 theorem axiom outputs and all nine endpoint types but returned exit 1 because `pp.width` is not a registered Lean 4.19 option. I had missed that formatting-option name in pre-execution review. The real registered option is `format.width`; the revised runner simply removes the optional formatting setting. The failed run and its original source/log hashes remain preserved and must remain labeled FAIL.

The successful safe audit covers 1,453 theorems, 414 safe definitions, zero safe opaque declarations, and 3,940 unsafe compiler implementation declarations. I checked the successful audit's source/log hashes and all requested executable definition names. The 3,940 entries consist of the same 20 unsafe-axiom placeholders identified by the repaired verifier plus 3,920 unsafe implementation definitions: 3,628 names ending `_cstage2`, 279 ending `_cstage1`, and 13 inherited foundation names ending `_unsafe_rec`. None is a source-written unsafe definition. The safe declarations' transitive dependencies exclude these implementation placeholders and satisfy the foundational whitelist.

The safe summary's axiom list wrapped over three lines. The initial parser retained only the first line of that display, so a second reporting repair captures the complete bracketed list across newlines and normalizes whitespace. The semantic Lean axiom rejection was already correct; this repair prevents a truncated human-readable union.

I independently reviewed and **APPROVED** the revised runner at SHA-256:

`1aeedfea7977790e0eea844532e33809ce0976a83df754d00aca8c56275daf5f`

Its new optional reuse path accepts the previously successful safe stage only when the prior verifier-report hash, source manifest, all 19 object hashes, compiler map, exact generated safe-audit source, source hash, log hash, successful exit, and explicit trust-zero argv match. It records `REUSED_EXACT_SUCCESS`, keeps the original command/timing, and reruns only the corrected literal stage. This is legitimate exact-success reuse from an overall failed two-stage run; it does not relabel the failed stage or bypass an obligation. No third module build or second safe-audit execution is needed.

## Final observed result

**PASS**, based on the actual `supplement-002` records, not on pre-execution approval.

The reused safe audit retains its actual exit 0, and the corrected literal audit freshly exited 0. All 115 theorem names printed by actual `#print axioms` agree with the module-origin list, and all nine endpoint types were checked. I independently parsed the complete safe declaration axiom lists: 1,453 theorems plus 414 definitions, no opaque declarations, and no dependency outside `Classical.choice`, `Quot.sound`, `propext`. The seven new modules contribute 115 theorem constants and 50 safe definitions.

I recomputed both audit source hashes, both log hashes, all five FILES manifest entries, all 19 object hashes, and the prior-report binding; every comparison matched. Final RESULT.json SHA-256 is `8ba902b4b355d7d4c289f19723406433c5a645520602b8a660be3174bd1242e2`. Safe audit source/log hashes are `1eb6f60e11448252ddb320ae5f8724128b90a162fca913a5361fd2289c8c3438` / `0e62a11d297f1f20a98449ef192c72cf6b0e67835db79335da2decd1ae1f4565`; corrected literal source/log hashes are `37e6bc3afdcf84d1359a610b27190d74d47d2854c0f224b203d7c051e549eba6` / `c9d79d74f6401539b6df5ac63b22e279fe3c1ae0c4e753b96c2691164ae52733`.

The supplemental coverage gap is closed for exact PR #177 source H. Original verifier failure and supplement-001 failure remain honestly labeled and preserved; neither is retrospectively called PASS.
