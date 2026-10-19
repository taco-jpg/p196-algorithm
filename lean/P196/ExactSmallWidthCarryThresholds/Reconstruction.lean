import P196.ExactSmallWidthCarryThresholds.SixSmoothing
import P196.ExactSmallWidthCarryThresholds.SymmetricBoxFour
import P196.ExactSmallWidthCarryThresholds.WidthSixExclusion

/-!
Six complete carry observations determine all active initial pair sums at
the exact common widths four and six. The shared smoothing bound proves
width-four rigidity directly. At width six, the two possible nonzero
symmetric profiles are excluded using all six actual carry observations.
Later widths are unrestricted, and every observed terminal carry is included.
-/

namespace ExactSmallWidthCarryThresholds

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual DifferenceObservability

private theorem cappedDiff_symmetric
    (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r) :
    ∀ i, i < L → cappedDiff q r L i = cappedDiff q r L (L - 1 - i) := by
  intro i hi
  have hmir : L - 1 - i < L := by omega
  simp only [cappedDiff, if_pos hi, if_pos hmir]
  rw [hq.2.2.2.1 i hi, hr.2.2.2.1 i hi]

/-- Six complete carry words reconstruct every active pair sum at exact
admissible initial width four. -/
theorem six_carry_words_determine_pair_sums_of_width_four
    (q r : Nat → Nat)
    (hq : Admissible 4 q) (hr : Admissible 4 r)
    (hc : ∀ t, t < 6 → ∀ i, i ≤ (iterPairs q 4 t).1 →
      carry (iterPairs q 4 t).2 i = carry (iterPairs r 4 t).2 i) :
    ∀ i, i < 4 → q i = r i := by
  have hg := six_carries_smooth_four_box_four q r 4 hq hr hc
  have hz := smooth_four_box_four_width_four_rigidity (cappedDiff q r 4)
    (by
      intro i hi
      simp [cappedDiff, Nat.not_lt.mpr hi])
    (cappedDiff_symmetric q r 4 hq hr) hg
  intro i hi
  have h := hz i
  simp only [cappedDiff, if_pos hi] at h
  omega

/-- Six complete carry words reconstruct every active pair sum at exact
admissible initial width six. Both orientations of the exceptional algebraic
profiles are excluded by the actual six-word prefix certificate. -/
theorem six_carry_words_determine_pair_sums_of_width_six
    (q r : Nat → Nat)
    (hq : Admissible 6 q) (hr : Admissible 6 r)
    (hc : ∀ t, t < 6 → ∀ i, i ≤ (iterPairs q 6 t).1 →
      carry (iterPairs q 6 t).2 i = carry (iterPairs r 6 t).2 i) :
    ∀ i, i < 6 → q i = r i := by
  have hg := six_carries_smooth_four_box_four q r 6 hq hr hc
  have hclass := smooth_four_box_four_width_six_classification (cappedDiff q r 6)
    (by
      intro i hi
      simp [cappedDiff, Nat.not_lt.mpr hi])
    (cappedDiff_symmetric q r 6 hq hr) hg
  have hsign : cappedDiff q r 6 0 = 0 ∨ cappedDiff q r 6 0 = 1 ∨
      cappedDiff q r 6 0 = -1 := by omega
  rcases hsign with hzero | hpos | hneg
  · intro i hi
    have hz : cappedDiff q r 6 i = 0 := by
      rcases hclass.2 with ha | hb
      · simpa [hzero] using ha i
      · simpa [hzero] using hb i
    simp only [cappedDiff, if_pos hi] at hz
    omega
  · exfalso
    rcases hclass.2 with ha | hb
    · have h0 := hpos
      have h1 := ha 1
      have h2 := ha 2
      rw [hpos] at h1 h2
      simp [cappedDiff, core_six_a] at h0 h1 h2
      exact six_carries_exclude_width_six_profiles q r hq hr hc
        (by omega) (Or.inl ⟨by omega, by omega⟩)
    · have h0 := hpos
      have h1 := hb 1
      have h2 := hb 2
      rw [hpos] at h1 h2
      simp [cappedDiff, core_six_b] at h0 h1 h2
      exact six_carries_exclude_width_six_profiles q r hq hr hc
        (by omega) (Or.inr ⟨by omega, by omega⟩)
  · have hcSwap : ∀ t, t < 6 → ∀ i, i ≤ (iterPairs r 6 t).1 →
        carry (iterPairs r 6 t).2 i = carry (iterPairs q 6 t).2 i := by
      intro t ht i hi
      have hw := matched_widths q r 6 t (fun s hs => hc s (by omega))
      have hiq : i ≤ (iterPairs q 6 t).1 := by omega
      exact (hc t ht i hiq).symm
    exfalso
    rcases hclass.2 with ha | hb
    · have h0 := hneg
      have h1 := ha 1
      have h2 := ha 2
      rw [hneg] at h1 h2
      simp [cappedDiff, core_six_a] at h0 h1 h2
      exact six_carries_exclude_width_six_profiles r q hr hq hcSwap
        (by omega) (Or.inl ⟨by omega, by omega⟩)
    · have h0 := hneg
      have h1 := hb 1
      have h2 := hb 2
      rw [hneg] at h1 h2
      simp [cappedDiff, core_six_b] at h0 h1 h2
      exact six_carries_exclude_width_six_profiles r q hr hq hcSwap
        (by omega) (Or.inr ⟨by omega, by omega⟩)

#print axioms six_carry_words_determine_pair_sums_of_width_four
#print axioms six_carry_words_determine_pair_sums_of_width_six

end ExactSmallWidthCarryThresholds
