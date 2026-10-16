import Agent1GroupIIIHandoffNumeric
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#check P196.Agent1.GroupIIIHandoff.first_domain
#print axioms P196.Agent1.GroupIIIHandoff.first_domain
#check P196.Agent1.GroupIIIHandoff.first_return_component
#print axioms P196.Agent1.GroupIIIHandoff.first_return_component
#check P196.Agent1.GroupIIIHandoff.afterTwo_carry
#print axioms P196.Agent1.GroupIIIHandoff.afterTwo_carry
#check P196.Agent1.GroupIIIHandoff.wholeTwo_carry
#print axioms P196.Agent1.GroupIIIHandoff.wholeTwo_carry
#check P196.Agent1.GroupIIIHandoff.componentThree_carry
#print axioms P196.Agent1.GroupIIIHandoff.componentThree_carry
#check P196.Agent1.GroupIIIHandoff.wholeThree_carry
#print axioms P196.Agent1.GroupIIIHandoff.wholeThree_carry
#check P196.Agent1.GroupIIIHandoff.afterTwo_no_overflow
#print axioms P196.Agent1.GroupIIIHandoff.afterTwo_no_overflow
#check P196.Agent1.GroupIIIHandoff.wholeTwo_no_overflow
#print axioms P196.Agent1.GroupIIIHandoff.wholeTwo_no_overflow
#check P196.Agent1.GroupIIIHandoff.componentThree_no_overflow
#print axioms P196.Agent1.GroupIIIHandoff.componentThree_no_overflow
#check P196.Agent1.GroupIIIHandoff.wholeThree_no_overflow
#print axioms P196.Agent1.GroupIIIHandoff.wholeThree_no_overflow
#check P196.Agent1.GroupIIIHandoff.afterTwo_next
#print axioms P196.Agent1.GroupIIIHandoff.afterTwo_next
#check P196.Agent1.GroupIIIHandoff.wholeTwo_next
#print axioms P196.Agent1.GroupIIIHandoff.wholeTwo_next
#check P196.Agent1.GroupIIIHandoff.componentThree_next
#print axioms P196.Agent1.GroupIIIHandoff.componentThree_next
#check P196.Agent1.GroupIIIHandoff.wholeThree_next
#print axioms P196.Agent1.GroupIIIHandoff.wholeThree_next
#check P196.Agent1.GroupIIIHandoff.continue_no_overflow
#print axioms P196.Agent1.GroupIIIHandoff.continue_no_overflow
#check P196.Agent1.GroupIIIHandoff.component_time_three
#print axioms P196.Agent1.GroupIIIHandoff.component_time_three
#check P196.Agent1.GroupIIIHandoff.whole_time_three
#print axioms P196.Agent1.GroupIIIHandoff.whole_time_three
#check P196.Agent1.GroupIIIHandoff.component_time_four
#print axioms P196.Agent1.GroupIIIHandoff.component_time_four
#check P196.Agent1.GroupIIIHandoff.whole_time_four
#print axioms P196.Agent1.GroupIIIHandoff.whole_time_four
#check P196.Agent1.GroupIIIHandoff.component_width_through_four
#print axioms P196.Agent1.GroupIIIHandoff.component_width_through_four
#check P196.Agent1.GroupIIIHandoff.whole_width_through_four
#print axioms P196.Agent1.GroupIIIHandoff.whole_width_through_four
#check P196.Agent1.GroupIIIHandoff.finiteComponent_three
#print axioms P196.Agent1.GroupIIIHandoff.finiteComponent_three
#check P196.Agent1.GroupIIIHandoff.finiteComponent_four
#print axioms P196.Agent1.GroupIIIHandoff.finiteComponent_four
#check P196.Agent1.GroupIIIHandoff.time_three_departure
#print axioms P196.Agent1.GroupIIIHandoff.time_three_departure
#check P196.Agent1.GroupIIIHandoff.time_four_overlap
#print axioms P196.Agent1.GroupIIIHandoff.time_four_overlap
#check P196.Agent1.GroupIIIHandoff.wholeTwo_not_bad
#print axioms P196.Agent1.GroupIIIHandoff.wholeTwo_not_bad
#check P196.Agent1.GroupIIIHandoff.wholeThree_not_bad
#print axioms P196.Agent1.GroupIIIHandoff.wholeThree_not_bad
#check P196.Agent1.GroupIIIHandoff.r1_component_time4_width
#print axioms P196.Agent1.GroupIIIHandoff.r1_component_time4_width
#check P196.Agent1.GroupIIIHandoff.r1_component_time4_columns
#print axioms P196.Agent1.GroupIIIHandoff.r1_component_time4_columns
#check P196.Agent1.GroupIIIHandoff.r1_whole_time4_width
#print axioms P196.Agent1.GroupIIIHandoff.r1_whole_time4_width
#check P196.Agent1.GroupIIIHandoff.r1_time4_signed_defect
#print axioms P196.Agent1.GroupIIIHandoff.r1_time4_signed_defect
#check P196.Agent1.GroupIIIHandoff.r1_actual_time4_overlap_fails
#print axioms P196.Agent1.GroupIIIHandoff.r1_actual_time4_overlap_fails
#check P196.Agent1.GroupIIIHandoff.time_four_overlap_iff
#print axioms P196.Agent1.GroupIIIHandoff.time_four_overlap_iff
#check P196.Agent1.GroupIIIHandoff.time_one_departure
#print axioms P196.Agent1.GroupIIIHandoff.time_one_departure
#check P196.Agent1.GroupIIIHandoff.time_two_overlap
#print axioms P196.Agent1.GroupIIIHandoff.time_two_overlap
#check P196.Agent1.GroupIIIHandoff.two_genuine_repairs
#print axioms P196.Agent1.GroupIIIHandoff.two_genuine_repairs
#check P196.Agent1.GroupIIIHandoff.numeric_time_two
#print axioms P196.Agent1.GroupIIIHandoff.numeric_time_two
#check P196.Agent1.GroupIIIHandoff.numeric_time_three
#print axioms P196.Agent1.GroupIIIHandoff.numeric_time_three
#check P196.Agent1.GroupIIIHandoff.numeric_time_four
#print axioms P196.Agent1.GroupIIIHandoff.numeric_time_four
#check P196.Agent1.GroupIIIHandoff.numeric_time_four_iff
#print axioms P196.Agent1.GroupIIIHandoff.numeric_time_four_iff
#check P196.Agent1.GroupIIIHandoff.numeric_four_step_safety
#print axioms P196.Agent1.GroupIIIHandoff.numeric_four_step_safety
#check P196.Agent1.GroupIIIHandoff.numeric_safe_handoff
#print axioms P196.Agent1.GroupIIIHandoff.numeric_safe_handoff
#check P196.Agent1.GroupIIIHandoff.realized_safe_handoff
#print axioms P196.Agent1.GroupIIIHandoff.realized_safe_handoff
run_cmd do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let selected : List String := ["Agent1GroupIIIHandoff", "Agent1GroupIIIHandoffNumeric"]
  let mut count := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        match info with
        | .axiomInfo _ => throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          count := count + 1
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then throwError m!"DISALLOWED_AXIOMS {name} : {axl}"
          logInfo m!"AUDIT_THEOREM {mod} {name} : {axl}"
        | _ => pure ()
  logInfo m!"MODULE_AUDIT theorems={count} union={union}"
