import P196.Agent1GroupIII.Agent1GroupIII

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

theorem component_width_through_four (r : Nat) (hr : 1 ≤ r) :
    ∀ t, t ≤ 4 → (iterPairs (component r 1 10 6) (2*r+6) t).1 = 2*r+6 := by
  intro t ht
  have hc : t=0 ∨ t=1 ∨ t=2 ∨ t=3 ∨ t=4 := by omega
  rcases hc with rfl | rfl | rfl | rfl | rfl
  · rfl
  · change nextWidth (component r 1 10 6) (2*r+6) = 2*r+6
    simp only [nextWidth, GroupIII.component_no_overflow r 1 10 6 (first_domain r hr), if_true]
  · exact (GroupIII.component_two_step_return r 1 10 6 (first_domain r hr)).1
  · exact (component_time_three r hr).1
  · exact (component_time_four r hr).1

theorem whole_width_through_four (r : Nat) (hr : 2 ≤ r) :
    ∀ t, t ≤ 4 → (iterPairs (DelayedOverlapGate.initial r 1 10 6) (2*r+7) t).1 = 2*r+7 := by
  intro t ht
  have hc : t=0 ∨ t=1 ∨ t=2 ∨ t=3 ∨ t=4 := by omega
  rcases hc with rfl | rfl | rfl | rfl | rfl
  · rfl
  · change nextWidth (DelayedOverlapGate.initial r 1 10 6) (2*r+7) = 2*r+7
    simp only [nextWidth, GroupIII.initial_no_overflow r 1 10 6 (first_domain r (by omega)), if_true]
  · exact (GroupIII.whole_two_step_return r 1 10 6 (first_domain r (by omega))).1
  · exact (whole_time_three r (by omega)).1
  · exact (whole_time_four r hr).1

/-- Zero extension uses the actual component width, including any future overflow. -/
def finiteComponent (r t i : Nat) : Nat :=
  if i < (iterPairs (component r 1 10 6) (2*r+6) t).1 then
    (iterPairs (component r 1 10 6) (2*r+6) t).2 i else 0

def OverlapAt (r t : Nat) : Prop :=
  (iterPairs (DelayedOverlapGate.initial r 1 10 6) (2*r+7) t).1 =
    (iterPairs (component r 1 10 6) (2*r+6) t).1 + 1 ∧
  ∀ i, i < (iterPairs (DelayedOverlapGate.initial r 1 10 6) (2*r+7) t).1 →
    (iterPairs (DelayedOverlapGate.initial r 1 10 6) (2*r+7) t).2 i =
      shiftOne (finiteComponent r t) i

theorem finiteComponent_three (r : Nat) (hr : 1 ≤ r) :
    finiteComponent r 3 = componentThree r := by
  funext i
  have h3 := component_time_three r hr
  unfold finiteComponent
  rw [h3.1]
  split
  · exact h3.2 i (by assumption)
  · simp only [componentThree, sixWord]
    repeat (first | omega | split)

theorem finiteComponent_four (r : Nat) (hr : 1 ≤ r) :
    finiteComponent r 4 = componentFour r := by
  funext i
  have h4 := component_time_four r hr
  unfold finiteComponent
  rw [h4.1]
  split
  · exact h4.2 i (by assumption)
  · simp only [componentFour, sixWord]
    repeat (first | omega | split)

theorem time_three_departure (r : Nat) (hr : 1 ≤ r) : ¬ OverlapAt r 3 := by
  intro ho
  have h3 := whole_time_three r hr
  have he := ho.2 (r+3) (by rw [h3.1]; omega)
  rw [h3.2 (r+3) (by omega), finiteComponent_three r hr] at he
  have hw : wholeThree r (r+3) = 8 := by
    simp only [wholeThree, if_true, true_or]
    repeat (first | omega | split)
  have hc : shiftOne (componentThree r) (r+3) = 28 := by
    simp only [shiftOne, componentThree, sixWord, true_or, or_true, if_true]
    repeat (first | omega | split)
  rw [hw, hc] at he
  omega

