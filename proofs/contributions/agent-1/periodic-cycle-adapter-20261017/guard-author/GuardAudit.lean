import Agent1PeriodicCycleGuard
import Lean.Elab.BuiltinEvalCommand
import Lean.Util.CollectAxioms
open Lean Elab Command

#check Agent1.Periodic.quotientPathExponent_accounting
#check Agent1.Periodic.quotientCycleExponent_guarded
#check Agent1.Periodic.quotientCycleExponent_step
#check Agent1.Periodic.quotient_return_guarded_schedule

run_cmd do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let required : List Name := [``Agent1.Periodic.quotientPathExponent_accounting,
    ``Agent1.Periodic.quotientCycleExponent_guarded,
    ``Agent1.Periodic.quotientCycleExponent_step,
    ``Agent1.Periodic.quotient_return_guarded_schedule]
  let mut count := 0
  let mut definitions := 0
  let mut generatedRuntime := 0
  let mut seen : List Name := []
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      if env.allImportedModuleNames[idx.toNat]!.toString == "Agent1PeriodicCycleGuard" then
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
          if value.safety == .safe then
            if name != ``Agent1.Periodic.quotientCycleExponent then
              throwError m!"UNEXPECTED_SAFE_DEFINITION {name}"
            definitions := definitions + 1
            let axs ← liftCoreM (Lean.collectAxioms name)
            let axl := axs.toList
            for ax in axl do
              if !(union.contains ax) then union := ax :: union
            if axl.any (fun ax => !(allowed.contains ax)) then
              throwError m!"DISALLOWED_DEFINITION_AXIOMS {name} : {axl}"
            logInfo m!"AUDIT_SAFE_DEFINITION {name} : {axl}"
          else
            if !(["Agent1.Periodic.quotientCycleExponent._cstage1",
                "Agent1.Periodic.quotientCycleExponent._cstage2"].contains name.toString) then
              throwError m!"UNEXPECTED_UNSAFE_DEFINITION {name}"
            generatedRuntime := generatedRuntime + 1
            logInfo m!"GENERATED_RUNTIME_IMPLEMENTATION {name}"
        | _ => throwError m!"UNEXPECTED_NEW_CONSTANT {name}"
  for name in required do
    if !(seen.contains name) then throwError m!"MISSING_REQUIRED_ENDPOINT {name}"
  if count == 0 then throwError "MODULE_NOT_AUDITED"
  if definitions != 1 || generatedRuntime != 2 then
    throwError "INCOMPLETE_DEFINITION_INVENTORY"
  logInfo m!"MODULE_AUDIT theorems={count} required_endpoints={required.length} safe_definitions={definitions} generated_runtime={generatedRuntime} custom_axioms=0 union={union}"
