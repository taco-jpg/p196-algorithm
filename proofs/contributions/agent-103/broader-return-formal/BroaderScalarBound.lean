import BroaderClock
import ScalarBound

/-!
Agent #103. Unconditional Lean bounds on consecutive seven-step returns of
the actual pair word to the two-column prefix (4,4), obtained from
`BroaderClock.returns_clock_segment` and the kernel-checked scalar endpoints
of `ScalarBound` (Agent #103 v2 scalar finite instance).

These are weaker than the written bound `R <= 90 + warmup L <= 94` of
`2026-10-14-component-specific-bound`; that sharper bound needs the separate
broader 15-job finite instance. Finite-horizon obstruction only: nothing is
asserted about palindromes after the pattern ends, about 196, or about
Lychrel existence.
-/

namespace BroaderScalarBound

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory BroaderClock

/-- From the initial word: at most `94 + warmup L` consecutive returns. -/
theorem returns_le_94_plus_warmup (q : Nat → Nat) (L R : Nat)
    (ha : Admissible L q) (hL : 2 ≤ L)
    (hret : ∀ k, k ≤ R → pairAt q L (7 * k) = (4, 4)) :
    R ≤ 94 + ScalarOrbit.warmup L :=
  ScalarBound.initial_width_dependent_bound q L 0 R ha
    (returns_clock_segment q L 0 R ha hL (by simpa using hret))

/-- Uniformly, from any start time: at most 98 consecutive returns. -/
theorem returns_le_98 (q : Nat → Nat) (L a R : Nat)
    (ha : Admissible L q) (hL : 2 ≤ L)
    (hret : ∀ k, k ≤ R → pairAt q L (a + 7 * k) = (4, 4)) :
    R ≤ 98 :=
  ScalarBound.periods_le_98 q L a 0 R ha (returns_clock_segment q L a R ha hL hret)

/-- Once the actual width is at least 14: at most 94 consecutive returns. -/
theorem wide_returns_le_94 (q : Nat → Nat) (L a R : Nat)
    (ha : Admissible L q) (hL : 2 ≤ L) (hwidth : 14 ≤ ScalarOrbit.widthAt q L a)
    (hret : ∀ k, k ≤ R → pairAt q L (a + 7 * k) = (4, 4)) :
    R ≤ 94 :=
  ScalarBound.wide_periods_le_94 q L a 0 R ha hwidth (returns_clock_segment q L a R ha hL hret)

/-- No admissible word of width at least two returns to (4,4) every seven
steps 99 consecutive times. -/
theorem no_99_returns (q : Nat → Nat) (L a : Nat) (ha : Admissible L q) (hL : 2 ≤ L) :
    ¬ ∀ k, k ≤ 99 → pairAt q L (a + 7 * k) = (4, 4) := by
  intro h
  have := returns_le_98 q L a 99 ha hL h
  omega

end BroaderScalarBound
