import P196.SevenCarryMaximalWidth.SymmetricBoxTwo
import P196.SevenCarryMaximalWidth.WidthSevenExclusion
import P196.CarryPrefixThresholds.ExteriorReconstruction

/-!
Seven complete carry observations determine all active initial pair
coefficients through width eight. Removing the already determined exterior
pair leaves a symmetric core of length at most six. Its only possible
nonzero forms have length five, and the actual width-seven prefix exclusion
rules out both forms and their opposite orientations.
-/

namespace SevenCarryMaximalWidth

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual DifferenceObservability

/-- Complete carry reconstruction at every common admissible initial width
at most eight. Later widths are unrestricted and terminal carries are observed. -/
theorem seven_carry_words_determine_pair_sums_of_width_le_eight
    (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r) (hL : L ≤ 8)
    (hc : ∀ t, t < 7 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    ∀ i, i < L → q i = r i := by
  have houter := CarryPrefixThresholds.seven_carries_determine_exterior_pair
    q r L hq hr hc
  by_cases hsmall : L ≤ 2
  · intro i hi
    by_cases hi0 : i = 0
    · simpa only [hi0] using houter
    · have hm : L - 1 - i = 0 := by omega
      rw [hq.2.2.2.1 i hi, hr.2.2.2.1 i hi, hm]
      exact houter
  have hS4 := CarryPrefixThresholds.seven_carries_smooth_four_box_two q r L hq hr hc
  let g : Series := fun i => cappedDiff q r L (1 + i)
  have gz : ∀ i, L - 2 ≤ i → g i = 0 := by
    intro i hi
    by_cases hin : 1 + i < L
    · have hm : L - 1 - (1 + i) = 0 := by omega
      have hqi := hq.2.2.2.1 (1 + i) hin
      have hri := hr.2.2.2.1 (1 + i) hin
      rw [hm] at hqi hri
      simp only [g, cappedDiff, if_pos hin]
      omega
    · simp only [g, cappedDiff, if_neg hin]
  have gs : ∀ i, i < L - 2 → g i = g (L - 2 - 1 - i) := by
    intro i hi
    have hin : 1 + i < L := by omega
    have hmir : 1 + (L - 2 - 1 - i) < L := by omega
    have hm : L - 1 - (1 + i) = 1 + (L - 2 - 1 - i) := by omega
    simp only [g, cappedDiff, if_pos hin, if_pos hmir]
    rw [hq.2.2.2.1 (1 + i) hin, hr.2.2.2.1 (1 + i) hin, hm]
  have gh : ∀ i, -2 ≤ smoothPow 4 g i ∧ smoothPow 4 g i ≤ 2 := by
    have hz0 : ∀ j, j < 1 → cappedDiff q r L j = 0 := by
      intro j hj
      have hj0 : j = 0 := by omega
      subst j
      simp [cappedDiff, hq.1, houter]
    intro i
    have ht := smoothPow_tail (cappedDiff q r L) 1 4 hz0 i
    change smoothPow 4 g i = smoothPow 4 (cappedDiff q r L) (1 + i) at ht
    rw [ht]
    exact hS4 (1 + i)
  have hclass := smooth_four_box_two_short_classification g (L - 2)
    (by omega) gz gs gh
  rcases hclass with hzero | ⟨hR, hforms⟩
  · intro i hi
    by_cases hi0 : i = 0
    · simpa only [hi0] using houter
    · have he := hzero (i - 1)
      have hind : 1 + (i - 1) = i := by omega
      change cappedDiff q r L (1 + (i - 1)) = 0 at he
      rw [hind] at he
      simp only [cappedDiff, if_pos hi] at he
      omega
  · have hseven : L = 7 := by omega
    subst L
    have hcSwap : ∀ t, t < 7 → ∀ i, i ≤ (iterPairs r 7 t).1 →
        carry (iterPairs r 7 t).2 i = carry (iterPairs q 7 t).2 i := by
      intro t ht i hi
      have hw := matched_widths q r 7 t (fun s hs => hc s (by omega))
      have hiq : i ≤ (iterPairs q 7 t).1 := by omega
      exact (hc t ht i hiq).symm
    exfalso
    rcases hforms with ha | ha | hb | hb
    · have h0 := ha 0
      have h1 := ha 1
      have h2 := ha 2
      simp [g, cappedDiff, core_five_a] at h0 h1 h2
      exact seven_carries_exclude_width_seven_profiles q r hq hr hc houter
        (by omega) (Or.inl ⟨by omega, by omega⟩)
    · have h0 := ha 0
      have h1 := ha 1
      have h2 := ha 2
      simp [g, cappedDiff, core_five_a] at h0 h1 h2
      exact seven_carries_exclude_width_seven_profiles r q hr hq hcSwap houter.symm
        (by omega) (Or.inl ⟨by omega, by omega⟩)
    · have h0 := hb 0
      have h1 := hb 1
      have h2 := hb 2
      simp [g, cappedDiff, core_five_b] at h0 h1 h2
      exact seven_carries_exclude_width_seven_profiles q r hq hr hc houter
        (by omega) (Or.inr ⟨by omega, by omega⟩)
    · have h0 := hb 0
      have h1 := hb 1
      have h2 := hb 2
      simp [g, cappedDiff, core_five_b] at h0 h1 h2
      exact seven_carries_exclude_width_seven_profiles r q hr hq hcSwap houter.symm
        (by omega) (Or.inr ⟨by omega, by omega⟩)

/-- At shared canonical initial widths through eight, the seven observations
determine the next ordinary reverse-and-add integer. -/
theorem seven_carry_words_determine_next_integer_of_width_le_eight
    (n m : Nat) (d e : Nat → Nat) (L : Nat)
    (hn : Canonical n d L) (hm : Canonical m e L) (hL : L ≤ 8)
    (hc : ∀ t, t < 7 → ∀ i, i ≤ (iterPairs (columnSum d L) L t).1 →
      carry (iterPairs (columnSum d L) L t).2 i =
        carry (iterPairs (columnSum e L) L t).2 i) :
    Lychrel196.step n = Lychrel196.step m := by
  have hq := NormalizationBridge.canonical_admissible n d L hn
  have hr := NormalizationBridge.canonical_admissible m e L hm
  have he := seven_carry_words_determine_pair_sums_of_width_le_eight
    (columnSum d L) (columnSum e L) L hq hr hL hc
  calc
    Lychrel196.step n = value (columnSum d L) L :=
      step_eq_word_value n d (columnSum d L) L hn (by intro i hi; rfl)
    _ = value (columnSum e L) L := value_congr _ _ L he
    _ = Lychrel196.step m :=
      (step_eq_word_value m e (columnSum e L) L hm (by intro i hi; rfl)).symm

#print axioms seven_carry_words_determine_pair_sums_of_width_le_eight
#print axioms seven_carry_words_determine_next_integer_of_width_le_eight

end SevenCarryMaximalWidth
