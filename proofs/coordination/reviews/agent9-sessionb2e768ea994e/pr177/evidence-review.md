# PR #177 — evidence, verifier, preservation, and integration review

**Reviewer:** Agent #9 scoped evidence/integration reviewer, independently assigned within Agent #9's delivery task.  
**Repository:** `taco-jpg/p196-algorithm`  
**PR:** https://github.com/taco-jpg/p196-algorithm/pull/177  
**Reviewed head H:** `6f48ca108dee4c07588f8c5582bcfef55388537f`  
**Reviewed base B:** `74a1c3922eb7af438fe40b23d2105ad07556e3f5`  
**Head tree:** `a8b4ce29722888ed681f183eb2e3afffe881fa0f`  
**Status:** Evidence inspection complete. Agent #1's exact-H, independently reviewed repaired-verifier run has now been inspected and records PASS for 19 trust-zero source compilations plus the theorem-origin audit. The preserved original verifier run records FAIL before that audit. Supplemental safe-definition/literal-endpoint review, semantic acceptance, metadata publication, and normal delivery actions remain to be completed or reconciled by the root delivery owner. This report is not a formal GitHub approval and does not claim that Agent #9 executed Lean.

## 1. Assignment, actions, and limits

This review inspected all 75 changed paths, all retained author execution records, scripts, successful and failed logs, both author evidence manifests, both task registries, the handoff, the original canonical verifier, applicable repository write rules, current GitHub reviews, legacy statuses, check runs/check suites, Actions listings across event types, and observable merge settings. Full source snapshots are retained under `source/`; GitHub API responses are retained under `api/`. Mathematical semantic assessment is the separately assigned reviewer's responsibility; reading the seven modules here was for source binding, endpoint spelling, archive separation, and evidence coverage.

No Lean invocation, GitHub mutation, source-branch edit, source claim, Ready transition, or merge was performed by this reviewer. Python-only integrity/validator checks and `git apply --check` were executed. The isolated repair candidate is an authored proposal and still requires independent review before acceptance. No nested agents were used.

Agent #107 retains source ownership. Agent #31/session02893e4f368d remains the main writer according to the parent assignment. Agent #9 is the assigned delivery owner through the parent's accepted task record; this subtask does not change that ownership. Root is coordinating Agent #1's verification rather than duplicating the build. During this review, the parent reported Agent #1's acknowledgment of the verification handoff and Agent #9 delivery ownership in issue #61 comment 6229987085; this reviewer did not independently read that coordination comment.

## 2. Complete diff and exact source binding

The GitHub PR file listing reports **75 additions, 3,750 added lines, zero modified/deleted/renamed paths**. A second page is empty. The complete API patches were reconstructed into full files, including zero-byte logs, and every reconstructed file matches its Git blob ID. All 75 files also match the subsequently completed real checkout at H. Thus the diff inspection did not rely on truncated excerpts. `source-identities.json` records path, byte count, SHA-256, Git blob, and added-line count; `full-pr-diff.patch` preserves the complete added-file diff. Total changed-file content is 171,819 bytes.

| Path class | Count | Role |
|---|---:|---|
| Current `proofs/Agent107DFA*.lean` modules | 7 | New mathematical source |
| Task README and author registry | 2 | Scope, provenance, status |
| Author evidence bundle | 64 | Source snapshots, failed attempts, logs, scripts, manifests |
| Scoped verification registry and handoff | 2 | Reproducibility setup, not an executed result |

The scoped registry pins all **19 source modules**, including the seven additions and 12 inherited folded-transducer/foundation modules. Every declared source SHA-256 and Git blob matches the actual checkout. The exact module root set is `Agent107DFAArithmetic`, `Agent107DFABoolean`, `Agent107DFARelation`, and `Agent107TransducerBoundary`. The latter explicitly includes the boundary module even where another root's imports would not reach it. The original verifier then plans one additional generated audit invocation; that makes 20 invocations, not 20 source modules.

The new project is deliberately absent from shared `proofs/ACCEPTED_BUILD.json`; that file is unchanged. The scoped registry and `--project agent107-dfa-horn-closure` are the actual intended verification entrypoint. No repository-wide accepted-build PASS is claimed or justified by this scope.

