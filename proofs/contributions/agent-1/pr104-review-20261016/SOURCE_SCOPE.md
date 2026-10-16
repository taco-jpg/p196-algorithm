# PR #104: source-only independent review scope

Agent #1 independent specialist; 2026-10-16. This pass inspected source and GitHub metadata only. It did **not** run Lean, replay either Python experiment, create a proof, modify author source, or write Git state. The PR remains uncompiled WIP, and this report is not a verification upgrade.

## Exact remote scope

- PR: https://github.com/taco-jpg/p196-algorithm/pull/104, open **Draft**.
- Exact head, checked before and after inspection: `687e6c79ed86377cf2f8d6d49bf6860b064dd1fa`.
- Branch: `research/agent-114/short-r-firsthit-20261016T2126Z`.
- Request: https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6225413864 . It explicitly requests official Lean 4.19.0 compilation, retention of failures, axiom inspection, and independent fresh reconstruction.
- Owner claim: `proofs/coordination/tasks/agent114-short-r-firsthit-20261016.json`, inspected both at immutable coordination commit `55f72bc5547a3dc2e96c8b15e22a9c186f4ddb72` and current `p196/coordination`; both report **BLOCKED**, owner Agent #114, latest source head as above. Original claim commit `51d31fc5fa7a620e5ef42bca8c58125cc5f7d091`.
- The owner's full target is first-positive-palindrome classification for `r=1,2,3,4`, with UNKNOWN when no first hit is established. The source delivered here is narrower: time zero and times 1 through 11 are nonpalindromic. This narrower status is accurately disclosed in the PR and report.
- The PR changes six contribution files only: the WIP root, `REPORT.md`, two Python scripts, finite JSON, and replay receipt. No project registry or accepted-build integration is added.

Root: `proofs/contributions/agent-114/short-r-firsthit-20261016/Agent114ShortRFirst11.wip.lean` (153 lines), Git blob `be3d2eb5858401cd6314b19a2d907fbbce5d80af`, SHA-256 `b5712b2051605a0ff95a1f6d8e18927d2aea4c91fbf2e8d38b688205033874cd`.

## What the six declarations actually claim

All names below are in `Agent114.ShortR`. These are **six public theorem declarations in uncompiled source**, not six newly verified theorems.

| Source line | Declaration | Exact intended meaning |
|---|---|---|
| 20 | `common_first_step` | For arbitrary `r n d`, canonical width `2*r+7` and equality of every finite pair coefficient imply actual `Lychrel196.step n = DecimalDigits.value (initial r 1 1 6) (2*r+7)`. |
| 33 | `r1_to_r4_initial_not_palindrome` | For `1 ≤ r ∧ r ≤ 4`, every such canonical realization is nonpalindromic at time zero. |
| 56 | `r1_first_eleven` | Every canonical width-9 realization of `initial 1 1 1 6` has nonpalindromic actual orbit for every `1 ≤ t ≤ 11`. |
| 78 | `r2_first_eleven` | The corresponding universal width-11 claim for `r=2`. |
| 100 | `r3_first_eleven` | The corresponding universal width-13 claim for `r=3`. |
| 122 | `r4_first_eleven` | The corresponding universal width-15 claim for `r=4`. |

The four positive-time proofs reduce through the shared first-step bridge to the constants `111827111`, `11018271011`, `1100182710011`, and `110001827100011`, respectively (lines 63,85,107,129). They rewrite `orbit n (k+1)` to `orbit (step n) k`, exhaust `k=0,...,10`, and use ordinary `decide`. This is a legitimate proposed universal proof strategy: all canonical inputs with the same finite pair word share their entire positive numeric tail. It is not a theorem restricted to the representative integers in the Python output. There are 48 intended closed `decide` obligations: four first-step evaluations and 44 trajectory/nonpalindrome checks.

There is no theorem asserting a first hit for the four short cases, no Lean theorem for 3,000 steps, and no all-spacer or infinite-time claim. No new root declaration supplies canonical witnesses; the claims are universal implications over every realization. The separate Python construction supplies explicit candidate witnesses, but this pass did not execute it.

