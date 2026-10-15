import AncestryExtinction
#print axioms RunAncestry.carry_le_one
#print axioms RunAncestry.carry_after_constant
#print axioms RunAncestry.next_no_overflow
#print axioms RunAncestry.next_overflow_pos
#print axioms RunAncestry.next_overflow_zero
#print axioms RunAncestry.next_overflow_top
#print axioms RunAncestry.carry_pred
#print axioms RunAncestry.carry_top
#print axioms RunAncestry.run_facts
#print axioms RunAncestry.reset_zero
#print axioms RunAncestry.reset_eighteen
#print axioms RunAncestry.pair_eq_iff
#print axioms RunAncestry.neighbor_no_overflow
#print axioms RunAncestry.neighbor_overflow
#print axioms RunAncestry.run_value
#print axioms RunAncestry.descendant_step
#print axioms RunAncestry.descendant_sub
#print axioms RunAncestry.nextWidth_eq
#print axioms RunAncestry.track_empty_succ
#print axioms RunAncestry.track_empty_mono
#print axioms RunAncestry.track_invariant
#print axioms RunAncestry.potential_telescope
#print axioms RunAncestry.survival_bound
#print axioms RunAncestry.extinct_after
#print axioms RunAncestry.extinct_uniform
#print axioms RunAncestry.orbit_ancestry_extinct
set_option pp.fullNames true in
#check @RunAncestry.orbit_ancestry_extinct
set_option pp.fullNames true in
#check @RunAncestry.extinct_after
#print RunAncestry.MaximalRun
