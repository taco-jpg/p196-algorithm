import BroaderRoot
import BroaderHierarchy

/-!
Agent #103. The written broader two-column return bound
(`2026-10-14-component-specific-bound/COMPONENT_SPECIFIC_BOUND.md`, eq. (2)):
if an admissible pair word of width `L >= 2` has first two coefficients (4,4)
at times `7k`, `0 <= k <= R`, under the actual reverse-and-add pair update,
then `R <= 90 + ceil((14-L)/3) <= 94`. Here `ScalarOrbit.warmup L =
(14-L+2)/3` is that ceiling (and 0 for `L >= 14`).

All three return branches and arbitrary switching are included. This is a
finite-horizon obstruction to one return mechanism only: leaving the pattern
does not imply a palindrome, and nothing is asserted about 196 or about the
existence of decimal Lychrel numbers.
-/

namespace BroaderBound

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory BroaderClock

/-- Once the actual width is at least 14: at most 90 consecutive returns. -/
theorem wide_returns_le_90 (q : Nat → Nat) (L a R : Nat) (ha : Admissible L q) (hL : 2 ≤ L)
    (hwidth : 14 ≤ ScalarOrbit.widthAt q L a)
    (hret : ∀ k, k ≤ R → pairAt q L (a + 7 * k) = (4, 4)) : R ≤ 90 := by
  obtain ⟨path, hp⟩ := BroaderRoot.actual_broader_root_path q L a R ha hL hret
  have hb := BroaderHierarchy.finite_root_bound (iterPairs q L a).2 (iterPairs q L a).1 0 0
    (7 * R + 1) path (iterPairs_admissible q L a ha) hwidth hp
  omega

/-- From the initial word: at most `90 + warmup L` consecutive returns. -/
theorem returns_le_90_plus_warmup (q : Nat → Nat) (L R : Nat) (ha : Admissible L q) (hL : 2 ≤ L)
    (hret : ∀ k, k ≤ R → pairAt q L (7 * k) = (4, 4)) :
    R ≤ 90 + ScalarOrbit.warmup L := by
  by_cases hR : R ≤ ScalarOrbit.warmup L
  · omega
  · have hseg := returns_clock_segment q L 0 R ha hL (by simpa using hret)
    have hw : ScalarOrbit.ClockSegment q L 0 0 (7 * ScalarOrbit.warmup L) :=
      fun i hi => hseg i (by omega)
    have h14 := ScalarOrbit.warmup_reaches_fourteen q L 0 ha hw
    have hrest := wide_returns_le_90 q L (7 * ScalarOrbit.warmup L) (R - ScalarOrbit.warmup L)
      ha hL h14 (fun k hk => by
        have := hret (ScalarOrbit.warmup L + k) (by omega)
        simpa [Nat.mul_add] using this)
    omega

/-- Uniform bound from any start time, as in the written statement. -/
theorem returns_le_94 (q : Nat → Nat) (L a R : Nat) (ha : Admissible L q) (hL : 2 ≤ L)
    (hret : ∀ k, k ≤ R → pairAt q L (a + 7 * k) = (4, 4)) : R ≤ 94 := by
  have had := iterPairs_admissible q L a ha
  have hwa : 2 ≤ (iterPairs q L a).1 := by
    have := ScalarOrbit.widthAt_lower q L a
    unfold ScalarOrbit.widthAt at this; omega
  have h := returns_le_90_plus_warmup (iterPairs q L a).2 (iterPairs q L a).1 R had hwa
    (fun k hk => by
      have := hret k hk
      simpa [pairAt, BroaderRoot.iterPairs_restart] using this)
  have hw := ScalarOrbit.warmup_at_most_four _ hwa
  omega

/-- No admissible word of width at least two makes 95 consecutive seven-step
returns to the two-column prefix (4,4). -/
theorem no_95_returns (q : Nat → Nat) (L a : Nat) (ha : Admissible L q) (hL : 2 ≤ L) :
    ¬ ∀ k, k ≤ 95 → pairAt q L (a + 7 * k) = (4, 4) := by
  intro h
  have := returns_le_94 q L a 95 ha hL h
  omega

end BroaderBound
