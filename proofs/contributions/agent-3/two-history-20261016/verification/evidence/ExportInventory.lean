import Lean
import FamilyDefinitions
import FamilyCardinality
import FiniteHorizonOverflow
import SafetyBridge
import NormalizedSafety
import FiniteHorizonTheorem
import HistoryInterfaces
import TwoLayerCertificate
import IntegerInterfaces
import ActualHistories
import HistoryFamily
import HistorySafety
import TwoHistoryTheorem

open Lean Elab Command
run_cmd do
  let env ← getEnv
  let auditedModules : List String := ["FamilyDefinitions", "FamilyCardinality", "FiniteHorizonOverflow", "SafetyBridge", "NormalizedSafety", "FiniteHorizonTheorem", "HistoryInterfaces", "TwoLayerCertificate", "IntegerInterfaces", "ActualHistories", "HistoryFamily", "HistorySafety", "TwoHistoryTheorem"]
  for (name, info) in env.constants.toList do
    if let some index := env.getModuleIdxFor? name then
      let owner := env.header.moduleNames[index]!
      if auditedModules.contains owner.toString then
        let user := (privateToUserName? name).getD name
        let isPrivate := (privateToUserName? name).isSome
        liftIO <| IO.println s!"P196_AUDIT_DECL {owner} {name} {user} {isPrivate} {info.isUnsafe} {info.isPartial}"
