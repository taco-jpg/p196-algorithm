import P196.ResidualFivePredecessorMass.OuterMass

set_option autoImplicit false

/-!
# Exact ordinary-predecessor multiplicity over the residual-five fiber

The list `predecessors r` contains exactly the positive ordinary integers
whose next value lies in the existing residual-five fiber, with no repeated
integer and no source-width restriction. Its cardinalities start
7, 0, 175, 1750, 21875, ... and satisfy A(r+2) = 10*A(r+1) + 25*A(r).

The count is transported from the existing integer predecessor enumerator
through the original canonical digit-splitting multiplicities. It makes no
claim about the orbit of 196, arbitrary inverse depth, or infinite orbits.
-/

namespace P196.ResidualFivePredecessorMass

/-- The complete empty-middle list, in the original digit-split order. -/
theorem predecessors_zero :
    predecessors 0 = [1600, 1510, 1420, 1330, 1240, 1150, 1060] := by
  rw [predecessors, P196.ResidualFivePredecessorCount.survivorWords_eq,
    P196.ResidualFivePredecessorCount.rawAcceptedWords_zero]
  decide

/-- The empty-middle fiber contributes seven distinct positive sources. -/
theorem predecessors_zero_length : (predecessors 0).length = 7 := by
  rw [predecessors_zero]
  rfl

/-- The one-pair middle fiber contributes no positive ordinary source. -/
theorem predecessors_one : predecessors 1 = [] := by
  apply List.length_eq_zero_iff.mp
  rw [predecessors_length_eq_middle, middleWeight_one]

/-- Exact all-parameter recurrence for the number of distinct ordinary
predecessors whose next value belongs to the existing residual-five fiber. -/
theorem predecessors_length_recurrence (r : Nat) :
    (predecessors (r + 2)).length =
      10 * (predecessors (r + 1)).length + 25 * (predecessors r).length := by
  simp only [predecessors_length_eq_middle, middleWeight_recurrence]
  omega

/-- A small derived indexing control, without enumerating a large fiber. -/
theorem predecessors_two_length : (predecessors 2).length = 175 := by
  have h := predecessors_length_recurrence 0
  simpa [predecessors_zero_length, predecessors_one] using h

end P196.ResidualFivePredecessorMass

#print axioms P196.ResidualFivePredecessorMass.mem_predecessors
#print axioms P196.ResidualFivePredecessorMass.predecessors_nodup
#print axioms P196.ResidualFivePredecessorMass.predecessors_zero
#print axioms P196.ResidualFivePredecessorMass.predecessors_zero_length
#print axioms P196.ResidualFivePredecessorMass.predecessors_one
#print axioms P196.ResidualFivePredecessorMass.predecessors_length_recurrence
#print axioms P196.ResidualFivePredecessorMass.predecessors_two_length
