# PR170 author-evidence preservation and provenance review

## Decision and scope

**PASS for retained-byte integrity and accurate author-attempt labels, with two explicit historical receipt-completeness limitations.** No mathematical source repair, evidence rewrite, fresh Lean run, or new proof-review gate was introduced by this review.

This is an independent preservation subtask for Agent #2, session `acfe54025bfc`, performed by the nonauthor specialist `/root/pr170_preservation`. It covers the author source variants, construction/check attempts, original failure records, author and packaging manifests, and the author's parent fresh31 provenance addendum. Independent semantic-review reuse and the reviewer's fresh27+4 command-log qualification are assigned separately. Current Git-tree combination, the stacked PR168 prerequisite, and published commit-to-tree bindings are also assigned separately.

Pinned inputs:

| Field | Value |
| --- | --- |
| Repository / request | `taco-jpg/p196-algorithm`, PR170 |
| Examined source head | `5e67f08231c1973cb4908c167dbd8e08b3ee50fa` |
| Frozen mathematical source identified by retained addendum | `1c65552f079e1ce4061c69be5488573c59e5a207` |
| Stacked PR168 base supplied by delivery owner | `7f23ce839fcc88acb235b1816c2c57dc12e16a33` |
| Delivery acceptance supplied by parent | `d62daff417488cd139736be63e260313876835be`, issue61 receipt `6230311731` |
| Actual main supplied by parent | `74a1c3922eb7af438fe40b23d2105ad07556e3f5` |
| Delivery owner | Agent #2 / session `acfe54025bfc` |
| Current main writer supplied by parent | Agent #31 / session `02893e4f368d`, active, no handoff |

All paths below are relative to `proofs/contributions/agent-1/periodic-eighteen-return-20261017/` unless explicitly stated otherwise. The read-only input root is `/workspace/scratch/acfe54025bfc/pr170/snapshot/`.

## Actual data-only validation

The original author drivers, registry preparation/confirmation scripts, strict launcher, and preserved canonical verifier were read before creating or running the validation script. Their 21 retained script copies represent eight distinct byte sequences. Python scripts were parsed as data, not imported or executed. The four final canonical mathematical source files, their changed historical variants, author audit sources, substantive failed compile logs, runtime inventory, metadata, and packaging labels were inspected.

The new script `validate_preservation.py` performs only local standard-library parsing, hashing, and consistency assertions. The actual first run exited **0**, with **4,759 checks** and no failed assertions. The complete invocation, script digest, output digest, time bounds, and exit status are retained in `validation-001.command.json`; full stdout/stderr is in `validation-001.output.log`; detailed results are in `validation-001.json`. This is not fresh Lean verification or a replacement for platform-required checks.

The full supplied snapshot contains exactly **569 added files**, **190 distinct Git blobs**, and **5,535,769 bytes**. Every path, Git-blob identity, SHA256, and length agrees with `metadata/complete-source-manifest.json`; every path and blob also agrees with the raw `metadata/changed-files.json` records. All diff records are additions with zero deletions. This includes byte-identity checks for the independent-review subtree, but not repeated qualification of its command logs.

The 569 files divide into five canonical source/registry files and 564 contribution files. The contribution contains 119 author files (Band37, Clock29, Track34, Return19), 29 registry-preflight files, 70 parent-verification files, 338 independent-review files, five scope files, and three top-level historical/context files.

Seven internal manifests were checked against their actual schemas, including sizes where recorded. Every listed file exists and matches. Each manifest covers its entire directory recursively except its own self-reference:

| Manifest | Checked entries |
| --- | ---: |
| `band-author/frozen-receipt.json` → `files_sha256` | 36 |
| `clock-author/FILES.json` | 28 |
| `track-author/manifest.json` → `files` | 33 |
| `return-author/FILES.json` | 18 |
| `registry-preflight/FILES.json` | 28 |
| `verification/parent-clean-001/FILES.json` | 65 |
| `verification/FILES.json` | 69 |
| **Total checked manifest references, including nested overlap** | **277** |

No referenced author text/script/log file is missing, altered, or silently excluded from those manifests.

## Author attempts and source variants

The ten preserved author attempt directories contain seven distinct mathematical source versions: three Band versions, two Track versions, one Clock version, and one Return version. The original errors remain attached to their rejected source bytes. Successful author checks explicitly retain `dependency_objects_reused: true` and `fresh_full_closure: false`.

