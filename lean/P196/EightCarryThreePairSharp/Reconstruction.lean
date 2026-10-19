import P196.EightCarryWidthBound.Reconstruction
import P196.EightCarryMaximalWidth.PrefixExclusion
import P196.EightCarryThreePairSharp.BoundedSmoothing
import P196.EightCarryThreePairSharp.PrefixExclusion

/-!
Agent #10: eight complete carry observations determine the first three
active initial pair coefficients at every common admissible width.

The imported width-fourteen theorem handles small widths. At larger widths,
four nonoverflow transitions already give full reconstruction. In the remaining
three-nonoverflow case, the actual difference recurrence puts the fourth
smoothing in the unit interval. The bounded smoothing classification and the
two exact prefix exclusions then rule out a positive third-pair difference.
Swapping the matched histories gives the reverse inequality.

All complete carry words include the terminal overflow carry. The conclusion
concerns active pair coefficients and has no bound on the initial width.
-/

set_option maxHeartbeats 10000000
set_option maxRecDepth 100000

namespace EightCarryThreePairSharp

open DifferenceObservability CarryObservabilityActual
open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory

/-- A positive difference in the third pair would have one of the two
classified initial patterns, each excluded by a complete prefix history. -/
private theorem eight_carries_third_pair_le
    (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r) (h7 : 7 ≤ L)
    (hc : ∀ t, t < 8 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    q 2 ≤ r 2 := by
  by_cases hmany : 4 ≤ orbitCount q L 7
  · have he := iterPairs_endpoint_carry_history_injective q r L 7 hq hr
      (fun t ht i hi => hc t (by omega) i hi) hmany
    exact Nat.le_of_eq (he 2 (by omega))
  have hcount : orbitCount q L 7 = 3 := by
    have hminimum := Agent10SevenStepCount.actual_seven_step_count_all_widths q L hq
    omega
  have hrecurrence := matched_difference_formula q r L 7 hq hr
    (fun t ht => hc t (by omega))
  have hseventh := cappedDiff_bounds (iterPairs q L 7).2 (iterPairs r L 7).2
    (iterPairs q L 7).1 (hc 7 (by decide))
  have hunit : ∀ i, -1 ≤ smoothPow 4 (cappedDiff q r L) i ∧
      smoothPow 4 (cappedDiff q r L) i ≤ 1 := by
    intro i
    have he := hrecurrence i
    simp only [hcount] at he
    change cappedDiff (iterPairs q L 7).2 (iterPairs r L 7).2
      (iterPairs q L 7).1 i = 8 * smoothPow 4 (cappedDiff q r L) i at he
    have hb := hseventh i
    omega
  have hbounded := cappedDiff_bounds q r L (hc 0 (by decide))
  have hfirst := Agent10ThreeColumnCarry.eight_carries_determine_first_two_active_pairs
    q r L hq hr hc
  have h0 : q 0 = r 0 := hfirst 0 (by decide) (by omega)
  have h1 : q 1 = r 1 := hfirst 1 (by decide) (by omega)
  have hf0 : cappedDiff q r L 0 = 0 := by
    simp only [cappedDiff, if_pos (by omega : 0 < L), h0, Int.sub_self]
  have hf1 : cappedDiff q r L 1 = 0 := by
    simp only [cappedDiff, if_pos (by omega : 1 < L), h1, Int.sub_self]
  have h2L : 2 < L := by omega
  have h3L : 3 < L := by omega
  have h4L : 4 < L := by omega
  have h5L : 5 < L := by omega
  have h6L : 6 < L := by omega
  by_cases hle : q 2 ≤ r 2
  · exact hle
  exfalso
  have hsmall := hunit 2
  simp [smoothPow, smooth, hf0, hf1] at hsmall
  have h2 : cappedDiff q r L 2 = 1 := by
    simp only [cappedDiff, if_pos h2L] at hsmall ⊢
    omega
  obtain ⟨h3, h4, hnext⟩ := bounded_unit_four_initial_cases
    (cappedDiff q r L) hf0 hf1 h2 hbounded hunit
  simp only [cappedDiff, if_pos h2L, if_pos h3L, if_pos h4L] at h2 h3 h4
  rcases hnext with ⟨h5, h6⟩ | ⟨h5, h6⟩
  · simp only [cappedDiff, if_pos h5L, if_pos h6L] at h5 h6
    exact EightCarryMaximalWidth.eight_carries_exclude_positive_short_core_prefix
      q r L hq hr h7 hc h0 h1 (by omega) (by omega) (by omega)
      (by omega) (by omega)
  · simp only [cappedDiff, if_pos h5L, if_pos h6L] at h5 h6
    exact eight_carries_exclude_minus_seven_prefix
      q r L hq hr h7 hc h0 h1 (by omega) (by omega) (by omega)
      (by omega) (by omega)

/-- Eight matching complete carry words determine all active initial pair
coefficients at indices zero, one, and two, with no initial-width bound. -/
theorem eight_carries_determine_first_three_active_pairs
    (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hc : ∀ t, t < 8 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    ∀ i, i < 3 → i < L → q i = r i := by
  by_cases hsmall : L ≤ 14
  · intro i _ hiL
    exact EightCarryWidthBound.eight_carry_words_determine_pair_sums_of_width_le_fourteen
      q r L hq hr hsmall hc i hiL
  have h7 : 7 ≤ L := by omega
  have hfirst := Agent10ThreeColumnCarry.eight_carries_determine_first_two_active_pairs
    q r L hq hr hc
  intro i hi hiL
  by_cases hi2 : i < 2
  · exact hfirst i hi2 hiL
  have he : i = 2 := by omega
  subst i
  apply Nat.le_antisymm
  · exact eight_carries_third_pair_le q r L hq hr h7 hc
  · have hcSwap : ∀ t, t < 8 → ∀ j, j ≤ (iterPairs r L t).1 →
        carry (iterPairs r L t).2 j = carry (iterPairs q L t).2 j := by
      intro t ht j hj
      have hwidth := matched_widths q r L t (fun k hk => hc k (by omega))
      have hjq : j ≤ (iterPairs q L t).1 := by
        rw [hwidth]
        exact hj
      exact (hc t ht j hjq).symm
    exact eight_carries_third_pair_le r q L hr hq h7 hcSwap

#print axioms eight_carries_determine_first_three_active_pairs

end EightCarryThreePairSharp
