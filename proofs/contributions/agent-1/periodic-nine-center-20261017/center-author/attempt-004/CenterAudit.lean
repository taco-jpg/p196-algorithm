import Agent1PeriodicNinesCenter
import Lean.Elab.BuiltinEvalCommand
import Lean.Util.CollectAxioms
open Lean Elab Command

#check Agent1.Periodic.rawCenter_nines_mixed
#check Agent1.Periodic.quotientCenter_nines_mixed
#check Agent1.Periodic.centerPeriods_nines_mixed

run_cmd do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let required : List Name := [``Agent1.Periodic.rawCenter_nines_mixed,
    ``Agent1.Periodic.quotientCenter_nines_mixed, ``Agent1.Periodic.centerPeriods_nines_mixed]
  let mut count := 0
  let mut seen : List Name := []
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      if env.allImportedModuleNames[idx.toNat]!.toString == "Agent1PeriodicNinesCenter" then
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
        | _ => throwError m!"UNEXPECTED_NEW_CONSTANT {name}"
  for name in required do
    if !(seen.contains name) then throwError m!"MISSING_REQUIRED_ENDPOINT {name}"
  logInfo m!"MODULE_AUDIT theorems={count} required_endpoints=3 safe_definitions=0 generated_runtime=0 custom_axioms=0 union={union}"
