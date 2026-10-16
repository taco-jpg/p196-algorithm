import Agent1GroupIII

/-! Finite r=1 control for Group III (p,u,v)=(1,10,6), at time four.
This file makes no statement for other r or for subsequent times. -/
namespace P196.Agent1.GroupIIIHandoff

open Lychrel196 DecimalDigits FoldedDecimal OverflowCarryNormalization
  CarryHistory DelayedOverlapGate

set_option maxHeartbeats 4000000
set_option maxRecDepth 10000

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
  have h : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 ∨ i = 7 := by omega
  rcases h with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> decide

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
  have h : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 ∨ i = 7 ∨ i = 8 := by omega
  rcases h with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> decide

/-- The actual finite component and whole states do not overlap at time four. -/
theorem r1_actual_time4_overlap_fails :
    ¬ (∀ i, i < 9 →
      (iterPairs (DelayedOverlapGate.initial 1 1 10 6) 9 4).2 i =
        shiftOne
          (fun j => if j < 8 then
            (iterPairs (DelayedOverlapGate.component 1 1 10 6) 8 4).2 j
            else 0) i) := by
  intro he
  have hd := r1_time4_signed_defect 0 (by decide)
  rw [he 0 (by decide)] at hd
  simp at hd

#print axioms r1_component_time4_width
#print axioms r1_component_time4_columns
#print axioms r1_whole_time4_width
#print axioms r1_time4_signed_defect
#print axioms r1_actual_time4_overlap_fails

end P196.Agent1.GroupIIIHandoff