theorem time_four_overlap (r : Nat) (hr : 2 ≤ r) : OverlapAt r 4 := by
  have hc := component_time_four r (by omega)
  have hw := whole_time_four r hr
  refine ⟨?_, ?_⟩
  · rw [hw.1, hc.1]
  · intro i hi
    rw [hw.1] at hi
    rw [hw.2 i hi, finiteComponent_four r (by omega)]

theorem wholeTwo_not_bad (r : Nat) (hr : 1 ≤ r) : ¬ BadWord (2*r+7) (wholeTwo r) := by
  have hc : wholeTwo r (r+3) = 14 := by
    simp only [wholeTwo, shiftOne, afterTwo, sixWord, true_or, or_true, if_true]
    repeat (first | omega | split)
  have ho : wholeTwo r 0 = 4 := by
    simp only [wholeTwo, shiftOne, afterTwo, sixWord, true_or, if_true]
  rintro (hlo | ⟨houter, _⟩)
  · have hb := hlo (r+3) (by omega)
    rw [hc] at hb
    omega
  · rw [ho] at houter
    omega

theorem wholeThree_not_bad (r : Nat) (hr : 1 ≤ r) : ¬ BadWord (2*r+7) (wholeThree r) := by
  have hc : wholeThree r (r+2) = 17 := by
    simp only [wholeThree, true_or, if_true]
    repeat (first | omega | split)
  have ho : wholeThree r 0 = 8 := by
    simp only [wholeThree, true_or, if_true]
    repeat (first | omega | split)
  rintro (hlo | ⟨houter, _⟩)
  · have hb := hlo (r+2) (by omega)
    rw [hc] at hb
    omega
  · rw [ho] at houter
    omega

/-! The following finite boundary proofs were supplied by the genuine Agent #1
`handoff_boundary` specialist. They use kernel reduction only. Their independent
source/log records are preserved with the author evidence. -/

/-- The actual component has width eight at time four. -/
theorem r1_component_time4_width :
    (iterPairs (DelayedOverlapGate.component 1 1 10 6) 8 4).1 = 8 := by
  decide

/-- Exact finite component word at the shortest boundary. -/
theorem r1_component_time4_columns :
    ∀ i, i < 8 →
      (iterPairs (DelayedOverlapGate.component 1 1 10 6) 8 4).2 i =
        GroupIII.sixWord 1 16 8 5 9 i := by
  intro i hi
  have h : ∀ j : Fin 8,
      (iterPairs (DelayedOverlapGate.component 1 1 10 6) 8 4).2 j =
        GroupIII.sixWord 1 16 8 5 9 j := by decide
  exact h ⟨i, hi⟩

/-- The actual whole word has width nine at time four. -/
theorem r1_whole_time4_width :
    (iterPairs (DelayedOverlapGate.initial 1 1 10 6) 9 4).1 = 9 := by
  decide

/-- Signed coefficient defect, preserving the negative entries. -/
theorem r1_time4_signed_defect :
    ∀ i, i < 9 →
      ((iterPairs (DelayedOverlapGate.initial 1 1 10 6) 9 4).2 i : Int) -
        (shiftOne
          (fun j => if j < 8 then
            (iterPairs (DelayedOverlapGate.component 1 1 10 6) 8 4).2 j
            else 0) i : Int) =
        ([1, -20, 1, 0, 0, 0, 1, -20, 1] : List Int)[i]! := by
  intro i hi
  have h : ∀ k : Fin 9,
      ((iterPairs (DelayedOverlapGate.initial 1 1 10 6) 9 4).2 k : Int) -
        (shiftOne
          (fun j => if j < 8 then
            (iterPairs (DelayedOverlapGate.component 1 1 10 6) 8 4).2 j
            else 0) k : Int) =
        ([1, -20, 1, 0, 0, 0, 1, -20, 1] : List Int)[k.val]! := by decide
  exact h ⟨i, hi⟩

