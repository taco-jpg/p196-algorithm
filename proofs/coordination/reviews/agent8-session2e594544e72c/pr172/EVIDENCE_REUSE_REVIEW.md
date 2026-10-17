# PR172 — Qualification of retained independent evidence

**Result: `PASS_RETAINED_EVIDENCE_REUSE`**

The existing independent `symbolic_scope` review and its retained strict fresh-build evidence qualify for reuse for the two new PR172 mathematical modules at final head `b8c17a5204ae56ad1fc99d8f9932ca9f57b6ac80`. The actual review contains substantive semantic findings, and its source, dependency closure, command records, raw audits, and final publication identities are sufficiently bound. No new full mathematical review or Lean build is required merely because delivery ownership changed.

This result is limited to evidence reuse. It does not accept or merge prerequisite PR168, verify an intended combination with main, satisfy unknown platform requirements, or claim that a qualifying quotient cycle exists.

## 1. Identity, assignment and examined records

| Item | Exact identity |
|---|---|
| Repository / PR | `taco-jpg/p196-algorithm#172` |
| Final source head H | `b8c17a5204ae56ad1fc99d8f9932ca9f57b6ac80` |
| Original reviewed mathematical publication R | `24c29104b6855fe19ad593c0b78fd5ee766a7d26` |
| Prerequisite PR168 head P | `7f23ce839fcc88acb235b1816c2c57dc12e16a33` |
| Observed main B in parent binding | `74a1c3922eb7af438fe40b23d2105ad07556e3f5` |
| Existing actual review | `5555494440`, submitted 2026-10-17 02:07:32 UTC, state `COMMENTED`, `commit_id = H` |
| Registry blob | `efe03f3f3f146d7ddce2e96cb126ea81f710fcc3` |
| Registry SHA-256 | `d3fca8aa3b055bd287f347a21d132a02c41c6713cdd754fd42a90bf5afcccc80` |
| Reviewer receipt SHA-256 | `d747c06561717cd4d10e29f6156c259a972b33c3d27381593bc02e76d597080b` |
| Reviewer manifest SHA-256 | `1460748582eba52ec7755a93a29a24bb4f85043a12b0b621e89eb898dff47d87` |
| This reviewer | Agent #8 delegated nonauthor specialist `/root/pr157_payload_audit`, reused for this bounded PR172 task |

The actual platform review is retained in `FORMAL_REVIEWS.json` and is accessible at https://github.com/taco-jpg/p196-algorithm/pull/172#pullrequestreview-5555494440. It expressly identifies itself as a same-session, same-account specialist comment rather than an external-account approval. Its final paragraph binds the reviewed sources and all three evidence manifests to H.

In this report, **`C/`** means `proofs/contributions/agent-1/periodic-nine-cycle-20261017/`. Source references are relative to the materialized `source/` directory unless stated otherwise.

Agent #8 supplied all 288 added files, 2,534,744 bytes, with advertised Git blob identities checked during materialization. I read the actual review, semantic report, prepublication report, independent replay/pinning/sealing programs, generated audit program, relevant raw audit output, source/registry manifests, parent provenance and packaging logic, and the two new mathematical source files. I did not restart the proof review of every inherited module. I additionally executed the narrow local record checks documented in section 8.

## 2. Independence and semantic scope

The completed reviewer is the genuine separate specialist `symbolic_scope`. The package assigns `Agent1PeriodicNinesPath` to `cap4_existing_theorems` and `Agent1PeriodicNinesCycle` to `numeric_bridge_review`; the reviewer authored neither new module. The reviewer explicitly discloses prior authorship of some frozen dependencies. The registry preparer/parent-evidence packager, `verification_plan`, also discloses its role and prior dependency authorship and does not claim that packaging constitutes independent mathematical review. See `C/README.md:7–15`, `C/review/semantic-review.md:3`, and `C/verification/README.md:3–7`.

This qualifies as nonauthor review of the two new modules. It does not establish that the reviewer was a nonauthor of the entire inherited 34-module closure. Rebuilding dependencies establishes fresh technical verification; it does not retroactively establish semantic nonauthorship. Existing prerequisite review and integration remain separately scoped under Agent #8's delivery process.

The semantic report is substantive and covers all five public interfaces. I compared those coverage claims with the current two source files and their retained printed types; no uncovered new public declaration or material mismatch was found.

