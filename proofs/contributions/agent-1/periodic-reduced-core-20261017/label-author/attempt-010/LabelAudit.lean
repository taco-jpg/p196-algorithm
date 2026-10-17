import Agent1PeriodicEighteenLabel
import Lean.Elab.BuiltinEvalCommand
import Lean.Util.CollectAxioms
open Lean Elab Command

#check Agent1.Periodic.outerComponent_eighteen_phase

run_cmd do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let safeNames : List String := ["_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_8.splitter", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_4.splitter", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_2.splitter", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_3.splitter", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_1.splitter", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_7.splitter", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_6.splitter", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_5.splitter"]
  let runtimeNames : List String := ["_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_4.splitter._cstage1", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_6.splitter._rarg._cstage2", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_6.splitter._cstage1", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_4.splitter._rarg._cstage2", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_2.splitter._rarg._cstage2", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_1.splitter._cstage2", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_7.splitter._cstage2", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_3.splitter._rarg._cstage2", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_6.splitter._cstage2", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_7.splitter._cstage1", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_1.splitter._rarg._cstage2", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_3.splitter._cstage1", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_2.splitter._cstage1", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_5.splitter._cstage1", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_8.splitter._cstage1", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_7.splitter._rarg._cstage2", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_8.splitter._rarg._cstage2", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_4.splitter._cstage2", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_5.splitter._cstage2", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_2.splitter._cstage2", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_8.splitter._cstage2", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_5.splitter._rarg._cstage2", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_1.splitter._cstage1", "_private.Agent1PeriodicEighteenLabel.0.Agent1.Periodic.outerComponent.match_3.splitter._cstage2"]
  let mut definitions := 0
  let mut generatedRuntime := 0
  let mut count := 0
  let mut seen : List Name := []
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      if env.allImportedModuleNames[idx.toNat]!.toString == "Agent1PeriodicEighteenLabel" then
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
        | .defnInfo value =>
          if value.safety == .safe then
            if !(safeNames.contains name.toString) then
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
            if !(runtimeNames.contains name.toString) then
              throwError m!"UNEXPECTED_RUNTIME_DEFINITION {name}"
            generatedRuntime := generatedRuntime + 1
            logInfo m!"GENERATED_RUNTIME_IMPLEMENTATION {name} SAFETY {repr value.safety}"
        | _ => throwError m!"UNEXPECTED_NEW_CONSTANT {name}"
  if !(seen.contains ``Agent1.Periodic.outerComponent_eighteen_phase) then
    throwError "MISSING_REQUIRED_ENDPOINT"
  if definitions != 8 || generatedRuntime != 24 then
    throwError "INCOMPLETE_DEFINITION_INVENTORY"
  logInfo m!"MODULE_AUDIT theorems={count} required_endpoints=1 safe_definitions={definitions} generated_runtime={generatedRuntime} custom_axioms=0 union={union}"
