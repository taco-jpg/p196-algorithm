import Lean
import SharpHistoryTheorem
set_option pp.privateNames true
set_option maxRecDepth 100000
set_option maxHeartbeats 0
open Lean Elab Command
run_cmd do
  let env ← getEnv
  let owners : List String := ["FamilyDefinitions", "FamilyCardinality", "FiniteHorizonOverflow", "SafetyBridge", "NormalizedSafety", "FiniteHorizonTheorem", "HistoryInterfaces", "TwoLayerCertificate", "ActualHistories", "IntegerInterfaces", "HistoryFamily", "HistorySafety", "TwoHistoryTheorem", "DeadPrefix", "ActualDepth", "SharpHistoryFamily", "SharpHistoryTheorem"]
  for (name, info) in env.constants.toList do
    if let some index := env.getModuleIdxFor? name then
      let owner := env.header.moduleNames[index]!
      if owners.contains owner.toString then
        let user := (privateToUserName? name).getD name
        let isPrivate := (privateToUserName? name).isSome
        liftIO <| IO.println s!"INDEPENDENT_DECL {owner} {name} {user} {isPrivate} {info.isUnsafe} {info.isPartial}"
        unless info.isUnsafe || info.isPartial do
          elabCommand (← `(command| #print axioms $(mkIdent name)))
