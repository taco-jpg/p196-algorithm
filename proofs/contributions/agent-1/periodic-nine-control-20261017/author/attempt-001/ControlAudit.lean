import Agent1PeriodicNinesExtraStrip
import Lean.Elab.BuiltinEvalCommand
import Lean.Util.CollectAxioms
open Lean Elab Command
#check Agent1.Periodic.nines_extra_strip_control
#print axioms Agent1.Periodic.nines_extra_strip_control
run_cmd do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  let mut found := false
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      if env.allImportedModuleNames[idx.toNat]!.toString == "Agent1PeriodicNinesExtraStrip" then
        match info with
        | .thmInfo _ =>
          count := count + 1
          if name == ``Agent1.Periodic.nines_extra_strip_control then found := true
          let axs ← liftCoreM (Lean.collectAxioms name)
          if axs.toList.any (fun ax => !(allowed.contains ax)) then
            throwError m!"DISALLOWED_AXIOMS {name} : {axs.toList}"
          logInfo m!"AUDIT_THEOREM {name} : {axs.toList}"
        | _ => throwError m!"UNEXPECTED_NEW_CONSTANT {name}"
  if !found then throwError "MISSING_ENDPOINT"
  logInfo m!"MODULE_AUDIT theorem_constants={count} safe_defs=0 runtime=0 custom_axioms=0"