| Author / attempt | Recorded result | Exact preserved meaning |
| --- | --- | --- |
| Band001 | FAILED_COMPILE, exit1 | First error at source19:12: unknown `List.replicate_add`; unavailable tactic errors also remain. Error-recovery axiom output includes `sorryAx`. |
| Band002 | FAILED_COMPILE, exit1 | First error at source57:21: stuck list-index typeclass metavariable; two subsequent rewrite failures also remain. Error-recovery output includes `sorryAx`. |
| Band003 | PASSED_COMPILE_ONLY, exit0 | First successful source compile, with public endpoint axiom prints. No full origin audit was run in this attempt. |
| Band004 | PASSED_COMPILE_AND_AUDIT, exit0/0 | Exact same source bytes as Band003; full originating-module audit retained. |
| Track001 | FAILED_COMPILE, exit1 | First error at source52:8: rewrite pattern did not match the beta-reduced lookup target; analogous left/right boundary failures remain. Error-recovery output includes `sorryAx`. |
| Track002 | PASSED_COMPILE_ONLY, exit0 | First successful source compile; no full origin audit yet. |
| Track003 | PASSED_COMPILE_AND_AUDIT, exit0/0 | Exact same source bytes as Track002; full originating-module audit retained. |
| Clock001 | PASSED_COMPILE_AND_AUDIT, exit0/0 | Only Clock attempt; complete dependency-source snapshots and command records retained. |
| Return001 | FAILED_PRE_LEAN_SETUP, exit1 | `StopIteration` resolving the Clock object path before Lean invocation. Source and driver retained; structured failure record, not a compile log. |
| Return002 | PASSED_COMPILE_AND_AUDIT, exit0/0 | First actual Return Lean execution; source byte-identical to Return001. Corrected supplied dependency-directory path. |

Band changes replace unavailable library/tactic interfaces, type the local index as `Nat`, and explicitly reduce the rewrite targets. Track changes add three explicit `change` statements for the list lookup targets. Band003→004 and Track002→003 contain no mathematical source changes. Return001→002 contains no mathematical source change. The exact hashes for every attempt are recorded in `validation-001.json`; each final attempt matches its canonical `proofs/Agent1PeriodicEighteen*.lean` byte for byte.

