import DelayedOverlapGate

/-!
Agent #1: Group III of the retained twenty-core delayed-overlap construction.
Source: renewal_pass/constructive/STATUS.md, section 1, original blob
d684dc1865a3e59e1c699ad1ec28a4dbec0a74e2. The old Group I definitions and
theorems remain unchanged. All equalities below concern the represented
finite prefix. No recurrent or infinite-safety conclusion is asserted.
-/

namespace P196.Agent1.GroupIII

open Lychrel196 DecimalDigits FoldedDecimal OverflowCarryNormalization
  CarryHistory DelayedOverlapGate

set_option maxHeartbeats 4000000
set_option maxRecDepth 10000

def Domain (r p u v : Nat) : Prop :=
  1 ≤ r ∧ 1 ≤ p ∧ p ≤ 4 ∧ 10 ≤ u ∧ u ≤ 13 ∧
    5 ≤ v ∧ v ≤ 6 ∧ u + v ≤ 18

/-- Six central columns, allowing an empty zero run when r=1. -/
def sixWord (r p a b c i : Nat) : Nat :=
  if i = 0 ∨ i = 2*r+5 then p
  else if i = r ∨ i = r+5 then a
  else if i = r+1 ∨ i = r+4 then b
  else if i = r+2 ∨ i = r+3 then c
  else 0

def firstComponent (r p u v : Nat) : Nat → Nat :=
  sixWord r (2*p) 1 (2*u-20) (2*v+1)

def returnedComponent (r p u v : Nat) : Nat → Nat :=
  sixWord r (4*p) 2 (4*u-39) (4*v-17)

/-- The outer and central contributions add at the shortest boundary. -/
def middle (r p u v i : Nat) : Nat :=
  (if i = 0 ∨ i = 1 ∨ i = 2*r+5 ∨ i = 2*r+6 then 2*p else 0) +
  (if i = r ∨ i = r+6 then 1
   else if i = r+1 ∨ i = r+5 then 2*u-19
   else if i = r+2 ∨ i = r+4 then 2*(u+v)-18
   else if i = r+3 then 4*v-18
   else 0)

def componentCarry (r i : Nat) : Nat :=
  if i = r+2 ∨ i = r+5 then 1 else 0

def initialCarry (r i : Nat) : Nat :=
  if r+2 ≤ i ∧ i ≤ r+6 then 1 else 0

theorem initial_admissible (r p u v : Nat) (h : Domain r p u v) :
    Admissible (2*r+7) (DelayedOverlapGate.initial r p u v) := by
  unfold Domain at h
  exact fiveWord_admissible r p u (u+v) (2*v)
    (by omega) (by omega) (by omega) (by omega) (by omega) (by omega) (by omega)

