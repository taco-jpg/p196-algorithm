import Agent105AffineBasics
import Agent105TailSelection
import Agent105ReturnTimeBound
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#check Agent105.AffineDynamics.wordAt_nil
#check Agent105.AffineDynamics.wordAt_cons
#check Agent105.AffineDynamics.wordAt_append
#check Agent105.AffineDynamics.wordAt_singleton
#check Agent105.AffineDynamics.wordAt_constRun
#check Agent105.AffineDynamics.wordAt_reverse
#check Agent105.AffineDynamics.minusOne_eval
#check Agent105.AffineDynamics.minusOne_toNat
#check Agent105.AffineDynamics.specBound_nil
#check Agent105.AffineDynamics.specBound_cons
#check Agent105.AffineDynamics.specBound_reverse
#check Agent105.AffineDynamics.wordAt_bounded
#check Agent105.AffineDynamics.hasAffineRuns_wordAt
#check Agent105.TailSelection.eventually_of_forall
#check Agent105.TailSelection.eventually_mono
#check Agent105.TailSelection.eventually_and
#check Agent105.TailSelection.eventually_not_contradiction
#check Agent105.TailSelection.tailStable_const
#check Agent105.TailSelection.tailStable_congr
#check Agent105.TailSelection.tailStable_of_eventually
#check Agent105.TailSelection.tailStable_of_eventually_not
#check Agent105.TailSelection.tailStable_not
#check Agent105.TailSelection.tailStable_and
#check Agent105.TailSelection.tailStable_iff_eventually_or_not
#check Agent105.TailSelection.eventually_forall_list
#check Agent105.TailSelection.tailStable_forall_list
#check Agent105.TailSelection.tailStable_forall_pos_le
#check Agent105.TailSelection.uniform_tail_of_finite_cover
#check Agent105.TailSelection.uniform_bounded_tail_selection
#check Agent105.TailSelection.return_and_safety_tailStable
#check Agent105.TailSelection.uniform_safe_return_time
#check Agent105.ReturnTimeBound.orbit_width_potential_bound
#check Agent105.ReturnTimeBound.return_width_potential_bound
#check Agent105.ReturnTimeBound.return_time_bounds_of_width_gain
#check Agent105.ReturnTimeBound.positive_return_time_bound_of_width_gain
#check Agent105.ReturnTimeBound.return_time_bound_with_offset
#check Agent105.ReturnTimeBound.same_head_return_time_bound_with_offset
#check Agent105.ReturnTimeBound.word_family_return_time_bound
#check Agent105.ReturnTimeBound.affine_endpoint_return_time_bound
#check Agent105.ReturnTimeBound.affine_endpoint_return_time_bound_with_offset
run_cmd do
  let env ← getEnv
  let selected : List String := ["Agent102RunDefs", "PeriodObstructions", "ActualWordBridge", "Agent105AffineBasics", "Agent105TailSelection", "Agent105ReturnTimeBound"]
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
