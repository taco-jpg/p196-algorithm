import Agent1PeriodicNinesCycle
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#check Agent1.Periodic.quotient_path_nines_phase
#check Agent1.Periodic.quotient_path_nines_entry_sum
#check Agent1.Periodic.periodic_nines_input_nonpalindrome
#check Agent1.Periodic.quotient_cycle_nines_safe
#check Agent1.Periodic.quotient_cycle_nines_positive_seed
run_cmd do
  let env ← getEnv
  let selected : List String := ["PeriodObstructions", "ActualWordBridge", "PrefixSemantics", "LychrelDigitSums", "IncomingCarry", "Agent1RepeatedBlock", "Agent1RepeatedBlockContext", "Agent1PeriodicDigits", "Agent1PeriodicSlices", "Agent1PeriodicGuard", "Agent1PeriodicGuardFacts", "Agent1PeriodicOuterStrip", "Agent1PeriodicCenterStrip", "Agent1PeriodicQuotient", "Agent1PeriodicParity", "Agent1PeriodicPositivity", "Agent1PeriodicValidity", "Agent1PeriodicSafetyAlphabet", "Agent1PeriodicOuter", "Agent1PeriodicWidthPath", "Agent1PeriodicReturnClock", "Agent1PeriodicCyclePath", "Agent1PeriodicZeroPeriod", "Agent1PeriodicZeroNumeric", "Agent1PeriodicRealizability", "Agent1PeriodicGuardedPath", "Agent1PeriodicCycleGuard", "Agent1PeriodicSafety", "Agent1PeriodicSafetyNumeric", "Agent1PeriodicCycleNumeric", "Agent1PeriodicNines", "Agent1PeriodicPhase", "Agent1PeriodicNinesPath", "Agent1PeriodicNinesCycle"]
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        match info with
        | .axiomInfo v =>
          if v.isUnsafe then logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {mod} {name}"
          else throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          count := count + 1
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then throwError m!"DISALLOWED_AXIOMS {mod} {name} : {axl}"
          logInfo m!"AUDIT_THEOREM {mod} {name} : {axl}"
        | _ => pure ()
  logInfo m!"FULL_MODULE_AUDIT theorems={count} union={union}"
