import ScopeTests
import ExactTypesApplied
import ActualMapObligations
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  for mod in env.allImportedModuleNames do
    logInfo m!"AUDIT_IMPORT {mod}"
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if (["NoAlternatingReturn", "LychrelDigitSums", "ScopeTests", "ExactTypesApplied", "ActualMapObligations"] : List String).contains mod.toString then
        match info with
        | .axiomInfo v =>
          if v.isUnsafe then
            logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {mod} {name}"
          else
            throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          logInfo m!"AUDIT_THEOREM {mod} {name}"
          elabCommand (← `(command| #print axioms $(mkIdent name)))
        | _ => pure ()

run_cmd do
  let env ← getEnv
  let names : List Name := [`Agent104.TemporalStripObligations.ActualPrefixTransportObligation, `Agent104.TemporalStripObligations.UniformBandTailObligation]
  for name in names do
    let some info := env.find? name | throwError m!"MISSING_CONTRACT {name}"
    match info with
    | .defnInfo v =>
      logInfo m!"UNPROVED_PROP_CONTRACT {name}"
      logInfo m!"CONTRACT_TYPE {name} {v.type}"
    | _ => throwError m!"CONTRACT_IS_NOT_DEF {name}"
