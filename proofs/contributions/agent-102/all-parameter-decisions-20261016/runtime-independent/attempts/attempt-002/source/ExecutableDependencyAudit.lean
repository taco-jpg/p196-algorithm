import Agent102AllParameterControls
import Lean

open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0

run_cmd do
  let env ← getEnv
  let selected : List String := ["Agent102RunDefs", "Agent102AffineArithmetic", "Agent102RunWord", "Agent102RunEndpoints", "Agent102AffineRuns", "Agent102AffineDecision", "Agent102AffineBoundary", "Agent102RunDecision", "Agent102AffineAllParameters", "Agent102AllParameterControls"]
  let forbidden : List Name := [``Agent102.word, ``Agent102.wordAt,
    ``Agent102.equalOnTail, ``Agent102.palindromicOnTail, ``List.replicate]
  let builtinNames : List Name := [``List.range, ``List.all, ``List.any]
  let roots : List Name := [``Agent102.compressedEqual, ``Agent102.equalAt,
    ``Agent102.allEqual, ``Agent102.someEqual, ``Agent102.allUnequal, ``Agent102.someUnequal,
    ``Agent102.allPalindromic, ``Agent102.somePalindromic,
    ``Agent102.allNonpalindromic, ``Agent102.someNonpalindromic]
  for root in roots do
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
      if builtinNames.contains name then
        logInfo m!"BUILTIN_EXECUTABLE_DEP {root} {name}"
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
