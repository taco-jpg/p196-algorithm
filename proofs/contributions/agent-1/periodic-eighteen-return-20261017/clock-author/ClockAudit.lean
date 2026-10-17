import Agent1PeriodicEighteenClock
import Lean.Elab.BuiltinEvalCommand
import Lean.Util.CollectAxioms
open Lean Elab Command

#check Agent1.Periodic.periodicWord_carry_eq_rawGamma
#check Agent1.Periodic.quotient_path_actual_carry_step
#check Agent1.Periodic.quotient_path_actual_carry_sum

run_cmd do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let required : List Name := [``Agent1.Periodic.periodicWord_carry_eq_rawGamma,
    ``Agent1.Periodic.quotient_path_actual_carry_step,
    ``Agent1.Periodic.quotient_path_actual_carry_sum]
  let mut count := 0
  let mut seen : List Name := []
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      if env.allImportedModuleNames[idx.toNat]!.toString == "Agent1PeriodicEighteenClock" then
        match info with
        | .thmInfo _ =>
          count := count + 1
          seen := name :: seen
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then
            throwError m!"DISALLOWED_AXIOMS {name} : {axl}"
          logInfo m!"AUDIT_THEOREM {name} : {axl}"
        | _ => throwError m!"UNEXPECTED_NON_THEOREM_CONSTANT {name}"
  for name in required do
    if !(seen.contains name) then throwError m!"MISSING_REQUIRED_ENDPOINT {name}"
  if count == 0 then throwError "MODULE_NOT_AUDITED"
  logInfo m!"MODULE_AUDIT theorems={count} required_endpoints={required.length} safe_definitions=0 unsafe_definitions=0 custom_axioms=0 union={union}"
