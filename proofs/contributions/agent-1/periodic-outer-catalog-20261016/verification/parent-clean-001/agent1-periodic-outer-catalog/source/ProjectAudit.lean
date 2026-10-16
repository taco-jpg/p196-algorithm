import Agent1PeriodicOuterCatalog
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#check Agent1.Periodic.outside_bounds
#check Agent1.Periodic.quotient_outside_step
#check Agent1.Periodic.mem_outerImages_of_actual
#check Agent1.Periodic.outerOutputs_mem_of_phaseEdge
#check Agent1.Periodic.strictNatKeys_pairwise
#check Agent1.Periodic.nodup_of_strictNatKeys
#check Agent1.Periodic.outerCatalog_nodup_of_checked
#check Agent1.Periodic.outerEdges_spec
#check Agent1.Periodic.outerCatalog_length
#check Agent1.Periodic.outerCatalog_nodup
#check Agent1.Periodic.outerEdges_length
#check Agent1.Periodic.outerCatalog_initial
#check Agent1.Periodic.outerCatalog_phases_checked
#check Agent1.Periodic.outerEdges_targets_checked
#check Agent1.Periodic.outerCatalog_phase_mem
#check Agent1.Periodic.outerEdge_target_mem
#check Agent1.Periodic.quotient_outer_catalog_edge
#check Agent1.Periodic.quotient_valid_in_outerCatalog
run_cmd do
  let env ← getEnv
  let selected : List String := ["PeriodObstructions", "ActualWordBridge", "PrefixSemantics", "LychrelDigitSums", "IncomingCarry", "Agent1RepeatedBlock", "Agent1RepeatedBlockContext", "Agent1PeriodicDigits", "Agent1PeriodicSlices", "Agent1PeriodicGuard", "Agent1PeriodicGuardFacts", "Agent1PeriodicOuterStrip", "Agent1PeriodicCenterStrip", "Agent1PeriodicQuotient", "Agent1PeriodicParity", "Agent1PeriodicPositivity", "Agent1PeriodicValidity", "Agent1PeriodicSafetyAlphabet", "Agent1PeriodicOuter", "Agent1PeriodicPhase", "Agent1PeriodicNines", "Agent1PeriodicPhaseCatalog", "Agent1PeriodicOuterChoices", "Agent1PeriodicCatalogOrder", "Agent1PeriodicOuterCatalog"]
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
