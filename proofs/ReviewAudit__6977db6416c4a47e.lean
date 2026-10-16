import Counting
#print axioms Agent13SafeFamily.familyDigit_bounded
#print axioms Agent13SafeFamily.familyDigit_leading
#print axioms Agent13SafeFamily.family_canonical
#print axioms Agent13SafeFamily.family_columns
#print axioms Agent13SafeFamily.family_not_palindrome
#print axioms Agent13SafeFamily.value_nines
#print axioms Agent13SafeFamily.value_single
#print axioms Agent13SafeFamily.familyColumn_value
#print axioms Agent13SafeFamily.family_step
#print axioms Agent13SafeFamily.familyColumn_carry
#print axioms Agent13SafeFamily.family_column_overflow
#print axioms Agent13SafeFamily.family_injective
#print axioms Agent13SafeFamily.targetDigit_leading
#print axioms Agent13SafeFamily.targetDigit_units
#print axioms Agent13SafeFamily.target_canonical
#print axioms Agent13SafeFamily.target_not_palindrome
#print axioms Agent13SafeFamily.target_outer_column
#print axioms Agent13SafeFamily.target_step_not_palindrome
#print axioms Agent13SafeFamily.target_gt_pow
#print axioms Agent13SafeFamily.target_safe
#print axioms Agent13SafeFamily.value_lt_pow
#print axioms Agent13SafeFamily.family_bounds
#print axioms Agent13SafeFamily.family_safe
#print axioms Agent13SafeFamily.family_safe_predecessor
#print axioms Agent13SafeFamily.natDigit_bounded
#print axioms Agent13SafeFamily.natDigit_eq_div
#print axioms Agent13SafeFamily.natDigit_value
#print axioms Agent13SafeFamily.indexed_high_bounds
#print axioms Agent13SafeFamily.indexed_high_leading
#print axioms Agent13SafeFamily.predecessor_spec
#print axioms Agent13SafeFamily.predecessor_injective
#print axioms Agent13SafeFamily.family_congr
#print axioms Agent13SafeFamily.predecessor_complete
#print axioms Agent13SafeFamily.safe_predecessor_family
#print axioms Agent13SafeFamily.index_capacity
#print axioms Agent13SafeFamily.safe_fibers_unbounded
set_option pp.fullNames true in
#check @Agent13SafeFamily.safe_predecessor_family
set_option pp.fullNames true in
#check @Agent13SafeFamily.safe_fibers_unbounded
set_option pp.fullNames true in
#check @Agent13SafeFamily.predecessor_complete
#print Agent13SafeFamily.Safe

#eval (List.range 9).map fun j => if h : j < 9*10^0 then Agent13SafeFamily.predecessor 0 ⟨j, h⟩ else 0
#eval (List.range 5).map fun j => if h : j*177 < 9*10^2 then Agent13SafeFamily.predecessor 2 ⟨j*177, h⟩ else 0
