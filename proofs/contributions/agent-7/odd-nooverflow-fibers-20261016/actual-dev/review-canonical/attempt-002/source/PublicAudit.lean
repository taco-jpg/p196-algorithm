import OddCanonical
import ReviewCanonical
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#print axioms P196.Agent9.InverseFibers.weight_eq_table
#print axioms P196.Agent9.InverseFibers.local_unique
#print axioms P196.Agent9.InverseFibers.advance_formula
#print axioms P196.Agent9.InverseFibers.advance_bounds
#print axioms P196.Agent9.InverseFibers.fib_zero
#print axioms P196.Agent9.InverseFibers.fib_one
#print axioms P196.Agent9.InverseFibers.fib_succ_succ
#print axioms P196.Agent9.InverseFibers.fib_le_succ
#print axioms P196.Agent9.InverseFibers.run_bound
#print axioms P196.Agent9.InverseFibers.two_symbol_bound
#print axioms P196.Agent9.InverseFibers.one_symbol_bound
#print axioms P196.Agent9.InverseFibers.inverseCount_bound
#print axioms P196.Agent9.InverseFibers.run_append
#print axioms P196.Agent9.InverseFibers.advance_nine
#print axioms P196.Agent9.InverseFibers.replicate_snoc
#print axioms P196.Agent9.InverseFibers.nines_exact
#print axioms P196.Agent9.InverseFibers.first_eleven_eq_nine
#print axioms P196.Agent9.InverseFibers.leading_eleven_exact
#print axioms P196.Agent9.InverseFibers.leading_eleven_labels
#print axioms P196.Agent9.InverseFibers.mem_states
#print axioms P196.Agent9.InverseFibers.mem_labels
#print axioms P196.Agent9.InverseFibers.mem_extend
#print axioms P196.Agent9.InverseFibers.length_extend
#print axioms P196.Agent9.InverseFibers.mem_preimages
#print axioms P196.Agent9.InverseFibers.dot_suffix
#print axioms P196.Agent9.InverseFibers.dot_run
#print axioms P196.Agent9.InverseFibers.preimages_length
#print axioms P196.Agent9.InverseFibers.local_next_unique
#print axioms P196.Agent9.InverseFibers.extend_nodup
#print axioms P196.Agent9.InverseFibers.preimages_nodup
#print axioms P196.Agent9.InverseFibers.exact_fiber_bound
#print axioms P196.Agent9.InverseFibers.exact_sharp_family
#print axioms P196.Agent9.InverseFibers.scan_append
#print axioms P196.Agent9.InverseFibers.scan_length
#print axioms P196.Agent9.InverseFibers.scan_carry_bound
#print axioms P196.Agent9.InverseFibers.low_bound
#print axioms P196.Agent9.InverseFibers.high_bound
#print axioms P196.Agent9.InverseFibers.path_realizes
#print axioms P196.Agent9.InverseFibers.low_mkState
#print axioms P196.Agent9.InverseFibers.high_mkState
#print axioms P196.Agent9.InverseFibers.realizes_path
#print axioms P196.Agent9.InverseFibers.mem_preimages_iff_realizes
#print axioms P196.Agent7.OddFibers.oddMirror_nil
#print axioms P196.Agent7.OddFibers.oddMirror_cons
#print axioms P196.Agent7.OddFibers.oddMirror_length
#print axioms P196.Agent7.OddFibers.oddMirror_reverse
#print axioms P196.Agent7.OddFibers.center_iff
#print axioms P196.Agent7.OddFibers.center_exists_iff
#print axioms P196.Agent7.OddFibers.center_unique
#print axioms P196.Agent7.OddFibers.centerValue_center
#print axioms P196.Agent7.OddFibers.oddPath_length
#print axioms P196.Agent7.OddFibers.oddPath_bounds
#print axioms P196.Agent7.OddFibers.mem_oddExtend
#print axioms P196.Agent7.OddFibers.length_oddExtend
#print axioms P196.Agent7.OddFibers.mem_oddPreimages
#print axioms P196.Agent7.OddFibers.oddExtend_nodup
#print axioms P196.Agent7.OddFibers.oddPreimages_nodup
#print axioms Agent8.mass_append
#print axioms Agent8.mass_reverse
#print axioms Agent8.mass_zipAdd
#print axioms Agent8.mass_pair
#print axioms Agent8.normalize_mass_mod
#print axioms Agent8.step_mass_mod
#print axioms Agent8.six_steps_mass_mod
#print axioms Agent8.orbit_add
#print axioms Agent8.six_multiple_mass_mod
#print axioms Agent8.mass_replicate
#print axioms Agent8.template_mass
#print axioms Agent8.returned_template_mass_congruence
#print axioms Agent8.finite_exterior_certificate
#print axioms Agent8.exterior_bounds
#print axioms Agent8.path_potential_bounds
#print axioms Agent8.closed_path_bounds
#print axioms Agent8.returned_period_at_least_four
#print axioms Agent8.no_two_step_return
#print axioms Agent8.six_step_forced_loss
#print axioms Agent8.no_repeatable_six_step_return
#print axioms Agent8.short_return_equal_gains
#print axioms Agent8.twelve_step_gains
#print axioms Agent8.eighteen_step_gains
#print axioms Agent8.no_repeatable_six_step_template_return
#print axioms P196.Agent9.InverseFibers.normalize_scan
#print axioms P196.Agent9.InverseFibers.zipAdd_repository
#print axioms P196.Agent9.InverseFibers.zipAdd_length
#print axioms P196.Agent9.InverseFibers.zipAdd_append
#print axioms P196.Agent9.InverseFibers.zipAdd_comm
#print axioms P196.Agent9.InverseFibers.zipAdd_reverse
#print axioms P196.Agent9.InverseFibers.pair_halves
#print axioms P196.Agent9.InverseFibers.realizes_actual
#print axioms P196.Agent9.InverseFibers.actual_realizes
#print axioms P196.Agent9.InverseFibers.mem_preimages_iff_actual
#print axioms P196.Agent9.InverseFibers.canonical_membership
#print axioms P196.Agent9.InverseFibers.canonical_nodup
#print axioms P196.Agent9.InverseFibers.canonical_bound
#print axioms P196.Agent9.InverseFibers.leading_eleven_positive
#print axioms P196.Agent9.InverseFibers.canonical_sharp
#print axioms P196.Agent7.OddFibers.oddPath_realizes
#print axioms P196.Agent7.OddFibers.oddRealizes_path
#print axioms P196.Agent7.OddFibers.oddPath_iff_realizes
#print axioms P196.Agent7.OddFibers.pair_odd_halves
#print axioms P196.Agent7.OddFibers.oddMirror_injective
#print axioms P196.Agent7.OddFibers.oddRealizes_actual
#print axioms P196.Agent7.OddFibers.oddActual_realizes
#print axioms P196.Agent7.OddFibers.oddPath_iff_actual
#print axioms P196.Agent7.OddFibers.oddPath_normalize
#print axioms P196.Agent7.OddFibers.symmetric_odd_decomposition
#print axioms P196.Agent7.OddFibers.odd_word_encoding_injective
#print axioms P196.Agent7.OddFibers.odd_word_center
#print axioms P196.Agent7.OddFibers.oddMirror_head
#print axioms P196.Agent7.OddFibers.canonicalOdd_membership
#print axioms P196.Agent7.OddFibers.canonicalOdd_nodup
#print axioms P196.Agent7.OddFibers.fullOddPreimages_nodup
#print axioms P196.Agent7.OddFibers.fullOddPreimages_membership_encoded
#print axioms P196.Agent7.OddFibers.canonicalOdd_of_encoding
#print axioms P196.Agent7.OddFibers.canonicalOdd_has_encoding
#print axioms P196.Agent7.OddFibers.fullOddPreimages_membership
#print axioms P196.Agent7.OddFibers.width_one_witness
#print axioms P196.Agent7.ReviewCanonical.width_one_complete
#print axioms P196.Agent7.ReviewCanonical.odd_head_even_center_accepted
#print axioms P196.Agent7.ReviewCanonical.even_head_odd_center_rejected
#print axioms P196.Agent7.ReviewCanonical.width_three_complete
#print axioms P196.Agent7.ReviewCanonical.empty_full_word_rejected
run_cmd do
  let env ← getEnv
  let selected : List String := ["InverseFibers", "PathCounts", "WordBridge", "OddCenter", "PeriodObstructions", "ActualWords", "OddActual", "OddWords", "OddCanonical", "ReviewCanonical"]
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        match info with
        | .axiomInfo v =>
          if !v.isUnsafe then throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          let axs ← liftCoreM (Lean.collectAxioms name)
          if axs.toList.any (fun a => !(allowed.contains a)) then throwError m!"DISALLOWED_AXIOMS {mod} {name}: {axs.toList}"
          count := count + 1
          logInfo m!"AUDIT_THEOREM {mod} {name}: {axs.toList}"
        | _ => pure ()
  logInfo m!"FULL_MODULE_AUDIT theorems={count}"
