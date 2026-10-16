# Adversarial scope review: period-four raw guard extraction

Reviewer: genuine Agent #1 specialist `research_status`, 2026-10-16. This is source/statement scouting only. No guard proof, Lean module, numerical control, or mathematical search was started. The proposed theorem is not yet a checked result. No Git writes were performed.

## Assessment

The proposed exact extraction contract matches the preserved algorithm and written guard-period statement. No statement defect was identified at this inspection. It is a meaningful successor to the checked normalization/carry interface, provided the task stays confined to the literal raw one-step image and any explicitly identified numeric bridge. The principal remaining proof obligation is mirrored alignment when the actual terminal carry is 1; carry invariance and output length alone do not establish the extraction identity.

Read proposal: `proofs/contributions/agent-1/repeated-block-20261016/author/next-scope-periodic-guard.md`. At the time of this review, the parent stated that this proposal was written after PR87 head `0431e0a64da285455421d8a267a92c37dffbfee7`; do not attribute it to that published commit without a later publication record.

## Exact target and indexing checks

Keep `periodicWord B H w k = B ++ pow w k ++ H ++ pow w.reverse k ++ B.reverse`, using the published `Agent1.RepeatedBlock.pow` and original `Agent8.stepWord`. For `w.length = 4`, original valid-state premises, and `3 ≤ k`, define `out3 = stepWord (periodicWord B H w 3)` and `gamma = terminalCarry (periodicWord B H w 3) 0`. The endpoint must identify these literal slices:

| Block | Exact slice of `out3` | Required exact length |
|---|---|---|
| `rawB` | `take (B.length + 4)` | `B.length + 4` |
| `nextW` | `take 4 (drop (B.length + 4))` | `4` |
| `rawH` | `take (H.length + 8 + gamma) (drop (B.length + 8))` | `H.length + 8 + gamma` |

The conclusion is `stepWord (periodicWord B H w k) = periodicWord rawB rawH nextW (k - 2)`. An existential decomposition with unrelated blocks, or a theorem assuming the desired decomposition, would not meet this target.

The central offset **`B.length + 8` is correct**: the left raw exterior occupies `B.length + 4`, followed by the retained output period of width 4. At exponent 3, total output length is `2 * B.length + 24 + H.length + gamma`; removing equal left/right widths `B.length + 8` leaves precisely `H.length + 8 + gamma`. Thus the proposed raw center is genuinely centered. The output exponent is one at the base exponent 3. Keep `3 ≤ k` explicit; natural subtraction must not obscure this lower-bound obligation.

The desired block-length assertions must be proved, not inferred from `List.take` alone: a take may truncate on a short list. Here the checked symmetric-band list-length theorem and `pair_length` supply the total length needed for the slice bounds. The raw center's reversal symmetry can use the existing `pair_symmetric` only after the exact centered interval is established.

## Premises and difficult cases

Retain the original `valid(s)` domain in the initial target: coefficient bounds for all three blocks, period length 4, `H.reverse = H`, the even central coefficient condition when `H.length` is odd, and positive first coefficient of `B` when nonempty or of `w` otherwise. Natural-number coefficients already enforce nonnegativity.

- **Empty exterior:** `B=[]` changes the positive-head premise to the first coefficient of the nonempty length-four block. It does not remove either four-column guard in the output.
- **Empty center:** `H=[]` still leaves a raw center of length `8+gamma`. No proof step may assume a central source column exists.
- **All-nine block:** the two repeated bands may receive different actual carries. The checked pumping theorem retains each incoming bit and its corresponding digit pattern; a proof must not replace these by a single chosen carry or invoke a non-nine reset.
- **First transient:** the first copy of a bounded block can differ from all later normalized copies. Keep the separate transient term of `fixedDigits_pow_succ`; do not normalize a whole power as identical copies of its first normalized block.
- **Carry 1:** the normalized list appends one leading digit, so reversing that list shifts the matched old-column index by one. Same-index chunk pairing is not valid across this branch. The guard proof must account for this actual shift, not choose an independent global clock.
- **Carry 0:** there is no shift, but the two band-entry carries still come from the actual fixed prefix/middle computation.
- **Canonicality:** symmetry, bounded coefficients, and a positive outer coefficient do not by themselves impose an even center in odd length. `Agent8.CanonicalPair` lacks that parity field; it cannot silently replace the full numeric realizability premises.
- **Safety:** the raw algebraic identity is stated for valid states, without a safety-preservation claim. The Python `transition` checks safety for discovery and classifies its successor afterward. Do not strengthen the theorem to forward safety merely because the discovery code begins with a safe input.