| Public theorem | Covered obligation and boundary |
|---|---|
| `quotient_path_nines_phase` | Original literal `QuotientPath`, both nine-phase endpoints, and all indices through N; includes N=0. Bounds are used only at actual source indices below N. No initial validity, positive N, complete-tuple return or safety premise is inserted. |
| `quotient_path_nines_entry_sum` | The original computed left/right entry scans sum to one for used transitions. No free bits or substitution of the complete-word `rawGamma` is introduced. |
| `periodic_nines_input_nonpalindrome` | Positive repetition, original canonical digits at the exact width, and full in-range column representation yield a real coefficient nine. The original palindrome equivalence would make it twice a natural digit. Leading-digit, width, and input/time-zero conventions remain explicit. |
| `quotient_cycle_nines_safe` | Positive N, initial validity, and complete literal B/H/w return remain hypotheses. Safety follows using the successor's nine-phase representation, including the final modulo-N wrap, before applying the next-output safety equivalence at the current state. |
| `quotient_cycle_nines_positive_seed` | The same full-cycle hypotheses yield one positive all-time palindrome-avoiding seed through the inherited same-seed criterion. The inherited successor witness handles the original `IsLychrel` time-zero requirement. No horizon-dependent witnesses are substituted. |

Evidence: `C/review/semantic-review.md:5–17`; `proofs/Agent1PeriodicNinesPath.lean:62–103`; `proofs/Agent1PeriodicNinesCycle.lean:20–89`; and exact printed types in `C/review/clean-001/ReviewAudit.log:3541–3562`.

The review consistently excludes construction of a qualifying cycle, an unconditional decimal Lychrel witness, a nine-center obstruction, generic nine-run ancestry, or any conclusion about 196. The preserved conditional hypotheses are not a review defect and do not justify demanding an unadvertised concrete cycle instance.

## 3. Final-head source and dependency binding

The independent pinning program checks published Git bytes, SHA-256 and Git blob identities, literal imports, exact root reachability, and equality between discovered new public declarations and registered endpoints. It refuses overwriting an earlier identity receipt. The replay then checks every source again against both that identity and `git show R:path`, copies it to a new empty build directory, and rechecks working source hashes after the run. See `C/review/pin_published.py:14–67` and `C/review/replay.py:67–90,239–242`.

My local checks confirmed all 34 independent compiled-source snapshots match their registered SHA-256/Git blobs and their parent-run source copies. Independently parsed literal imports produce the same exact topological 34-module closure rooted at `Agent1PeriodicNinesCycle`, with no registered module outside it and no unregistered nonstandard import. The two current added mathematical files match the independent snapshots, the final author snapshots, and the registry. The registry's five endpoint names equal all five public declarations found in the two new files; neither new module introduces a public definition.

The initial added-file materialization alone contains only the two new canonical mathematical paths, so I did not infer final-H binding of inherited files from preserved copies. Agent #8 separately retrieved exact nontruncated shallow Git trees at H, R, P and B and supplied:

- `CANONICAL_BINDING_INPUT.json`;
- `check_canonical_binding.py`;
- `CANONICAL_BINDING_RESULT.json`;
- `canonical-binding-execution.json` with actual exit code 0.

I inspected that input, checker and result. All 34 canonical source blobs and file modes agree between H, R and the independent identity receipt. All 32 inherited modules also agree with P. The registry is byte-identical at H/R; the direct canonical verifier has unchanged blob `21131b03dfa516eb19a0a7a4df4f2a41020d4db1` across H/R/P/B. This supplies the otherwise missing final-head binding and supports reuse at H.

The same binding records 25 closure modules already present with matching bytes at B and nine absent, comprising seven prerequisite modules plus the two new modules. That is a real stacked-delivery boundary, not a defect in the retained review. The result here does not claim that a bare application to current main supplies those missing prerequisites.

## 4. Independent strict fresh execution

The historical independent run is `clean-001`. It is distinct from both author incremental checks and the parent canonical run.

| Field | Verified retained record |
|---|---|
| Compiler | Lean 4.19.0, `x86_64-unknown-linux-gnu`, release commit `6caaee842e94` |
| Compiler SHA-256 | `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023` |
| Source compilations | 34, in the complete dependency order |
| Audit invocation | 1, `ReviewAudit.lean` |
| Commands | 35; all recorded exit 0; none timed out |
| Required arguments in every command | `--trust=0 -j1 -DElab.async=false` |
| Memory cap | 8,192 MiB address space per child |
| Timeout | 600 seconds per command |
| Existing output handling | Both build and evidence directories must be new |
| Project object reuse | None; the explicit `LEAN_PATH` points to the fresh build directory |

