import P196.ExactWidthCarryThresholds.SymmetricBoxTwo
import P196.ExactWidthCarryThresholds.WidthTenExclusion
import P196.CarryPrefixThresholds.ExteriorReconstruction

/-!
Seven complete carry observations determine all active initial pair sums at
the exact common width ten. The already determined exterior pair is removed
from the capped difference, leaving a symmetric core of length eight. The
fourth-smoothing classification and the actual prefix exclusion rule out
both orientations of the only nonzero core. Later widths are unrestricted.
-/

namespace ExactWidthCarryThresholds

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual DifferenceObservability

/-- Seven complete carry words, including every observed terminal carry,
reconstruct all active pair sums at exact admissible initial width ten. -/
theorem seven_carry_words_determine_pair_sums_of_width_ten
    (q r : Nat → Nat)
    (hq : Admissible 10 q) (hr : Admissible 10 r)
    (hc : ∀ t, t < 7 → ∀ i, i ≤ (iterPairs q 10 t).1 →
      carry (iterPairs q 10 t).2 i = carry (iterPairs r 10 t).2 i) :
    ∀ i, i < 10 → q i = r i := by
  have houter := CarryPrefixThresholds.seven_carries_determine_exterior_pair
    q r 10 hq hr hc
  have hS4 := CarryPrefixThresholds.seven_carries_smooth_four_box_two
    q r 10 hq hr hc
  let g : Series := fun i => cappedDiff q r 10 (1 + i)
  have gz : ∀ i, 8 ≤ i → g i = 0 := by
    intro i hi
    by_cases hin : 1 + i < 10
    · have hm : 10 - 1 - (1 + i) = 0 := by omega
      have hqi := hq.2.2.2.1 (1 + i) hin
      have hri := hr.2.2.2.1 (1 + i) hin
      rw [hm] at hqi hri
      simp only [g, cappedDiff, if_pos hin]
      omega
    · simp only [g, cappedDiff, if_neg hin]
  have gs : ∀ i, i < 8 → g i = g (8 - 1 - i) := by
    intro i hi
    have hin : 1 + i < 10 := by omega
    have hmir : 1 + (8 - 1 - i) < 10 := by omega
    have hm : 10 - 1 - (1 + i) = 1 + (8 - 1 - i) := by omega
    simp only [g, cappedDiff, if_pos hin, if_pos hmir]
    rw [hq.2.2.2.1 (1 + i) hin, hr.2.2.2.1 (1 + i) hin, hm]
  have gh : ∀ i, -2 ≤ smoothPow 4 g i ∧ smoothPow 4 g i ≤ 2 := by
    have hz0 : ∀ j, j < 1 → cappedDiff q r 10 j = 0 := by
      intro j hj
      have hj0 : j = 0 := by omega
      subst j
      simp [cappedDiff, houter]
    intro i
    have ht := smoothPow_tail (cappedDiff q r 10) 1 4 hz0 i
    change smoothPow 4 g i = smoothPow 4 (cappedDiff q r 10) (1 + i) at ht
    rw [ht]
    exact hS4 (1 + i)
  have hclass := smooth_four_box_two_width_eight_classification g gz gs gh
  have hsign : g 0 = 0 ∨ g 0 = 1 ∨ g 0 = -1 := by omega
  rcases hsign with hzero | hpos | hneg
  · intro i hi
    by_cases hi0 : i = 0
    · simpa only [hi0] using houter
    · have he : g (i - 1) = 0 := by
        simpa [hzero] using hclass.2 (i - 1)
      have hind : 1 + (i - 1) = i := by omega
      change cappedDiff q r 10 (1 + (i - 1)) = 0 at he
      rw [hind] at he
      simp only [cappedDiff, if_pos hi] at he
      omega
  · exfalso
    have h0 := hpos
    have h1 := hclass.2 1
    have h2 := hclass.2 2
    have h3 := hclass.2 3
    rw [hpos] at h1 h2 h3
    simp [g, cappedDiff, core_eight] at h0 h1 h2 h3
    exact seven_carries_exclude_width_ten_profile q r hq hr hc houter
      (by omega) (by omega) (by omega) (by omega)
  · have hcSwap : ∀ t, t < 7 → ∀ i, i ≤ (iterPairs r 10 t).1 →
        carry (iterPairs r 10 t).2 i = carry (iterPairs q 10 t).2 i := by
      intro t ht i hi
      have hw := matched_widths q r 10 t (fun s hs => hc s (by omega))
      have hiq : i ≤ (iterPairs q 10 t).1 := by omega
      exact (hc t ht i hiq).symm
    exfalso
    have h0 := hneg
    have h1 := hclass.2 1
    have h2 := hclass.2 2
    have h3 := hclass.2 3
    rw [hneg] at h1 h2 h3
    simp [g, cappedDiff, core_eight] at h0 h1 h2 h3
    exact seven_carries_exclude_width_ten_profile r q hr hq hcSwap houter.symm
      (by omega) (by omega) (by omega) (by omega)

#print axioms seven_carry_words_determine_pair_sums_of_width_ten

end ExactWidthCarryThresholds
