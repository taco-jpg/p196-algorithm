import DelayedOverlapGate

/-! Exact Group II two-step overlap repair for all positive spacer lengths.
The returned component grows a six-column core.  In particular, at r = 1
its shifted contribution is added to the exterior coefficient.
This proves a finite transition, not a recurrent or infinite certificate. -/

namespace Agent100.GroupII

set_option maxHeartbeats 4000000
set_option maxRecDepth 10000

open Lychrel196 DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory
open DelayedOverlapGate

def Domain (r p u v : Nat) : Prop :=
  1 ≤ r ∧ 1 ≤ p ∧ p ≤ 4 ∧ 5 ≤ u ∧ u ≤ 8 ∧ 5 ≤ v ∧ v ≤ 6 ∧ u + v ≤ 13

def middle (r p u v : Nat) : Nat → Nat :=
  fiveWord r (2 * p) (2 * u + 1) (2 * (u + v) - 19) (4 * v - 18)

def returnedComponent (r p u v i : Nat) : Nat :=
  if i = 0 ∨ i = 2 * r + 5 then 4 * p
  else if i = r ∨ i = r + 5 then 1
  else if i = r + 1 ∨ i = r + 4 then 4 * u - 19
  else if i = r + 2 ∨ i = r + 3 then 4 * v - 18
  else 0

def returned (r p u v : Nat) : Nat → Nat := shiftOne (returnedComponent r p u v)

def initialCarry (r i : Nat) : Nat :=
  if i = r + 3 ∨ i = r + 4 ∨ i = r + 5 then 1 else 0

def middleCarry (r i : Nat) : Nat :=
  if i = r + 2 ∨ i = r + 6 then 1 else 0

def componentDoubleCarry (r i : Nat) : Nat :=
  if i = r + 2 ∨ i = r + 3 ∨ i = r + 4 ∨ i = r + 5 then 1 else 0

theorem domain_core_bounds (r p u v : Nat) (h : Domain r p u v) :
    1 ≤ 4 * u - 19 ∧ 4 * u - 19 ≤ 13 ∧
      2 ≤ 4 * v - 18 ∧ 4 * v - 18 ≤ 6 ∧
      1 ≤ 2 * (u + v) - 19 ∧ 2 * (u + v) - 19 ≤ 7 := by
  unfold Domain at h
  omega

theorem domain_seven_cores (r p u v : Nat) (h : Domain r p u v) :
    (u = 5 ∧ v = 5) ∨ (u = 5 ∧ v = 6) ∨
      (u = 6 ∧ v = 5) ∨ (u = 6 ∧ v = 6) ∨
      (u = 7 ∧ v = 5) ∨ (u = 7 ∧ v = 6) ∨ (u = 8 ∧ v = 5) := by
  unfold Domain at h
  omega