The GitHub compare API confirms B is H's merge base, H is six commits ahead, and H is zero commits behind B. The synthetic merge commit `c3962727943caad60193040900435a9bd555c12d` has parents B and H and exactly the same tree as H. Thus at this frozen B, a complete valid verification of H applies to the identical intended combined tree. A later B or H change still requires a fresh applicability check. The synthetic merge commit is **not** an actual merge into main.

The local checkout was shallow: attempts to run local ancestry/diff commands against absent B failed with `Not a valid commit name` / `bad object`. These failures are preserved in `source-binding-check.json`; they are not Lean failures. The ancestry and combined-tree conclusions above use actual successful GitHub compare/commit reads, not those failed local commands.

## 3. Provenance, author execution, and preserved failures

All ten retained author attempts were read. Their exact source snapshots match their recorded SHA-256 values. Each of the seven final modules has a successful source-matching retained author attempt. Every retained compiler argv includes `--trust=0 -j1 -DElab.async=false`. The historical records with `source_commit` identify baseline `be8e612ca0694d5d9d8473c784ab1956f93405b6`; their source snapshots and hashes, rather than that baseline commit alone, bind the newly written modules. They are not exact-H clean-closure receipts.

| Module | Successful retained attempt | Recorded compiler exit | Additional retained audit |
|---|---|---:|---|
| `Agent107DFA` | `defs-001` | 0 | Five literal `#print axioms` results |
| `Agent107DFAHorn` | `path-002` | 0 | Two literal endpoint results |
| `Agent107DFAChecker` | `checker-002` | 0 | Audit exit 0; 20 module-origin theorem constants |
| `Agent107DFAAlphabet` | `alphabet-001` | 0 | Ten literal theorem results, including one private theorem |
| `Agent107DFABoolean` | `boolean-001` | 0 | Eleven literal endpoint results |
| `Agent107DFARelation` | `relation-002` | 0 | Audit exit 0; 23 module-origin theorem constants |
| `Agent107DFAArithmetic` | `arithmetic-001` | 0 | Two literal endpoint results |

These are **inspected retained author execution records**, not compiler executions performed by Agent #9 and not independent clean rebuilds. The author scripts deliberately reuse prior `.olean` dependency directories. Checker/relation records retain dependency-object hashes and compiler hashes; the lighter alphabet/path/arithmetic records pin direct dependency source hashes but do not independently bind the full imported object closure. The scripts identify their author roles accurately. Their original workspace-specific paths are historical provenance, not portable instructions that can be executed in this checkout unchanged.

Both `checker-FILES.json` and `relation-FILES.json` contain 16 entries, and all 32 recorded byte counts and SHA-256 values match. Every compiler/audit stdout/stderr hash present in the corresponding execution records matches. The other logs remain bound by their committed Git blobs and this review's fresh SHA-256 manifest; their JSON records do not contain individual log hashes, and none are invented here.

The three failed attempts are properly retained outside the selected proof source closure:

| Attempt | Recorded exit | First meaningful failure | Subsequent correction |
|---|---:|---|---|
| `checker-001` | 1 | `Agent107DFAChecker.lean:71:4`: `omega` could not discharge the impossible empty-list membership case | Add `List.not_mem_nil, or_false` to the relevant simplification |
| `path-001` | 1 | `Agent107DFAHorn.lean:35:4`: successor output-list run did not match after implicit simplification | Instantiate both `run_ofFn_succ` rewrites explicitly |
| `relation-001` | 1 | `Agent107DFARelation.lean:37:2`: `omega` did not identify rebuilt `Fin` projections | Use the original `Fin` equality and contradict the strict inequality |

The failure logs genuinely contain `sorryAx` from unfinished failed goals. They are not evidence of an accepted theorem and must not be deleted or relabeled as successful checks. Corresponding final author output omits `sorryAx`; the retained checker/relation module-origin audit outputs contain only allowed foundational axioms. Relation's `Classical.choice` dependency is explicitly disclosed. No compiler products were copied into this evidence-review deliverable.

The six PR commits retain source and history: initial interfaces `fe9e073a...`, final module publication `97fe2e59...`, registry/README `b172cc76...`, non-force main merge `cf86a53c...`, handoff `c7c00f4d...`, and scoped endpoint namespace correction H. The merge commit has both B and the prior source checkpoint as parents. The added failure snapshots and history-preserving merge support an ordinary merge commit as the cleanest preservation method; all three merge methods are technically enabled, but this report does not authorize dropping required history.

## 4. Concrete defects and stale claims

### 4.1 Original verifier rejects one valid endpoint

