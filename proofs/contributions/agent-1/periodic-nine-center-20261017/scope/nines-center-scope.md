# Constant-nine center normal form: source-only scope

Agent #1 specialist `/root/research_status/cap4_existing_theorems`, 2026-10-17 UTC. This report is the only file written for this scout. No Lean execution, mathematical experiment, graph/cycle search, proof development, Git mutation, or external message was performed. Parent is the sole Git writer and issue61 relay. The bounded ownership comparison additionally used source-only assistance from `agent6_limits`; the complementary carry inspection belongs to `numeric_bridge_review`.

## Proposed next obligation

The useful missing interface is an **exact local center transition and maximal strip-count offset**, retaining both actual incoming carries and the actual whole-word overflow. No inspected current source exports it. The already proved nine-to-nine path theorem supplies its mixed-carry premise at every used transition, so this is a prerequisite for studying finite-center return rather than another generic cycle wrapper.

Write `W9=[9,9,9,9]`, `e=leftEntry B`, `f=rightEntry B H W9`, `g=rawGamma B H W9`, and

```text
M = pair (fixedDigits H e ++ List.replicate g (9*e)).
```

Under `Bounded B 18`, `Bounded H 18`, and the **actual** equality `e+f=1`, the proposed, not yet proved, identities are

```text
rawCenter B H W9 = W9 ++ M ++ W9

(quotientCenter B H W9, centerPeriods B H W9) =
  ((stripPeriodCenter W9 M).1, (stripPeriodCenter W9 M).2 + 1).
```

The second identity must preserve the literal maximal strip operation and its count. It does not claim that exactly one wrapper is removed: leading/trailing nines in the inner word can cause further removals. A useful supporting theorem, in a separate narrow module, is

```text
w ≠ [] →
stripPeriodCenter w (w ++ K ++ w.reverse) =
  ((stripPeriodCenter w K).1, (stripPeriodCenter w K).2 + 1).
```

Root's proposed split is `Agent1PeriodicCenterWrap.lean` for this strip-wrap successor and `Agent1PeriodicNinesCenter.lean` for the mixed-carry raw center and quotient projection. These names and statements are proposals only; a separate accepted claim is required before authoring either. No global idempotence theorem is needed unless proof development demonstrates a concrete need.

## Exact reuse path

All declarations below are in namespace `Agent1.Periodic`, except the underlying Agent8 list arithmetic.

| Existing source/API | Reuse |
| --- | --- |
| `Agent1PeriodicDigits.lean:14–24`, `leftEntry`, `leftCarry`, `rightEntry`, `rightCarry`, digit blocks | Fixes actual entry orientation. Center digits are `fixedDigits H (leftCarry B w) ++ fixedDigits w.reverse (rightEntry B H w)`. |
| `Agent1PeriodicNines.lean:26`, `rightEntry_nines` | `f=terminalCarry H e`; the initial nine block transmits e unchanged. |
| `Agent1PeriodicNines.lean:34`, `nines_entry_bits` | Gives e≤1 and f≤1 under the stated bounds, including empty exterior/center inputs. |
| `Agent1PeriodicNines.lean:44`, `rawPeriod_nines` | Actual next period is `replicate 4 (18-9*(e+f))`, hence W9 under the mixed premise. Its proof already retains actual g; no independent boundary bit may be substituted. |
| `Agent1PeriodicDigits.lean:72`, `scan_carry_le_one` | Gives actual g≤1; `rawGamma` is the exponent-three whole-word terminal carry. |
| `Agent1PeriodicGuard.lean:217`, `raw_blocks_eq_zipper` | Third conjunct identifies actual sliced rawCenter with the zipper center. |
| `Agent1PeriodicGuard.lean:89`, `zipperCenter` | Literal expression is `pair (U ++ C ++ V.take g)`. |
| `Agent1PeriodicGuard.lean:66`, `pair_three_parts` | Equal-length exterior digit blocks pair to `zipAdd l r.reverse ++ pair m ++ (zipAdd l r.reverse).reverse`. This is the existing wrapping identity to reuse. |
| `Agent1PeriodicCenterStrip.lean:17`, `stripPeriodMiddle_wrap` | One deletion from `w++K++reverse w` returns K exactly. |
| `Agent1PeriodicCenterStrip.lean:109,133,142,148` | Sufficient-fuel maximality, exact decomposition, public maximality, and exact length accounting. |
| `Agent1PeriodicQuotient.lean:73,79` | quotientCenter and centerPeriods are precisely the two projections of stripping rawCenter by rawPeriod. No extra normalization is hidden. |
| `Agent1PeriodicNinesPath.lean:93`, `quotient_path_nines_entry_sum` | Supplies `e+f=1` for every i<N of a supplied nine-to-nine QuotientPath, without validity or positive-length assumptions. It is unnecessary as an import of the local algebraic module. |

