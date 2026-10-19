import P196.EightCarryWidthBound.SymmetricSmoothing
import P196.Agent10TwoPairReconstruction.Agent10ThreeColumnCarry

/-!
Agent #10: eight complete carry observations reconstruct every initial pair
coefficient when the shared initial decimal width is at most fourteen.

The existing seven-transition count leaves either four nonoverflow steps,
which already force reconstruction, or three nonoverflows and four overflows.
In the latter case the exact difference recurrence bounds the fourth smoothing
by one. Existing first-two-pair reconstruction removes two zero coefficients
at each end, and short symmetric smoothing rigidity eliminates what remains.

All observations include the terminal carry. The integer conclusion identifies
the next integer, not the initial digit splitting. This theorem does not assert
that eight observations suffice at every width, that fourteen is the largest
valid width bound, or that any orbit avoids palindromes.
-/

namespace EightCarryWidthBound

open DifferenceObservability CarryObservabilityActual
open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory

/-- Removing two zero coefficients from each end leaves a symmetric series of
length at most ten. The input coefficients need no separate magnitude bound. -/
theorem smooth_four_rigidity_of_width_le_fourteen
    (f : Series) (L : Nat) (hL : L ≤ 14)
    (hz : ∀ i, L ≤ i → f i = 0)
    (hs : ∀ i, i < L → f i = f (L - 1 - i))
    (houter : ∀ i, i < 2 → f i = 0)
    (hg : ∀ i, -1 ≤ smoothPow 4 f i ∧ smoothPow 4 f i ≤ 1) :
    ∀ i, f i = 0 := by
  by_cases hsmall : L ≤ 4
  · intro i
    by_cases hi : i < L
    · by_cases hlow : i < 2
      · exact houter i hlow
      · rw [hs i hi]
        exact houter (L - 1 - i) (by omega)
    · exact hz i (by omega)
  · let g : Series := fun i => f (2 + i)
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
    have hzero := smooth_four_short_symmetric g (L - 4) (by omega) gz gs gg
    intro i
    by_cases hi : i < 2
    · exact houter i hi
    · have he := hzero (i - 2)
      change f (2 + (i - 2)) = 0 at he
      have hind : 2 + (i - 2) = i := by omega
      simpa only [hind] using he

/-- Eight complete carry words suffice at every admissible initial width up to
fourteen, including the small widths where outer positions overlap. -/
theorem eight_carry_words_determine_pair_sums_of_width_le_fourteen
    (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hL : L ≤ 14)
    (hc : ∀ t, t < 8 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    ∀ i, i < L → q i = r i := by
  by_cases hN : 4 ≤ orbitCount q L 7
  · apply iterPairs_endpoint_carry_history_injective q r L 7 hq hr
    · intro t ht i hi
      exact hc t (by omega) i hi
    · exact hN
  · have hlo := Agent10SevenStepCount.actual_seven_step_count_all_widths q L hq
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
      by_cases hiL : i < L
      · simp only [cappedDiff, if_pos hiL, hfirst i hi hiL, Int.sub_self]
      · simp only [cappedDiff, if_neg hiL]
    have hz : ∀ i, L ≤ i → cappedDiff q r L i = 0 := by
      intro i hi
      simp only [cappedDiff, if_neg (by omega : ¬ i < L)]
    have hs : ∀ i, i < L →
        cappedDiff q r L i = cappedDiff q r L (L - 1 - i) := by
      intro i hi
      have hm : L - 1 - i < L := by omega
      simp only [cappedDiff, if_pos hi, if_pos hm,
        hq.2.2.2.1 i hi, hr.2.2.2.1 i hi]
    have hzero := smooth_four_rigidity_of_width_le_fourteen
      (cappedDiff q r L) L hL hz hs houter hunit
    intro i hi
    have he := hzero i
    simp only [cappedDiff, if_pos hi] at he
    omega

/-- Ordinary decimal inputs with a common canonical width at most fourteen and
the same eight complete carry words have the same next integer. -/
theorem eight_carry_words_determine_next_integer_of_width_le_fourteen
    (n m : Nat) (d e : Nat → Nat) (L : Nat)
    (hn : Canonical n d L) (hm : Canonical m e L)
    (hL : L ≤ 14)
    (hc : ∀ t, t < 8 → ∀ i, i ≤ (iterPairs (columnSum d L) L t).1 →
      carry (iterPairs (columnSum d L) L t).2 i =
        carry (iterPairs (columnSum e L) L t).2 i) :
    Lychrel196.step n = Lychrel196.step m := by
  have hq := NormalizationBridge.canonical_admissible n d L hn
  have hr := NormalizationBridge.canonical_admissible m e L hm
  have he := eight_carry_words_determine_pair_sums_of_width_le_fourteen
    (columnSum d L) (columnSum e L) L hq hr hL hc
  calc
    Lychrel196.step n = value (columnSum d L) L :=
      step_eq_word_value n d (columnSum d L) L hn (by intro i hi; rfl)
    _ = value (columnSum e L) L := value_congr _ _ L he
    _ = Lychrel196.step m :=
      (step_eq_word_value m e (columnSum e L) L hm (by intro i hi; rfl)).symm

#print axioms smooth_four_rigidity_of_width_le_fourteen
#print axioms eight_carry_words_determine_pair_sums_of_width_le_fourteen
#print axioms eight_carry_words_determine_next_integer_of_width_le_fourteen

end EightCarryWidthBound
