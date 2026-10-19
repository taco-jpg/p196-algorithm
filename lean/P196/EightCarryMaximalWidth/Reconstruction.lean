import P196.EightCarryWidthBound.Reconstruction
import P196.EightCarryMaximalWidth.ShortCoreClassification
import P196.EightCarryMaximalWidth.PrefixExclusion

/-!
Agent #10: eight complete carry observations reconstruct initial pair sums
through shared decimal width sixteen. The imported width-fourteen theorem
handles every smaller width. At widths fifteen and sixteen, the short-core
classifiers leave two signs of a possible nonzero difference; the exact
seven-column observation checker excludes both signs.

The numerical conclusion determines the next integer. It does not identify
an initial digit splitting or assert avoidance of decimal palindromes.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace EightCarryMaximalWidth

open DifferenceObservability CarryObservabilityActual
open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory

/-- Stripping two zero coefficients from each end leaves one of the two
classified core widths. Only the first five core coefficients are needed
to expose every nonzero case to the finite prefix exclusion. -/
private theorem short_symmetric_difference_cases
    (f : Series) (L : Nat) (hL : L = 15 ∨ L = 16)
    (hz : ∀ i, L ≤ i → f i = 0)
    (hs : ∀ i, i < L → f i = f (L - 1 - i))
    (houter : ∀ i, i < 2 → f i = 0)
    (hg : ∀ i, -1 ≤ smoothPow 4 f i ∧ smoothPow 4 f i ≤ 1) :
    (∀ i, f i = 0) ∨
      (f 2 = 1 ∧ f 3 = -3 ∧ f 4 = 5 ∧ f 5 = -6 ∧
        (f 6 = 5 ∨ f 6 = 6)) ∨
      (f 2 = -1 ∧ f 3 = 3 ∧ f 4 = -5 ∧ f 5 = 6 ∧
        (f 6 = -5 ∨ f 6 = -6)) := by
  let g : Series := fun i => f (2 + i)
  have gz : ∀ i, L - 4 ≤ i → g i = 0 := by
    intro i hi
    change f (2 + i) = 0
    by_cases hin : 2 + i < L
    · rw [hs (2 + i) hin]
      exact houter (L - 1 - (2 + i)) (by omega)
    · exact hz (2 + i) (by omega)
  have gs : ∀ i, i < L - 4 → g i = g (L - 4 - 1 - i) := by
    intro i hi
    change f (2 + i) = f (2 + (L - 4 - 1 - i))
    rw [hs (2 + i) (by omega)]
    congr 1
    omega
  have gg : ∀ i, -1 ≤ smoothPow 4 g i ∧ smoothPow 4 g i ≤ 1 := by
    intro i
    have ht := smoothPow_tail f 2 4 houter i
    change smoothPow 4 g i = smoothPow 4 f (2 + i) at ht
    rw [ht]
    exact hg (2 + i)
  have hclass : (-1 ≤ g 0 ∧ g 0 ≤ 1) ∧
      ((∀ i, g i = g 0 * Agent10SmoothingBoundary.witness i) ∨
        (∀ i, g i = g 0 * core_twelve i)) := by
    rcases hL with rfl | rfl
    · have h := smooth_four_eleven_classification g gz gs gg
      exact ⟨h.1, Or.inl h.2⟩
    · have h := smooth_four_twelve_classification g gz gs gg
      exact ⟨h.1, Or.inr h.2⟩
  have hp : g 1 = -3 * g 0 ∧ g 2 = 5 * g 0 ∧ g 3 = -6 * g 0 ∧
      (g 4 = 5 * g 0 ∨ g 4 = 6 * g 0) := by
    rcases hclass.2 with h | h
    · have h1 := h 1
      have h2 := h 2
      have h3 := h 3
      have h4 := h 4
      simp only [Agent10SmoothingBoundary.witness] at h1 h2 h3 h4
      omega
    · have h1 := h 1
      have h2 := h 2
      have h3 := h 3
      have h4 := h 4
      simp only [core_twelve] at h1 h2 h3 h4
      omega
  have hsign : g 0 = 0 ∨ g 0 = 1 ∨ g 0 = -1 := by
    have hb := hclass.1
    omega
  rcases hsign with hsign | hsign | hsign
  · left
    have hzero : ∀ i, g i = 0 := by
      intro i
      rcases hclass.2 with h | h
      · simpa only [hsign, Int.zero_mul] using h i
      · simpa only [hsign, Int.zero_mul] using h i
    intro i
    by_cases hi : i < 2
    · exact houter i hi
    · have he := hzero (i - 2)
      change f (2 + (i - 2)) = 0 at he
      have heq : 2 + (i - 2) = i := by omega
      simpa only [heq] using he
  · right
    left
    change g 0 = 1 ∧ g 1 = -3 ∧ g 2 = 5 ∧ g 3 = -6 ∧ (g 4 = 5 ∨ g 4 = 6)
    omega
  · right
    right
    change g 0 = -1 ∧ g 1 = 3 ∧ g 2 = -5 ∧ g 3 = 6 ∧ (g 4 = -5 ∨ g 4 = -6)
    omega