/-- The actual finite component and whole states do not overlap at time four. -/
theorem r1_actual_time4_overlap_fails :
    ¬ (∀ i, i < 9 →
      (iterPairs (DelayedOverlapGate.initial 1 1 10 6) 9 4).2 i =
        shiftOne
          (fun j => if j < 8 then
            (iterPairs (DelayedOverlapGate.component 1 1 10 6) 8 4).2 j
            else 0) i) := by
  intro he
  have hne :
      (iterPairs (DelayedOverlapGate.initial 1 1 10 6) 9 4).2 0 ≠
        shiftOne
          (fun j => if j < 8 then
            (iterPairs (DelayedOverlapGate.component 1 1 10 6) 8 4).2 j
            else 0) 0 := by decide
  exact hne (he 0 (by decide))


/-- Exact spacer threshold for the second repair, with actual dynamic widths. -/
theorem time_four_overlap_iff (r : Nat) (hr : 1 ≤ r) : OverlapAt r 4 ↔ 2 ≤ r := by
  constructor
  · intro ho
    by_cases hn : 2 ≤ r
    · exact hn
    · have h1 : r=1 := by omega
      subst r
      have hf : False := by
        apply r1_actual_time4_overlap_fails
        intro i hi
        have he := ho.2 i (by simpa only [r1_whole_time4_width] using hi)
        simpa only [finiteComponent, r1_component_time4_width] using he
      exact hf.elim
  · exact time_four_overlap r

theorem time_one_departure (r : Nat) (hr : 1 ≤ r) : ¬ OverlapAt r 1 := by
  intro ho
  have hd := first_domain r hr
  have hw : (iterPairs (DelayedOverlapGate.initial r 1 10 6) (2*r+7) 1).1 = 2*r+7 := by
    change nextWidth (DelayedOverlapGate.initial r 1 10 6) (2*r+7) = 2*r+7
    simp only [nextWidth, GroupIII.initial_no_overflow r 1 10 6 hd, if_true]
  have hf : finiteComponent r 1 =
      (fun j => if j < 2*r+6 then nextColumns (component r 1 10 6) (2*r+6) j else 0) := by
    funext j
    unfold finiteComponent
    change (if j < nextWidth (component r 1 10 6) (2*r+6) then
      nextColumns (component r 1 10 6) (2*r+6) j else 0) = _
    simp only [nextWidth, GroupIII.component_no_overflow r 1 10 6 hd, if_true]
  apply GroupIII.actual_intermediate_overlap_fails r 1 10 6 hd
  intro i hi
  have he := ho.2 i (by rw [hw]; exact hi)
  rw [hf] at he
  exact he

theorem time_two_overlap (r : Nat) (hr : 1 ≤ r) : OverlapAt r 2 := by
  have hc := GroupIII.component_two_step_return r 1 10 6 (first_domain r hr)
  have hw := GroupIII.whole_two_step_return r 1 10 6 (first_domain r hr)
  rw [first_return_component] at hc hw
  have hf : finiteComponent r 2 = afterTwo r := by
    funext i
    unfold finiteComponent
    rw [hc.1]
    split
    · exact hc.2 i (by assumption)
    · simp only [afterTwo, sixWord]
      repeat (first | omega | split)
  refine ⟨?_, ?_⟩
  · rw [hw.1, hc.1]
  · intro i hi
    rw [hw.1] at hi
    rw [hw.2 i hi, hf]

/-- Both repairs are genuine departures followed by restoration. -/
theorem two_genuine_repairs (r : Nat) (hr : 2 ≤ r) :
    ¬ OverlapAt r 1 ∧ OverlapAt r 2 ∧ ¬ OverlapAt r 3 ∧ OverlapAt r 4 :=
  ⟨time_one_departure r (by omega), time_two_overlap r (by omega),
    time_three_departure r (by omega), time_four_overlap r hr⟩

end P196.Agent1.GroupIIIHandoff
