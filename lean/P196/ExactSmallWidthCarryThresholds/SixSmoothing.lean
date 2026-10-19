import P196.CarryPrefixThresholds.SevenSmoothing

/-!
Six complete carry observations constrain the fourth smoothing of the
zero-extended initial pair difference to the integer interval [-4, 4].
The argument uses the existing actual six-transition count theorem and
applies at every admissible initial width.
-/

namespace ExactSmallWidthCarryThresholds

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory
open CarryObservabilityActual DifferenceObservability

private theorem smoothPow_succ_box (f : Series) (k : Nat) (b : Int)
    (hb : ∀ i, -b ≤ smoothPow k f i ∧ smoothPow k f i ≤ b) :
    ∀ i, -(b + b) ≤ smoothPow (k + 1) f i ∧
      smoothPow (k + 1) f i ≤ b + b := by
  intro i
  have hcur := hb i
  have hprev := hb (i - 1)
  change -(b + b) ≤ smoothPow k f i +
      (if i = 0 then 0 else smoothPow k f (i - 1)) ∧
    smoothPow k f i +
      (if i = 0 then 0 else smoothPow k f (i - 1)) ≤ b + b
  by_cases hi : i = 0
  · simp only [if_pos hi]
    omega
  · simp only [if_neg hi]
    omega

/-- Equality of six complete carry words forces the fourth smoothing of
the initial capped difference into [-4, 4], including the entire zero tail. -/
theorem six_carries_smooth_four_box_four
    (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hc : ∀ t, t < 6 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    ∀ i, -4 ≤ smoothPow 4 (cappedDiff q r L) i ∧
      smoothPow 4 (cappedDiff q r L) i ≤ 4 := by
  by_cases hN : 4 ≤ orbitCount q L 5
  · have heq : ∀ i, i < L → q i = r i := by
      apply iterPairs_endpoint_carry_history_injective q r L 5 hq hr
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
  · have hlo : 1 ≤ orbitCount q L 5 := by
      have h := CarryPrefixThresholds.actual_six_step_count_all_widths q L hq
      change 2 ≤ orbitCount q L 5 +
        (if carry (iterPairs q L 5).2 (iterPairs q L 5).1 = 0 then 1 else 0) at h
      split at h <;> omega
    have hcases : orbitCount q L 5 = 1 ∨ orbitCount q L 5 = 2 ∨
        orbitCount q L 5 = 3 := by omega
    have hf := matched_difference_formula q r L 5 hq hr
      (fun t ht => hc t (by omega))
    have hb := cappedDiff_bounds (iterPairs q L 5).2 (iterPairs r L 5).2
      (iterPairs q L 5).1 (hc 5 (by decide))
    rcases hcases with hn | hn | hn
    · intro i
      have he := hf i
      rw [hn] at he
      change cappedDiff (iterPairs q L 5).2 (iterPairs r L 5).2
        (iterPairs q L 5).1 i = 2 * smoothPow 4 (cappedDiff q r L) i at he
      have h := hb i
      rw [he] at h
      omega
    · have hthree : ∀ i, -2 ≤ smoothPow 3 (cappedDiff q r L) i ∧
          smoothPow 3 (cappedDiff q r L) i ≤ 2 := by
        intro i
        have he := hf i
        rw [hn] at he
        change cappedDiff (iterPairs q L 5).2 (iterPairs r L 5).2
          (iterPairs q L 5).1 i = 4 * smoothPow 3 (cappedDiff q r L) i at he
        have h := hb i
        rw [he] at h
        omega
      simpa using smoothPow_succ_box (cappedDiff q r L) 3 2 hthree
    · have htwo : ∀ i, -1 ≤ smoothPow 2 (cappedDiff q r L) i ∧
          smoothPow 2 (cappedDiff q r L) i ≤ 1 := by
        intro i
        have he := hf i
        rw [hn] at he
        change cappedDiff (iterPairs q L 5).2 (iterPairs r L 5).2
          (iterPairs q L 5).1 i = 8 * smoothPow 2 (cappedDiff q r L) i at he
        have h := hb i
        rw [he] at h
        omega
      have hthree : ∀ i, -2 ≤ smoothPow 3 (cappedDiff q r L) i ∧
          smoothPow 3 (cappedDiff q r L) i ≤ 2 := by
        simpa using smoothPow_succ_box (cappedDiff q r L) 2 1 htwo
      simpa using smoothPow_succ_box (cappedDiff q r L) 3 2 hthree

#print axioms six_carries_smooth_four_box_four

end ExactSmallWidthCarryThresholds
