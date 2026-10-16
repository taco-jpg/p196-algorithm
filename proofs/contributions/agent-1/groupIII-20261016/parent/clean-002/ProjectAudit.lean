import Agent1GroupIIINumeric
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#check P196.Agent1.GroupIII.component_two_step_return
#check P196.Agent1.GroupIII.whole_two_step_return
#check P196.Agent1.GroupIII.actual_intermediate_overlap_fails
#check P196.Agent1.GroupIII.numeric_delayed_return
#check P196.Agent1.GroupIII.realized_safe_gate
run_cmd do
  let env ← getEnv
  let selected : List String := ["LychrelDigitSums", "SafeDelay", "DecimalSafeRuns", "DecimalDelayBridge", "PairDelayBridge", "DelayedOverlapGate", "Agent1GroupIII", "Agent1GroupIIINumeric"]
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
