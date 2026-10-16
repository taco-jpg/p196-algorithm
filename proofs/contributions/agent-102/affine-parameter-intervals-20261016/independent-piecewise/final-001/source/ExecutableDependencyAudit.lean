import ReviewerControls
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let selected : List String := ["Agent102RunDefs", "Agent102ParameterIntervalDefs", "Agent102AffineInequalityIntervals", "Agent102ParameterIntervalAlgebra", "Agent102ParameterIntervalCompact", "Agent102AffineArithmetic", "Agent102PiecewiseCounts", "ReviewerControls"]
  let forbidden : List Name := [``List.range, ``List.replicate,
    ``Agent102.word, ``Agent102.wordAt, ``Agent102.ParameterSets.CountExpr.value]
  for root in [``Agent102.ParameterSets.CountExpr.pieces,
      ``Agent102.ParameterSets.comparisonRegion, ``Agent102.ParameterSets.ltRegion,
      ``Agent102.ParameterSets.leRegion, ``Agent102.ParameterSets.eqRegion] do
    let mut pending : List Name := [root]
    let mut seen : List Name := []
    let mut count := 0
    while !pending.isEmpty do
      let name := pending.head!
      pending := pending.tail!
      if seen.contains name then continue
      seen := name :: seen
      if forbidden.contains name then throwError m!"FORBIDDEN_EXECUTABLE_DEP {root} {name}"
      if let some info := env.find? name then
        if let some idx := env.getModuleIdxFor? name then
          let mod := env.allImportedModuleNames[idx.toNat]!
          if selected.contains mod.toString then
            count := count + 1
            logInfo m!"EXECUTABLE_PROJECT_DEP {root} {mod} {name}"
            for dep in info.type.getUsedConstants do pending := dep :: pending
            if let some value := info.value? true then
              for dep in value.getUsedConstants do pending := dep :: pending
    logInfo m!"EXECUTABLE_DEPENDENCY_CHECK {root} project_constants={count} forbidden=0"