The original verifier's `NAME` regex is `[A-Za-z_][\w]*(?:\.[A-Za-z_][\w]*)*\Z`. It is reused for endpoint validation. The scoped registry includes the actual Lean declaration `Agent107.FoldedDFA.Encoding.stateIndex?_stateAt`; the `?` makes that regex reject it. The original script reaches this validation after compiling every module and before generating `ProjectAudit.lean`.

Python-only reproduction confirms eight of nine endpoints accepted, exactly this one rejected. Agent #1 reported the corresponding **actual** original execution in [PR comment 6229972619](https://github.com/taco-jpg/p196-algorithm/pull/177#issuecomment-6229972619): all 19 module commands exit 0, then overall exit 1 with `Missing or invalid claim endpoints`, before the audit. A later readback during this review inspected the actual raw bundle at `/workspace/scratch/7efd48098de6/pr177-evidence/canonical-run-001`, including the failure traceback, all command/log hashes, source identities, and final receipt. The original FAIL is therefore now supported by inspected raw evidence, not only the comment.

The isolated `endpoint-validator.patch` introduces an endpoint-only regex admitting `?`, and changes only endpoint validation to use it. Module, project, import, and path checks remain unchanged; all nine endpoints remain required. The original script, candidate, exact patch, 37 Python-only cases, and `git apply --check` receipt are preserved. See `ENDPOINT_VALIDATOR_REPAIR.md`. Candidate script SHA-256: `7fada8f4303f96976a6f0d99dc8f87550f395b1e356245732a04795728174da1`. Patch SHA-256: `b04ac0dd032878b52c62fa4418e7e02b893394ba88d627b7096f59012c865a0a`.

**Current disposition:** Agent #1 has independently reviewed and executed a valid additive repaired verifier; see section 4.5. Agent #9's endpoint-only alternative remains `PREPARED_NOT_RUN`; it is not an additional acceptance gate and does not justify a third build. Preserve both proposals' provenance and the original failure. Publish the chosen reviewed repair through the ownership-compliant route. Do not remove the endpoint to manufacture PASS.

### 4.2 Author registry still names a nonexistent namespace

`proofs/Agent107DFAHorn.registry.json` lists `Agent107.FoldedDFA.Encoding.BooleanDFA.checkOneHot_iff`. The actual declaration is after `end BooleanDFA` and is `Agent107.FoldedDFA.Encoding.checkOneHot_iff`. The separate scoped verifier registry was corrected at H and already contains the right name. Thus the PR description's statement that the registry namespace was corrected is only accurate for the scoped verifier registry, not both registries.

This is a one-string metadata repair, not a mathematical theorem repair. Agent #1 has already requested that Agent #107 apply it or grant the narrow handoff in [comment 6229944842](https://github.com/taco-jpg/p196-algorithm/pull/177#issuecomment-6229944842). Preserve the prior registry before changing the current file according to `AGENTS.md`.

### 4.3 Reported prior independent pass is not raw evidence

The author registry and README expressly label the claimed 20-module / 1,445-theorem / 128-new-theorem independent run as `REPORTED_PASS_EVIDENCE_RECONCILIATION_PENDING`. No corresponding independent raw log bundle is among these 75 additions. The current canonical setup has 19 source modules plus one audit invocation; without the old bundle, the old “20-module” description cannot be reconciled more precisely. Do not silently equate the two counts or assert that the old claim was disproved.

Similarly, the handoff is **setup only**, and its “no Lean runtime in this environment” statement describes its author's historical environment. This session has a real checkout and a retained Lean executable; the original limitation is not a present global blocker. Preserve the historical text and append a dated reconciliation with actual evidence.

### 4.4 “No checks” is too broad

The PR description says the commit status has no checks. The precise observation is that the **legacy status collection is empty**. There is a successful GitGuardian check run at H and three queued external check suites with no runs. None is mathematical proof verification. The corrected report should use these channel-specific statements.

### 4.5 Later actual Agent #1 repaired execution: reusable exact-H evidence

After the initial platform inspection, root made Agent #1's shared raw bundle available. This reviewer read the original and repaired scripts, their exact diff, the independent infrastructure review at `/workspace/scratch/7efd48098de6/pr177-review/verifier-repair-review.md`, both execution receipts, the generated `ProjectAudit.lean`, and the actual audit output. Programmatic full-log parsing and digest verification cover all 39 commands across both runs, all 19 source identities in each run, and every one of the 1,453 unique theorem audit entries.

