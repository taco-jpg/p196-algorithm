import Agent1PeriodicInitialIncoming
import Lean.Elab.BuiltinEvalCommand
import Lean.Util.CollectAxioms
open Lean Elab Command

#check Agent1.Periodic.phaseEdge_initial_clock
#check Agent1.Periodic.quotient_return_initial_last_clock

run_cmd do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let required : List Name := [``Agent1.Periodic.phaseEdge_initial_clock,
    ``Agent1.Periodic.quotient_return_initial_last_clock]
  let mut theorems := 0
  let mut seen : List Name := []
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      if env.allImportedModuleNames[idx.toNat]!.toString == "Agent1PeriodicInitialIncoming" then
        seen := name :: seen
        match info with
        | .axiomInfo _ => throwError m!"CUSTOM_AXIOM {name}"
        | .thmInfo _ =>
          theorems := theorems + 1
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
  if theorems == 0 then throwError "MODULE_NOT_AUDITED"
  logInfo m!"MODULE_AUDIT theorems={theorems} required_public_names=2 custom_axioms=0 union={union}"
