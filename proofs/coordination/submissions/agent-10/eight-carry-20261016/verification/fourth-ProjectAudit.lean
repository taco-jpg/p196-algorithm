import Agent10ThreeColumnCarry
import Agent10SixCarryCounterexample
import Agent10SevenCarryCounterexample
import Agent10NineCarrySharp
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#check Agent10SmoothingBoundary.prefix_rigidity
#check Agent10SmoothingBoundary.four_rigidity_at_five
#check Agent10SmoothingBoundary.witness_zero_after
#check Agent10SmoothingBoundary.witness_symmetric
#check Agent10SmoothingBoundary.witness_bounds
#check Agent10SmoothingBoundary.four_witness_zero_after
#check Agent10SmoothingBoundary.four_witness_bounds
#check Agent10SmoothingBoundary.six_is_not_rigid
#check Agent10SmoothingBoundary.sharp_threshold
#check Agent10SmoothingBridge.four_eq_smoothPow
#check Agent10SmoothingBridge.smooth_four_rigidity_at_five
#check Agent10SmoothingBridge.smooth_four_symmetric_counterexample
#check Agent10SmoothingBridge.eight_carries_small_difference
#check Agent10SmoothingBridge.initial_nonoverflow_difference_bound
#check Agent10SmoothingBridge.eight_carries_initial_nonoverflow
#check Agent10SevenStepCount.rank_seven_minimum_fin
#check Agent10SevenStepCount.rank_seven_minimum
#check Agent10SevenStepCount.seven_step_minimum
#check Agent10SevenStepCount.seven_step_path_bound
#check Agent10SevenStepCount.seven_step_trajectory_bound
#check Agent10SevenStepCount.actual_seven_step_count
#check Agent10SevenStepCount.singleton_seven_count
#check Agent10SevenStepCount.actual_seven_step_count_all_widths
#check Agent10EightCarry.eight_carry_words_determine_pair_sums_of_small_difference
#check Agent10EightCarry.eight_carry_words_determine_pair_sums_of_initial_nonoverflow
#check Agent10EightCarry.eight_carry_words_determine_next_integer_of_initial_nonoverflow
#check Agent10PrefixWitness.seven_prefix_exclusion_fin
#check Agent10PrefixWitness.six_prefix_survival
#check Agent10PrefixWitness.seven_prefix_exclusion
#check Agent10PrefixExclusion.survives_step_of
#check Agent10PrefixExclusion.survives_of_trajectory
#check Agent10PrefixExclusion.actual_history_survives
#check Agent10PrefixExclusion.seven_carries_exclude_positive_witness_prefix
#check Agent10PrefixExclusion.seven_carries_exclude_negative_witness_prefix
#check Agent10PrefixExclusion.smooth_four_first_coefficients
#check Agent10PrefixExclusion.smooth_four_nonzero_first_prefix
#check Agent10PrefixExclusion.eight_carries_determine_exterior_pair
#check Agent10SixCarryCounterexample.left_canonical
#check Agent10SixCarryCounterexample.right_canonical
#check Agent10SixCarryCounterexample.left_widths
#check Agent10SixCarryCounterexample.right_widths
#check Agent10SixCarryCounterexample.widths_agree
#check Agent10SixCarryCounterexample.six_complete_carries
#check Agent10SixCarryCounterexample.initial_pair_sums_differ
#check Agent10SixCarryCounterexample.next_integer_values
#check Agent10SixCarryCounterexample.next_integers_differ
#check Agent10SixCarryCounterexample.numeric_orbit_representations
#check Agent10SixCarryCounterexample.seventh_carry_differs
#check Agent10SixCarryCounterexample.six_carry_counterexample
#check Agent10ThreeColumnExclusion.decode_encode3
#check Agent10ThreeColumnExclusion.exclusion_p0
#check Agent10ThreeColumnExclusion.exclusion_p1
#check Agent10ThreeColumnExclusion.exclusion_p2
#check Agent10ThreeColumnExclusion.exclusion_p3
#check Agent10ThreeColumnExclusion.exclusion_p4
#check Agent10ThreeColumnExclusion.exclusion_p5
#check Agent10ThreeColumnExclusion.exclusion_p6
#check Agent10ThreeColumnExclusion.exclusion_p7
#check Agent10ThreeColumnExclusion.exclusion_p8
#check Agent10ThreeColumnExclusion.exclusion_p9
#check Agent10ThreeColumnExclusion.exclusion_p10
#check Agent10ThreeColumnExclusion.exclusion_p11
#check Agent10ThreeColumnExclusion.exclusion_p12
#check Agent10ThreeColumnExclusion.exclusion_p13
#check Agent10ThreeColumnExclusion.exclusion_p14
#check Agent10ThreeColumnExclusion.exclusion_p15
#check Agent10ThreeColumnExclusion.exclusion_p16
#check Agent10ThreeColumnExclusion.exclusion_p17
#check Agent10ThreeColumnExclusion.eight_three_prefix_exclusion_fin
#check Agent10ThreeColumnExclusion.seven_three_prefix_survival
#check Agent10ThreeColumnExclusion.eight_three_prefix_exclusion
#check Agent10ThreeColumnExclusion.observedBit3_value
#check Agent10ThreeColumnExclusion.state3_valid
#check Agent10ThreeColumnExclusion.prefix_carries3_exact
#check Agent10ThreeColumnExclusion.prefix_step3_exact
#check Agent10ThreeColumnCarry.survives3_step_of
#check Agent10ThreeColumnCarry.survives3_of_trajectory
#check Agent10ThreeColumnCarry.actual_history_survives3
#check Agent10ThreeColumnCarry.eight_carries_exclude_positive_shifted_prefix
#check Agent10ThreeColumnCarry.eight_carries_exclude_negative_shifted_prefix
#check Agent10ThreeColumnCarry.eight_carries_determine_second_pair
#check Agent10ThreeColumnCarry.eight_carries_determine_first_two_pairs
#check Agent10ThreeColumnCarry.eight_carries_determine_first_two_active_pairs
#check Agent10SevenCarryCounterexample.left_canonical
#check Agent10SevenCarryCounterexample.right_canonical
#check Agent10SevenCarryCounterexample.left_widths
#check Agent10SevenCarryCounterexample.right_widths
#check Agent10SevenCarryCounterexample.widths_agree
#check Agent10SevenCarryCounterexample.seven_complete_carries
#check Agent10SevenCarryCounterexample.initial_pair_sums_differ
#check Agent10SevenCarryCounterexample.next_integer_values
#check Agent10SevenCarryCounterexample.next_integers_differ
#check Agent10SevenCarryCounterexample.numeric_orbit_representations
#check Agent10SevenCarryCounterexample.eighth_carry_differs
#check Agent10SevenCarryCounterexample.initial_pair_difference_active
#check Agent10SevenCarryCounterexample.first_separation_at_seven
#check Agent10SevenCarryCounterexample.seven_carry_counterexample
#check Agent10EightCarryCounterexample.left_canonical
#check Agent10EightCarryCounterexample.right_canonical
#check Agent10EightCarryCounterexample.left_widths
#check Agent10EightCarryCounterexample.right_widths
#check Agent10EightCarryCounterexample.widths_agree
#check Agent10EightCarryCounterexample.eight_complete_carries
#check Agent10EightCarryCounterexample.initial_pair_sums_differ
#check Agent10EightCarryCounterexample.next_integer_values
#check Agent10EightCarryCounterexample.next_integers_differ
#check Agent10EightCarryCounterexample.numeric_orbit_representations
#check Agent10EightCarryCounterexample.ninth_carry_differs
#check Agent10EightCarryCounterexample.initial_pair_difference_active
#check Agent10EightCarryCounterexample.first_separation_at_eight
#check Agent10EightCarryCounterexample.eight_carry_counterexample
#check Agent10EightCarryCounterexample.palindrome_values_at_four
#check Agent10EightCarryCounterexample.first_palindromes_at_four
#check Agent10NineCarrySharp.pair_reconstruction_of_nine_le
#check Agent10NineCarrySharp.next_integer_reconstruction_of_nine_le
#check Agent10NineCarrySharp.not_pair_reconstruction_of_lt_nine
#check Agent10NineCarrySharp.not_next_integer_reconstruction_of_lt_nine
#check Agent10NineCarrySharp.uniform_pair_reconstruction_iff
#check Agent10NineCarrySharp.uniform_next_integer_reconstruction_iff
#check Agent10NineCarrySharp.eight_insufficient
#check Agent10NineCarrySharp.nine_sufficient
#check Agent10NineCarrySharp.nine_is_exact_uniform_threshold
run_cmd do
  let env ← getEnv
  let selected : List String := ["Lychrel196Research", "PrefixCarryBound", "ActualCarryObservability", "DifferenceObservability", "Agent10SevenStepCount", "Agent10SmoothingBoundary", "Agent10SmoothingBridge", "Agent10EightCarry", "Agent10PrefixWitness", "Agent10PrefixExclusion", "Agent10ThreeColumnExclusion", "Agent10ThreeColumnCarry", "Agent10SixCarryCounterexample", "Agent10SevenCarryCounterexample", "Agent10EightCarryCounterexample", "Agent10NineCarrySharp"]
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
