import Agent9FiniteHorizonCount
import Lean

open Lean Elab Command

set_option maxRecDepth 100000
set_option maxHeartbeats 0

/- Exhaustive theorem 和 safe-definition audit by compiled module origin.
The exact preserved compatibility import contributes no declarations. -/

#check @P196.Agent9.Ensemble.mem_unmarkedSeeds
#check @P196.Agent9.Ensemble.unmarkedSeeds_nodup
#check @P196.Agent9.Ensemble.length_unmarkedSeeds
#check @P196.Agent9.Ensemble.selected_digits_le
#check @P196.Agent9.Ensemble.selected_position_geometry
#check @P196.Agent9.Ensemble.mem_positiveHits
#check @P196.Agent9.Ensemble.positiveHits_subset_unmarkedSeeds
#check @P196.Agent9.Ensemble.positiveHits_count_le

#print axioms P196.Agent9.Ensemble.wordChoices
#print axioms P196.Agent9.Ensemble.mem_wordChoices
#print axioms P196.Agent9.Ensemble.length_flatMap_map
#print axioms P196.Agent9.Ensemble.nodup_flatMap_map
#print axioms P196.Agent9.Ensemble.wordChoices_nodup
#print axioms P196.Agent9.Ensemble.length_wordChoices
#print axioms P196.Agent9.Ensemble.appendProduct
#print axioms P196.Agent9.Ensemble.mem_appendProduct
#print axioms P196.Agent9.Ensemble.length_appendProduct
#print axioms P196.Agent9.Ensemble.appendProduct_nodup
#print axioms P196.Agent9.Ensemble.blockChoices
#print axioms P196.Agent9.Ensemble.length_blockChoices
#print axioms P196.Agent9.Ensemble.blockChoices_nodup
#print axioms P196.Agent9.Ensemble.blockChoices_word_length
#print axioms P196.Agent9.Ensemble.mem_blockChoices
#print axioms P196.Agent9.Ensemble.pairAlphabet
#print axioms P196.Agent9.Ensemble.outerAlphabet
#print axioms P196.Agent9.Ensemble.mem_pairAlphabet
#print axioms P196.Agent9.Ensemble.mem_outerAlphabet
#print axioms P196.Agent9.Ensemble.pairAlphabet_nodup
#print axioms P196.Agent9.Ensemble.outerAlphabet_nodup
#print axioms P196.Agent9.Ensemble.length_pairAlphabet
#print axioms P196.Agent9.Ensemble.length_outerAlphabet
#print axioms P196.Agent9.Ensemble.goodBlocks
#print axioms P196.Agent9.Ensemble.nines_mem_wordChoices
#print axioms P196.Agent9.Ensemble.mem_goodBlocks
#print axioms P196.Agent9.Ensemble.goodBlocks_nodup
#print axioms P196.Agent9.Ensemble.goodBlocks_word_length
#print axioms P196.Agent9.Ensemble.length_goodBlocks
#print axioms P196.Agent9.Ensemble.wrapPairs
#print axioms P196.Agent9.Ensemble.length_wrapPairs
#print axioms P196.Agent9.Ensemble.wrapPairs_append
#print axioms P196.Agent9.Ensemble.wrapPairs_injective
#print axioms P196.Agent9.Ensemble.digitsBounded_wrapPairs
#print axioms P196.Agent9.Ensemble.wrapPairs_low
#print axioms P196.Agent9.Ensemble.wrapPairs_high
#print axioms P196.Agent9.Ensemble.exists_wrapPairs
#print axioms P196.Agent9.Ensemble.wrappedPairsProduct
#print axioms P196.Agent9.Ensemble.wrappedPairsProduct_nodup
#print axioms P196.Agent9.Ensemble.length_wrappedPairsProduct
#print axioms P196.Agent9.Ensemble.unmarkedPairs
#print axioms P196.Agent9.Ensemble.unmarkedPairs_nodup
#print axioms P196.Agent9.Ensemble.unmarkedPairs_word_length
#print axioms P196.Agent9.Ensemble.unmarkedPairs_bounded
#print axioms P196.Agent9.Ensemble.length_unmarkedPairs
#print axioms P196.Agent9.Ensemble.mem_unmarkedPairs
#print axioms P196.Agent9.Ensemble.frameChoices
#print axioms P196.Agent9.Ensemble.mem_frameChoices
#print axioms P196.Agent9.Ensemble.frameChoices_nodup
#print axioms P196.Agent9.Ensemble.frameChoices_word_length
#print axioms P196.Agent9.Ensemble.length_frameChoices
#print axioms P196.Agent9.Ensemble.markerWords
#print axioms P196.Agent9.Ensemble.markerWords_nodup
#print axioms P196.Agent9.Ensemble.length_markerWords
#print axioms P196.Agent9.Ensemble.mem_markerWords_repr
#print axioms P196.Agent9.Ensemble.markerWords_word_length
#print axioms P196.Agent9.Ensemble.markerWords_canonical
#print axioms P196.Agent9.Ensemble.ninesChunk_iff
#print axioms P196.Agent9.Ensemble.WordMarker
#print axioms P196.Agent9.Ensemble.wrapPairs_wordMarker_iff
#print axioms P196.Agent9.Ensemble.mem_markerWords
#print axioms P196.Agent9.Ensemble.markerCount
#print axioms P196.Agent9.Ensemble.freePairs
#print axioms P196.Agent9.Ensemble.markerCount_mul_le
#print axioms P196.Agent9.Ensemble.pairs_decomposition
#print axioms P196.Agent9.Ensemble.width_decomposition
#print axioms P196.Agent9.Ensemble.selected_digits_le
#print axioms P196.Agent9.Ensemble.free_exponent
#print axioms P196.Agent9.Ensemble.selected_block_bound
#print axioms P196.Agent9.Ensemble.selected_position_geometry
#print axioms P196.Agent9.Ensemble.oneDigitWords
#print axioms P196.Agent9.Ensemble.mem_oneDigitWords
#print axioms P196.Agent9.Ensemble.oneDigitWords_nodup
#print axioms P196.Agent9.Ensemble.length_oneDigitWords
#print axioms P196.Agent9.Ensemble.unmarkedDigits
#print axioms P196.Agent9.Ensemble.mem_unmarkedDigits
#print axioms P196.Agent9.Ensemble.unmarkedDigits_nodup
#print axioms P196.Agent9.Ensemble.length_unmarkedDigits
#print axioms P196.Agent9.Ensemble.numericDigit
#print axioms P196.Agent9.Ensemble.numericDigit_value
#print axioms P196.Agent9.Ensemble.canonical_numericDigit
#print axioms P196.Agent9.Ensemble.NumericMarker
#print axioms P196.Agent9.Ensemble.numericMarker_natValue_iff
#print axioms P196.Agent9.Ensemble.unmarkedSeeds
#print axioms P196.Agent9.Ensemble.unmarkedSeeds_nodup
#print axioms P196.Agent9.Ensemble.mem_unmarkedSeeds
#print axioms P196.Agent9.Ensemble.length_unmarkedSeeds
#print axioms P196.Agent9.Ensemble.numericMarker_iff_mirroredNines
#print axioms P196.Agent9.Ensemble.widthSeeds
#print axioms P196.Agent9.Ensemble.mem_widthSeeds
#print axioms P196.Agent9.Ensemble.widthSeeds_nodup
#print axioms P196.Agent9.Ensemble.length_widthSeeds
#print axioms P196.Agent9.Ensemble.positiveHitB
#print axioms P196.Agent9.Ensemble.positiveHitB_iff
#print axioms P196.Agent9.Ensemble.positiveHits
#print axioms P196.Agent9.Ensemble.mem_positiveHits
#print axioms P196.Agent9.Ensemble.positiveHits_nodup
#print axioms P196.Agent9.Ensemble.nodup_length_le_of_subset
#print axioms P196.Agent9.Ensemble.positiveHits_subset_unmarkedSeeds
#print axioms P196.Agent9.Ensemble.positiveHits_count_le

