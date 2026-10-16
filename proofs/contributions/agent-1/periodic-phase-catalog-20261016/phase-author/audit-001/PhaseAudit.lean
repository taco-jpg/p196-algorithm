import Agent1PeriodicPhase
import Lean
open Lean Elab Command
#check Agent1.Periodic.phaseImage
#print axioms Agent1.Periodic.phaseImage
#check Agent1.Periodic.mem_nonNine_of_length_four
#print axioms Agent1.Periodic.mem_nonNine_of_length_four
#check Agent1.Periodic.reverse_ne_nines
#print axioms Agent1.Periodic.reverse_ne_nines
#check Agent1.Periodic.terminalCarry_eq_of_nonNine
#print axioms Agent1.Periodic.terminalCarry_eq_of_nonNine
#check Agent1.Periodic.rawPeriod_eq_phaseImage
#print axioms Agent1.Periodic.rawPeriod_eq_phaseImage
run_cmd do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  let mut defs := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if mod.toString == "Agent1PeriodicPhase" then
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
            throwError m!"NONSAFE_DEFINITION {mod} {name}"
          defs := defs + 1
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          if axl.any (fun ax => !(allowed.contains ax)) then
            throwError m!"DISALLOWED_DEFINITION_AXIOMS {name} : {axl}"
          logInfo m!"AUDIT_DEFINITION {mod} {name} : {axl}"
        | _ => throwError m!"UNEXPECTED_NEW_CONSTANT {mod} {name}"
  if count == 0 then throwError "MODULE_NOT_AUDITED"
  logInfo m!"MODULE_AUDIT theorems={count} definitions={defs} union={union}"
