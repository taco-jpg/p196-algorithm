import Agent1PeriodicReturnCore
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#check Agent1.Periodic.componentRank_pos
#check Agent1.Periodic.outerEdge_rank_le
#check Agent1.Periodic.outerEdge_rank_drop
#check Agent1.Periodic.outerEdge_internal_component
#check Agent1.Periodic.outerComponent_zero_phase
#check Agent1.Periodic.outerComponent_initial_core
#check Agent1.Periodic.quotient_path_valid_catalog
#check Agent1.Periodic.quotient_path_outer_edge
#check Agent1.Periodic.quotient_path_zeroStateOrbit
#check Agent1.Periodic.quotient_path_zero_interface_ne
#check Agent1.Periodic.quotient_path_zero_no_return
#check Agent1.Periodic.quotient_return_component_constant
#check Agent1.Periodic.quotient_return_core
#check Agent1.Periodic.quotient_return_initial_outside
run_cmd do
  let env ← getEnv
  let selected : List String := ["PeriodObstructions", "ActualWordBridge", "PrefixSemantics", "LychrelDigitSums", "IncomingCarry", "Agent1RepeatedBlock", "Agent1RepeatedBlockContext", "Agent1PeriodicDigits", "Agent1PeriodicSlices", "Agent1PeriodicGuard", "Agent1PeriodicGuardFacts", "Agent1PeriodicOuterStrip", "Agent1PeriodicCenterStrip", "Agent1PeriodicQuotient", "Agent1PeriodicParity", "Agent1PeriodicPositivity", "Agent1PeriodicValidity", "Agent1PeriodicSafetyAlphabet", "Agent1PeriodicOuter", "Agent1PeriodicPhase", "Agent1PeriodicNines", "Agent1PeriodicPhaseCatalog", "Agent1PeriodicOuterChoices", "Agent1PeriodicCatalogOrder", "Agent1PeriodicOuterCatalog", "Agent1PeriodicOuterRank", "Agent1PeriodicWidthPath", "Agent1PeriodicQuotientPath", "Agent1PeriodicZeroPeriod", "Agent1PeriodicZeroState", "Agent1PeriodicZeroExponent", "Agent1PeriodicZeroNumeric", "Agent1PeriodicZeroMass", "Agent1PeriodicRealizability", "Agent1PeriodicZeroCycle", "Agent1PeriodicZeroPath", "CondensationBound", "Agent1PeriodicReturnCore"]
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
