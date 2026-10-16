import Agent108WindowEndpoints
import Lean

open Lean Elab Command

private def constantKind : ConstantInfo → String
  | .axiomInfo _ => "axiom"
  | .defnInfo _ => "definition"
  | .thmInfo _ => "theorem"
  | .opaqueInfo _ => "opaque"
  | .quotInfo _ => "quotient"
  | .inductInfo _ => "inductive"
  | .ctorInfo _ => "constructor"
  | .recInfo _ => "recursor"

elab "classify_window_core" : command => do
  let env ← getEnv
  for (name, info) in env.constants.toList do
    if name.toString.startsWith "Agent108.WindowWeights." ||
       name.toString.startsWith "List.mapTR.loop._at.Agent108.WindowWeights.choices." then
      logInfo m!"METADATA|{name}|{constantKind info}|{info.isUnsafe}|{info.isPartial}"

classify_window_core
