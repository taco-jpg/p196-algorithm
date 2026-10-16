import Agent1PeriodicWidthPath
import Lean.Elab.BuiltinEvalCommand
import Lean.Util.CollectAxioms
open Lean Elab Command
#check Agent1.Periodic.QuotientPath
#print axioms Agent1.Periodic.QuotientPath
#check Agent1.Periodic.quotientClockSum
#print axioms Agent1.Periodic.quotientClockSum
#check Agent1.Periodic.quotientDeltaSum
#print axioms Agent1.Periodic.quotientDeltaSum
#check Agent1.Periodic.quotient_path_width_balance
#print axioms Agent1.Periodic.quotient_path_width_balance
#check Agent1.Periodic.quotient_path_equal_width_clock
#print axioms Agent1.Periodic.quotient_path_equal_width_clock
run_cmd do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  let mut defs := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      if env.allImportedModuleNames[idx.toNat]!.toString == "Agent1PeriodicWidthPath" then
        if let .defnInfo v := info then
          if v.safety != .safe then
            logInfo m!"NONSAFE_INVENTORY {name}"
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if mod.toString == "Agent1PeriodicWidthPath" then
        match info with
        | .axiomInfo _ => throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          count := count + 1
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then
            throwError m!"DISALLOWED_AXIOMS {name} : {axl}"
          logInfo m!"AUDIT_THEOREM {mod} {name} : {axl}"
        | .defnInfo v =>
          if v.safety != .safe then
            if !(["_private.Agent1PeriodicWidthPath.0.Agent1.Periodic.quotientClockSum.match_1.splitter._cstage2",
                  "Agent1.Periodic.quotientClockSum._cstage2",
                  "Agent1.Periodic.quotientClockSum.match_1._cstage1",
                  "Agent1.Periodic.quotientDeltaSum._cstage1",
                  "Agent1.Periodic.quotientClockSum._unsafe_rec",
                  "Agent1.Periodic.quotientDeltaSum._cstage2",
                  "Agent1.Periodic.quotientDeltaSum._unsafe_rec",
                  "_private.Agent1PeriodicWidthPath.0.Agent1.Periodic.quotientClockSum.match_1.splitter._rarg._cstage2",
                  "Agent1.Periodic.quotientDeltaSum._closed_1._cstage2",
                  "_private.Agent1PeriodicWidthPath.0.Agent1.Periodic.quotientClockSum.match_1.splitter._cstage1",
                  "Agent1.Periodic.quotientClockSum._cstage1"].contains name.toString) then
              throwError m!"NONCOMPILER_NONSAFE_DEFINITION {mod} {name}"
            logInfo m!"COMPILER_IMPLEMENTATION_DEFINITION {mod} {name}"
          else
            defs := defs + 1
            let axs ← liftCoreM (Lean.collectAxioms name)
            let axl := axs.toList
            if axl.any (fun ax => !(allowed.contains ax)) then
              throwError m!"DISALLOWED_DEFINITION_AXIOMS {name} : {axl}"
            logInfo m!"AUDIT_DEFINITION {mod} {name} : {axl}"
        | _ => throwError m!"UNEXPECTED_NEW_CONSTANT {mod} {name}"
  if count == 0 then throwError "MODULE_NOT_AUDITED"
  logInfo m!"MODULE_AUDIT theorems={count} definitions={defs} union={union}"
