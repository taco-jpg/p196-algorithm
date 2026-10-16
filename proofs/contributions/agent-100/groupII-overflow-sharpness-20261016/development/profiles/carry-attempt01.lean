import Agent100GroupIIDefect

/-! Exact first-step and normalization profiles for the upper-exterior
Group II family.  The old GroupII.Domain and all old definitions remain
unchanged.  All widths and carry certificates include the r = 1 boundary. -/

namespace Agent100.GroupIIOverflow

set_option maxHeartbeats 4000000
set_option maxRecDepth 10000

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory
open DelayedOverlapGate

def UpperDomain (r p u v : Nat) : Prop :=
  1 ≤ r ∧ 5 ≤ p ∧ p ≤ 9 ∧ 5 ≤ u ∧ u ≤ 8 ∧ 5 ≤ v ∧ v ≤ 6 ∧ u + v ≤ 13

def componentDoubleCarry (r i : Nat) : Nat :=
  if i = 1 ∨ i = r + 2 ∨ i = r + 3 ∨ i = r + 4 ∨ i = r + 5 ∨ i = 2 * r + 6
  then 1 else 0

def middleCarry (r i : Nat) : Nat :=
  if i = 1 ∨ i = 2 ∨ i = r + 2 ∨ i = r + 6 ∨ i = 2 * r + 6 ∨ i = 2 * r + 7
  then 1 else 0

def redundantCarry (r i : Nat) : Nat :=
  if i = r + 3 ∨ i = r + 4 ∨ i = r + 5 then 2
  else if i = 1 ∨ i = 2 ∨ i = r + 2 ∨ i = r + 6 ∨ i = 2 * r + 6 ∨ i = 2 * r + 7
  then 1 else 0

theorem component_low (r p u v : Nat) (h : UpperDomain r p u v) :
    ∀ i, component r p u v i ≤ 9 := by
  unfold UpperDomain at h
  intro i
  simp only [component]
  repeat (first | omega | split)

theorem component_carry (r p u v : Nat) (h : UpperDomain r p u v) :
    ∀ i, i ≤ 2 * r + 6 → carry (component r p u v) i = 0 := by
  apply carry_certificate _ (fun _ => 0) _ rfl
  intro i hi
  have hb := component_low r p u v h i
  omega

theorem initial_carry (r p u v : Nat) (h : UpperDomain r p u v) :
    ∀ i, i ≤ 2 * r + 7 → carry (initial r p u v) i = GroupII.initialCarry r i := by
  unfold UpperDomain at h
  apply carry_certificate _ _ _ (by unfold GroupII.initialCarry; split <;> omega)
  intro i hi
  simp only [initial, fiveWord, GroupII.initialCarry]
  repeat (first | omega | split)

theorem component_double_carry (r p u v : Nat) (h : UpperDomain r p u v) :
    ∀ i, i ≤ 2 * r + 6 → carry (component r (2 * p) (2 * u) (2 * v)) i =
      componentDoubleCarry r i := by
  unfold UpperDomain at h
  apply carry_certificate _ _ _ (by unfold componentDoubleCarry; split <;> omega)
  intro i hi
  simp only [component, componentDoubleCarry]
  repeat (first | omega | split)

theorem middle_carry (r p u v : Nat) (h : UpperDomain r p u v) :
    ∀ i, i ≤ 2 * r + 7 → carry (GroupII.middle r p u v) i = middleCarry r i := by
  unfold UpperDomain at h
  apply carry_certificate _ _ _ (by unfold middleCarry; split <;> omega)
  intro i hi
  simp only [GroupII.middle, fiveWord, middleCarry]
  repeat (first | omega | split)

theorem redundant_carry (r p u v : Nat) (h : UpperDomain r p u v) :
    ∀ i, i ≤ 2 * r + 7 → carry (redundant r p u v) i = redundantCarry r i := by
  unfold UpperDomain at h
  apply carry_certificate _ _ _
    (by unfold redundantCarry; repeat (first | omega | split))
  intro i hi
  simp only [redundant, initial, fiveWord, redundantCarry]
  repeat (first | omega | split)

theorem component_no_overflow (r p u v : Nat) (h : UpperDomain r p u v) :
    carry (component r p u v) (2 * r + 6) = 0 :=
  component_carry r p u v h _ (Nat.le_refl _)

theorem initial_no_overflow (r p u v : Nat) (h : UpperDomain r p u v) :
    carry (initial r p u v) (2 * r + 7) = 0 := by
  rw [initial_carry r p u v h _ (Nat.le_refl _)]
  unfold GroupII.initialCarry
  split <;> omega

theorem component_double_overflow (r p u v : Nat) (h : UpperDomain r p u v) :
    carry (component r (2 * p) (2 * u) (2 * v)) (2 * r + 6) = 1 := by
  rw [component_double_carry r p u v h _ (Nat.le_refl _)]
  simp only [componentDoubleCarry, or_true, if_true]

theorem middle_overflow (r p u v : Nat) (h : UpperDomain r p u v) :
    carry (GroupII.middle r p u v) (2 * r + 7) = 1 := by
  rw [middle_carry r p u v h _ (Nat.le_refl _)]
  simp only [middleCarry, or_true, if_true]

theorem redundant_overflow (r p u v : Nat) (h : UpperDomain r p u v) :
    carry (redundant r p u v) (2 * r + 7) = 1 := by
  rw [redundant_carry r p u v h _ (Nat.le_refl _)]
  simp only [redundantCarry, or_true, if_true]
  split <;> omega

theorem component_double_width (r p u v : Nat) (h : UpperDomain r p u v) :
    nextWidth (component r (2 * p) (2 * u) (2 * v)) (2 * r + 6) = 2 * r + 7 := by
  simp only [nextWidth, component_double_overflow r p u v h, Nat.one_ne_zero, if_false]

theorem middle_width (r p u v : Nat) (h : UpperDomain r p u v) :
    nextWidth (GroupII.middle r p u v) (2 * r + 7) = 2 * r + 8 := by
  simp only [nextWidth, middle_overflow r p u v h, Nat.one_ne_zero, if_false]

theorem redundant_width (r p u v : Nat) (h : UpperDomain r p u v) :
    nextWidth (redundant r p u v) (2 * r + 7) = 2 * r + 8 := by
  simp only [nextWidth, redundant_overflow r p u v h, Nat.one_ne_zero, if_false]

end Agent100.GroupIIOverflow

#print axioms Agent100.GroupIIOverflow.component_low
#print axioms Agent100.GroupIIOverflow.component_carry
#print axioms Agent100.GroupIIOverflow.initial_carry
#print axioms Agent100.GroupIIOverflow.component_double_carry
#print axioms Agent100.GroupIIOverflow.middle_carry
#print axioms Agent100.GroupIIOverflow.redundant_carry
#print axioms Agent100.GroupIIOverflow.component_no_overflow
#print axioms Agent100.GroupIIOverflow.initial_no_overflow
#print axioms Agent100.GroupIIOverflow.component_double_overflow
#print axioms Agent100.GroupIIOverflow.middle_overflow
#print axioms Agent100.GroupIIOverflow.redundant_overflow
#print axioms Agent100.GroupIIOverflow.component_double_width
#print axioms Agent100.GroupIIOverflow.middle_width
#print axioms Agent100.GroupIIOverflow.redundant_width