theorem component_low (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, component r p u v i ≤ 9 := by
  unfold Domain at h
  intro i
  unfold component
  repeat (first | omega | split)

theorem component_carry (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i ≤ 2 * r + 6 → carry (component r p u v) i = 0 := by
  apply carry_certificate _ (fun _ => 0) _ rfl
  intro i hi
  have hb := component_low r p u v h i
  omega

theorem initial_carry (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i ≤ 2 * r + 7 → carry (initial r p u v) i = initialCarry r i := by
  unfold Domain at h
  apply carry_certificate _ _ _ (by unfold initialCarry; split <;> omega)
  intro i hi
  simp only [initial, fiveWord, initialCarry]
  repeat (first | omega | split)

theorem middle_carry (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i ≤ 2 * r + 7 → carry (middle r p u v) i = middleCarry r i := by
  unfold Domain at h
  apply carry_certificate _ _ _ (by unfold middleCarry; split <;> omega)
  intro i hi
  simp only [middle, fiveWord, middleCarry]
  repeat (first | omega | split)

theorem component_double_carry (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i ≤ 2 * r + 6 → carry (component r (2 * p) (2 * u) (2 * v)) i =
      componentDoubleCarry r i := by
  unfold Domain at h
  apply carry_certificate _ _ _ (by unfold componentDoubleCarry; split <;> omega)
  intro i hi
  simp only [component, componentDoubleCarry]
  repeat (first | omega | split)

theorem component_no_overflow (r p u v : Nat) (h : Domain r p u v) :
    carry (component r p u v) (2 * r + 6) = 0 :=
  component_carry r p u v h _ (Nat.le_refl _)

theorem initial_no_overflow (r p u v : Nat) (h : Domain r p u v) :
    carry (initial r p u v) (2 * r + 7) = 0 := by
  rw [initial_carry r p u v h _ (Nat.le_refl _)]
  unfold initialCarry
  split <;> omega

theorem middle_no_overflow (r p u v : Nat) (h : Domain r p u v) :
    carry (middle r p u v) (2 * r + 7) = 0 := by
  rw [middle_carry r p u v h _ (Nat.le_refl _)]
  unfold middleCarry
  split <;> omega

theorem component_double_no_overflow (r p u v : Nat) (h : Domain r p u v) :
    carry (component r (2 * p) (2 * u) (2 * v)) (2 * r + 6) = 0 := by
  rw [component_double_carry r p u v h _ (Nat.le_refl _)]
  unfold componentDoubleCarry
  split <;> omega

theorem returnedComponent_symmetric (r p u v : Nat) (hr : 1 ≤ r) :
    ∀ i, i < 2 * r + 6 →
      returnedComponent r p u v i = returnedComponent r p u v (2 * r + 6 - 1 - i) := by
  intro i hi
  simp only [returnedComponent]
  repeat (first | omega | split)

theorem returnedComponent_core_table (r p u v : Nat) (hr : 1 ≤ r) :
    returnedComponent r p u v r = 1 ∧
      returnedComponent r p u v (r + 1) = 4 * u - 19 ∧
      returnedComponent r p u v (r + 2) = 4 * v - 18 ∧
      returnedComponent r p u v (r + 3) = 4 * v - 18 ∧
      returnedComponent r p u v (r + 4) = 4 * u - 19 ∧
      returnedComponent r p u v (r + 5) = 1 := by
  simp only [returnedComponent, true_or, or_true, if_true]
  repeat (first | omega | split)

/-- At the shortest spacer the new outer core coefficient overlaps the
exterior coefficient; the shift is an addition at this boundary. -/
theorem returned_first_neighbor (r p u v : Nat) (hr : 1 ≤ r) :
    returned r p u v 1 = 4 * p + if r = 1 then 1 else 0 := by
  simp only [returned, shiftOne, returnedComponent, Nat.sub_self, true_or, or_true, if_true]
  repeat (first | omega | split)

theorem component_next (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i < 2 * r + 6 → nextColumns (component r p u v) (2 * r + 6) i =
      component r (2 * p) (2 * u) (2 * v) i := by
  intro i hi
  simp only [nextColumns, component_no_overflow r p u v h,
    if_true, columnSum, reflected, output]
  rw [component_carry r p u v h i (by omega),
    component_carry r p u v h (2 * r + 6 - 1 - i) (by omega)]
  unfold Domain at h
  simp only [component]
  repeat (first | omega | split)

theorem component_double_next (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i < 2 * r + 6 →
      nextColumns (component r (2 * p) (2 * u) (2 * v)) (2 * r + 6) i =
        returnedComponent r p u v i := by
  intro i hi
  simp only [nextColumns, component_double_no_overflow r p u v h,
    if_true, columnSum, reflected, output]
  rw [component_double_carry r p u v h i (by omega),
    component_double_carry r p u v h (2 * r + 6 - 1 - i) (by omega)]
  unfold Domain at h
  simp only [component, returnedComponent, componentDoubleCarry]
  repeat (first | omega | split)

theorem initial_next (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i < 2 * r + 7 → nextColumns (initial r p u v) (2 * r + 7) i =
      middle r p u v i := by
  intro i hi
  simp only [nextColumns, initial_no_overflow r p u v h,
    if_true, columnSum, reflected, output]
  rw [initial_carry r p u v h i (by omega),
    initial_carry r p u v h (2 * r + 7 - 1 - i) (by omega)]
  unfold Domain at h
  simp only [initial, middle, fiveWord, initialCarry]
  repeat (first | omega | split)

theorem middle_next (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i < 2 * r + 7 → nextColumns (middle r p u v) (2 * r + 7) i =
      returned r p u v i := by
  intro i hi
  simp only [nextColumns, middle_no_overflow r p u v h,
    if_true, columnSum, reflected, output]
  rw [middle_carry r p u v h i (by omega),
    middle_carry r p u v h (2 * r + 7 - 1 - i) (by omega)]
  have hs : middle r p u v i = middle r p u v (2 * r + 7 - 1 - i) :=
    fiveWord_symmetric r (2 * p) (2 * u + 1) (2 * (u + v) - 19)
      (4 * v - 18) h.1 i hi
  rw [← hs]
  unfold Domain at h
  simp only [middle, returned, fiveWord, middleCarry, shiftOne, returnedComponent]
  repeat (first | omega | split)

theorem returned_is_overlap (r p u v : Nat) :
    ∀ i, returned r p u v i = shiftOne (returnedComponent r p u v) i := by
  intro i
  rfl

/-- The first step has an unavoidable +1 discrepancy at column r + 1. -/
theorem intermediate_overlap_fails (r p u v : Nat) (h : Domain r p u v) :
    ¬ ∀ i, i < 2 * r + 7 →
      nextColumns (initial r p u v) (2 * r + 7) i =
        shiftOne (component r (2 * p) (2 * u) (2 * v)) i := by
  intro he
  have hx := he (r + 1) (by omega)
  rw [initial_next r p u v h (r + 1) (by omega),
    ← initial_is_overlap r (2 * p) (2 * u) (2 * v) h.1 (r + 1)] at hx
  have hd := h
  unfold Domain at hd
  simp only [middle, initial, fiveWord, true_or, or_true, if_true] at hx
  repeat (first | omega | split at hx)

theorem component_two_step_return (r p u v : Nat) (h : Domain r p u v) :
    (iterPairs (component r p u v) (2 * r + 6) 2).1 = 2 * r + 6 ∧
      ∀ i, i < 2 * r + 6 → (iterPairs (component r p u v) (2 * r + 6) 2).2 i =
        returnedComponent r p u v i :=
  two_steps_of_explicit_columns _ _ _ _ (by omega)
    (component_no_overflow r p u v h) (component_double_no_overflow r p u v h)
    (component_next r p u v h) (component_double_next r p u v h)

/-- Full finite overlap repair, including the adjacent-core case r = 1. -/
theorem whole_two_step_return (r p u v : Nat) (h : Domain r p u v) :
    (iterPairs (initial r p u v) (2 * r + 7) 2).1 = 2 * r + 7 ∧
      ∀ i, i < 2 * r + 7 → (iterPairs (initial r p u v) (2 * r + 7) 2).2 i =
        shiftOne (returnedComponent r p u v) i :=
  two_steps_of_explicit_columns _ _ _ _ (by omega)
    (initial_no_overflow r p u v h) (middle_no_overflow r p u v h)
    (initial_next r p u v h) (middle_next r p u v h)

end Agent100.GroupII

#print axioms Agent100.GroupII.domain_core_bounds
#print axioms Agent100.GroupII.domain_seven_cores
#print axioms Agent100.GroupII.component_low
#print axioms Agent100.GroupII.component_carry
#print axioms Agent100.GroupII.initial_carry
#print axioms Agent100.GroupII.middle_carry
#print axioms Agent100.GroupII.component_double_carry
#print axioms Agent100.GroupII.component_no_overflow
#print axioms Agent100.GroupII.initial_no_overflow
#print axioms Agent100.GroupII.middle_no_overflow
#print axioms Agent100.GroupII.component_double_no_overflow
#print axioms Agent100.GroupII.returnedComponent_symmetric
#print axioms Agent100.GroupII.returnedComponent_core_table
#print axioms Agent100.GroupII.returned_first_neighbor
#print axioms Agent100.GroupII.component_next
#print axioms Agent100.GroupII.component_double_next
#print axioms Agent100.GroupII.initial_next
#print axioms Agent100.GroupII.middle_next
#print axioms Agent100.GroupII.returned_is_overlap
#print axioms Agent100.GroupII.intermediate_overlap_fails
#print axioms Agent100.GroupII.component_two_step_return
#print axioms Agent100.GroupII.whole_two_step_return
