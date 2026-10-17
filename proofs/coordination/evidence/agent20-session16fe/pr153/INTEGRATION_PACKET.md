# PR153 exact-source integration packet

## Disposition and immediate action

**PASS: exact-source semantic evidence reuse, independent fresh compilation of 13 modules, full module-origin and mathematical dependency audit, corrected complete literal reporting, and current-base source/preservation rebinding.** The remaining delivery operation is the ordinary guarded integration by the acknowledged main writer, after refreshing the live source/base/role/check state. Readiness transitions, review identifiers, publication readback and actual merge outcomes are recorded separately in `DELIVERY_STATUS.json` and the accepted coordination task.

Agent #20/session `16fe9eef625c` owns this integration delivery. Agent #52/session `04d7e624b3b0` retains source authorship and source-write ownership. At the recorded ownership refresh, Agent #31/session `02893e4f368d` remained the ACTIVE sole main writer for PR104. Agent #1/session `7efd48098de6` was the queue coordinator awaiting an acknowledged main handoff. This packet does not assign the main slot to either Agent20 or Agent1.

| Field | Exact value |
|---|---|
| Repository / PR | `taco-jpg/p196-algorithm` / [PR153](https://github.com/taco-jpg/p196-algorithm/pull/153) |
| Reviewed source H | `6641b1ea166fcef0e6f9d1fa23afed7b1f6b8a82` |
| Tested direct main ref B | `74a1c3922eb7af438fe40b23d2105ad07556e3f5` |
| Actual combined tree T | `6cfa3582ce49216a0fc055f42dba84532a608407` |
| Incoming contribution | 13 added files, 114,502 bytes |
| Mathematical compilation | 11 unchanged local dependencies plus 2 new modules |
| Actual independent completion | `PASS_WITH_REUSED_FRESH_BUILD` |
| Completion report SHA-256 | `5c77f804527ab63345c73662e95df260f1f94d38ef8816e68bc4d96d0acb5dd5` |
| Permitted merge method | Ordinary `merge`, preserving published history |
| Main-write claim by this session | None |

The task is `proofs/coordination/tasks/agent20-session16fe-pr153-evidence-20261017.json`. Its delivery extension was accepted and read back at commit `3db8494e7b940d6263f26248a497afc393c186f3`, task blob `18608edcee0914524f017dda041c38d743187c27`. The earlier missing-auditor evidence request remains historically unacknowledged; the precise evidence gap was subsequently completed in this independent session. It is not an extra source-owner permission gate for nonsource review and readiness actions.

## What the mathematics establishes

For every positive ordinary decimal seed `n` and every natural threshold `B`, the set of times at which the unchanged decimal reverse-add orbit has digit sum greater than `B` has both lower asymptotic density and lower Banach density at least

```text
1 / (DecimalUniformEscape.sharpDigitSumEscapeBound B + 1)
```

with the denominator interpreted in the reals. The generic analytic result derives the density bound from the existing translated interval-count theorem. The decimal specialization applies the existing sharp digit-sum window bound through the unchanged Agent9 count interface. The published endpoints also include positivity consequences and two unconditional seed 196 specializations.

The Banach definition takes the liminf of the infimum over **all natural interval starts**, with intervals `[s,s+N)`. Length zero has density zero. The implementation proves the required boundedness and a real epsilon estimate whose eventual threshold is uniform over the translate. The asymptotic definition is the corresponding prefix liminf. These results establish lower densities; they do not assert existence of an ordinary density limit, pointwise digit-sum divergence, palindrome avoidance, or a solution of the 196 problem.

The exact source and contract match the retained independent [semantic contract review](https://github.com/taco-jpg/p196-algorithm/blob/6641b1ea166fcef0e6f9d1fa23afed7b1f6b8a82/proofs/contributions/agent-52/digit-sum-density-20261016/review/semantic/CONTRACT_REVIEW.md) and [implementation review](https://github.com/taco-jpg/p196-algorithm/blob/6641b1ea166fcef0e6f9d1fa23afed7b1f6b8a82/proofs/contributions/agent-52/digit-sum-density-20261016/review/semantic/IMPLEMENTATION_REVIEW.md). Those qualifying reviews were reused. No mathematical source repair or gratuitous replacement semantic review was introduced.

## Actual independent execution and trust boundary

The complete execution report is `VERIFICATION_REPORT.md`; the lossless evidence archive retains the actual sources, commands, generated audit drivers, raw stdout/stderr, return codes and manifests.

| Verified obligation | Observed result |
|---|---:|
| Fresh local modules, initially empty project-object directory | 13 / 13 exit 0 |
| Compiler flags on every compilation and audit | `--trust=0 -j1 -DElab.async=false` |
| Source/object external import closure, including the Lean audit infrastructure | 2,665 modules |
| Local module-origin declarations | 2,500 |
| Module-origin theorems, including private and generated declarations | 1,483 |
| Safe mathematical roots | 1,658 |
| Transitive mathematical closure constants | 8,340 |
| Published endpoint types and axiom reports | 29 / 29 |
| Safe-definition bodies and axiom reports | 161 / 161 |
| Literal axiom outputs, with exact multiplicities | 1,673 |
| Pretty-printer truncation markers | 0 |
| Watched input hashes checked before and after continuation | 5,386 |

The permitted theorem-axiom union is exactly `{propext, Classical.choice, Quot.sound}`. The safe dependency traversal covers types, mathematical definition/proof/opaque bodies, inductive families, constructors and recursor rules. Unsupported axioms, `sorryAx`, compiler-trust reduction constants, and unsafe or partial mathematical dependencies are rejected.

The complete local inventory separately records 806 generated unsafe definitions, 16 unsafe implementation axioms, and 20 generated partial definitions. These 842 implementation helpers are outside the accepted mathematical closure. They are preserved in the inventory and are not silently accepted as proof dependencies. Implementation redirections and extern annotations are recorded separately from mathematical bodies. The two new modules have 29 public theorem endpoints and three additional generated theorem constants, all covered by the full origin census.

The official Lean runtime is version 4.19.0, release commit `6caaee842e94`. Its executable SHA-256 is `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`; its principal shared library is `2ab605c74c78f9ba4431a7b5305a4b28a9071d8a826f223eb14fe5530f78e14d`.

Mathlib source is pinned to `c44e0c8ee63ca166450922a373c7409c5d26b00b`, with manifest SHA-256 `5c6421b650bc87a2427a892a39e5522dc44543ca4ac1bd6e9f08d536c044a752`. The retained workflow artifact and a 76-file canonical cache supplement supplied the external objects. All 7,265 source files, eight dependency commits and 29 protected configuration files were checked. Source-hash cache keys match the pinned inputs; producer comments name the requested commit for 68 supplement archives and an earlier producer for 8. Full provenance is in `RUNTIME_EVIDENCE.md`. External standard-library and Mathlib objects were reused; this is not a fresh build of Mathlib or the entire repository.

## Failures, repairs and precise evidence reuse

The published author package contains 13 files and a 46-member development archive. Every member and manifest entry was verified. That archive preserves successful author development and its failed attempts. It contains no raw original independent 13-module run, no original auditor API-error source/log, and no completed portable independent verifier. The bounded recovery search and request are documented in `EVIDENCE_QUALIFICATION.md` and the supporting [Agent18 diagnosis](https://github.com/taco-jpg/p196-algorithm/blob/14b972d3ca4b2dd862d9a5dc0f6eafe1d3892474/proofs/coordination/reviews/agent18-sessionc6d78d258d21/pr153-support/DIAGNOSIS.md). The new execution is recorded as a new independent run, without relabeling it as recovered historical evidence.

| Stage | Retained outcome and resolution |
|---|---|
| Initial static verifier | External-source text scanning mishandled character/interpolated strings. Exact failing cases and prior script snapshots are preserved. A reviewed external-header parser correction passed all 13 local and 2,665 external source/import checks. |
| Independent `run-001` | Failed before any compiler command because an unused `Cli` package lacked an object directory. The correction records absent unused package roots while retaining unique source/object checks for every actual import. |
| Independent `run-002` | All 13 mathematical compilations and the full module audit exited 0. The later literal report exited 1 because Lean 4.19 does not recognize `pp.width` and `pp.maxDepth`. Its overall report remains `FAIL`. |
| Literal continuation | Replaced exactly those options with `format.width` and `pp.deepTerms true`. Revalidated all 120 retained run artifacts, 43 original command records/logs, 5,386 watched inputs and 13 exact H source/object pins before and after. Repeated only the literal reporting command; exit 0 and every completeness/axiom check passed. |

The original executed verifier SHA-256 is `2eae51ee30e805c976314d8533345c9fd45fbbdfb6bb76befc1bffd6e439e37f`. The continuation driver is `9c33549cf45b4d51c0468e8e7ea5a2ca0df3d419d3f9e63c39d1a20d62aa004c`. The complete corrected portable reproducer is `5841e26c12f2ceefa672b5d5ef7ae18243fc0872ec2a52d7eb9083d3335e0f06`; it includes the required manifest, audit template and provenance inputs. It was not run as an additional full rebuild. The actual evidence is the preserved fresh 13-module execution plus the separately executed corrected continuation.

Root reviewed the infrastructure before its launches. A genuine independent specialist reviewed the original infrastructure and narrow parser correction. Agent18 separately reproduced the printer defect and validated the exact formatter repair in a neutral fixture; its [scoped repair receipt](https://github.com/taco-jpg/p196-algorithm/blob/a1c66ff82e50d63a1a2f5dbd931e03eb8e7714b7/proofs/coordination/reviews/agent18-sessionc6d78d258d21/pr153-verifier-review/REPAIR_SCOPED_RECEIPT.md) is supplementary evidence. No review is presented as an execution of a different script version.

## Current-base combination and preservation

An independently executed `git merge-tree --write-tree B H` returned exit 0 and T as pinned above. The complete `git diff-tree -r --no-renames B T` contains exactly 13 additions, zero modifications and zero deletions. Every incoming file matches its reviewed blob/SHA-256 and bytes. Every mathematical module in T matches H, its original source revision, and the actual fresh-build staging directory.

At the changed ancestor frontier, 5 repository-root siblings, 3,243 `proofs` siblings and all 33 existing contribution entries retain their exact modes, types and object identities. Equal subtree identities preserve their descendants. These are direct-entry counts, not a fabricated whole-repository file census. All 61 Git commands and 30 captured compiler/audit stream hashes are retained in `COMBINED_TREE_REVIEW.md` and its evidence. This establishes source-byte rebinding to the tested combination; it is not a separate Lean rebuild in a merged worktree.

## Platform observations and writer execution

At the recorded live check, `main` reported `protected:false`, status-check enforcement off, and no repository/parent rulesets. GitGuardian check 117250142395 completed successfully at H. The legacy status endpoint had zero contexts; its aggregate `pending` value was not interpreted as a failed check. Exact-head Actions enumeration had zero runs. The ordinary platform endpoint remains responsible for enforcing any applicable requirements at execution time. No protection or permission setting was changed.

The GitHub account used by this session is also the PR author account. The exact-head formal record is a `COMMENT` with independently produced technical evidence; no eligible separate-account `APPROVE` is claimed or invented as a missing gate.

The acknowledged main writer should:

1. Refresh PR H, the direct main ref, the canonical integration role and current required checks. Confirm this same source is the intended contribution.
2. If B changed, recompute the actual combination and compare the affected source/dependency identities; retain unchanged qualifying proof evidence.
3. Execute the ordinary merge with `merge_method:"merge"` and `expected_head_sha:"6641b1ea166fcef0e6f9d1fa23afed7b1f6b8a82"` while holding the single acknowledged slot.
4. Read back actual PR merged state, merge SHA, main, ordered parents and resulting content/tree, and complete applicable postchecks. Report actual results to the existing delivery task and issue61.
5. Release or explicitly hand off the slot according to the coordination protocol. Age or silence alone does not release it.

If the main writer remains occupied, the external blocker is that specific active role. The executable remedy is merge by the current writer or an acknowledged narrow slot transfer. Revisit on an actual role release/transfer, a merge result, changed H/B, or a new relevant finding/check.

## Preserved publication and reproduction

`evidence.tar.xz.b64`, `PAYLOAD_MANIFEST.json` and `ARCHIVE_MANIFEST.json` preserve the complete research, verifier, failed/successful logs, semantic qualification, combination evidence and runtime receipts. Generated `.olean`/`.pyc` files are explicitly inventoried as reproducible infrastructure exclusions; originals are not deleted. The original author archive is included unchanged. Recovery instructions and a member-by-member verifier accompany the archive. The portable reproducer README gives the exact pinned-runtime invocation and explains the distinction between fresh local compilation and reused external libraries.

Current source ownership, history and prior evidence classifications remain preserved. No main merge is implied by this verification packet; only an actual remote readback can establish integration.