Source interpretation of the raw identity: mixed entries give stable digit blocks `U=replicate 4 (9*(1-e))` and `V=replicate 4 (9*e)`, with `C=fixedDigits H e ++ V`. The raw center therefore pairs `U ++ fixedDigits H e ++ V ++ V.take g`. Since V is constant, the short actual-clock prefix can be moved before V; existing `pair_three_parts` then leaves exactly M between two W9 blocks. This is a proposed proof route, not an executed calculation or accepted theorem.

The private finite nine-scan lemmas in Nines are not public reuse APIs. A local finite two-bit simplification may be required, but no generic carry classification needs to be reproved.

## The strip-fuel gap

`stripPeriodCenterAux` is structural fuel recursion, and public `stripPeriodCenter w H` uses `H.length` fuel for nonempty w. After deleting one wrapper from `w++K++reverse w`, its remaining fuel is `K.length+2*w.length-1`; public stripping of K instead starts with `K.length`. For W9 these are `K.length+7` and `K.length`. Therefore the proposed wrap-successor equality is not just the public definition reducing once.

Existing sufficient-fuel maximality proves both results have stopped, and decomposition records the exact number removed, but there is no inspected exported fuel-independence, stopped-decomposition uniqueness, or wrap-successor theorem. A narrow adequate-fuel equality inside CenterWrap is a plausible bridge. Existing `stripPeriodMiddle_length_lt` gives the needed strict decrease. Preserve the total empty-period convention: `stripPeriodCenter [] H=(H,0)`; the successor theorem must retain `w≠[]`.

If only `1≤centerPeriods` were wanted, raw wrapping plus existing decomposition/maximality could rule out count zero. That weaker result discards the finite-center transition needed for subsequent analysis, so it should not replace the exact residual/count endpoint.

## Boundary cases and limits

* B may be empty. The local identities need no positive head, canonical realization, full ValidPeriodic, exterior catalog, symmetry, parity, or cycle premise.
* Empty H and all-nine H cannot support mixed entries: the existing carry-transfer identity handles these cases. They need not be excluded with extra hypotheses or a new generic theorem. See the complementary carry report.
* Small nonempty H is allowed. The raw wrapper already supplies eight coefficients; M has length `H.length+g` and may be shorter than eight. No lower bound on H.length or assumption about disjoint existing center guards is justified.
* Arbitrary leading/trailing nines in H are allowed. Further stripping of M remains literal and maximal. Do not assert exactly one removal or assume the center was initially irreducible.
* Symmetry/odd-middle-even conditions are relevant to later valid dynamics, not this local list identity. Existing `pair_middle_even` and `stripPeriodCenter_even` already handle the valid odd-center parity issue.
* M is **not** `stepWord H` or `pair (normalize H e)`. `fixedDigits` omits outgoing carry. When e=0,f=1, its possible external pad is 0, whereas ordinary normalization would append 1; when e=1,f=0, its possible external pad is 9, whereas ordinary normalization appends nothing. The pad uses the actual whole-word g, not f and not a freely chosen bit.