theorem component_carry (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i ≤ 2*r+6 → carry (component r p u v) i = componentCarry r i := by
  unfold Domain at h
  apply carry_certificate _ _ _ (by unfold componentCarry; split <;> omega)
  intro i hi
  simp only [component, componentCarry]
  repeat (first | omega | split)

theorem initial_carry (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i ≤ 2*r+7 → carry (DelayedOverlapGate.initial r p u v) i = initialCarry r i := by
  unfold Domain at h
  apply carry_certificate _ _ _ (by unfold initialCarry; split <;> omega)
  intro i hi
  simp only [DelayedOverlapGate.initial, fiveWord, initialCarry]
  repeat (first | omega | split)

theorem firstComponent_carry (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i ≤ 2*r+6 → carry (firstComponent r p u v) i = componentDoubleCarry r i := by
  unfold Domain at h
  apply carry_certificate _ _ _ (by unfold componentDoubleCarry; split <;> omega)
  intro i hi
  simp only [firstComponent, sixWord, componentDoubleCarry]
  repeat (first | omega | split)

theorem middle_carry (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i ≤ 2*r+7 → carry (middle r p u v) i = middleCarry r i := by
  unfold Domain at h
  apply carry_certificate _ _ _ (by unfold middleCarry; split <;> omega)
  intro i hi
  simp only [middle, middleCarry]
  repeat (first | omega | split)

theorem component_no_overflow (r p u v : Nat) (h : Domain r p u v) :
    carry (component r p u v) (2*r+6) = 0 := by
  rw [component_carry r p u v h _ (Nat.le_refl _)]
  unfold componentCarry
  split <;> omega

theorem initial_no_overflow (r p u v : Nat) (h : Domain r p u v) :
    carry (DelayedOverlapGate.initial r p u v) (2*r+7) = 0 := by
  rw [initial_carry r p u v h _ (Nat.le_refl _)]
  unfold initialCarry
  split <;> omega

theorem firstComponent_no_overflow (r p u v : Nat) (h : Domain r p u v) :
    carry (firstComponent r p u v) (2*r+6) = 0 := by
  rw [firstComponent_carry r p u v h _ (Nat.le_refl _)]
  unfold componentDoubleCarry
  split <;> omega

theorem middle_no_overflow (r p u v : Nat) (h : Domain r p u v) :
    carry (middle r p u v) (2*r+7) = 0 := by
  rw [middle_carry r p u v h _ (Nat.le_refl _)]
  unfold middleCarry
  split <;> omega

theorem component_admissible (r p u v : Nat) (h : Domain r p u v) :
    Admissible (2*r+6) (component r p u v) := by
  have hd := h
  unfold Domain at hd
  refine ⟨by omega, ?_, ?_, component_symmetric r p u v h.1, ?_⟩
  · simp only [component, true_or, if_true]
    omega
  · intro i hi
    simp only [component]
    repeat (first | omega | split)
  · intro i hi he
    omega

theorem component_next (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i < 2*r+6 → nextColumns (component r p u v) (2*r+6) i =
      firstComponent r p u v i := by
  intro i hi
  simp only [nextColumns, component_no_overflow r p u v h,
    if_true, columnSum, reflected, output]
  rw [component_carry r p u v h i (by omega),
    component_carry r p u v h (2*r+6-1-i) (by omega)]
  unfold Domain at h
  simp only [component, componentCarry, firstComponent, sixWord]
  repeat (first | omega | split)

theorem firstComponent_next (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i < 2*r+6 → nextColumns (firstComponent r p u v) (2*r+6) i =
      returnedComponent r p u v i := by
  intro i hi
  simp only [nextColumns, firstComponent_no_overflow r p u v h,
    if_true, columnSum, reflected, output]
  rw [firstComponent_carry r p u v h i (by omega),
    firstComponent_carry r p u v h (2*r+6-1-i) (by omega)]
  unfold Domain at h
  simp only [firstComponent, componentDoubleCarry, returnedComponent, sixWord]
  repeat (first | omega | split)

theorem initial_next (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i < 2*r+7 → nextColumns (DelayedOverlapGate.initial r p u v) (2*r+7) i =
      middle r p u v i := by
  intro i hi
  simp only [nextColumns, initial_no_overflow r p u v h,
    if_true, columnSum, reflected, output]
  rw [initial_carry r p u v h i (by omega),
    initial_carry r p u v h (2*r+7-1-i) (by omega)]
  unfold Domain at h
  simp only [DelayedOverlapGate.initial, fiveWord, initialCarry, middle]
  repeat (first | omega | split)

theorem middle_next (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i < 2*r+7 → nextColumns (middle r p u v) (2*r+7) i =
      shiftOne (returnedComponent r p u v) i := by
  intro i hi
  simp only [nextColumns, middle_no_overflow r p u v h,
    if_true, columnSum, reflected, output]
  rw [middle_carry r p u v h i (by omega),
    middle_carry r p u v h (2*r+7-1-i) (by omega)]
  unfold Domain at h
  simp only [middle, middleCarry, shiftOne, returnedComponent, sixWord]
  repeat (first | omega | split)

theorem component_two_step_return (r p u v : Nat) (h : Domain r p u v) :
    (iterPairs (component r p u v) (2*r+6) 2).1 = 2*r+6 ∧
      ∀ i, i < 2*r+6 → (iterPairs (component r p u v) (2*r+6) 2).2 i =
        returnedComponent r p u v i :=
  two_steps_of_explicit_columns _ _ _ _ (by omega)
    (component_no_overflow r p u v h) (firstComponent_no_overflow r p u v h)
    (component_next r p u v h) (firstComponent_next r p u v h)

theorem whole_two_step_return (r p u v : Nat) (h : Domain r p u v) :
    (iterPairs (DelayedOverlapGate.initial r p u v) (2*r+7) 2).1 = 2*r+7 ∧
      ∀ i, i < 2*r+7 → (iterPairs (DelayedOverlapGate.initial r p u v) (2*r+7) 2).2 i =
        shiftOne (returnedComponent r p u v) i :=
  two_steps_of_explicit_columns _ _ _ _ (by omega)
    (initial_no_overflow r p u v h) (middle_no_overflow r p u v h)
    (initial_next r p u v h) (middle_next r p u v h)

theorem component_next_zeroExtended (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, (if i < 2*r+6 then nextColumns (component r p u v) (2*r+6) i else 0) =
      firstComponent r p u v i := by
  intro i
  split
  · exact component_next r p u v h i (by assumption)
  · simp only [firstComponent, sixWord]
    repeat (first | omega | split)

/-- Exact first departure, using Int subtraction to retain the negative center. -/
theorem coefficient_defect_exact (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, (middle r p u v i : Int) - (shiftOne (firstComponent r p u v) i : Int) =
      coefficientDefect r i := by
  intro i
  unfold Domain at h
  simp only [middle, shiftOne, firstComponent, sixWord, coefficientDefect]
  repeat (first | omega | split)

/-- The first whole-word update genuinely departs from independent overlap. -/
theorem intermediate_overlap_fails (r p u v : Nat) (h : Domain r p u v) :
    ¬ (∀ i, i < 2*r+7 → nextColumns (DelayedOverlapGate.initial r p u v) (2*r+7) i =
      shiftOne (firstComponent r p u v) i) := by
  intro he
  have hec := he (r+3) (by omega)
  rw [initial_next r p u v h (r+3) (by omega)] at hec
  have hd := coefficient_defect_exact r p u v h (r+3)
  rw [hec] at hd
  have hdef : coefficientDefect r (r+3) = -20 := by
    unfold coefficientDefect
    split <;> omega
  rw [hdef] at hd
  omega

theorem initial_not_bad (r p u v : Nat) (h : Domain r p u v) :
    ¬ BadWord (2*r+7) (DelayedOverlapGate.initial r p u v) := by
  have hc : DelayedOverlapGate.initial r p u v (r+3) = 2*v :=
    fiveWord_center r p u (u+v) (2*v) h.1
  have ho : DelayedOverlapGate.initial r p u v 0 = p := fiveWord_zero _ _ _ _ _
  unfold Domain at h
  rintro (hlo | ⟨houter, _⟩)
  · have hb := hlo (r+3) (by omega)
    rw [hc] at hb
    omega
  · rw [ho] at houter
    omega

theorem middle_not_bad (r p u v : Nat) (h : Domain r p u v) :
    ¬ BadWord (2*r+7) (middle r p u v) := by
  have hd := h
  unfold Domain at hd
  have hc : middle r p u v (r+2) = 2*(u+v)-18 := by
    simp only [middle]
    repeat (first | omega | split)
  have ho : middle r p u v 0 = 2*p := by
    simp only [middle]
    repeat (first | omega | split)
  rintro (hlo | ⟨houter, _⟩)
  · have hb := hlo (r+2) (by omega)
    rw [hc] at hb
    omega
  · rw [ho] at houter
    omega

end P196.Agent1.GroupIII