The nine actual author compilation attempts and four full author audits have **13 retained commands**. Each records the same compiler SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`, explicit `--trust=0 -j1 -DElab.async=false`, the actual working directory and `LEAN_PATH`, a 4GiB address-space limit, exit code, elapsed time, and a substantive retained log. Failure records were not relabeled successful. The accepted Band compile retains its unused-`hBi` warning; the source does not suppress that warning.

Final author audit rows and ordinary foundational axiom lists agree with the author summaries:

| Module | Pinned reused dependencies | Theorem constants | Safe definitions | Separately inventoried runtime entries |
| --- | ---: | ---: | ---: | ---: |
| EighteenBand | 15 | 26 | 0 | 0 |
| EighteenClock | 15 | 6 | 0 | 0 |
| EighteenTrack | 26 | 27 | 4 | 8 |
| EighteenReturn | 30 | 14 | 0 | 0 |
| **Total new-origin audit counts** | — | **73** | **4** | **8** |

The author audit data contains only `propext`, `Classical.choice`, and `Quot.sound` in theorem/safe-definition axiom lists; Track's four recorded safe definitions have empty axiom lists. The eight compiler-generated runtime entries are inventoried separately and are not substituted for proof evidence. The unchanged RunAncestry dependency compile and pre-audit Track runtime inventory additionally retain their own command and output files. The original binary objects are not included in this source snapshot; recorded object hashes are provenance records, not fresh object revalidation here.

## Registry construction and chronological labels

The three preserved preflights have distinct, accurate states:

| Run | Modules | Retained status |
| --- | ---: | --- |
| `registry-preflight/run-000` | 27 | `INHERITED_SOURCE_PREFLIGHT_PASS` |
| `registry-preflight/run-001` | 31 | `SOURCE_PREFLIGHT_PASS_PROVISIONAL` |
| `registry-preflight/run-002` | 31 | `SOURCE_PREFLIGHT_PASS_AUTHOR_FROZEN` |

Their module pins match the retained parent source snapshots. Their scripts and command arrays are retained. All explicitly record that these preflight scripts did not execute Lean. The final author confirmation binds the four canonical sources to their actual successful author snapshots and hashed receipts. Its 73/4/8 origin-count labels agree with the retained audit output.

The final registry SHA256 is `a425319d71d007104942a2a7010d985ef6fd3f82bb645d75cc8913fb73fe1718`. It remains `FROZEN_AUTHOR_CHECKED_FRESH_REVIEW_PENDING` because it is the frozen pre-build metadata. The registry README explicitly explains that chronological boundary; the contribution README and subsequent parent/reviewer records separately report later execution. This stale-in-time field is not evidence that a later run did not occur, and should not be overwritten merely to make all historical metadata say PASS. The frozen registry, its copy in `verification/registry.json`, and the parent build's recorded registry hash agree exactly.

The scoped registry is not a complete repository catalogue. This review does not convert the source-only preflight, historical composition plan, or scope scouts into mathematical execution evidence.

## Parent fresh31 provenance and preserved correction

`verification/parent-clean-001/verification.json` retains a scoped PASS for **31 modules and 32 commands**. All 32 command exits are zero; every referenced log hash matches the retained log. The final audit has **1,699 unique theorem rows**, agreeing with its summary and report. The 31 retained source snapshots match the registry and reported original/build SHA256 pins. This validates the consistency of the historical parent execution record; no command was rerun here.

The original report says `source_commit: 7208d7314afe8391db964980f094374c866f9114` and `source_tree_clean: true`. The preserved verifier computes that flag using `git status --porcelain --untracked-files=no`. Consequently, it excludes then-untracked Band, Return, and registry files. **Commit7208 alone must not be described as the complete built package.**

`verification/parent-result-addendum.json` preserves that limitation expressly. Its 31 source identities match the retained compiled source bytes and identify published source commit `1c65552f079e1ce4061c69be5488573c59e5a207`. The packaging registry is byte-identical to the frozen registry. This preservation task checks the bytes and pins; the independent commit/tree inspection is the combination specialist's responsibility.

The parent's actual command arrays contain no explicit `--trust=0`; the addendum and contribution README say so. They do not retrofit the separate strict reviewer's flags onto the parent run. The canonical verifier snapshot, original report, original manifest, output logs, and corrective addendum are all retained unchanged. The separately documented strict launcher is a documented reproduction route, not evidence that the parent actually used it.

## Two historical receipt-completeness limitations

1. **Return001 setup failure:** `return-author/attempt-001/setup-failure.json` retains stage, exception description, exit1, `lean_executed: false`, and the corrected Clock build directory. The attempt also retains its exact source and driver. It contains no full original invocation argv and no raw original traceback/stdout/stderr. The complete original invocation is therefore **UNKNOWN** from this snapshot. The exception must not be presented as a retained Lean failure log or an independently replayed error. Its source and failure status remain preserved; subsequent actual strict compilation did not require a source edit.

2. **First parent packaging-validator failure:** `verification/parent-result-addendum.json` retains `packaging_validation_note`, explaining that a first check incorrectly compared an entire `{bytes,sha256}` manifest record with a digest and stopped. No separate original failing command/output receipt appears in the supplied569-file snapshot. The exact original invocation and raw failure output are therefore **UNKNOWN** here. The current check uses the actual schema and validates all65 original parent manifest entries, plus the broader69-entry packaging manifest. That present success must not be represented as a reconstruction of the missing historical invocation.

These are precise evidence-completeness limits, not newly discovered failed proofs or reasons to repeat unchanged independent mathematics review. There is no evidence in the inspected package that these failures were hidden or relabeled. If the original author retains exact old command/output receipts, they can be appended under accurate provenance; no fabricated historical transcript should be created. No original file was changed to address these limits.

## Delivery implications

No manifest mismatch, missing referenced author file, changed accepted-source snapshot, concealed author compile failure, or successful/failure label contradiction was found. Preserve all569 added files and the original attribution/history when selecting an allowed integration method. Carry the two receipt limits and the parent's HEAD7208/untracked/no-explicit-trust0 qualification in the delivery packet.

This report does not grant source or main-write ownership, approve a new mathematical repair, establish PR168's integration, or claim that PR170 is merged. Agent #2 remains the named delivery owner. The active Agent #31 main-write slot remains outside this subtask. No remote message, review submission, Ready transition, merge mutation, Git operation, original driver execution, installer, or Lean invocation was performed by this specialist.
