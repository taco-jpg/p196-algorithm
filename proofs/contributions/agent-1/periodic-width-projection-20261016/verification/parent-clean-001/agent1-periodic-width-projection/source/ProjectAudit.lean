import Agent1PeriodicWidthLift
import Agent1PeriodicWidthPath
import Agent1PeriodicWidthNumeric
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#check Agent1.Periodic.widthResidue_lt
#check Agent1.Periodic.periodicWord_length_mod_eight
#check Agent1.Periodic.quotient_width_mod_eight
#check Agent1.Periodic.quotient_widthResidue
#check Agent1.Periodic.widthCatalog_length
#check Agent1.Periodic.widthEdges_length
#check Agent1.Periodic.widthCatalog_nodup
#check Agent1.Periodic.mem_widthCatalog_iff
#check Agent1.Periodic.liftOuterEdge_mem
#check Agent1.Periodic.widthEdge_target_mem
#check Agent1.Periodic.quotient_width_catalog_edge
#check Agent1.Periodic.quotient_valid_in_widthCatalog
#check Agent1.Periodic.quotient_path_width_balance
#check Agent1.Periodic.quotient_path_equal_width_clock
#check Agent1.Periodic.periodic_decimalLength_mod_eight
#check Agent1.Periodic.periodic_actual_step_decimalLength_mod_eight
run_cmd do
  let env ← getEnv
  let selected : List String := ["PeriodObstructions", "ActualWordBridge", "PrefixSemantics", "LychrelDigitSums", "IncomingCarry", "Agent1RepeatedBlock", "Agent1RepeatedBlockContext", "Agent1PeriodicDigits", "Agent1PeriodicSlices", "Agent1PeriodicGuard", "Agent1PeriodicGuardFacts", "Agent1PeriodicOuterStrip", "Agent1PeriodicCenterStrip", "Agent1PeriodicQuotient", "Agent1PeriodicParity", "Agent1PeriodicPositivity", "Agent1PeriodicValidity", "Agent1PeriodicSafetyAlphabet", "Agent1PeriodicOuter", "Agent1PeriodicPhase", "Agent1PeriodicNines", "Agent1PeriodicPhaseCatalog", "Agent1PeriodicOuterChoices", "Agent1PeriodicCatalogOrder", "Agent1PeriodicOuterCatalog", "Agent1PeriodicWidth", "Agent1PeriodicWidthLift", "Agent1PeriodicWidthPath", "Agent1PeriodicNumeric", "Agent1PeriodicWidthNumeric"]
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
