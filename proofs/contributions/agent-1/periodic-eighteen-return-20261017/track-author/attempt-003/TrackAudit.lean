import Agent1PeriodicEighteenTrack
import Lean.Elab.BuiltinEvalCommand
import Lean.Util.CollectAxioms
open Lean Elab Command

#check Agent1.Periodic.quotient_eighteen_track

run_cmd do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let runtime : List String := [
    "Agent1.Periodic.quotientEighteenTrack._unsafe_rec",
    "Agent1.Periodic.quotientEighteenTrack._lambda_1._cstage2",
    "_private.Agent1PeriodicEighteenTrack.0.Agent1.Periodic.quotientEighteenTrack.match_1.splitter._cstage1",
    "Agent1.Periodic.quotientEighteenTrack._cstage2",
    "_private.Agent1PeriodicEighteenTrack.0.Agent1.Periodic.quotientEighteenTrack.match_1.splitter._rarg._cstage2",
    "Agent1.Periodic.quotientEighteenTrack._cstage1",
    "Agent1.Periodic.quotientEighteenTrack.match_1._cstage1",
    "_private.Agent1PeriodicEighteenTrack.0.Agent1.Periodic.quotientEighteenTrack.match_1.splitter._cstage2"]
  let mut count := 0
  let mut definitions := 0
  let mut generatedRuntime := 0
  let mut seen : List Name := []
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      if env.allImportedModuleNames[idx.toNat]!.toString == "Agent1PeriodicEighteenTrack" then
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
            definitions := definitions + 1
            let axs ← liftCoreM (Lean.collectAxioms name)
            let axl := axs.toList
            for ax in axl do
              if !(union.contains ax) then union := ax :: union
            if axl.any (fun ax => !(allowed.contains ax)) then
              throwError m!"DISALLOWED_DEFINITION_AXIOMS {name} : {axl}"
            logInfo m!"AUDIT_SAFE_DEFINITION {name} : {axl}"
          else
            if !(runtime.contains name.toString) then
              throwError m!"UNEXPECTED_UNSAFE_DEFINITION {name}"
            generatedRuntime := generatedRuntime + 1
            logInfo m!"GENERATED_RUNTIME_IMPLEMENTATION {name} SAFETY {repr value.safety}"
        | _ => throwError m!"UNEXPECTED_NEW_CONSTANT {name}"
  if !(seen.contains ``Agent1.Periodic.quotient_eighteen_track) then
    throwError "MISSING_REQUIRED_ENDPOINT"
  if count == 0 then throwError "MODULE_NOT_AUDITED"
  if definitions != 4 || generatedRuntime != 8 then
    throwError "INCOMPLETE_DEFINITION_INVENTORY"
  logInfo m!"MODULE_AUDIT theorems={count} required_endpoints=1 safe_definitions={definitions} generated_runtime={generatedRuntime} custom_axioms=0 union={union}"
