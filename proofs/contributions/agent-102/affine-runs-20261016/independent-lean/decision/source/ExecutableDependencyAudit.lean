import Agent102AffineDecision
import Lean

open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0

run_cmd do
  let env ← getEnv
  let selected : List String := ["Agent102RunDefs", "Agent102AffineArithmetic",
    "Agent102RunEndpoints", "Agent102RunWord", "Agent102AffineRuns", "Agent102AffineDecision"]
  let forbidden : List Name := [``Agent102.word, ``Agent102.wordAt, ``Agent102.runsAt,
    ``Agent102.spansFrom, ``Agent102.spans, ``Agent102.Affine.eval,
    ``Agent102.Affine.cutoff, ``Agent102.Affine.compareCutoff, ``Agent102.lengthCutoff,
    ``Agent102.pairCutoff, ``Agent102.equalityCutoff, ``Agent102.palindromeCutoff,
    ``Agent102.equalOnTail, ``Agent102.palindromicOnTail, ``Agent102.AffineSpan.at,
    ``List.replicate]
  for root in [``Agent102.fastEqualOnTail, ``Agent102.fastPalindromicOnTail] do
    let mut pending : List Name := [root]
    let mut seen : List Name := []
    let mut projectCount := 0
    while !pending.isEmpty do
      let name := pending.head!
      pending := pending.tail!
      if seen.contains name then continue
      seen := name :: seen
      if forbidden.contains name then
        throwError m!"FORBIDDEN_EXECUTABLE_DEP {root} {name}"
      if let some info := env.find? name then
        if let some idx := env.getModuleIdxFor? name then
          let mod := env.allImportedModuleNames[idx.toNat]!
          if selected.contains mod.toString then
            projectCount := projectCount + 1
            logInfo m!"EXECUTABLE_PROJECT_DEP {root} {mod} {name}"
            for dep in info.type.getUsedConstants do
              pending := dep :: pending
            if let some value := info.value? true then
              for dep in value.getUsedConstants do
                pending := dep :: pending
    logInfo m!"EXECUTABLE_DEPENDENCY_CHECK {root} project_constants={projectCount} forbidden=0"