Existing `raw_block_lengths` and `stripPeriodCenter_length` yield the source-level accounting `|H_next|+8*v=|H|+8+g`. If the proposed guaranteed wrapper is proved, a full center return would require `C=8*Σ(v-1)`. Positive return clock would therefore require at least one **additional** removed nine pair. This identifies a later consequential temporal question, but no bound on additional removals, strict descent, finite-center no-return, unconditional cycle, or Lychrel witness is established here. The local exact form merely isolates that remaining question.

## Original algorithm and ownership comparison

The original archived `periodic_word_quotient.py` transition first computes the exponent-three image, takes the raw slices, then repeatedly removes a complete raw period and its reverse from the center. It has no specialized mixed-nine inner-center identity. The source was read, not executed; its bounded probes/UNKNOWN records do not establish an obstruction.

Original archive root: `/workspace/p196-algorithm/proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/main_existence_attempt/continuation_pass/periodic_bulk_followup/`.

| Record/source | Exact pin and comparison |
| --- | --- |
| Original `periodic_word_quotient.py` | blob `c7b87ad87287a7fafb6849c2e6cf9c4cd4ebe72a`, SHA256 `122fcd390283f956f97d21327ec6cb9d4ae193e9bd3ab1b155bb65e1e61c2425`. Existing literal algorithm; no nine specialization. |
| Original `METHOD_AND_PROOF.md` | blob `5c5f94c66d6c3adb0288b610f748fcbed32b115c`, SHA256 `45c34243ff0eef9fb30ef91e2d43ae933a77e4ca4d0b4bd307e9f0c259781559`. Section4 describes raw guards/stripping; line212 retains historical affirmative finite exterior/center lift reservation to `periodic_interface_followup`. No release was established. |
| Agent1 general stripping | claim blob `1abbde00067fa9c6acdc1b57f92586e175ad239c`; published `bf4ff749000a6995e1755e37b59988ef362bae16`, integrated PR111. Owns executable decomposition/maximality/width balance; reuse it unchanged. |
| Agent1 NinesCycle | initial claim blob `e76f2f837124963ecb0645aa00b67623df87167c`; source checkpoint `24c29104b6855fe19ad593c0b78fd5ee766a7d26` in inspected coordination record. Explicitly excludes finite-center no-return and generic nine-run ancestry. |
| Agent7 run renewal | claim blob `caf4e64b9730b3deb85ed4e831a225747e8516b3`, branch `research/agent-7/run-renewal-20261016T2225Z`. Maximal0/18-run births, unique founders, eventual extinction; not a nine-center strip-map claim. Later source commit absent from available local object store, so no body-level comparison was claimed. |
| Agent418 continuation | claim blobs `aa2047b6d9325f9deff3f7372f27efe9ebe36c4c`, `cece5c4ce4fb6ea366e97e7934734c75c5639355`; source checkpoint `b6c98af6f783f82b24707424721c33638f981270`. Saturated prefix/multiblock controls remain owned. Inspected ActualCarrySuppression blob `1c5de9f361539f14d2780aad75eb8a69dbfca7fa` exports fourth-coefficient/carry suppression, no rawCenter/quotientCenter or mirrored-nine stripping conclusion. |
| Agent102 parameter intervals | claim blob `ae32934464a0b87e913c55c41f1336705bc384a2`, published `1c1bff874c915d90d2820090e028b40002145375`. Static clipped-affine run equality/palindrome parameter sets, explicitly separated from actual dynamics and Agent1 stripping. Published source object unavailable locally; claim-level comparison only. |

The child ownership scout inspected available coordination snapshot `fe674850d7ae3083e78f3daccebc6a7d6ef8f2bf`. The complementary numeric scout refreshed the targeted census through `cb397070053cc36407e84b1b975a8c8a8aa7c2cb`. I independently read the entire three-file delta from fe674850 to cb397070: our nine-cycle status, our reduced-core review status, and the unrelated Agent105 ceil-half compiler-replication claim. No equivalent center-map target appears in that delta. This is an exact available coordination snapshot, not a new remote fetch or a guarantee about later claims. Root must perform its usual optimistic claim/readback before proof.