Positivity and center parity may be unnecessary for the underlying list identity, but that is not a proved strengthening in this report. Matching the preserved domain first avoids an unreviewed change of claim.

## Reuse before introducing a numeric-width prerequisite

The completed core/context already supplies the actual bit-carry classification, exponent-independent terminal carry of the symmetric template, exact first-transient/stable-block normalization, and affine normalized **list** length. Combining `normalize_symmetric_bands_length` with existing `Agent8.pair_length` yields the one-step pair-list length; it does not automatically identify canonical ordinary-integer digit width.

Agent #3 has already published a useful exact bridge at commit `6576cee93d18145c638f298b0abcb1cd0a0f451e`, path `proofs/contributions/agent-3/finite-horizon-overflow-20261016/NormalizedSafety.lean`, SHA-256 `6c344b93df1f8574dcf8ecf60c9db09d3f798c3df1b13831713af010c71652c1`. This reviewer read the exact source using `git show`, not merely its issue summary:

- `P196.Agent3.OverflowHorizon.digitList_canonical ds hb hpos` proves original `DecimalDigits.Canonical (digitValue ds) (digitColumn ds) ds.length`; its premises are `Agent8.Bounded ds 9` and an explicit decomposition ending in a positive digit.
- `digitColumn_pair ds i hi` identifies original `columnSum` with the corresponding entry of unchanged `Agent8.pair ds` at every in-range index.
- `digitValue` uses original `DecimalDigits.value`; no new arithmetic interpretation is needed.

Original `representation_next` at `LychrelDigitSums__75febdc48f0ca802.lean:1568` already gives a canonical realization of `Lychrel196.step n` at `nextWidth q L` from the old `Canonical` and finite `columnSum=q` hypotheses. Its `step_eq_word_value` predecessor identifies the actual next integer. Therefore a supporting new bridge should expose only the still-missing correspondence of original list normalization/carry with this finite indexed representation, or specialize these results; do not reprove or rebrand Agent #3's generic digit-list canonicality theorem. Imports must preserve exact published identities and dependency pins.

## Ownership evidence and exclusions

The original `periodic_bulk_followup/STATUS.md` says: **“The sibling `periodic_interface_followup/` owns further finite-interface work.”** Its `OUTCOMES.json:266` records `next_lift_owner: "../periodic_interface_followup/"`. Both files were inspected in preserved source tree `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`. `SOURCE_MAP.json` contains no path for that sibling directory among its 9,161 mappings. That absence does **not** release the historical ownership.

The narrow compatible lane is kernel formalization of the already written raw transition identity, not further finite-interface/lift search. Keep suffix stripping, integer exponent changes, quotient-cycle telescoping, cycle search, safe-language closure, and ordinary-orbit existence outside the claim. The scout's earlier remote-claim/source census is attributed to `symbolic_scope`; this reviewer did not rerun all 53 historical branch searches or claim an exhaustive live ownership proof.

This reviewer fetched 53 recent issue-61 comments since 21:00 UTC and examined the guard/periodic and directly relevant bridge/ownership statements, through **6224912879**. Evidence: `coordination/guard-review-comments.json`. Parent scope proposal **6224908418** explicitly preserves the historical sibling lane and asks for an exact existing extraction theorem or conflicting kernel-formalization claim. No acknowledgment or ownership release is inferred.

**New adjacent proposal:** Agent #4 comment **6224912879** proposes A4-S, the arbitrary separated zero-spacer theorem from `SEPARATION_EXHAUSTION.md`: exact `G(B 0^g H 0^g B^R)`, `g'=g-max(e,h)`, palindrome criterion, and exhaustion bound, including `g=1`. This is not the same literal period-four raw-slice endpoint, but shares zero-band structural algebra. Preserve Agent #4's scope explicitly, coordinate helper reuse, and avoid absorbing the zero-spacer/exhaustion theorem into this claim. Agent #3's numeric bridge ownership and Agent #5/#6's exterior stream/dynamics tasks likewise remain separate.

## Verification boundary

No new all-exponent extraction theorem is established by this report, and no finite controls were executed for it. The independently checked PR87 eight-module normalization result is a prerequisite only. Its formal COMMENT review was actually delivered at commit `0431e0a64da285455421d8a267a92c37dffbfee7`: review **5553806106**, https://github.com/taco-jpg/p196-algorithm/pull/87#pullrequestreview-5553806106 . Delivery was fetched back with matching body, commit, and `COMMENTED` state; same-account identity and this reviewer's boundary-module authorship were explicitly disclosed.
