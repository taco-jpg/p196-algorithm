import P196.CarryPrefixThresholds.OuterCertificate
import P196.CarryPrefixThresholds.SecondCertificate
import P196.CarryPrefixThresholds.ThirdCertificate
import P196.Agent10CarryObservability.Agent10PrefixExclusion

/-!
Seven complete actual carry observations exclude a positive exterior
difference. The fourth-smoothing box bound restricts only the next two
coefficients. Every finite membership step is connected to the existing
actual-history checker at the same observation count, including terminal
carries and valid successor words.
-/

namespace CarryPrefixThresholds

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual SevenColumnProjection DifferenceObservability
open EightCarryMaximalWidth.PrefixHistory
open Candidates

/-- A positive exterior difference cannot have seven equal complete carry
words and the fourth-smoothing box-two bound at an initial width at least 3. -/
theorem seven_carries_exclude_positive_exterior
    (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hL : 3 ≤ L)
    (hc : ∀ t, t < 7 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i)
    (hS4 : ∀ i, -2 ≤ smoothPow 4 (cappedDiff q r L) i ∧
      smoothPow 4 (cappedDiff q r L) i ≤ 2)
    (hpos : r 0 < q 0) : False := by
  have hzero : 0 < L := by omega
  have hone : 1 < L := by omega
  have htwo : 2 < L := by omega
  have hq0 := hq.2.1
  have hr0 := hr.2.1
  have hq0b := hq.2.2.1 0 hzero
  have hr0b := hr.2.2.1 0 hzero
  have hq1b := hq.2.2.1 1 hone
  have hr1b := hr.2.2.1 1 hone
  have hq2b := hq.2.2.1 2 htwo
  have hr2b := hr.2.2.1 2 htwo

  have hs1 : accepted ([q 0], [r 0]) = true := by
    exact actual_history_survives_encoded q r L 1 7 hq hr (by decide)
      (by omega) hc
  have hm0 : ([q 0], [r 0]) ∈ positiveOuterStarts := by
    unfold positiveOuterStarts
    apply List.mem_flatMap.mpr
    refine ⟨q 0 - 1, List.mem_range.mpr (by omega), ?_⟩
    apply List.mem_map.mpr
    refine ⟨r 0 - 1, List.mem_range.mpr (by omega), ?_⟩
    simp only [Nat.sub_add_cancel (by omega : 1 ≤ q 0),
      Nat.sub_add_cancel (by omega : 1 ≤ r 0)]
  have hm1 : ([q 0], [r 0]) ∈ outerCover := by
    have h := List.all_eq_true.mp outer_cover ([q 0], [r 0]) hm0
    apply List.contains_iff_mem.mp
    simpa only [hs1, Bool.not_true, Bool.or_false] using h
  have hstep : q 0 = r 0 + 1 := by
    have h := hm1
    simp [outerCover] at h
    rcases h with h | h | h | h <;> omega

  rcases Agent10PrefixExclusion.smooth_four_first_coefficients
    (cappedDiff q r L) with ⟨_, hcoef1, hcoef2, _⟩
  have hb1 := hS4 1
  rw [hcoef1] at hb1
  simp only [cappedDiff, if_pos hzero, if_pos hone] at hb1
  have hsecondBounds : q 1 + 2 ≤ r 1 ∧ r 1 ≤ q 1 + 6 := by omega
  let d := r 1 - q 1 - 2
  have hd : d < 5 := by dsimp [d]; omega
  have heq : r 1 = q 1 + (d + 2) := by dsimp [d]; omega
  have ha : q 1 < 17 - d := by dsimp [d]; omega
  have hmSecond : ([q 0, q 1], [r 0, r 1]) ∈ secondStarts := by
    unfold secondStarts
    apply List.mem_flatMap.mpr
    refine ⟨d, List.mem_range.mpr hd, ?_⟩
    have he := EightCarryMaximalWidth.Candidates.extensions_mem
      0 (d + 2) (17 - d) outerCover [q 0] [r 0] hm1 (q 1) ha
    simpa only [Nat.add_zero, List.cons_append, List.nil_append, heq] using he
  have hs2 : accepted ([q 0, q 1], [r 0, r 1]) = true := by
    exact actual_history_survives_encoded q r L 2 7 hq hr (by decide)
      (by omega) hc
  have hm2 : ([q 0, q 1], [r 0, r 1]) ∈ secondCover := by
    have h := List.all_eq_true.mp second_cover ([q 0, q 1], [r 0, r 1]) hmSecond
    apply List.contains_iff_mem.mp
    simpa only [hs2, Bool.not_true, Bool.or_false] using h
  have hshape := hm2
  simp [secondCover] at hshape
  have hq0eq : q 0 = 15 := by omega
  have hq1eq : q 1 = 16 := by omega
  have hr0eq : r 0 = 14 := by omega
  have hr1eq : r 1 = 18 := by omega

  have hb2 := hS4 2
  rw [hcoef2] at hb2
  simp only [cappedDiff, if_pos hzero, if_pos hone, if_pos htwo,
    hq0eq, hq1eq, hr0eq, hr1eq] at hb2
  have hthirdBounds : r 2 ≤ q 2 ∧ q 2 ≤ r 2 + 4 := by omega
  let e := q 2 - r 2
  have hed : e < 5 := by dsimp [e]; omega
  have heq2 : q 2 = r 2 + e := by dsimp [e]; omega
  have hea : r 2 < 19 - e := by dsimp [e]; omega
  have hmThird : ([q 0, q 1, q 2], [r 0, r 1, r 2]) ∈ thirdStarts := by
    unfold thirdStarts
    apply List.mem_flatMap.mpr
    refine ⟨e, List.mem_range.mpr hed, ?_⟩
    have he := EightCarryMaximalWidth.Candidates.extensions_mem
      e 0 (19 - e) secondCover [q 0, q 1] [r 0, r 1] hm2 (r 2) hea
    simpa only [Nat.add_zero, List.cons_append, List.nil_append, heq2] using he
  have hs3 : accepted ([q 0, q 1, q 2], [r 0, r 1, r 2]) = true := by
    exact actual_history_survives_encoded q r L 3 7 hq hr (by decide) hL hc
  have hfinal := List.all_eq_true.mp third_exclusion
    ([q 0, q 1, q 2], [r 0, r 1, r 2]) hmThird
  simp only [hs3, Bool.not_true, Bool.false_eq_true] at hfinal

#print axioms seven_carries_exclude_positive_exterior

end CarryPrefixThresholds
