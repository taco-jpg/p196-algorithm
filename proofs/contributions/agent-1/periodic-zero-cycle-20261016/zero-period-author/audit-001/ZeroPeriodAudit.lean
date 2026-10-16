import Agent1PeriodicZeroPeriod
import Lean
open Lean Elab Command
#check Agent1.Periodic.leftPeriodDigits_zero
#print axioms Agent1.Periodic.leftPeriodDigits_zero
#check Agent1.Periodic.rightPeriodDigits_zero
#print axioms Agent1.Periodic.rightPeriodDigits_zero
#check Agent1.Periodic.rawPeriod_zero
#print axioms Agent1.Periodic.rawPeriod_zero
#check Agent1.Periodic.zero_quotient_valid
#print axioms Agent1.Periodic.zero_quotient_valid
run_cmd do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  let mut defs := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if mod.toString == "Agent1PeriodicZeroPeriod" then
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
            if !(name.toString.endsWith "._cstage1" || name.toString.endsWith "._cstage2") then
              throwError m!"NONCOMPILER_NONSAFE_DEFINITION {mod} {name}"
            logInfo m!"COMPILER_IMPLEMENTATION_DEFINITION {mod} {name}"
          else
            defs := defs + 1
            let axs ← liftCoreM (Lean.collectAxioms name)
            let axl := axs.toList
            if axl.any (fun ax => !(allowed.contains ax)) then
              throwError m!"DISALLOWED_DEFINITION_AXIOMS {name} : {axl}"
            logInfo m!"AUDIT_DEFINITION {mod} {name} : {axl}"
        | _ => pure ()
  if count == 0 then throwError "MODULE_NOT_AUDITED"
  logInfo m!"MODULE_AUDIT theorems={count} definitions={defs} union={union}"
