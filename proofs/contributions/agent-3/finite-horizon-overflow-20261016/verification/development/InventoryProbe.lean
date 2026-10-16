import Lean
import NormalizedSafety

open Lean Elab Command

run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if name.toString.startsWith "P196.Agent3.OverflowHorizon." then
      liftIO <| IO.println s!"P196_AUDIT_DECL {name}"
