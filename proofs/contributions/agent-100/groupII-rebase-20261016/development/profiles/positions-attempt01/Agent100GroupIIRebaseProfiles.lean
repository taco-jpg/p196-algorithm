import Agent100GroupIIOverflowBridge

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
  simp only [component, componentDoubleCarry]
  repeat (first | omega | split)

theorem finite_component_inner (r p u v : Nat) (h : UpperDomain r p u v)
    (i : Nat) (hi : i = r + 2 ∨ i = r + 4) :
    finiteNextComponent r p u v i = 2 * (u + v) - 18 := by
  rw [finite_next_component_columns r p u v h i (by omega)]
  simp only [columnSum, reflected]
  rw [component_digits_formula r p u v h, component_digits_formula r p u v h]
  unfold UpperDomain at h
  simp only [component, componentDoubleCarry]
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

end Agent100.GroupIIRebase

#print axioms Agent100.GroupIIRebase.finite_component_flank
#print axioms Agent100.GroupIIRebase.finite_component_inner
#print axioms Agent100.GroupIIRebase.finite_component_admissible