The executed repair changes three lines: it admits `?` in the existing anchored `NAME` identifier-tail classes, and explicitly adds `--trust=0` to both source-module and generated-audit invocations. Its exact script SHA-256 is `b3108555ed0a3eee6a339ca7346f85ad2636c5008e250c675bf843542db7500f`; patch SHA-256 is `1a7da925535cc670ce7e1b536d7da3ad722471e9eb7719621e2a6c0bd4edd540`. The independent reviewer approved those exact bytes for isolated verification. Allowing `?` globally is broader than this reviewer's optional endpoint-only proposal, but the pattern remains anchored, components remain nonempty with controlled starts, command execution uses argv arrays, and safe path checks remain. No concrete security or correctness defect was found in the executed repair, and this stylistic difference is not a blocker.

`trust0-run-001/verification.json` records source H, `source_tree_clean=true`, registry SHA-256 `791d9d1595c50de05ed044e8d1186313a1c78c643280cf64fd794c6bc0cf6e83`, overall/project PASS, and `repository_wide_pass=false`. Every one of its 19 module invocations and the additional ProjectAudit invocation has `--trust=0 -j1 -DElab.async=false` and exit 0. The audit contains 1,453 unique theorem constants with union `[Classical.choice, Quot.sound, propext]`; parsing every recorded axiom list finds no other theorem dependency. The new seven modules account for **115** theorem constants: DFA 13, Horn 6, Checker 20, Alphabet 27, Boolean 24, Relation 23, Arithmetic 2. These are the actual current counts; they should supersede the unarchived historical summary for this exact run without fabricating an explanation for its 128/1,445 totals.

The audit records 20 compiler-generated unsafe implementation axioms, including two generated BooleanDFA `toDFA` implementation placeholders. These are separately listed in the raw report and not found in the accepted theorem-axiom union. The pending safe-definition/literal-endpoint supplement must assess the executable-declaration coverage and classify those placeholders; this review does not silently treat the theorem-only audit as that supplement.

`agent1-evidence-readback.json`, `agent1-observed/`, and the executed `validate_evidence.py` / `validation-replay.json` retain this readback's exact findings and selected raw snapshots. These are readbacks of Agent #1's actual execution, not a second Agent #9 compiler run. Root retains responsibility for publishing Agent #1's complete raw bundle and finishing the supplemental review. A third unchanged closure build is unnecessary.

## 5. What the original canonical verifier actually guarantees

The original script SHA-256 is `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`.

Its useful gates are substantial: a new output directory; supported registry schema and fixed allowed-axiom list; recorded actual Git HEAD; pinned module SHA-256 and Git blob identities; comment/string-aware forbidden-token scan; exact declared-import match; rejection of unregistered nonstandard imports; available pinned-runtime standard imports; acyclic exact selected-root closure; a fresh isolated source directory and `LEAN_PATH`; official-version string check; compiler/runtime file hashes checked again afterwards; sequential source compilation; all registered endpoints checked; module-origin enumeration of every theorem in the selected source closure; transitive `Lean.collectAxioms` checks against `propext`, `Classical.choice`, and `Quot.sound`; rejection of safe custom axioms; complete-count checks; source/build snapshot identity checks after execution; preserved command/log/hash/exit receipts; and explicit refusal to call an incomplete global catalogue a repository-wide PASS.

Its material limits are:

- It **does not pass `--trust=0`** to compilation or audit. The registry's toolchain argument metadata is not used to add that option.
- It records `source_tree_clean` but does **not reject false**; it also records actual HEAD without comparing it to an externally expected H. External before/after exact-HEAD and tracked-clean checks are required for the intended exact-source claim. Untracked files are not included in that cleanliness field, although the selected source hashes still bind the files copied for this scope.
- It checks only selected source closure, not all of main, all historical archives, or every accepted project.
- Its module-origin audit analyzes `.thmInfo` declarations and rejects safe `.axiomInfo`; it does not exhaustively collect dependencies of safe definitions. Unsafe implementation axioms are reported, not automatically forbidden. The planned safe-definition audit addresses this separate coverage question.
- `#check` validates endpoint existence/typechecking; literal `#print axioms` adds inspectable endpoint evidence. Existing theorem-origin collection already gives transitive theorem-axiom checks when it actually runs.
- Version text and binary hashes record identity; release provenance still depends on the runtime acquisition evidence. The exact binary at `/tmp/p196-agent5-lean/lean-4.19.0-linux/bin/lean` hashes to `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`, matching the retained author compiler hash. This review did not independently repeat the runtime download authentication.
- Its report hardcodes `agent: Agent #1`. Preserve the original receipt and identify the actual operator separately; do not rewrite a historical receipt's identity to imply another execution.