For each ordinary module M, the exact recorded argv is:

```text
/workspace/p196-tools/lean-4.19.0-linux/bin/lean --trust=0 -j1 -DElab.async=false -o M.olean M.lean
```

The audit uses the same compiler and strict flags with `ReviewAudit.lean`, without an output-object argument. My local check compared all 35 complete argv arrays, module order, return codes, timeout flags, resource records and actual log hashes. The evidence-directory replay and identity snapshots equal their published counterparts. The top-level launch and process exit are retained in `C/review/execution-command.json`; child results are in `C/review/clean-001/results.json`.

The driver source confirms the fresh-directory and isolation behavior, compiler hash check, explicit strict flags and fail-fast retention of command logs. It would preserve a failed or timed-out Lean invocation and stop before writing a successful final result. The accepted record contains no failed/interrupted reviewer Lean invocation. This is a statement about the one retained reviewer attempt, not a denial of earlier author failures.

I did not run this driver, invoke Lean, rehash a currently installed compiler, or reproduce the historical execution. Compiler/environment identity here is retained evidence bound by the manifests and actual review, not a newly measured runtime.

## 5. Complete recorded origin audit

The generated Lean audit iterates environment constants by actual originating module. It applies transitive `Lean.collectAxioms` to every theorem and safe definition/safe opaque in the selected closure, rejects nonstandard mathematical axioms, and separately records unsafe implementation categories. It also requires theorem coverage for each of the 34 selected modules. The source-level declaration scans mask nested comments and strings; the auxiliary lexical scan is not used as a replacement for the environment-origin audit. See `C/review/clean-001/ReviewAudit.lean:1–61` and `C/review/replay.py:11–56,136–278`.

My new local inspection parsed the complete raw `ReviewAudit.log`, checked record uniqueness and module coverage, and verified:

| Category | Actual retained count / result |
|---|---|
| Theorem constants | 1,547; all 34 selected modules represented |
| Safe definitions/opaques audited | 244 |
| Theorem axiom union | Exactly `{Classical.choice, Quot.sound, propext}` |
| Safe-definition axiom union | Exactly `{propext}` |
| New module theorem constants | Path 16; Cycle 7; total 23 |
| New module safe definitions or runtime helpers | 0 |
| Printed public Agent1 theorem types | 136, including all five new endpoints |
| Generated non-safe definitions | 978 |
| Compilation-stage helpers | 947 |
| Unsafe-recursion helpers | 31; every recorded safe base is present in the safe-definition audit |
| Inherited unsafe implementation axioms | 13 |
| Unsafe opaques / unclassified runtime definitions | 0 / 0 |

The raw summaries at `C/review/clean-001/ReviewAudit.log:3001–3002` agree with the individual parsed records. All 978 runtime names and all 13 implementation-axiom names match the separate structured inventories. None appears as an unpermitted dependency of an accepted theorem or safe definition. The two new modules contribute no such runtime entries.

The count is a complete origin audit of the stated theorem/definition categories, not a count of every inductive constructor or recursor, independent discovery, or repository-wide theorem. The retained environment audit and compiled-source closure disclose no material coverage omission for the advertised five endpoints.

## 6. Parent provenance and historical distinctions

The preserved parent canonical run also reports 34 modules, 35 successful commands and 1,547 theorem constants. I verified its 35 command-log hashes and raw theorem count, as well as the original report, original manifest and console identities against the additive provenance receipt.

Its argv contains `-j1 -DElab.async=false` but **does not explicitly pass `--trust=0`**. The evidence accurately preserves that distinction. No compiler default is inferred, and the parent run is not used to substitute for the independent strict run or to claim the independent 244-safe-definition audit. Its `source_tree_clean` field comes from tracked-file status with `--untracked-files=no`; it does not attest to absence of untracked files. See `C/verification/README.md:17–39`, `C/verification/parent-result-addendum.json`, and `C/verification/canonical-verifier.py:83`.

The packaging driver copies and hashes already completed evidence and performs no Lean run. Its helper provenance identifies the predecessor implementation and adaptations. The existing frozen registry retains `FROZEN_AUTHOR_CHECKED_FRESH_REVIEW_PENDING` and earlier pending text as historical metadata. The completed additive receipts and actual final-H review supply the later state. Rewriting the preserved registry merely to modernize that label is unnecessary and would change the source identity being reused.

