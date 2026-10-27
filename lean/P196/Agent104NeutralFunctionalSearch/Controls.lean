import P196.Agent104NeutralFunctionalSearch.Main

/-!
# Small kernel-reduced controls for the actual functional search

These scopes are controls, not new mathematical lower-bound discoveries.
The positive binary control executes one explicit return and proves its
membership in the complete finite search. No decimal search negative is claimed.
-/

namespace Agent104.NeutralFunctionalSearch

open Agent104.NeutralJointWidth

/-- An accepted edge must retain a target that fails Hyp on the following step. -/
theorem accepted_invalid_target :
    successor 10 1 2 ([1], [10]) = some ([3], [0]) := by decide

theorem invalid_target_stops : successor 10 1 2 ([3], [0]) = none := by decide

theorem binary_empty_exterior_search : functionalSearch 2 0 2 = false := by decide

theorem binary_small_search : functionalSearch 2 1 2 = false := by decide

theorem binary_return_witness :
    returns 2 2 4 ([2, 1], [1, 0, 0, 1]) ([2, 1], [1, 0, 0, 1])
      (stateBound 2 2 4) = true := by decide

theorem binary_positive_search : functionalSearch 2 2 4 = true := by
  apply List.any_eq_true.mpr
  refine ⟨([2, 1], [1, 0, 0, 1]), ?_, binary_return_witness⟩
  exact (stateOK_iff_mem 2 2 4 _).mp (by decide)

theorem binary_positive_exists : JointRealizable 2 2 4 :=
  (functionalSearch_iff 2 2 4 (by decide)).mp binary_positive_search

end Agent104.NeutralFunctionalSearch

#print axioms Agent104.NeutralFunctionalSearch.accepted_invalid_target
#print axioms Agent104.NeutralFunctionalSearch.invalid_target_stops
#print axioms Agent104.NeutralFunctionalSearch.binary_empty_exterior_search
#print axioms Agent104.NeutralFunctionalSearch.binary_small_search
#print axioms Agent104.NeutralFunctionalSearch.binary_return_witness
#print axioms Agent104.NeutralFunctionalSearch.binary_positive_search
#print axioms Agent104.NeutralFunctionalSearch.binary_positive_exists
