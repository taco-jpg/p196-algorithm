import P196.Drafts.Agent100GroupIIRebase.Agent100GroupIIRebaseAlgebra

/-! Exact normalization bounds for the rebased upper-domain component.
All support and symmetry statements use the actual enlarged finite width. -/

namespace Agent100.GroupIIRebase

set_option maxHeartbeats 4000000
set_option maxRecDepth 10000

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory
open DelayedOverlapGate GroupIIOverflow

theorem finite_component_flank (r p u v : Nat) (h : UpperDomain r p u v)
    (i : Nat) (hi : i = r + 1 ∨ i = r + 5) :
    finiteNextComponent r p u v i = 2 * u - 9 := by
  rw [finite_next_component_columns r p u v h i (by omega)]
  simp only [columnSum, reflected]
  rw [component_digits_formula r p u v h, component_digits_formula r p u v h]
  unfold UpperDomain at h
  simp only [component, GroupIIOverflow.componentDoubleCarry]
  repeat (first | omega | split)

theorem finite_component_inner (r p u v : Nat) (h : UpperDomain r p u v)
    (i : Nat) (hi : i = r + 2 ∨ i = r + 4) :
    finiteNextComponent r p u v i = 2 * (u + v) - 18 := by
  rw [finite_next_component_columns r p u v h i (by omega)]
  simp only [columnSum, reflected]
  rw [component_digits_formula r p u v h, component_digits_formula r p u v h]
  unfold UpperDomain at h
  simp only [component, GroupIIOverflow.componentDoubleCarry]
  repeat (first | omega | split)

theorem finite_component_admissible (r p u v : Nat) (h : UpperDomain r p u v) :
    Admissible (2 * r + 7) (finiteNextComponent r p u v) := by
  have ha := NormalizationBridge.admissible_next
    (component r (2 * p) (2 * u) (2 * v)) (2 * r + 6)
    (component_double_admissible r p u v h)
  rw [component_double_width r p u v h] at ha
  apply NormalizationBridge.admissible_congr _ _ _ ha
  intro i hi
  simp only [finiteNextComponent, hi, if_true]

/-- The signed correction is nonnegative at every index before conversion. -/
theorem rebased_nonnegative (r p u v : Nat) (h : UpperDomain r p u v) :
    ∀ i, 0 ≤ rebasedInt r p u v i := by
  intro i
  by_cases hp : i = r + 1 ∨ i = r + 5
  · unfold rebasedInt
    simp only [rebaseDelta, hp, if_true]
    omega
  · by_cases hm : i = r + 2 ∨ i = r + 4
    · have hv := finite_component_inner r p u v h i hm
      unfold rebasedInt
      rw [hv]
      simp only [rebaseDelta, hp, hm, if_false, if_true]
      unfold UpperDomain at h
      omega
    · unfold rebasedInt
      simp only [rebaseDelta, hp, hm, if_false]
      omega

theorem rebased_bounded (r p u v : Nat) (h : UpperDomain r p u v) :
    ∀ i, rebasedInt r p u v i ≤ 18 := by
  intro i
  have hb : finiteNextComponent r p u v i ≤ 18 := by
    by_cases hi : i < 2 * r + 7
    · exact (finite_component_admissible r p u v h).2.2.1 i hi
    · simp only [finiteNextComponent, hi, if_false]
      omega
  by_cases hp : i = r + 1 ∨ i = r + 5
  · have hv := finite_component_flank r p u v h i hp
    unfold rebasedInt
    rw [hv]
    simp only [rebaseDelta, hp, if_true]
    unfold UpperDomain at h
    omega
  · unfold rebasedInt
    simp only [rebaseDelta, hp, if_false]
    split <;> omega

/-- Conversion to Nat preserves the signed coefficient exactly. -/
theorem rebased_toNat_exact (r p u v : Nat) (h : UpperDomain r p u v) :
    ∀ i, (rebasedComponent r p u v i : Int) = rebasedInt r p u v i := by
  intro i
  have hn := rebased_nonnegative r p u v h i
  unfold rebasedComponent
  omega

theorem rebased_zero_after_width (r p u v : Nat) (h : UpperDomain r p u v)
    (i : Nat) (hi : 2 * r + 7 ≤ i) : rebasedComponent r p u v i = 0 := by
  have hr := h.1
  have hn : ¬ i < 2 * r + 7 := by omega
  simp only [rebasedComponent, rebasedInt, finiteNextComponent, hn, if_false,
    rebaseDelta]
  repeat (first | omega | split)

theorem rebased_symmetric (r p u v : Nat) (h : UpperDomain r p u v) :
    ∀ i, i < 2 * r + 7 → rebasedComponent r p u v i =
      rebasedComponent r p u v (2 * r + 7 - 1 - i) := by
  intro i hi
  have hs := (finite_component_admissible r p u v h).2.2.2.1 i hi
  have hd : rebaseDelta r i = rebaseDelta r (2 * r + 7 - 1 - i) := by
    simp only [rebaseDelta]
    repeat (first | omega | split)
  simp only [rebasedComponent, rebasedInt, hs, hd]

theorem rebased_center_eq (r p u v : Nat) (h : UpperDomain r p u v) :
    rebasedComponent r p u v (r + 3) = finiteNextComponent r p u v (r + 3) := by
  simp only [rebasedComponent, rebasedInt, rebaseDelta]
  repeat (first | omega | split)

theorem rebased_outer_eq (r p u v : Nat) (h : UpperDomain r p u v) :
    rebasedComponent r p u v 0 = finiteNextComponent r p u v 0 := by
  simp only [rebasedComponent, rebasedInt, rebaseDelta]
  repeat (first | omega | split)

/-- The rebased component satisfies the original finite pair-word predicate. -/
theorem rebased_admissible (r p u v : Nat) (h : UpperDomain r p u v) :
    Admissible (2 * r + 7) (rebasedComponent r p u v) := by
  have ha := finite_component_admissible r p u v h
  refine ⟨ha.1, ?_, ?_, rebased_symmetric r p u v h, ?_⟩
  · rw [rebased_outer_eq r p u v h]
    exact ha.2.1
  · intro i hi
    have hb := rebased_bounded r p u v h i
    have he := rebased_toNat_exact r p u v h i
    omega
  · intro i hi hc
    have he : i = r + 3 := by omega
    subst i
    rw [rebased_center_eq r p u v h]
    exact ha.2.2.2.2 (r + 3) hi hc

end Agent100.GroupIIRebase

#print axioms Agent100.GroupIIRebase.finite_component_flank
#print axioms Agent100.GroupIIRebase.finite_component_inner
#print axioms Agent100.GroupIIRebase.finite_component_admissible
#print axioms Agent100.GroupIIRebase.rebased_nonnegative
#print axioms Agent100.GroupIIRebase.rebased_bounded
#print axioms Agent100.GroupIIRebase.rebased_toNat_exact
#print axioms Agent100.GroupIIRebase.rebased_zero_after_width
#print axioms Agent100.GroupIIRebase.rebased_symmetric
#print axioms Agent100.GroupIIRebase.rebased_center_eq
#print axioms Agent100.GroupIIRebase.rebased_outer_eq
#print axioms Agent100.GroupIIRebase.rebased_admissible
