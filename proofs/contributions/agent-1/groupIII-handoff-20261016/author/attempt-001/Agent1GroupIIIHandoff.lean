import Agent1GroupIII

/-! Agent #1: the second delayed repair of the fixed Group III (1,10,6) family.
Written source: renewal_pass/constructive/STATUS.md, section 3, original blob
d684dc1865a3e59e1c699ad1ec28a4dbec0a74e2. The shortest spacer is treated
separately; no time-six, recurrence, or all-time safety assertion is made. -/

namespace P196.Agent1.GroupIIIHandoff

open Lychrel196 DecimalDigits FoldedDecimal OverflowCarryNormalization
  CarryHistory DelayedOverlapGate
open P196.Agent1.GroupIII (sixWord)

set_option maxHeartbeats 4000000
set_option maxRecDepth 10000

def afterTwo (r : Nat) : Nat → Nat := sixWord r 4 2 1 7
def componentThree (r : Nat) : Nat → Nat := sixWord r 8 4 2 14
def componentFour (r : Nat) : Nat → Nat := sixWord r 16 8 5 9
def wholeTwo (r : Nat) : Nat → Nat := shiftOne (afterTwo r)

def wholeThree (r i : Nat) : Nat :=
  (if i=0 ∨ i=1 ∨ i=2*r+5 ∨ i=2*r+6 then 8 else 0) +
  (if i=r ∨ i=r+6 then 4
   else if i=r+1 ∨ i=r+5 then 6
   else if i=r+2 ∨ i=r+4 then 17
   else if i=r+3 then 8
   else 0)

theorem first_domain (r : Nat) (hr : 1 ≤ r) : GroupIII.Domain r 1 10 6 := by
  unfold GroupIII.Domain
  omega

theorem first_return_component (r : Nat) :
    GroupIII.returnedComponent r 1 10 6 = afterTwo r := rfl

theorem afterTwo_carry (r : Nat) (hr : 1 ≤ r) :
    ∀ i, i ≤ 2*r+6 → carry (afterTwo r) i = 0 := by
  apply carry_certificate _ (fun _ => 0) _ rfl
  intro i hi
  simp only [afterTwo, sixWord]
  repeat (first | omega | split)

theorem wholeTwo_carry (r : Nat) (hr : 1 ≤ r) :
    ∀ i, i ≤ 2*r+7 → carry (wholeTwo r) i = DelayedOverlapGate.initialCarry r i := by
  apply carry_certificate _ _ _ (by unfold DelayedOverlapGate.initialCarry; split <;> omega)
  intro i hi
  simp only [wholeTwo, shiftOne, afterTwo, sixWord, DelayedOverlapGate.initialCarry]
  repeat (first | omega | split)

theorem componentThree_carry (r : Nat) (hr : 1 ≤ r) :
    ∀ i, i ≤ 2*r+6 → carry (componentThree r) i = componentDoubleCarry r i := by
  apply carry_certificate _ _ _ (by unfold componentDoubleCarry; split <;> omega)
  intro i hi
  simp only [componentThree, sixWord, componentDoubleCarry]
  repeat (first | omega | split)

theorem wholeThree_carry (r : Nat) (hr : 2 ≤ r) :
    ∀ i, i ≤ 2*r+7 → carry (wholeThree r) i = middleCarry r i := by
  apply carry_certificate _ _ _ (by unfold middleCarry; split <;> omega)
  intro i hi
  simp only [wholeThree, middleCarry]
  repeat (first | omega | split)

end P196.Agent1.GroupIIIHandoff
