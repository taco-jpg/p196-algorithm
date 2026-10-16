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

end P196.Agent1.GroupIII
