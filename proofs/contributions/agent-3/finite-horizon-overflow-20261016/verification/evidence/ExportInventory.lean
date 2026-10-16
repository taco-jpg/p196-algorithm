import Lean
import FamilyDefinitions
import FamilyCardinality
import FiniteHorizonOverflow
import SafetyBridge
import NormalizedSafety
import FiniteHorizonTheorem

open Lean Elab Command
run_cmd do
  let env ← getEnv
  for (name, info) in env.constants.toList do
    if name.toString.startsWith "P196.Agent3.OverflowHorizon." then
      liftIO <| IO.println s!"P196_AUDIT_DECL {name} {info.isUnsafe} {info.isPartial}"