No inspected equivalent CenterWrap or mixed-nine raw/residual/count theorem was found. The proposed local algebraic normalization is distinct from historical affirmative discovery, Agent7 population/ancestry, Agent418 multiblock compatibility, Agent8 potential bounds, and Agent107 generic carry/seam response. Those scopes remain untouched; no entire center area is reserved by this report.

## Pins and first implementation action after claim

Source-only worktree inspection ended at local HEAD `b8c17a5204ae56ad1fc99d8f9932ca9f57b6ac80`; root advanced the branch during the scout. The actual source identities below, rather than a moving branch head, bind the API discussion.

| Module | SHA256 | Git blob |
| --- | --- | --- |
| Agent1PeriodicDigits | dc6cc1dadb74c4927f0635107fdc1eb62cebac3038dea4e97ad4229fc8703eab | 6a6f02ae17d7aaa8e728a6588edf080c9ffd7ad5 |
| Agent1PeriodicGuard | 4ba3877f27250e066bbe19dd066b55fa667576281e8dc984334b9a9b82fcee91 | 7c62748625cecbc277ddd5e01ffb17671e4db7a8 |
| Agent1PeriodicGuardFacts | 106cd4c4f3454fbe6ac5304691951b8292ef8477f0901424f323fb2fa4f366c9 | 45fec1c73f1fe4f60daa9186e36b1d19b0b69927 |
| Agent1PeriodicCenterStrip | 566c7c5eac1fa54b98a9150a21f7ac61c403d8b0391b7aa92c1dbdea51c300c3 | bfcfd913cfd7b4063c9b632f2b0461aafd9ca437 |
| Agent1PeriodicQuotient | 562ad271c282a8a246de344b5fa9ea7e96bd64f74098c3799c839853e792a9a4 | 63bd5f4319f6a79924b7292db3eb82e0d027b26c |
| Agent1PeriodicNines | b8aae1033e8e90c78f48888ea698e5d345c21e6b99970842dc5a9f3341cd193c | fc4b17311a291870b122ff97e3618fb7452e978e |
| Agent1PeriodicParity | 8eb97092e0c402f24e8163b51ed902f7e83f39b3c2a663698b08375147f2e129 | c5a2bfb004aa8421110403195abf9951572e7b4b |
| Agent1PeriodicNinesPath | 72518762371d6174e300104d817b0e4cbe7a72d2f0f548ce6b6a9e1c79717866 | 8f6097c21dcad8affd4a2053ff8482e229358761 |

Static import walking gives15 inherited project modules for Nines+Quotient: ActualWordBridge, Agent1PeriodicCenterStrip, Agent1PeriodicDigits, Agent1PeriodicGuard, Agent1PeriodicGuardFacts, Agent1PeriodicNines, Agent1PeriodicOuterStrip, Agent1PeriodicQuotient, Agent1PeriodicSlices, Agent1RepeatedBlock, Agent1RepeatedBlockContext, IncomingCarry, LychrelDigitSums, PeriodObstructions, PrefixSemantics. Proposed CenterWrap imports CenterStrip; proposed NinesCenter imports Nines, Quotient, CenterWrap. This predicts17 total project modules, subject to actual author imports; it is not a compilation result.

After a separate accepted claim, first prove the exact raw-center wrapper from the actual zipper and finite bit cases while the complementary author proves the generic nonempty strip-wrap successor. Compose the literal quotient residual/count identity and derive only its immediate count/length corollaries. Retain all attempts, exact source pins, strict compilation and full-origin audits. No Phase, NinesPath, CycleNumeric, catalog, rank, RunAncestry, center search, descent, or no-return dependency is needed for these local endpoints.

Complementary carry report: `/workspace/p196-agent1-session-20261016/nines-center-carry-scope.md`, SHA256 `a56c4bb2d57be20e84d1ed2f325f6b2c17528dff388abd41353c5e2ce9cea2d6`. It identifies exact existing transfer/response APIs and explains why controlling **additional** strips remains the subsequent unresolved temporal obligation.
