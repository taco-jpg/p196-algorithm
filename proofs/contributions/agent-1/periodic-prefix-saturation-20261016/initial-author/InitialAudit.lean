import Agent1PeriodicInitialUnsaturated
import Lean.Elab.BuiltinEvalCommand
import Lean.Util.CollectAxioms
open Lean Elab Command

#check Agent1.Periodic.quotient_return_initial_clock_strict
#check Agent1.Periodic.quotient_return_initial_clock_gain
#check Agent1.Periodic.quotient_return_initial_length_ge_seventeen

run_cmd do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let required : List Name := [``Agent1.Periodic.quotient_return_initial_clock_strict,
    ``Agent1.Periodic.quotient_return_initial_clock_gain,
    ``Agent1.Periodic.quotient_return_initial_length_ge_seventeen]
  let mut count := 0
  let mut definitions := 0
  let mut seen : List Name := []
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      if env.allImportedModuleNames[idx.toNat]!.toString == "Agent1PeriodicInitialUnsaturated" then
        match info with
        | .axiomInfo _ => throwError m!"CUSTOM_AXIOM {name}"
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
        | .defnInfo value =>
          if value.safety != .safe then
            throwError m!"UNSAFE_NEW_DEFINITION {name}"
          definitions := definitions + 1
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then
            throwError m!"DISALLOWED_DEFINITION_AXIOMS {name} : {axl}"
          logInfo m!"AUDIT_SAFE_DEFINITION {name} : {axl}"
        | _ => throwError m!"UNEXPECTED_NEW_CONSTANT {name}"
  for name in required do
    if !(seen.contains name) then throwError m!"MISSING_REQUIRED_ENDPOINT {name}"
  if count == 0 then throwError "MODULE_NOT_AUDITED"
  logInfo m!"MODULE_AUDIT theorems={count} public_endpoints=3 safe_definitions={definitions} custom_axioms=0 union={union}"