/-- Eight complete carry words recover every initial pair coefficient when
the two admissible words share an initial width at most sixteen. -/
theorem eight_carry_words_determine_pair_sums_of_width_le_sixteen
    (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hL : L ≤ 16)
    (hc : ∀ t, t < 8 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    ∀ i, i < L → q i = r i := by
  by_cases hsmall : L ≤ 14
  · exact EightCarryWidthBound.eight_carry_words_determine_pair_sums_of_width_le_fourteen
      q r L hq hr hsmall hc
  have hwide : L = 15 ∨ L = 16 := by omega
  have h7 : 7 ≤ L := by omega
  by_cases hN : 4 ≤ orbitCount q L 7
  · apply iterPairs_endpoint_carry_history_injective q r L 7 hq hr
    · intro t ht i hi
      exact hc t (by omega) i hi
    · exact hN
  have hlo := Agent10SevenStepCount.actual_seven_step_count_all_widths q L hq
  have hn : orbitCount q L 7 = 3 := by omega
  have hf := matched_difference_formula q r L 7 hq hr
    (fun t ht => hc t (by omega))
  have hb := cappedDiff_bounds (iterPairs q L 7).2 (iterPairs r L 7).2
    (iterPairs q L 7).1 (hc 7 (by decide))
  have hunit : ∀ i, -1 ≤ smoothPow 4 (cappedDiff q r L) i ∧
      smoothPow 4 (cappedDiff q r L) i ≤ 1 := by
    intro i
    have he := hf i
    rw [hn] at he
    change cappedDiff (iterPairs q L 7).2 (iterPairs r L 7).2
      (iterPairs q L 7).1 i = 8 * smoothPow 4 (cappedDiff q r L) i at he
    have hi := hb i
    rw [he] at hi
    omega
  have hfirst := Agent10ThreeColumnCarry.eight_carries_determine_first_two_active_pairs
    q r L hq hr hc
  have houter : ∀ i, i < 2 → cappedDiff q r L i = 0 := by
    intro i hi
    have hiL : i < L := by omega
    simp only [cappedDiff, if_pos hiL, hfirst i hi hiL, Int.sub_self]
  have hz : ∀ i, L ≤ i → cappedDiff q r L i = 0 := by
    intro i hi
    simp only [cappedDiff, if_neg (by omega : ¬ i < L)]
  have hs : ∀ i, i < L →
      cappedDiff q r L i = cappedDiff q r L (L - 1 - i) := by
    intro i hi
    have hm : L - 1 - i < L := by omega
    simp only [cappedDiff, if_pos hi, if_pos hm,
      hq.2.2.2.1 i hi, hr.2.2.2.1 i hi]
  have hcases := short_symmetric_difference_cases (cappedDiff q r L) L
    hwide hz hs houter hunit
  have h0 : q 0 = r 0 := hfirst 0 (by decide) (by omega)
  have h1 : q 1 = r 1 := hfirst 1 (by decide) (by omega)
  have h2L : 2 < L := by omega
  have h3L : 3 < L := by omega
  have h4L : 4 < L := by omega
  have h5L : 5 < L := by omega
  have h6L : 6 < L := by omega
  rcases hcases with hzero | hp | hn
  · intro i hi
    have he := hzero i
    simp only [cappedDiff, if_pos hi] at he
    omega
  · exfalso
    simp only [cappedDiff, if_pos h2L, if_pos h3L, if_pos h4L,
      if_pos h5L, if_pos h6L] at hp
    exact eight_carries_exclude_positive_short_core_prefix q r L hq hr h7 hc h0 h1
      (by omega) (by omega) (by omega) (by omega) (by omega)
  · exfalso
    simp only [cappedDiff, if_pos h2L, if_pos h3L, if_pos h4L,
      if_pos h5L, if_pos h6L] at hn
    have hcSwap : ∀ t, t < 8 → ∀ i, i ≤ (iterPairs r L t).1 →
        carry (iterPairs r L t).2 i = carry (iterPairs q L t).2 i := by
      intro t ht i hi
      have hw := matched_widths q r L t (fun j hj => hc j (by omega))
      have hiq : i ≤ (iterPairs q L t).1 := by rw [hw]; exact hi
      exact (hc t ht i hiq).symm
    exact eight_carries_exclude_positive_short_core_prefix r q L hr hq h7 hcSwap
      h0.symm h1.symm (by omega) (by omega) (by omega) (by omega) (by omega)

/-- Canonical ordinary decimal inputs with a common initial width at most
sixteen and the same eight complete carry words have equal next integers. -/
theorem eight_carry_words_determine_next_integer_of_width_le_sixteen
    (n m : Nat) (d e : Nat → Nat) (L : Nat)
    (hn : Canonical n d L) (hm : Canonical m e L)
    (hL : L ≤ 16)
    (hc : ∀ t, t < 8 → ∀ i, i ≤ (iterPairs (columnSum d L) L t).1 →
      carry (iterPairs (columnSum d L) L t).2 i =
        carry (iterPairs (columnSum e L) L t).2 i) :
    Lychrel196.step n = Lychrel196.step m := by
  have hq := NormalizationBridge.canonical_admissible n d L hn
  have hr := NormalizationBridge.canonical_admissible m e L hm
  have he := eight_carry_words_determine_pair_sums_of_width_le_sixteen
    (columnSum d L) (columnSum e L) L hq hr hL hc
  calc
    Lychrel196.step n = value (columnSum d L) L :=
      step_eq_word_value n d (columnSum d L) L hn (by intro i hi; rfl)
    _ = value (columnSum e L) L := value_congr _ _ L he
    _ = Lychrel196.step m :=
      (step_eq_word_value m e (columnSum e L) L hm (by intro i hi; rfl)).symm

#print axioms eight_carry_words_determine_pair_sums_of_width_le_sixteen
#print axioms eight_carry_words_determine_next_integer_of_width_le_sixteen

end EightCarryMaximalWidth
