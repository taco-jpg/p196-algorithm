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

theorem afterTwo_no_overflow (r : Nat) (hr : 1 ≤ r) :
    carry (afterTwo r) (2*r+6) = 0 := afterTwo_carry r hr _ (Nat.le_refl _)

theorem wholeTwo_no_overflow (r : Nat) (hr : 1 ≤ r) :
    carry (wholeTwo r) (2*r+7) = 0 := by
  rw [wholeTwo_carry r hr _ (Nat.le_refl _)]
  unfold DelayedOverlapGate.initialCarry
  split <;> omega

theorem componentThree_no_overflow (r : Nat) (hr : 1 ≤ r) :
    carry (componentThree r) (2*r+6) = 0 := by
  rw [componentThree_carry r hr _ (Nat.le_refl _)]
  unfold componentDoubleCarry
  split <;> omega

theorem wholeThree_no_overflow (r : Nat) (hr : 2 ≤ r) :
    carry (wholeThree r) (2*r+7) = 0 := by
  rw [wholeThree_carry r hr _ (Nat.le_refl _)]
  unfold middleCarry
  split <;> omega

theorem afterTwo_next (r : Nat) (hr : 1 ≤ r) :
    ∀ i, i < 2*r+6 → nextColumns (afterTwo r) (2*r+6) i = componentThree r i := by
  intro i hi
  simp only [nextColumns, afterTwo_no_overflow r hr, if_true, columnSum, reflected, output]
  rw [afterTwo_carry r hr i (by omega), afterTwo_carry r hr (2*r+6-1-i) (by omega)]
  simp only [afterTwo, componentThree, sixWord]
  repeat (first | omega | split)

theorem wholeTwo_next (r : Nat) (hr : 1 ≤ r) :
    ∀ i, i < 2*r+7 → nextColumns (wholeTwo r) (2*r+7) i = wholeThree r i := by
  intro i hi
  simp only [nextColumns, wholeTwo_no_overflow r hr, if_true, columnSum, reflected, output]
  rw [wholeTwo_carry r hr i (by omega), wholeTwo_carry r hr (2*r+7-1-i) (by omega)]
  simp only [wholeTwo, shiftOne, afterTwo, sixWord, DelayedOverlapGate.initialCarry, wholeThree]
  repeat (first | omega | split)

theorem componentThree_next (r : Nat) (hr : 1 ≤ r) :
    ∀ i, i < 2*r+6 → nextColumns (componentThree r) (2*r+6) i = componentFour r i := by
  intro i hi
  simp only [nextColumns, componentThree_no_overflow r hr, if_true, columnSum, reflected, output]
  rw [componentThree_carry r hr i (by omega), componentThree_carry r hr (2*r+6-1-i) (by omega)]
  simp only [componentThree, componentFour, sixWord, componentDoubleCarry]
  repeat (first | omega | split)

theorem wholeThree_next (r : Nat) (hr : 2 ≤ r) :
    ∀ i, i < 2*r+7 → nextColumns (wholeThree r) (2*r+7) i = shiftOne (componentFour r) i := by
  intro i hi
  simp only [nextColumns, wholeThree_no_overflow r hr, if_true, columnSum, reflected, output]
  rw [wholeThree_carry r hr i (by omega), wholeThree_carry r hr (2*r+7-1-i) (by omega)]
  simp only [wholeThree, middleCarry, shiftOne, componentFour, sixWord]
  repeat (first | omega | split)

/-- Continue a represented prefix without making assumptions about its unused tail. -/
theorem continue_no_overflow (q s t : Nat → Nat) (L k : Nat) (hL : 0 < L)
    (hw : (iterPairs q L k).1 = L)
    (he : ∀ i, i < L → (iterPairs q L k).2 i = s i)
    (hs : carry s L = 0) (hst : ∀ i, i < L → nextColumns s L i = t i) :
    (iterPairs q L (k+1)).1 = L ∧ ∀ i, i < L → (iterPairs q L (k+1)).2 i = t i := by
  have hn := no_overflow_next_congr (iterPairs q L k).2 s L hL hs he
  change nextWidth (iterPairs q L k).2 (iterPairs q L k).1 = L ∧
    ∀ i, i < L → nextColumns (iterPairs q L k).2 (iterPairs q L k).1 i = t i
  rw [hw]
  exact ⟨hn.1, fun i hi => (hn.2 i hi).trans (hst i hi)⟩

theorem component_time_three (r : Nat) (hr : 1 ≤ r) :
    (iterPairs (component r 1 10 6) (2*r+6) 3).1 = 2*r+6 ∧
    ∀ i, i < 2*r+6 → (iterPairs (component r 1 10 6) (2*r+6) 3).2 i = componentThree r i := by
  have h2 := GroupIII.component_two_step_return r 1 10 6 (first_domain r hr)
  rw [first_return_component] at h2
  exact continue_no_overflow _ _ _ _ 2 (by omega) h2.1 h2.2
    (afterTwo_no_overflow r hr) (afterTwo_next r hr)

theorem whole_time_three (r : Nat) (hr : 1 ≤ r) :
    (iterPairs (DelayedOverlapGate.initial r 1 10 6) (2*r+7) 3).1 = 2*r+7 ∧
    ∀ i, i < 2*r+7 → (iterPairs (DelayedOverlapGate.initial r 1 10 6) (2*r+7) 3).2 i = wholeThree r i := by
  have h2 := GroupIII.whole_two_step_return r 1 10 6 (first_domain r hr)
  rw [first_return_component] at h2
  exact continue_no_overflow _ _ _ _ 2 (by omega) h2.1 h2.2
    (wholeTwo_no_overflow r hr) (wholeTwo_next r hr)

theorem component_time_four (r : Nat) (hr : 1 ≤ r) :
    (iterPairs (component r 1 10 6) (2*r+6) 4).1 = 2*r+6 ∧
    ∀ i, i < 2*r+6 → (iterPairs (component r 1 10 6) (2*r+6) 4).2 i = componentFour r i := by
  have h3 := component_time_three r hr
  exact continue_no_overflow _ _ _ _ 3 (by omega) h3.1 h3.2
    (componentThree_no_overflow r hr) (componentThree_next r hr)

theorem whole_time_four (r : Nat) (hr : 2 ≤ r) :
    (iterPairs (DelayedOverlapGate.initial r 1 10 6) (2*r+7) 4).1 = 2*r+7 ∧
    ∀ i, i < 2*r+7 → (iterPairs (DelayedOverlapGate.initial r 1 10 6) (2*r+7) 4).2 i =
      shiftOne (componentFour r) i := by
  have h3 := whole_time_three r (by omega)
  exact continue_no_overflow _ _ _ _ 3 (by omega) h3.1 h3.2
    (wholeThree_no_overflow r hr) (wholeThree_next r hr)

end P196.Agent1.GroupIIIHandoff
