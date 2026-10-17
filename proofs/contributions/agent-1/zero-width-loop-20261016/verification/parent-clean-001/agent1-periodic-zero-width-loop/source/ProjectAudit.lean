import Agent1PeriodicZeroWidthLoop
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#check Agent1.Periodic.zeroWidthEdge_mem
#check Agent1.Periodic.zeroWidthEdge_labels
#check Agent1.Periodic.zeroWidthNode_mem
#check Agent1.Periodic.zeroWidthNode_closed
#check Agent1.Periodic.zeroWidthEdge_clock_sum
#check Agent1.Periodic.zeroWidthLoop_initial_valid
#check Agent1.Periodic.zeroWidthLoop_initial_projection
#check Agent1.Periodic.zeroWidthLoop_initial_realizable
#check Agent1.Periodic.zeroWidthLoop_certificate
#check Agent1.Periodic.zeroWidthLoop_no_full_return
#check Agent1.Periodic.zeroWidthLoop_projection_not_sufficient
run_cmd do
  let env ← getEnv
  let selected : List String := ["PeriodObstructions", "ActualWordBridge", "PrefixSemantics", "LychrelDigitSums", "IncomingCarry", "Agent1RepeatedBlock", "Agent1RepeatedBlockContext", "Agent1PeriodicDigits", "Agent1PeriodicSlices", "Agent1PeriodicGuard", "Agent1PeriodicGuardFacts", "Agent1PeriodicOuterStrip", "Agent1PeriodicCenterStrip", "Agent1PeriodicQuotient", "Agent1PeriodicParity", "Agent1PeriodicPositivity", "Agent1PeriodicValidity", "Agent1PeriodicSafetyAlphabet", "Agent1PeriodicOuter", "Agent1PeriodicPhase", "Agent1PeriodicNines", "Agent1PeriodicPhaseCatalog", "Agent1PeriodicOuterChoices", "Agent1PeriodicCatalogOrder", "Agent1PeriodicOuterCatalog", "Agent1PeriodicWidth", "Agent1PeriodicWidthLift", "Agent1PeriodicWidthPath", "Agent1PeriodicZeroPeriod", "Agent1PeriodicZeroState", "Agent1PeriodicZeroExponent", "Agent1PeriodicZeroNumeric", "Agent1PeriodicZeroMass", "Agent1PeriodicRealizability", "Agent1PeriodicZeroCycle", "Agent1PeriodicZeroPath", "Agent1PeriodicZeroWidthLoop"]
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