The reviewed three-line `lean-trust-zero` launcher transparently executes that actual binary with `--trust=0` prepended and forwards `"$@"` unchanged. It is a reasonable narrow execution strengthening if its bytes and the actual runtime bytes are both pinned and retained. Its SHA-256 is `6bc1c6c34f3b36ad75f3b78dec9a566733cd38a8d8eb399c56402571c8d524f5`. The script's compiler manifest includes both the supplied launcher and `runtime/bin/lean`, so a report can distinguish them. **Launcher status: NOT_RUN by Agent #9.** Do not call the launcher the original compiler executable.

An audit-only continuation against Agent #1's fresh objects may avoid a duplicate build if all source/object identities and isolated-directory continuity are established, the original audit is faithfully regenerated, and strict actual audit execution is retained. It must remain a separately labeled continuation; the original canonical result stays FAIL. It cannot change the fact that earlier source-compilation argv omitted trust zero. If a fresh strict source rebuild is the required obligation, Agent #1's already-proposed reviewed strict run is justified and should be reused. Full conditions and limits are in `ENDPOINT_VALIDATOR_REPAIR.md`.

## 6. GitHub evidence and observable platform gates

The retained API snapshots are timestamped individually. No negative conclusion here is based solely on a `pull_request`-only workflow helper.

| Channel | Observed result at H | Meaning |
|---|---|---|
| PR state | Open, draft=true, mergeable=true, mergeable_state=clean | Draft still needs an actual Ready operation once qualified; clean is not proof acceptance |
| Formal review submissions | Empty, including the second page | No actual APPROVED or CHANGES_REQUESTED submission to reuse |
| Inline review comments | Empty | No observed inline objection; not proof of semantic review |
| Requested reviewers/teams | Empty | No platform review request presently recorded |
| Legacy combined status | state=pending, total_count=0, statuses=[] | Empty collection, not a failed or queued test |
| Check runs | One: GitGuardian Security Checks, completed/success | Security scan only; six commits scanned |
| Check suites | GitGuardian success; Vercel, Cloudflare Workers and Pages, Claude queued with zero check runs | Report actual queue states; no basis to invent mandatory math gates from them |
| Actions by exact head, all events | total_count=0 | No actual Actions run returned for H across event types |
| Actions by exact branch, all events | total_count=0 | No branch run returned |
| Synthetic merge commit channels | Zero check runs, zero legacy statuses, zero Actions runs | No merged-tree execution evidence from these channels |

There are 39 workflow files in the exact checkout, so “no workflow exists” would be false. The generic workflow collection endpoint was rejected by the connector's allowlist; that tool limitation is preserved. The exact-head, branch, and merge-commit Actions run queries succeeded and are the narrower observable evidence.

The `branches/main` read reports `protected=false`, protection `enabled=false`, status-check enforcement `off`, and empty required contexts/checks. Repository rulesets, including parents, returned an empty list. The admin-only branch-protection read returned 403 `Resource not accessible by integration`; an attempted branch-rules route was rejected by the connector allowlist. These limits must not be described as absent protections discovered through an administrative read, nor as a merge prohibition.

Repository metadata reports `push=true`, `admin=false`, and all three merge methods enabled. No observable platform rule requires an additional approval or merge queue. Project-required independent review still applies. The ordinary guarded merge endpoint, used by the acknowledged main writer after actual gates pass, remains the correct way to enforce any remaining platform restriction; no bypass or administrative mutation is proposed. PR author account is `taco-jpg`; the current coordination comments are from `sodium-qed`. Agent numbers alone do not establish account independence or reviewer eligibility.

## 7. Acceptance disposition and next concrete actions

**Do not merge H on the present author summary or this evidence review alone.** The actionable gaps are precise:

1. Preserve and publish the now-inspected Agent #1 original FAIL and independently reviewed repaired strict PASS. Finish/reconcile the planned safe-definition and literal-endpoint supplement using those fresh verified objects. The exact-H theorem build/audit obligation is satisfied by that reusable execution; do not launch a third unchanged closure build.
2. Correct the stale author-registry endpoint through Agent #107 or an acknowledged narrow handoff. Keep original registry bytes and avoid any mathematical source changes for this metadata repair.
3. Obtain and retain the separately assigned semantic review and combine it with the inspected exact-source execution evidence. Reuse valid existing source-bound evidence rather than creating a duplicate reviewer gate.
4. Reconcile historical “reported-only,” unavailable-runtime, no-checks, and canonical-pending statements in dated English delivery records. Preserve original author evidence and failure history.
5. Perform the actual Ready transition once review readiness is established. Refresh H/B, checks, review applicability, and the intended combined tree before the acknowledged main writer makes the guarded merge. Preserve the source history and inspect remote/post-merge results.

The exact conditional scope remains appropriate: a given finite Horn/Boolean certificate implies arbitrary-length closure and a real reverse-add step. This contribution does not claim a concrete safe certificate, formalized solver correctness, or resolution of 196. No concrete instance should be demanded merely because the result is conditional.

No source content has been lost, no active failed proof has been hidden as an archive, and no missing platform check has been fabricated. The source-specific report and exact repair proposal are handed to Agent #9's root delivery owner for publication and continued integration; a sent report is not an accepted external ownership handoff or a merge.

## 8. Evidence index

- `api/`: exact API payload snapshots with retrieval times and request URLs, including failed visibility attempts.
- `source/`: full added-file snapshots, all Git-blob verified.
- `source-identities.json`: all 75 exact path identities.
- `full-pr-diff.patch`: complete added-file patch snapshot assembled from the fully inspected API patches.
- `source-binding-check.json`: actual checkout identity, cleanliness, 19-module hash checks, compiler/launcher hashes, and retained shallow-checkout limitations.
- `retained-evidence-integrity.json`: all author attempt bindings, recorded statuses, command coverage, and both manifest validations.
- `endpoint-name-validation.json`: original validator's exact endpoint inventory results.
- `original-verifier.py`, `verifier-endpoint-fix.py`, `endpoint-validator.patch`: unchanged original and isolated proposal.
- `endpoint-validator-tests.json`, `patch-application-check.json`: actual Python-only and nonmutating patch checks.
- `ENDPOINT_VALIDATOR_REPAIR.md`: repair rationale and audit-only continuation constraints.
- `agent1-observed/` and `agent1-evidence-readback.json`: selected original/strict-run raw snapshots, exact executed repair, independent infrastructure review, and actual readback integrity results.
- `validate_evidence.py` and `validation-replay.json`: preserved executed Python-only validation program and PASS receipt; no compiler invocation or source mutation.

## Appendix: exact changed paths

All paths below are additions; no deletion, modification, or rename occurs in the reviewed PR diff.

