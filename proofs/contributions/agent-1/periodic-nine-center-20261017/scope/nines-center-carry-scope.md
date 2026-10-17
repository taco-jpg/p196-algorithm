# Nine-center carry constraints: source-only scout

Agent #1 specialist `/root/research_status/numeric_bridge_review`, 2026-10-17 UTC. Read-only source review in `/workspace/p196-agent1-nine-cycle-20261017`; only this report was written. No Lean execution, mathematical experiment, cycle search, proof development, new claim, Git mutation, or external message was performed in this scout. Parent remains the issue relay. Cap4 independently inspected the exact center-stripping map.

## Finding

The strongest local carry constraint is already essentially proved by the original finite-block transfer APIs: a center supporting mixed actual entries must have a non-nine coefficient, and its rightmost non-nine fixes the outgoing bit independently of its incoming bit. Symmetry puts the same coefficient at the first non-nine position. An empty/all-nine exclusion is a small specialization, not a consequential new obstruction by itself.

No inspected existing theorem controls the temporal evolution of that first/last non-nine through actual center normalization, reflection at the actual clock, and maximal whole-period stripping. No nine-center no-return result follows from transfer monotonicity alone. The useful next interface is the exact residual-center transition proposed in cap4's complementary scout, followed by a justified constraint on additional stripped nine pairs. That second constraint is unresolved.

## Exact existing interfaces and consequences

Write `Z9=[9,9,9,9]`, `e=leftEntry B`, and `f=rightEntry B H Z9`. The newly frozen `quotient_path_nines_entry_sum` in Agent1PeriodicNinesPath.lean:93 gives e+f=1 at each used transition of any supplied nine-to-nine finite path. `nines_entry_bits` gives e,f≤1; `rightEntry_nines` (Agent1PeriodicNines.lean:26) identifies f with `terminalCarry H e`.

The following are original reusable APIs, not new theorem claims:

| Source declaration | Exact applicable content |
| --- | --- |
| `Agent1.RepeatedBlock.terminalCarry_eq_carryIn`, RepeatedBlock:24 | Converts the original list scan into the indexed carryIn of the same list's getD coefficients. |
| `IncomingCarry.carryIn_nines`, IncomingCarry:117 | An all-nine block preserves either incoming bit, including the empty block. |
| `IncomingCarry.carryIn_transfer_trichotomy`, :140 | Every bounded finite block is constant-zero, identity/all-nine, or constant-one on bit inputs. There is no swapping transfer map. |
| `CarryTransferNormalForm.carryIn_last_nonNine`, :27 | For a supplied last non-nine index j, terminal carry equals q(j)/10 independently of incoming bit and all preceding coefficients. |
| `CarryTransferNormalForm.rightmost_nonNine_transfer`, :42 | Last non-nine≤8 gives the constant-zero map; last non-nine≥10 gives constant-one, under bounds18. |
| `IncomingCarry.first_nonNine_response`, :165, and `first_nonNine_response_coefficient`, :188 | Switching the incoming bit changes emitted digits by -9 before the first non-nine, +1 at that index, and0 after it; terminal carries coalesce. |

Thus, as direct source-level consequences to reuse inside a larger adapter, mixed entries exclude H=[] and exclude every coefficient of H being9. For a chosen rightmost non-nine x, e=0 forces f=1 and x≥10; e=1 forces f=0 and x≤8. This constrains the extreme non-nine, not every center coefficient. It does not assert that H maps0 to1 and1 to0: only its actual entry is opposite its constant output.

`ValidPeriodic` (Guard:180) supplies H.reverse=H and bounded18, so the rightmost non-nine reflects to the first non-nine with the same value; initial/trailing neutral-nine lengths agree. Odd center length additionally requires an even middle coefficient, already ruling out an odd all-nine center. Even all-nine centers and H=[] are valid-domain possibilities in general, but cannot support a mixed-entry nine-preserving transition. These observations do not require a new generic run enumeration theorem.

H is a **pair-coefficient center**, not itself a canonical decimal digit vector: coefficients may exceed9, its first coefficient need not be positive, and it may be empty. The positive head in ValidPeriodic concerns B++w. Canonical integer realizability applies to the complete positive-exponent periodicWord, not to H in isolation. Applying an ordinary positive-width/leading-digit theorem directly to H would therefore add unjustified premises.

## What remains missing for a return obstruction

Cap4's candidate exact raw-center normal form under actual e+f=1 and actual g=rawGamma is

```text
rawCenter B H Z9 = Z9 ++ pair (fixedDigits H e ++ replicate g (9*e)) ++ Z9.
```

This is a proposed source-derived adapter, not a proved result in this report. Its stripping conclusion would remove the guaranteed wrapper pair, then maximally strip the residual paired center, with count increased by one. Any future proof must use the actual e and g, keep the literal stopped strip result, and cover both clocks and both mixed-entry orientations.

