import P196.CarryPrefixThresholds.SevenSmoothing
import P196.CarryPrefixThresholds.ExteriorExclusion

/-!
Seven complete carry observations determine the exterior initial pair sum
at every common admissible width. Complete observations include the terminal
carry, and the ordinary orbit continues after a palindrome.
-/

namespace CarryPrefixThresholds

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory
open CarryObservabilityActual DifferenceObservability

private theorem short_width_exterior_pair
    (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hL : L < 3)
    (hS4 : ∀ i, -2 ≤ smoothPow 4 (cappedDiff q r L) i ∧
      smoothPow 4 (cappedDiff q r L) i ≤ 2) :
    q 0 = r 0 := by
  have hpositive := hq.1
  have hcases : L = 1 ∨ L = 2 := by omega
  rcases hcases with rfl | rfl
  · have h := hS4 2
    simp [smoothPow, smooth, cappedDiff] at h
    omega
  · have hq01 : q 0 = q 1 := by
      simpa using hq.2.2.2.1 0 (by decide)
    have hr01 : r 0 = r 1 := by
      simpa using hr.2.2.2.1 0 (by decide)
    have h := hS4 2
    simp [smoothPow, smooth, cappedDiff] at h
    omega

/-- Seven equal complete carry words recover the exterior pair coefficient
at every common admissible initial width. -/
theorem seven_carries_determine_exterior_pair
    (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hc : ∀ t, t < 7 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    q 0 = r 0 := by
  have hS4 := seven_carries_smooth_four_box_two q r L hq hr hc
  by_cases hL : 3 ≤ L
  · have hcSwap : ∀ t, t < 7 → ∀ i, i ≤ (iterPairs r L t).1 →
        carry (iterPairs r L t).2 i = carry (iterPairs q L t).2 i := by
      intro t ht i hi
      have hw := matched_widths q r L t (fun s hs => hc s (by omega))
      have hiq : i ≤ (iterPairs q L t).1 := by omega
      exact (hc t ht i hiq).symm
    have hS4Swap := seven_carries_smooth_four_box_two r q L hr hq hcSwap
    have hqr : ¬ r 0 < q 0 := by
      intro hpos
      exact seven_carries_exclude_positive_exterior q r L hq hr hL hc hS4 hpos
    have hrq : ¬ q 0 < r 0 := by
      intro hpos
      exact seven_carries_exclude_positive_exterior r q L hr hq hL hcSwap
        hS4Swap hpos
    omega
  · exact short_width_exterior_pair q r L hq hr (by omega) hS4

#print axioms seven_carries_determine_exterior_pair

end CarryPrefixThresholds
