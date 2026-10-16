import OddComplete
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#check P196.Agent7.OddFibers.oddMirror_nil
#check P196.Agent7.OddFibers.oddMirror_cons
#check P196.Agent7.OddFibers.oddMirror_length
#check P196.Agent7.OddFibers.oddMirror_reverse
#check P196.Agent7.OddFibers.center_iff
#check P196.Agent7.OddFibers.center_exists_iff
#check P196.Agent7.OddFibers.center_unique
#check P196.Agent7.OddFibers.centerValue_center
#check P196.Agent7.OddFibers.oddPath_length
#check P196.Agent7.OddFibers.oddPath_bounds
#check P196.Agent7.OddFibers.mem_oddExtend
#check P196.Agent7.OddFibers.length_oddExtend
#check P196.Agent7.OddFibers.mem_oddPreimages
#check P196.Agent7.OddFibers.oddExtend_nodup
#check P196.Agent7.OddFibers.oddPreimages_nodup
#check P196.Agent7.OddFibers.oddPath_realizes
#check P196.Agent7.OddFibers.oddRealizes_path
#check P196.Agent7.OddFibers.oddPath_iff_realizes
#check P196.Agent7.OddFibers.pair_odd_halves
#check P196.Agent7.OddFibers.oddMirror_injective
#check P196.Agent7.OddFibers.oddRealizes_actual
#check P196.Agent7.OddFibers.oddActual_realizes
#check P196.Agent7.OddFibers.oddPath_iff_actual
#check P196.Agent7.OddFibers.oddPath_normalize
#check P196.Agent7.OddFibers.symmetric_odd_decomposition
#check P196.Agent7.OddFibers.odd_word_encoding_injective
#check P196.Agent7.OddFibers.odd_word_center
#check P196.Agent7.OddFibers.oddMirror_head
#check P196.Agent7.OddFibers.canonicalOdd_membership
#check P196.Agent7.OddFibers.canonicalOdd_nodup
#check P196.Agent7.OddFibers.fullOddPreimages_nodup
#check P196.Agent7.OddFibers.fullOddPreimages_membership_encoded
#check P196.Agent7.OddFibers.canonicalOdd_of_encoding
#check P196.Agent7.OddFibers.canonicalOdd_has_encoding
#check P196.Agent7.OddFibers.fullOddPreimages_membership
#check P196.Agent7.OddFibers.width_one_witness
#check P196.Agent7.OddFibers.advance_eq_class
#check P196.Agent7.OddFibers.nineRun_succ
#check P196.Agent7.OddFibers.advance_nine_counts
#check P196.Agent7.OddFibers.nine_growth_good
#check P196.Agent7.OddFibers.nineRun_growth_good
#check P196.Agent7.OddFibers.advance_le_nine
#check P196.Agent7.OddFibers.four_class_bound
#check P196.Agent7.OddFibers.four_symbol_bound
#check P196.Agent7.OddFibers.run_le_nines
#check P196.Agent7.OddFibers.long_run_dominated
#check P196.Agent7.OddFibers.nine_near_balanced
#check P196.Agent7.OddFibers.nineRun_near_balanced
#check P196.Agent7.OddFibers.nineRun_total
#check P196.Agent7.OddFibers.nineRun_adjacent_exact
#check P196.Agent7.OddFibers.adjacent_monotone
#check P196.Agent7.OddFibers.one_class_adjacent_bound
#check P196.Agent7.OddFibers.two_class_adjacent_bound
#check P196.Agent7.OddFibers.three_class_adjacent_bound
#check P196.Agent7.OddFibers.adjacent_run_bound
#check P196.Agent7.OddFibers.odd_count_bound
#check P196.Agent7.OddFibers.nines_odd_count_sharp
#check P196.Agent7.OddFibers.odd_dot_suffix
#check P196.Agent7.OddFibers.odd_dot_run
#check P196.Agent7.OddFibers.odd_preimages_length
#check P196.Agent7.OddFibers.odd_preimages_bound
#check P196.Agent7.OddFibers.leading_eleven_odd_count
#check P196.Agent7.OddFibers.leading_eleven_odd_sharp
#check P196.Agent7.OddFibers.leading_eleven_odd_positive
#check P196.Agent7.OddFibers.odd_count_center_parity
#check P196.Agent7.OddFibers.odd_preimages_center_parity
#check P196.Agent7.OddFibers.oddEndpoint_monotone
#check P196.Agent7.OddFibers.one_class_endpoint_bound
#check P196.Agent7.OddFibers.two_class_endpoint_bound
#check P196.Agent7.OddFibers.three_class_endpoint_bound
#check P196.Agent7.OddFibers.odd_count_fixed_center_bound
#check P196.Agent7.OddFibers.odd_preimages_fixed_center_bound
#check P196.Agent7.OddFibers.leading_eleven_fixed_center_maximum
#check P196.Agent7.OddFibers.countPhase_advance
#check P196.Agent7.OddFibers.nineRun_countPhase
#check P196.Agent7.OddFibers.nineRun_even_endpoint
#check P196.Agent7.OddFibers.nineRun_odd_endpoint
#check P196.Agent7.OddFibers.nines_fixed_center_formula
#check P196.Agent7.OddFibers.odd_preimages_exact_center_bound
#check P196.Agent7.OddFibers.leading_eleven_exact_center
#check P196.Agent7.OddFibers.sharpCenter_six_or_seven
#check P196.Agent7.OddFibers.sharpCenter_large
#check P196.Agent7.OddFibers.oddCenterMax_sharp
#check P196.Agent7.OddFibers.explicit_leading_eleven_sharp
#check P196.Agent7.OddFibers.explicit_empty_sharp
#check P196.Agent7.OddFibers.fullOddPreimages_length_le
#check P196.Agent7.OddFibers.fullOddPreimages_bound
#check P196.Agent7.OddFibers.canonical_leading_eleven
#check P196.Agent7.OddFibers.full_leading_eleven_length
#check P196.Agent7.OddFibers.fullOddPreimages_center_bound
#check P196.Agent7.OddFibers.full_fixed_center_maximum
#check P196.Agent7.OddFibers.sharpTargetHalf_length
#check P196.Agent7.OddFibers.sharpFamily_zero
#check P196.Agent7.OddFibers.sharpFamily_length
#check P196.Agent7.OddFibers.sharpFamily_exact
#check P196.Agent7.OddFibers.complete_canonical_odd_fiber_maximum
#check P196.Agent7.OddFibers.scan_digits_lt_ten
#check P196.Agent7.OddFibers.odd_list_halves
#check P196.Agent7.OddFibers.zipAdd_digits_lt_nineteen
#check P196.Agent7.OddFibers.exists_symbol_list
#check P196.Agent7.OddFibers.odd_nooverflow_output_range
#check P196.Agent7.OddFibers.odd_output_range
#check P196.Agent7.OddFibers.decodeSymbol_val
#check P196.Agent7.OddFibers.targetHalf_encoded
#check P196.Agent7.OddFibers.targetCenter_encoded
#check P196.Agent7.OddFibers.universalOddPreimages_encoded
#check P196.Agent7.OddFibers.universalOddPreimages_nodup
#check P196.Agent7.OddFibers.universalOddPreimages_membership
#check P196.Agent7.OddFibers.universalOddPreimages_bound
#check P196.Agent7.OddFibers.universal_sharp_family
#check P196.Agent7.OddFibers.universal_odd_fiber_maximum
#check P196.Agent7.OddFibers.complete_odd_fiber_theorem
#check P196.Agent7.OddFibers.universal_width_one_zero
#check P196.Agent7.OddFibers.universal_width_one_six
#check P196.Agent7.OddFibers.universal_wrong_parity
run_cmd do
  let env ← getEnv
  let selected : List String := ["InverseFibers", "PathCounts", "WordBridge", "OddCenter", "PeriodObstructions", "ActualWords", "OddActual", "OddWords", "OddCanonical", "OddCounts", "OddCountsFixedCenter", "OddCountsPhase", "OddSharp", "OddOutputRange", "OddComplete"]
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        match info with
        | .axiomInfo v =>
          if v.isUnsafe then logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {mod} {name}"
          else throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          count := count + 1
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then throwError m!"DISALLOWED_AXIOMS {mod} {name} : {axl}"
          logInfo m!"AUDIT_THEOREM {mod} {name} : {axl}"
        | _ => pure ()
  logInfo m!"FULL_MODULE_AUDIT theorems={count} union={union}"