run_cmd do
  let env ← getEnv
  let selected : List String := [
    "LychrelDigitSums",
    "Lychrel196Research",
    "SafeDelay",
    "DecimalSafeRuns",
    "DecimalDelayBridge",
    "OverflowSafeRuns",
    "FiniteHorizonBlocks",
    "Agent101DigitPairs",
    "Agent101MultiplicityBounds",
    "Agent101SplitEnumeration",
    "Agent101NumericFibers",
    "Agent9FiniteProducts",
    "Agent9MarkerWords",
    "Agent9MarkerEnumeration",
    "Agent9NumericMarkerCount",
    "Agent9FiniteHorizonCount"]
  let permittedEmpty : List String := ["Lychrel196Research"]
  let imported := env.allImportedModuleNames.toList.map Name.toString
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut visited : List String := []
  let mut theoremCount := 0
  let mut definitionCount := 0
  let mut union : List Name := []
  for origin in selected do
    if !(imported.contains origin) then
      throwError m!"MISSING_COMPILED_IMPORT {origin}"
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let origin := env.allImportedModuleNames[idx.toNat]!
      if selected.contains origin.toString then
        if !(visited.contains origin.toString) then
          visited := origin.toString :: visited
        match info with
        | .axiomInfo value =>
          if value.isUnsafe then
            logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {origin} {name}"
          else
            throwError m!"CUSTOM_AXIOM {origin} {name}"
        | .thmInfo _ =>
          theoremCount := theoremCount + 1
          let dependencies ← liftCoreM (Lean.collectAxioms name)
          let axl := dependencies.toList
          for axiomName in axl do
            if !(allowed.contains axiomName) then
              throwError m!"DISALLOWED_AXIOM {origin} {name} {axiomName}"
            if !(union.contains axiomName) then
              union := axiomName :: union
          logInfo m!"AUDIT_THEOREM {origin} {name} : {axl}"
        | .defnInfo _ | .opaqueInfo _ =>
          if info.isUnsafe then
            logInfo m!"UNSAFE_IMPLEMENTATION_DEFINITION {origin} {name}"
          else
            definitionCount := definitionCount + 1
            let dependencies ← liftCoreM (Lean.collectAxioms name)
            let axl := dependencies.toList
            for axiomName in axl do
              if !(allowed.contains axiomName) then
                throwError m!"DISALLOWED_DEFINITION_AXIOM {origin} {name} {axiomName}"
              if !(union.contains axiomName) then
                union := axiomName :: union
            logInfo m!"AUDIT_DEFINITION {origin} {name} : {axl}"
        | _ => pure ()
  for origin in selected do
    if !(visited.contains origin) then
      if permittedEmpty.contains origin then
        logInfo m!"AUDIT_EMPTY_IMPORT {origin}"
      else
        throwError m!"MISSING_MODULE_ORIGIN {origin}"
  logInfo m!"FULL_MODULE_AUDIT theorems={theoremCount} union={union}"
  logInfo m!"FULL_DEFINITION_AUDIT definitions={definitionCount}"
  logInfo m!"AUDITED_MODULE_ORIGINS {visited}"
