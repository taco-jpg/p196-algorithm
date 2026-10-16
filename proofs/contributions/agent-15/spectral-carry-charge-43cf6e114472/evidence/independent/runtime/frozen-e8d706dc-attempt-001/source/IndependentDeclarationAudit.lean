import ChargeControls
import Lean


open Lean Elab Command
set_option pp.universes true
set_option pp.fullNames true
set_option pp.explicit true
set_option maxRecDepth 100000
set_option maxHeartbeats 0

run_cmd do
  let env ← getEnv
  let selected : List String := ["SpectralWeights", "BinaryCode", "ChargeSymmetry", "SourceFormula", "ChargeControls"]
  let required : List String := ["P196.Agent15.SpectralCarry.carryCharge_zero_iff", "P196.Agent15.SpectralCarry.odd_source_charge_zero_iff", "P196.Agent15.SpectralCarry.even_source_charge_zero_iff", "P196.Agent15.SpectralCarry.recurrence", "P196.Agent15.SpectralCarry.recurrence_zero", "P196.Agent15.SpectralCarry.recurrence_one", "P196.Agent15.SpectralCarry.recurrence_step", "P196.Agent15.SpectralCarry.U", "P196.Agent15.SpectralCarry.S", "P196.Agent15.SpectralCarry.U_zero", "P196.Agent15.SpectralCarry.U_one", "P196.Agent15.SpectralCarry.U_step", "P196.Agent15.SpectralCarry.S_zero", "P196.Agent15.SpectralCarry.S_one", "P196.Agent15.SpectralCarry.S_step", "P196.Agent15.SpectralCarry.oddWeight", "P196.Agent15.SpectralCarry.evenWeight", "P196.Agent15.SpectralCarry.oddWeight_zero", "P196.Agent15.SpectralCarry.oddWeight_one", "P196.Agent15.SpectralCarry.oddWeight_step", "P196.Agent15.SpectralCarry.evenWeight_zero", "P196.Agent15.SpectralCarry.evenWeight_one", "P196.Agent15.SpectralCarry.evenWeight_step", "P196.Agent15.SpectralCarry.weightSum", "P196.Agent15.SpectralCarry.weightSum_zero", "P196.Agent15.SpectralCarry.weightSum_succ", "P196.Agent15.SpectralCarry.oddWeight_pos", "P196.Agent15.SpectralCarry.evenWeight_pos", "P196.Agent15.SpectralCarry.oddWeight_growth", "P196.Agent15.SpectralCarry.evenWeight_growth", "P196.Agent15.SpectralCarry.oddWeight_superincreasing", "P196.Agent15.SpectralCarry.evenWeight_superincreasing", "P196.Agent15.SpectralCarry.Binary", "P196.Agent15.SpectralCarry.weighted", "P196.Agent15.SpectralCarry.binary_nil", "P196.Agent15.SpectralCarry.binary_tail", "P196.Agent15.SpectralCarry.weighted_bounds", "P196.Agent15.SpectralCarry.weighted_lt_next", "P196.Agent15.SpectralCarry.weighted_injective_binary", "P196.Agent15.SpectralCarry.reverse_take_half_iff", "P196.Agent15.SpectralCarry.halfCharge", "P196.Agent15.SpectralCarry.oddCharge", "P196.Agent15.SpectralCarry.evenCharge", "P196.Agent15.SpectralCarry.carryCharge", "P196.Agent15.SpectralCarry.binary_reverse", "P196.Agent15.SpectralCarry.binary_take", "P196.Agent15.SpectralCarry.halfCharge_zero_iff", "P196.Agent15.SpectralCarry.oddCharge_zero_iff", "P196.Agent15.SpectralCarry.evenCharge_zero_iff", "P196.Agent15.SpectralCarry.sumFirst", "P196.Agent15.SpectralCarry.sumFirst_eq_range_sum", "P196.Agent15.SpectralCarry.sumFirst_congr", "P196.Agent15.SpectralCarry.sumFirst_sub", "P196.Agent15.SpectralCarry.weighted_eq_sumFirst", "P196.Agent15.SpectralCarry.weighted_take_eq_sumFirst", "P196.Agent15.SpectralCarry.halfCharge_eq_source_sum", "P196.Agent15.SpectralCarry.oddCharge_eq_source_sum", "P196.Agent15.SpectralCarry.evenCharge_eq_source_sum", "P196.Agent15.SpectralCarry.carryCharge_eq_odd_source_sum", "P196.Agent15.SpectralCarry.carryCharge_eq_even_source_sum", "P196.Agent15.SpectralCarry.control_empty", "P196.Agent15.SpectralCarry.control_singletons", "P196.Agent15.SpectralCarry.control_length_two", "P196.Agent15.SpectralCarry.control_free_odd_center", "P196.Agent15.SpectralCarry.control_symmetric_even", "P196.Agent15.SpectralCarry.control_original_419", "P196.Agent15.SpectralCarry.control_nonbinary_counterexample", "P196.Agent15.SpectralCarry.control_incoming_zero_convention", "P196.Agent15.SpectralCarry.control_zero_overflow_convention"]
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut names : List String := []
  let mut safeNames : List String := []
  let mut safeCount := 0
  let mut implementationCount := 0
  let mut axiomUnion : List Name := []
  let mut count := 0
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let origin := env.allImportedModuleNames[idx.toNat]!
      if selected.contains origin.toString then
        unless (env.checked.get.find? name).isSome do
          throwError m!"UNCHECKED_DECLARATION {origin} {name}"
        let implementationOnly := info.isUnsafe || info.isPartial
        let kind : String := match info with
          | .axiomInfo _ => "axiom"
          | .defnInfo _ => "definition"
          | .thmInfo _ => "theorem"
          | .opaqueInfo _ => "opaque"
          | .quotInfo _ => "quotient"
          | .inductInfo _ => "inductive"
          | .ctorInfo _ => "constructor"
          | .recInfo _ => "recursor"
        if kind == "axiom" && !implementationOnly then
          throwError m!"NEW_AXIOM {origin} {name}"
        let axioms := (← liftCoreM (Lean.collectAxioms name)).qsort Name.lt
        let axl := axioms.toList
        if !implementationOnly && axl.any (fun ax => !(allowed.contains ax)) then
          throwError m!"DISALLOWED_AXIOMS {origin} {name} : {axl}"
        if implementationOnly then
          implementationCount := implementationCount + 1
        else
          safeCount := safeCount + 1
          safeNames := name.toString :: safeNames
          for ax in axl do
            unless axiomUnion.contains ax do
              axiomUnion := ax :: axiomUnion
        names := name.toString :: names
        count := count + 1
        let record := Json.mkObj [
          ("module", toJson origin.toString),
          ("name", toJson name.toString),
          ("kind", toJson kind),
          ("private", toJson (Lean.isPrivateName name)),
          ("implementation_only", toJson implementationOnly),
          ("unsafe", toJson info.isUnsafe),
          ("partial", toJson info.isPartial),
          ("axioms", toJson (axioms.map Name.toString))]
        logInfo m!"AUDIT_DECL_JSON {record.compress}"
        logInfo m!"SIGNATURE_BEGIN {name}"
        logInfo m!"{name} : {info.type}"
        logInfo m!"SIGNATURE_END {name}"
        elabCommand (← `(#print axioms $(mkIdent name)))
  for name in required do
    unless safeNames.contains name do
      throwError m!"MISSING_REQUIRED_DECLARATION {name}"
  if count == 0 then
    throwError "EMPTY_PROJECT_DECLARATION_AUDIT"
  let summary := Json.mkObj [
    ("count", toJson count),
    ("safe_count", toJson safeCount),
    ("implementation_count", toJson implementationCount),
    ("axiom_union", toJson ((axiomUnion.toArray.qsort Name.lt).map Name.toString))]
  logInfo m!"AUDIT_SUMMARY_JSON {summary.compress}"