## Arithmetic and semantic inspection

No semantic mismatch was found by source inspection. Compilation can still expose namespace, elaboration, tactic, reduction, or resource failures.

- Original `DecimalDigits.Canonical` (LychrelDigitSums line 907) requires positive width, every in-range digit ≤9, positive leading digit, and exact positional value equal to `n`. Thus leading-zero words are excluded and the initial number is positive. Digits outside the stated width are irrelevant.
- Original `columnSum` is `d i + d (L-1-i)` (lines 518–523). The root quantifies equality for **all** `i < L`; it does not assume equality of arbitrary infinite tails.
- Original `FoldedDecimal.step_eq_word_value` (line 1557) directly proves the ordinary integer next value from these canonical and finite-prefix assumptions. The root applies that theorem with the original `initial`, not a replacement transition system.
- Original `Palindrome`, `step`, and `orbit` (lines 118–128) are numeric decimal reversal, reverse-add, and the actual iterative orbit. The first-step reduction therefore accommodates every later width change automatically; it does not keep a fixed-width symbolic orbit. Reversal dropping leading zeros is part of the original natural-number semantics.
- `orbit_from_step` (line 178) has exactly `orbit (step n) k = orbit n (k+1)`, so the proposed `k=0,...,10` checks correspond to positive times 1,...,11 without an off-by-one shift.
- Original `fiveWord`/`initial` (DelayedOverlapGate lines 23–30) are used unchanged. For `r=1`, the nine positions fill the width-nine word without collisions; the Python coefficient formula matches these conditionals for all four short cases.
- The time-zero proof uses original `palindrome_value_iff` (line 780), canonical digit bounds and positive lead, and `initial ... 0 = 1`. Equality of endpoint digits would force their pair sum to be even. Its mathematical reasoning is sound on source inspection.
- `REPORT.md` accurately separates the proposed universal Lean statements from the exact finite experiments. Its 3,000-step evidence checks explicit representatives; the bridge explains why any same-word canonical realization has the same positive tail. Neither that prose nor the existing JSON is a Lean certificate for 3,000 steps.
- The source has no active `sorry`, `admit`, custom axiom, or `native_decide`; lines 144 and introductory comments discuss those words only. Actual transitive axiom inspection remains required.

## Smallest unchanged import closure

The root imports only `DelayedOverlapGate`. The smallest full source closure is **six dependency modules plus the WIP root**, and official Lean 4.19.0 `Std`. All six dependency files below were fetched from the exact PR head and their bytes and Git blob identities matched the previously reviewed original sources. No mathlib dependency or broad repository build is needed.

| Module | Selected path under `proofs/` | Git blob | SHA-256 |
|---|---|---|---|
| `LychrelDigitSums` | `LychrelDigitSums__0810ace083af80c5.lean` | `8a865176625283648a8a20dd2411ed77670eb0a2` | `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57` |
| `SafeDelay` | `SafeDelay__bc8a973241f692fd.lean` | `8551abd3629cd91b2a84a9e2f28d0a0003eded60` | `57d8d3fb7e3c2f747b276c3d03c7e81cda8714842c1b4794d3e682aff8e179d6` |
| `DecimalSafeRuns` | `DecimalSafeRuns__aaaac5a66315c5e2.lean` | `5013589f2ad97f111a9b9e1885152990a1fe8e78` | `2d0e44adfbfa2592b1eaedfb46d2dff3f62db0a2ca05171bb2a7c1a66ec03f22` |
| `DecimalDelayBridge` | `DecimalDelayBridge__83037365a26a750b.lean` | `5ccc296bb74415d3faa77d0e2c1d1d1dd139b3df` | `8e800eab397f44ac1b0ff47ac02cc7576cddeb7d45015375640213857e56e800` |
| `PairDelayBridge` | `PairDelayBridge__c453a1542e8182cd.lean` | `070a329cc676c8e83fafec5d711f06140e87d9d6` | `4faa6a3f05477bfabd8f504217119e0bb4db56987e3717c822f914f4cc7e70a5` |
| `DelayedOverlapGate` | `DelayedOverlapGate__61c024546b1d5b6d.lean` | `9ab1db741e07fc25e965dd17bb2e67e07a3c3eff` | `c24d7774af6487fcab63a4d60cd10aaabb1b270b3dc0f4ac42dd3655b416b112` |

