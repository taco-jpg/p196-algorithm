import Agent1PeriodicNinesExcursion
import Lean.Elab.BuiltinEvalCommand
import Lean.Util.CollectAxioms
open Lean Elab Command
#check Agent1.Periodic.quotient_return_nines_center_excursion
#check Agent1.Periodic.quotient_path_nines_small_centers_no_return
#print axioms Agent1.Periodic.quotient_return_nines_center_excursion
#print axioms Agent1.Periodic.quotient_path_nines_small_centers_no_return
run_cmd do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      if env.allImportedModuleNames[idx.toNat]!.toString == "Agent1PeriodicNinesExcursion" then
        match info with
        | .thmInfo _ =>
          count := count + 1
          let axs ← liftCoreM (Lean.collectAxioms name)
          if axs.toList.any (fun ax => !(allowed.contains ax)) then
            throwError m!"DISALLOWED_AXIOMS {name} : {axs.toList}"
          logInfo m!"AUDIT_THEOREM {name} : {axs.toList}"
        | _ => throwError m!"UNEXPECTED_NEW_CONSTANT {name}"
  logInfo m!"MODULE_AUDIT theorem_constants={count} safe_defs=0 runtime=0 custom_axioms=0"
