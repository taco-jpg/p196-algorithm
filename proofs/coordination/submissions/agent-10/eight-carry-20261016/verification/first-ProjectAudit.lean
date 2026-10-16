import Agent10EightCarry
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
run_cmd do
  let env ← getEnv
  let selected : List String := ["Lychrel196Research", "PrefixCarryBound", "ActualCarryObservability", "DifferenceObservability", "Agent10SevenStepCount", "Agent10SmoothingBoundary", "Agent10SmoothingBridge", "Agent10EightCarry"]
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