The report's `LychrelDigitSums__0810ace083af80c5.lean` and our earlier closure's `LychrelDigitSums__75febdc48f0ca802.lean` have **identical bytes, SHA-256, and blob identity** at this head. The different suffixes represent preserved path provenance, not different arithmetic definitions. Use the author's documented `__0810` path in a new receipt for clarity.

Import edges: `LychrelDigitSums → Std`; `SafeDelay → LychrelDigitSums`; `DecimalSafeRuns → LychrelDigitSums`; `DecimalDelayBridge → SafeDelay, DecimalSafeRuns`; `PairDelayBridge → DecimalDelayBridge`; `DelayedOverlapGate → PairDelayBridge`; WIP root → `DelayedOverlapGate`.

`proofs/README.md` says flattened current sources must be reconstructed to the original import layout with hash checks, and explicitly warns that the baseline project verifier is not evidence for new contributions. The six files should be copied byte-for-byte into a fresh directory under their ordinary module names. The WIP file may be copied byte-for-byte as `Agent114ShortRFirst11.lean` for an unambiguous importable module name; retain its original path and hash in the receipt. Do not rewrite its import or change the author branch merely to execute it.

## Counts, execution budget, and proposed review claim

Source declaration counts (`theorem`/`lemma`, including private declarations) are 295,12,11,23,17,49 for the six modules above, plus six new root declarations: **413 source theorem/lemma declarations** total. These are lexical source counts, not compiled-environment counts.

The previous independent clean audit of these byte-identical six dependency modules counted **1,511 module-origin theorem constants**, including generated auxiliaries: LychrelDigitSums 986; SafeDelay 24; DecimalSafeRuns 42; DecimalDelayBridge 41; PairDelayBridge 26; DelayedOverlapGate 392. The new seven-module total is **unknown until compilation**; do not estimate it as exactly 1,517 because tactics can generate auxiliary theorem constants. The review must print the exact types and axioms of all six new public declarations and audit every theorem originating in the seven selected modules. Fourteen compiler-generated unsafe implementation entries were present in these same earlier dependencies; keep any such entries separate from theorem logical axiom sets and inspect new-root provenance explicitly.

On this machine, the prior `--trust=0 -j1 -DElab.async=false` fresh compile of these exact six dependencies took **76.51 seconds** total (41.79 seconds for LychrelDigitSums and 32.00 for DelayedOverlapGate). That is historical measured evidence, not a new run or a guarantee. The WIP root is unmeasured. A first execution allowance of roughly **5–10 minutes** for reconstruction, seven-module compilation and full audit is reasonable, with an explicit 10-minute per-root timeout and retained logs if closed reduction is unexpectedly expensive. No additional package setup is indicated; the already verified official toolchain is available at `/workspace/p196-tools/lean-4.19.0-linux/bin/lean`.

Recommended separately published Agent #1 review claim: independently execute the exact PR #104 WIP plus the pinned seven-module closure; preserve unmodified-source build results even on failure; inspect canonical/arithmetic scope and all origin axioms; return diagnostics and concrete evidence to the author. This is review/execution support for Agent #114's existing task, not ownership of the first-hit problem. Any requested proof repair would need a separately specified writable contribution patch, preserving the original failed source and logs. Do not write the author's branch or upgrade accepted-math status from source inspection.

Parent will publish the review claim before execution. No compile or new proof was started in this pass. Temporary fetched inspection copies and hash metadata are at `/tmp/pr104-source-scope/`; this scope report is the durable requested artifact.
