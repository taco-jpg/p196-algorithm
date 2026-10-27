# Manager — no positive two-run return in at most four steps

**Status: LEAN-VERIFIED specialization of existing prefix theorems.**

Let fixed finite decimal blocks U, M, V 和 fixed decimal digits x, y define

\[
W(r)=U\mathbin{+\!+}x^r\mathbin{+\!+}M\mathbin{+\!+}y^r\mathbin{+\!+}V.
\]

The formal digit indexing is least significant first. Reversing the fixed
block order gives the same class as the conventional printed digit order.
Suppose both endpoint words are canonical decimal representations, r>=3,
和 P actual reverse-and-add steps send W(r) to W(r+S). Then

\[
4S\le P,\qquad P=4S\Longrightarrow P\equiv0\pmod8.
\]

Consequently **S>0 implies P>=5**. In particular the P=4,S=1 case is
impossible at every fixed-block width. A universal family return valid
only above a threshold is also covered: choose r at least that threshold
和 three. The proof needs only this one actual return.

## Scope 和 attribution

This is the manager's T5 review corollary of existing registered results,
developed after auditing Agent5's polynomial two-run format. It does not
reprove or claim the original finite prefix potential or saturation
certificate as new. It supplies the literal two-run specialization,
canonical representation transport, 和 all-width period-four exclusion.

The imported mathematical sources are unchanged at baseline
`eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`:

- `P196.Agent4.Saturation.closed_prefix_overflow_bounds` in
  [SaturationTheorem.lean](https://github.com/taco-jpg/p196-algorithm/blob/eafbbbfd6b5b857597f95f68268c56dbd96b6bcb/lean/P196/Agent2SaturatedProfile/SaturationTheorem.lean).
- `P196.Agent4.WholeWord.iterPairs_prefix_evolution`,
  `actual_width_overflow_identity`, 和 `actual_saturated_prefix_return` in
  [WholeWordBridge.lean](https://github.com/taco-jpg/p196-algorithm/blob/eafbbbfd6b5b857597f95f68268c56dbd96b6bcb/lean/P196/Agent2SaturatedProfile/WholeWordBridge.lean).
- Actual numeric semantics 和 canonical representation in
  [LychrelDigitSums.lean](https://github.com/taco-jpg/p196-algorithm/blob/eafbbbfd6b5b857597f95f68268c56dbd96b6bcb/lean/P196/Foundations/LychrelDigitSums.lean),
  plus `SevenColumnKernel.PalindromeBridge.canonical_unique` in
  [PalindromeBridge.lean](https://github.com/taco-jpg/p196-algorithm/blob/eafbbbfd6b5b857597f95f68268c56dbd96b6bcb/lean/P196/Agent104P620Witness/PalindromeBridge.lean).

The earlier `Agent112.SmallPeriod.checked_period_ne_four` concerns the
original complementary-gap quotient checker. This result instead applies
directly to literal decimal digit families, with actual numeric orbit
equality 和 explicit canonical endpoints.

No one-band `cycleOK 10` certificate, decimal Lychrel witness, exclusion
at every period, or claim about 196 is supplied. The signed multi-band
format in Agent3's T5 work has a different shape; this result does not
exclude that whole format.

## Why three outside columns suffice

For r>=3, each of the first three low digits lies in U or the first run.
Each of the first three high digits lies in V or the last run. Increasing
r therefore leaves both triples unchanged, even if U or V is empty or
shorter than three digits. Their pair sums also remain unchanged.

`twoRun_low_digit`, `twoRun_high_digit`, 和 `twoRun_prefix_stable` prove
this directly for the explicit piecewise digit function. Prefix stability
is a conclusion of the new code, not an additional premise.

The exact canonical width is

\[
L(r)=|U|+|M|+|V|+2r.
\]

Thus the target width is L(r)+2S. The existing finite prefix potential,
applied to the exact projected numeric orbit, gives
`2*L(r+S) <= 2*L(r)+P`, hence 4S<=P. If equality holds, the existing
saturated-prefix theorem gives P mod 8 = 0. A positive S with P<=4
would force S=1,P=4, contradicting that congruence.

The numeric bridge uses canonical uniqueness to identify the target word
with the representation produced by `iterPairs_representation`. It never
substitutes a freely chosen width or a surrogate digit sequence.

## Exact assumptions

- The source run length is at least three; no upper bound is imposed.
- The fixed blocks 和 run digits are the same at both endpoints.
- The common run increment S is natural. Strict positivity is required
  only for the final P>=5 corollary.
- Both endpoint digit functions satisfy the repository's `Canonical`
  predicate: positive width, all in-range digits at most nine, positive
  leading digit, 和 the stated numerical value.
- `Lychrel196.orbit n P = m` is the actual ordinary numeric return.

Trailing zero digits are allowed: `Canonical` does not require a positive
units digit, 和 the imported numeric semantics handle ordinary reversal.
Leading zero padding is excluded by canonicality, so an artificial width
increase cannot satisfy the premise. There are no assumptions about the
intermediate template forms, intermediate run lengths, or palindrome
avoidance. The obstruction applies even to orbits continued past a
palindrome.

## Registered endpoints 和 verification

New registered result: `ManagerTwoRunObstruction`.

| Endpoint | Meaning |
|---|---|
| `P196.ManagerTwoRun.numeric_prefix_return_constraints` | Canonical actual return with equal three-column prefixes implies the width bound 和 saturated mod-eight condition. |
| `P196.ManagerTwoRun.twoRun_prefix_stable` | Literal two-run digit families have stable first three pair columns for run lengths at least three. |
| `P196.ManagerTwoRun.twoRun_return_constraints` | Any actual literal two-run return satisfies 4S<=P; equality implies 8 divides P. |
| `P196.ManagerTwoRun.twoRun_positive_return_period_ge_five` | Positive common run increment requires P>=5 at arbitrary fixed-block widths. |

Reproduction from repository root with the pinned Lean 4.19.0 toolchain:

```bash
LEAN_NUM_THREADS=1 python3 tools/verify.py --changed
```

The unmodified gate returned `ALL CHECKS PASSED`: 5,219 Lean files 和
302 registered projects passed source rules; two changed modules built;
both modules were replayed by the matching v4.19.0 `lean4checker`; four
registered endpoints passed the allowed-axiom audit. The only axioms used
are `propext`, `Classical.choice`, 和 `Quot.sound`.

One-worker direct elaboration measurements were 0.822 seconds for
`NumericPrefixReturn.lean` 和 1.473 seconds for `TwoRunObstruction.lean`.
The measured process-family maximum resident set sizes were respectively
760,052 KiB 和 780,164 KiB; the latter is also a conservative upper bound
across both measurements. The full changed-file gate took 48.673 seconds.
Both new files satisfy the repository's per-file 20-minute/8-GB budget.

The stock compiler 和 stock kernel checker were used unchanged. No
enumeration of fixed block widths is part of this proof.
