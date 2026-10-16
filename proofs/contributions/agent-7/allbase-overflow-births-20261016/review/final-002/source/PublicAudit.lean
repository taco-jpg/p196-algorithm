import CanonicalOverflowBirths
import BoundaryContracts
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
set_option pp.width 100000
#print axioms BaseBirths.localPair_eq_zero_iff
#print axioms BaseBirths.localPair_eq_max_iff
#print axioms BaseBirths.new_zero_iff
#print axioms BaseBirths.new_max_iff
#print axioms BaseBirths.mixed_carries_not_extreme
#print axioms BaseBirths.births_have_interior_sources
#print axioms BaseBirths.binary_extremes_swap
#print axioms SignedDigitUniqueness.head_tail_zero
#print axioms SignedDigitUniqueness.all_zero_of_eval_zero_open
#print axioms SignedDigitUniqueness.all_zero_of_eval_zero
#print axioms SignedDigitUniqueness.eval_zero_of_all_zero
#print axioms SignedDigitUniqueness.eval_zero_iff_all_zero
#print axioms SignedDigitUniqueness.all_zero_of_reverse_eval_zero
#print axioms SignedDigitUniqueness.eval_ne_zero_of_nonzero_member
#print axioms SignedDigitUniqueness.carry_residual_bounds
#print axioms SignedDigitUniqueness.base_two_failure
#print axioms BaseReflection.raw_length
#print axioms BaseReflection.raw_eval
#print axioms BaseReflection.raw_high
#print axioms BaseReflection.eval_append
#print axioms BaseReflection.high_eq_reverse_eval
#print axioms BaseReflection.residual_high
#print axioms BaseReflection.overflow_residual_eval_zero
#print axioms BaseReflection.overflow_coefficient_rigidity
#print axioms BaseReflection.residual_bounds_of_columns
#print axioms BaseReflection.overflow_classification
#print axioms BaseReflection.high_append_zero
#print axioms BaseReflection.nooverflow_carries_zero
#print axioms BaseReflection.nooverflow_classification
#print axioms BaseReflection.raw_of_zero_carries
#print axioms BaseReflection.nooverflow_raw_equals_input
#print axioms ResetNormalization.carry_bit
#print axioms ResetNormalization.columns_qs
#print axioms ResetNormalization.columns_conditions
#print axioms ResetNormalization.placed_eq_raw
#print axioms ResetNormalization.placed_eval
#print axioms ResetNormalization.placed_overflow_classification
#print axioms ResetNormalization.placed_nooverflow_classification
#print axioms ResetNormalization.low_columns_zero
#print axioms ResetNormalization.low_placed
#print axioms ResetNormalization.high_carry
#print axioms ResetNormalization.high_columns_ignore_resets
#print axioms ResetNormalization.high_placed_equals_ordinary
#print axioms ResetNormalization.low_placed_equals_ordinary
#print axioms ResetNormalization.coefficient_mem_columns
#print axioms ResetNormalization.overflow_symmetry_forces_ordinary
#print axioms ResetNormalization.nooverflow_symmetry_forces_ordinary
#print axioms P196.Agent7.AllBaseOverflow.residue_zero_iff
#print axioms P196.Agent7.AllBaseOverflow.residue_max_iff
#print axioms P196.Agent7.AllBaseOverflow.adjacent_residues_zero_iff
#print axioms P196.Agent7.AllBaseOverflow.adjacent_residues_max_iff
#print axioms P196.Agent7.AllBaseOverflow.adjacentPair_zero_iff
#print axioms P196.Agent7.AllBaseOverflow.adjacentPair_max_iff
#print axioms P196.Agent7.AllBaseOverflow.adjacent_new_extreme_neutral
#print axioms P196.Agent7.AllBaseOverflow.adjacent_without_neutral
#print axioms PhysicalWidth.placed_body_terminal
#print axioms PhysicalWidth.body_length
#print axioms PhysicalWidth.terminal_bit
#print axioms PhysicalWidth.terminal_le_ordinary
#print axioms PhysicalWidth.ordinary_bound
#print axioms PhysicalWidth.ordinary_qs
#print axioms PhysicalWidth.ordinary_overflow_symmetry_forces_placed
#print axioms PhysicalWidth.ordinary_nooverflow_symmetry_forces_placed
#print axioms PhysicalWidth.overflow_symmetry_iff
#print axioms PhysicalWidth.nooverflow_terminal_zero
#print axioms PhysicalWidth.nooverflow_symmetry_iff
#print axioms PhysicalWidth.ordinaryTags_idempotent
#print axioms PhysicalWidth.actual_width_symmetry_iff
#print axioms PhysicalWidth.ordinary_body_digits
#print axioms PhysicalWidth.ordinary_body_positive_last
#print axioms PhysicalWidth.actual_digits_length
#print axioms PhysicalWidth.actual_digits_bounded
#print axioms PhysicalWidth.actual_digits_positive_last
#print axioms PhysicalWidth.canonical_normalization
#print axioms PhysicalWidth.actual_width_symmetry_forces_equality
#print axioms PhysicalWidth.canonical_raw_symmetry
#print axioms SeamSafety.raw_carry_injective
#print axioms SeamSafety.palindrome_forces_placed
#print axioms SeamSafety.palindrome_forces_carry_agreement
#print axioms SeamSafety.carry_list_defect_nonpalindromic
#print axioms SeamSafety.outgoing_defect_nonpalindromic
#print axioms SeamSafety.canonical_outgoing_defect_safety
#print axioms ReverseAdd.pairs_length
#print axioms ReverseAdd.pairs_symmetric
#print axioms ReverseAdd.eval_zip_add
#print axioms ReverseAdd.pairs_value
#print axioms ReverseAdd.zip_add_bounds
#print axioms ReverseAdd.pairs_bounds
#print axioms ReverseAdd.pairs_positive_last
#print axioms ReverseAdd.positive_terminal_append
#print axioms ReverseAdd.positive_terminal_of_projection
#print axioms ReverseAdd.tagged_pairs_bound
#print axioms ReverseAdd.reverse_add_normalization
#print axioms ReverseAdd.reverse_add_defect_safety
#print axioms ReverseAdd.eval_nonnegative
#print axioms ReverseAdd.canonical_input_positive
#print axioms ReverseAdd.base_three_palindromic_input_control
#print axioms ActualBaseBirths.ordinary_body_at
#print axioms ActualBaseBirths.actual_nooverflow_body
#print axioms ActualBaseBirths.actual_nooverflow_length
#print axioms ActualBaseBirths.actual_nooverflow_at
#print axioms ActualBaseBirths.incoming_bit
#print axioms ActualBaseBirths.pairs_at
#print axioms ActualBaseBirths.symmetric_coefficient_at
#print axioms ActualBaseBirths.actual_nooverflow_pair_at
#print axioms ActualBaseBirths.actual_zero_iff
#print axioms ActualBaseBirths.actual_max_iff
#print axioms ActualBaseBirths.canonical_reverse_add_extremes
#print axioms P196.Agent7.AllBaseOverflow.ordinary_terminal_take_succ
#print axioms P196.Agent7.AllBaseOverflow.incoming_succ
#print axioms P196.Agent7.AllBaseOverflow.incoming_predecessor
#print axioms P196.Agent7.AllBaseOverflow.incoming_mirror_predecessor
#print axioms P196.Agent7.AllBaseOverflow.actual_overflow_body
#print axioms P196.Agent7.AllBaseOverflow.actual_overflow_length
#print axioms P196.Agent7.AllBaseOverflow.overflow_length_pos
#print axioms P196.Agent7.AllBaseOverflow.actual_overflow_at
#print axioms P196.Agent7.AllBaseOverflow.actual_overflow_last
#print axioms P196.Agent7.AllBaseOverflow.actual_overflow_pair_at
#print axioms P196.Agent7.AllBaseOverflow.actual_overflow_pair_getD
#print axioms P196.Agent7.AllBaseOverflow.actual_overflow_endpoints
#print axioms P196.Agent7.AllBaseOverflow.actual_overflow_zero_iff
#print axioms P196.Agent7.AllBaseOverflow.actual_overflow_max_iff
#print axioms P196.Agent7.AllBaseOverflow.actual_overflow_new_extreme_neutral
#print axioms P196.Agent7.AllBaseOverflow.actual_overflow_without_neutral
#print axioms P196.Agent7.AllBaseOverflow.endpoint_residue_positive
#print axioms P196.Agent7.AllBaseOverflow.endpoint_residue_below_max
#print axioms P196.Agent7.AllBaseOverflow.endpoint_residue_max_iff
#print axioms P196.Agent7.AllBaseOverflow.overflow_head_coefficient_bound
#print axioms P196.Agent7.AllBaseOverflow.actual_overflow_endpoints_pos
#print axioms P196.Agent7.AllBaseOverflow.actual_overflow_endpoints_nonzero
#print axioms P196.Agent7.AllBaseOverflow.actual_overflow_endpoints_max_iff
#print axioms P196.Agent7.AllBaseOverflow.actual_overflow_endpoints_nonextreme
#print axioms P196.Agent7.AllBaseOverflow.canonical_reverse_add_overflow_theorem
#print axioms P196.Agent7.AllBaseOverflow.Review.canonical_binary_contract
#print axioms P196.Agent7.AllBaseOverflow.Review.canonical_binary_width_one_contract
#print axioms P196.Agent7.AllBaseOverflow.Review.actual_binary_maximum_contract
#print axioms P196.Agent7.AllBaseOverflow.Review.old_width_mirror_negative_control
#print axioms P196.Agent7.AllBaseOverflow.Review.reset_tag_erasure_control
#print axioms P196.Agent7.AllBaseOverflow.Review.endpoint_bound_is_needed_control
#print axioms P196.Agent7.AllBaseOverflow.Review.signed_unbounded_endpoint_contract
#print axioms P196.Agent7.AllBaseOverflow.Review.neutrality_is_not_sufficient_control
#print axioms P196.Agent7.AllBaseOverflow.Review.out_of_range_default_control
run_cmd do
  let env ← getEnv
  let selected : List String := ["BaseBirths", "SignedDigitUniqueness", "BaseReflection", "ResetNormalization", "AdjacentBirths", "PhysicalWidth", "SeamSafety", "ReverseAdd", "ActualBaseBirths", "OverflowDigits", "ActualOverflowBirths", "OverflowEndpoints", "CanonicalOverflowBirths", "BoundaryContracts"]
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        match info with
        | .axiomInfo v =>
          if v.isUnsafe then logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {mod} {name}"
          else throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          let axs ← liftCoreM (Lean.collectAxioms name)
          if axs.toList.any (fun a => !(allowed.contains a)) then throwError m!"DISALLOWED_AXIOMS {mod} {name}: {axs.toList}"
          count := count + 1
          logInfo m!"AUDIT_THEOREM {mod} {name}: {axs.toList}"
        | _ => pure ()
  logInfo m!"FULL_MODULE_AUDIT theorems={count}"