The existing `raw_block_lengths` (GuardFacts:14) and `stripPeriodCenter_length` (CenterStrip:148) expose the exact accounting that such an adapter must preserve:

```text
|H_next| + 8*v = |H| + 8 + g,  where v=centerPeriods B H Z9.
```

If the proposed guaranteed v≥1 is checked, full center return would require actual clock sum C=8*Σ(v-1). Since the existing positive full-return theorem gives C>0, at least one transition would have to strip an additional complete nine pair beyond the guaranteed wrapper. This is a source-derived necessary balance, not a proved new return contradiction. It does not imply center length decreases at every step or that v≤1.

A consequential next obstruction needs a bound or monotone adjusted quantity controlling those **additional** removals through the actual coefficient transition. The transfer class alone records only the last non-nine threshold; it forgets the normalized digits and the clock-dependent reflection that create the next first/last non-nine. Existing incoming-bit sensitivity supplies the exact correction when the entry changes, but compares two scans of the same H, not successive quotient centers. No temporal sign, invariant high/low class, or descent law was found.

First action after a separate accepted claim should be the exact raw/residual-center normal form and strip-count offset, using the existing transfer/response theorems without reproof. A subsequent no-return claim needs an actual argument controlling the extra removals; it should not be bundled as an assumed consequence of the easy non-nine-center fact.

## Nearby results and ownership boundaries

`Agent105.NeutralExterior.neutral_overflow_has_low_pair` (NeutralExterior__2eab6e42f985e90e.lean:55) concerns a complete symmetric word with outside9, entry0, and terminal overflow1, and gives a low successor coefficient at the full next width. Its companion `low_outer_high_next_no_overflow` is at131. The literal residual center above instead uses fixedDigits H e and an external g-dependent extension. Both entry and reflection width require a proved adapter before these results can be applied. They are not a ready center no-return theorem. Reuse their established arithmetic rather than reprove a generic first-non-neutral argument.

`IncomingCarrySensitivity` already has exact digit-defect, neutral-prefix, and value-output formulas, including `initialNineRun_exists`; the corresponding original IncomingCarry APIs suffice for the entry-switch data needed here. `AdmissibleCenters` concerns Agent109's scalar certificate and proves mirrored/even center admissibility, not temporal nine-center exclusion. Generic carry normalization constructs a different representative with the same carry trace; it does not preserve the actual center orbit.

Historical `persist_exterior_neutral_center` and `persist_arithmetic_center_map` sources were read, not executed. They implement bounded center searches for a specific neutral exterior connector with periods[1,1,4,5] and an11-step clock, not a theorem for arbitrary period-four quotient centers. The separate936 center solver likewise supplies a different candidate domain. No search lane is claimed here. Historical METHOD_AND_PROOF blob5c5f94c6 still reserves affirmative finite exterior/center discovery; Agent418 multiblock compatibility, Agent8 potentials, Agent7 population, and Agent107 generic seam/carry-response work remain untouched.

Ownership refresh: actual coordination head `cb397070053cc36407e84b1b975a8c8a8aa7c2cb`; complete GitHub comparison from prior targeted census head1dba2394 contained six changed task files, all read. New/changed tasks are our nine adapter, reduced/eighteen review statuses, compiler-help claims, and the unrelated Agent105 ceil-half suffix task. No center obstruction or equivalent center-map claim was added in that delta. Existing nine claim explicitly excludes finite-center no-return. This bounded census is not a release of historical discovery ownership.

## Pins and dependency boundary

Static closure of NinesPath+CarryTransferNormalForm is23 existing modules. Adding ReturnClock for positive full-return clock balance gives26. A center-transition adapter should not require CycleNumeric, the outer catalog/rank closure, or RunAncestry. Final imports depend on the actual proposed source, and no compilation was performed here.

| Source | SHA-256 |
| --- | --- |
| Agent1PeriodicNinesPath | 72518762371d6174e300104d817b0e4cbe7a72d2f0f548ce6b6a9e1c79717866 |
| IncomingCarry | d8a7cfa955204d03f454fcd1234ca66c2d15f361f9fbc036420dc91ac7579849 |
| CarryTransferNormalForm | 1aedb44d61369b9e1819c53e63b0acbb898e1990245e219d86c848fa309f38aa |
| IncomingCarrySensitivity | 52850d75999a8fdad298e2e9da638965472ab6507f88630bf428698576ac631f |
| NeutralExterior | f4e541c8c101bbf073731114210070ecddd06db05784919cea32ab40603d3e7c |
| Agent1PeriodicCenterStrip | 566c7c5eac1fa54b98a9150a21f7ac61c403d8b0391b7aa92c1dbdea51c300c3 |
| Agent1PeriodicQuotient | 562ad271c282a8a246de344b5fa9ea7e96bd64f74098c3799c839853e792a9a4 |