| # | Added path | Lines | Bytes |
|---:|---|---:|---:|
| 1 | `proofs/Agent107DFA.lean` | 74 | 2697 |
| 2 | `proofs/Agent107DFAAlphabet.lean` | 106 | 3546 |
| 3 | `proofs/Agent107DFAArithmetic.lean` | 44 | 1918 |
| 4 | `proofs/Agent107DFABoolean.lean` | 134 | 5405 |
| 5 | `proofs/Agent107DFAChecker.lean` | 107 | 3974 |
| 6 | `proofs/Agent107DFAHorn.lean` | 55 | 2291 |
| 7 | `proofs/Agent107DFAHorn.registry.json` | 114 | 4858 |
| 8 | `proofs/Agent107DFARelation.lean` | 133 | 5322 |
| 9 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/README.md` | 33 | 3765 |
| 10 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/alphabet-001/Agent107DFAAlphabet.lean` | 106 | 3546 |
| 11 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/alphabet-001/compiler.stderr.log` | 0 | 0 |
| 12 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/alphabet-001/compiler.stdout.log` | 11 | 910 |
| 13 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/alphabet-001/execution.json` | 21 | 1165 |
| 14 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/alphabet-README.md` | 45 | 2137 |
| 15 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/alphabet-run.py` | 48 | 2159 |
| 16 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/arithmetic-001/Agent107DFAArithmetic.lean` | 44 | 1918 |
| 17 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/arithmetic-001/compiler.stderr.log` | 0 | 0 |
| 18 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/arithmetic-001/compiler.stdout.log` | 2 | 161 |
| 19 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/arithmetic-001/execution.json` | 21 | 1236 |
| 20 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/arithmetic-README.md` | 47 | 2015 |
| 21 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/arithmetic-run.py` | 48 | 2214 |
| 22 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/boolean-001/Agent107DFABoolean.lean` | 134 | 5405 |
| 23 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/boolean-001/compiler.stderr.log` | 0 | 0 |
| 24 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/boolean-001/compiler.stdout.log` | 11 | 1050 |
| 25 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/boolean-001/execution.json` | 21 | 1054 |
| 26 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/checker-001/Agent107DFA.lean` | 74 | 2697 |
| 27 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/checker-001/Agent107DFAChecker.lean` | 107 | 3946 |
| 28 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/checker-001/compiler.stderr.log` | 0 | 0 |
| 29 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/checker-001/compiler.stdout.log` | 11 | 619 |
| 30 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/checker-001/execution.json` | 51 | 4444 |
| 31 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/checker-002/Agent107DFA.lean` | 74 | 2697 |
| 32 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/checker-002/Agent107DFAChecker.lean` | 107 | 3974 |
| 33 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/checker-002/CheckerModuleOriginAudit.lean` | 28 | 1140 |
| 34 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/checker-002/audit.stderr.log` | 0 | 0 |
| 35 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/checker-002/audit.stdout.log` | 21 | 1762 |
| 36 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/checker-002/compiler.stderr.log` | 0 | 0 |
| 37 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/checker-002/compiler.stdout.log` | 6 | 451 |
| 38 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/checker-002/execution.json` | 67 | 5073 |
| 39 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/checker-FILES.json` | 66 | 2249 |
| 40 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/checker-README.md` | 57 | 4027 |
| 41 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/checker-freeze.json` | 53 | 1774 |
| 42 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/checker-run.py` | 104 | 5561 |
| 43 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/defs-001/Agent107DFA.lean` | 74 | 2697 |
| 44 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/defs-001/compiler.stderr.log` | 0 | 0 |
| 45 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/defs-001/compiler.stdout.log` | 5 | 353 |
| 46 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/defs-001/execution.json` | 21 | 860 |
| 47 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/path-001/Agent107DFAHorn.lean` | 53 | 2215 |
| 48 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/path-001/compiler.stderr.log` | 0 | 0 |
| 49 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/path-001/compiler.stdout.log` | 11 | 749 |
| 50 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/path-001/execution.json` | 21 | 1137 |
| 51 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/path-002/Agent107DFAHorn.lean` | 55 | 2291 |
| 52 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/path-002/compiler.stderr.log` | 0 | 0 |
| 53 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/path-002/compiler.stdout.log` | 2 | 168 |
| 54 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/path-002/execution.json` | 21 | 1137 |
| 55 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/path-README.md` | 41 | 2039 |
| 56 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/path-run.py` | 48 | 2127 |
| 57 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/relation-001/Agent107DFA.lean` | 74 | 2697 |
| 58 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/relation-001/Agent107DFARelation.lean` | 134 | 5336 |
| 59 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/relation-001/compiler.stderr.log` | 0 | 0 |
| 60 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/relation-001/compiler.stdout.log` | 33 | 1350 |
| 61 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/relation-001/execution.json` | 51 | 4451 |
| 62 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/relation-002/Agent107DFA.lean` | 74 | 2697 |
| 63 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/relation-002/Agent107DFARelation.lean` | 133 | 5322 |
| 64 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/relation-002/RelationModuleOriginAudit.lean` | 28 | 1142 |
| 65 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/relation-002/audit.stderr.log` | 0 | 0 |
| 66 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/relation-002/audit.stdout.log` | 48 | 2645 |
| 67 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/relation-002/compiler.stderr.log` | 0 | 0 |
| 68 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/relation-002/compiler.stdout.log` | 9 | 991 |
| 69 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/relation-002/execution.json` | 67 | 5082 |
| 70 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/relation-FILES.json` | 66 | 2269 |
| 71 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/relation-README.md` | 75 | 4413 |
| 72 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/relation-freeze.json` | 81 | 2499 |
| 73 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/author/relation-run.py` | 104 | 5577 |
| 74 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/verification/Agent107DFAHorn.verify-registry.json` | 211 | 8162 |
| 75 | `proofs/contributions/agent-107/dfa-horn-closure-20261016/verification/EXACT-HEAD-HANDOFF.md` | 25 | 2253 |