## 7. Failures, cleanup and preservation

The unsuccessful Path author attempt remains visible. `C/path-author/attempt-001/result.json` records exit 1, and `compile.log:1–9` shows the Omega failure caused by separate presentations of `terminalCarry` and `rawGamma`, followed by the rejected elaboration's generated `sorryAx` reports. Attempt 002 supplies the explicit `rawGamma` type annotation, passes, and is the exact accepted Path source. Its successful source does not inherit the failed elaboration. This historical log must remain preserved and must not be presented as an axiom dependency of the accepted run.

All three Numeric author increments passed and remain preserved; the final accepted Cycle source equals attempt 003. The author runs explicitly disclose reused pinned dependency objects. They are not represented as independent fresh whole-closure evidence. The later strict reviewer run supplies that separate obligation.

The package also discloses two publication/processing incidents in `C/README.md:15,25`: an initial parent manifest validator treated a dictionary as a list, and an intermediate evidence commit accidentally tracked disposable reviewer build objects. I did not recreate those historical failures. The current manifests parse in their real dictionary form and all entries verify. The final review tree contains the 120 sealed manifest members, its manifest itself, and the later `.gitignore`; it contains no `fresh-build-*` directory. The required sources, commands, logs, snapshots, raw audits and failed author attempt remain available.

Agent #8 additionally supplied `PUBLICATION_CLEANUP.json`, the complete final-commit cleanup record against parent `61d9b76de69bcd61288d1fbe92eb95a7a9170966`. Its 71 changed paths consist of the README disclosure, the four-line review-local ignore file, and 69 removals confined to `review/fresh-build-001/`. The parent review records exact retained-at-H blob mappings for all 35 removed Lean source/auditor copies; the other 34 removals are regenerable object binaries retained in the published predecessor history. The final-H formal review confirms the same preservation boundary. This is reused parent publication evidence; this reviewer did not independently retrieve remote history or perform cleanup. No unique mathematical source, log, or audit record is shown as lost.

The preserved historical Path `.olean` is not used by the independent driver: its build directory is newly created and its source search path is the fresh closure. Preservation of an archival object is therefore not evidence of project-object reuse in the accepted independent run.

No original source, failure, log or ownership record was edited or removed by this reviewer.

## 8. New local checks and retained receipts

One new bounded Python check was executed, solely to inspect retained JSON, source identities, manifests, command metadata and raw audit records. It executed neither retained repository programs nor Lean. It passed on its first execution with exit code 0 and empty stderr on 2026-10-17 at 05:24:05 UTC.

Files under `evidence-reuse-review/`:

- `check_retained_records.py`: complete actual local check program;
- `check.stdout`: complete actual output;
- `check.stderr`: empty actual stderr;
- `check-execution.json`: exact argv, cwd, start/end timestamps, exit code, and script/stdout/stderr SHA-256 identities.

The checks verified 120 independent-review manifest entries, 81 parent-package entries, and 71 original-parent entries, including all sealed receipt hashes. These are overlapping preservation scopes, not 272 distinct files. They checked the 34 source snapshots and graph, exact strict argv/log identities, individual raw theorem/definition/runtime records, endpoint registration, parent-run distinctions and retained final author-source identities.

The local output lists the 32 inherited canonical paths absent from the added-file materialization as requiring Agent #8's separate final-head binding. That binding was subsequently supplied and inspected in the four `CANONICAL_BINDING_*`/execution/checker files described in section 3. The earlier output is preserved unchanged rather than being rewritten to imply that this script fetched remote sources.

## 9. Disposition and remaining boundary

**No material evidence-reuse gap remains for PR172 at H.** Reuse the existing nonauthor semantic review and explicit trust-zero fresh-closure records. A duplicate proof review or fresh Lean build is not made mandatory by this report.

Agent #8 remains the integration-only delivery owner. Agent #1 retains source ownership. Prerequisite PR168 remains under its existing delivery owner, Agent #16/session `02ac12cc16be`, and Agent #31 remains the active main writer as supplied in the assignment. This report neither transfers those responsibilities nor claims a target-write slot.

The next delivery work is the existing prerequisite/combined-tree and platform process owned by Agent #8 and the acknowledged writers. If source or dependency blobs change, reassess only the affected evidence. This qualified reuse result is not an overall integration verdict, a formal approval, a Ready transition, a merge attempt, or verified publication on main.
