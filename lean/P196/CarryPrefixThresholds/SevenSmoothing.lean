import P196.Agent10EightCarry.Agent10SevenStepCount

/-!
Seven complete carry observations constrain the fourth smoothing of the
zero-extended initial pair difference to the integer interval [-2, 2].
The argument applies at every admissible initial width.
-/

namespace CarryPrefixThresholds

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory
open CarryObservabilityActual DifferenceObservability

/-- Six actual transitions contain at least two nonoverflows. -/
theorem actual_six_step_count_all_widths (q : Nat → Nat) (L : Nat)
    (hq : Admissible L q) :
    2 ≤ orbitCount q L 6 := by
  have h := Agent10SevenStepCount.actual_seven_step_count_all_widths q L hq
  change 3 ≤ orbitCount q L 6 +
    (if carry (iterPairs q L 6).2 (iterPairs q L 6).1 = 0 then 1 else 0) at h
  split at h <;> omega

/-- Equality of seven complete carry words forces the fourth smoothing of
the initial capped difference into [-2, 2], including its entire zero tail. -/
theorem seven_carries_smooth_four_box_two
    (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hc : ∀ t, t < 7 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    ∀ i, -2 ≤ smoothPow 4 (cappedDiff q r L) i ∧
      smoothPow 4 (cappedDiff q r L) i ≤ 2 := by
  by_cases hN : 4 ≤ orbitCount q L 6
  · have heq : ∀ i, i < L → q i = r i := by
      apply iterPairs_endpoint_carry_history_injective q r L 6 hq hr
      · intro t ht i hi
        exact hc t (by omega) i hi
      · exact hN
    have hz : ∀ i, cappedDiff q r L i = 0 := by
      intro i
      by_cases hi : i < L
      · simp [cappedDiff, hi, heq i hi]
      · simp [cappedDiff, hi]
    intro i
    have hs := smoothPow_zero_below (cappedDiff q r L) (i + 1) 4
      (fun j _ => hz j) i (by omega)
    rw [hs]
    omega
  · have hlo := actual_six_step_count_all_widths q L hq
    have hcases : orbitCount q L 6 = 2 ∨ orbitCount q L 6 = 3 := by omega
    have hf := matched_difference_formula q r L 6 hq hr
      (fun t ht => hc t (by omega))
    have hb := cappedDiff_bounds (iterPairs q L 6).2 (iterPairs r L 6).2
      (iterPairs q L 6).1 (hc 6 (by decide))
    rcases hcases with hn | hn
    · intro i
      have he := hf i
      rw [hn] at he
      change cappedDiff (iterPairs q L 6).2 (iterPairs r L 6).2
        (iterPairs q L 6).1 i = 4 * smoothPow 4 (cappedDiff q r L) i at he
      have h := hb i
      rw [he] at h
      omega
    · have hthree : ∀ i, -1 ≤ smoothPow 3 (cappedDiff q r L) i ∧
          smoothPow 3 (cappedDiff q r L) i ≤ 1 := by
        intro i
        have he := hf i
        rw [hn] at he
        change cappedDiff (iterPairs q L 6).2 (iterPairs r L 6).2
          (iterPairs q L 6).1 i = 8 * smoothPow 3 (cappedDiff q r L) i at he
        have h := hb i
        rw [he] at h
        omega
      intro i
      have hcur := hthree i
      have hprev := hthree (i - 1)
      change -2 ≤ smoothPow 3 (cappedDiff q r L) i +
          (if i = 0 then 0 else smoothPow 3 (cappedDiff q r L) (i - 1)) ∧
        smoothPow 3 (cappedDiff q r L) i +
          (if i = 0 then 0 else smoothPow 3 (cappedDiff q r L) (i - 1)) ≤ 2
      by_cases hi : i = 0
      · simp only [if_pos hi]
        omega
      · simp only [if_neg hi]
        omega

#print axioms actual_six_step_count_all_widths
#print axioms seven_carries_smooth_four_box_two

end CarryPrefixThresholds
