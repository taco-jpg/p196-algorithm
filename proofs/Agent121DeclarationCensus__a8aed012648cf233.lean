import Lean
import Agent121ScopeRegression

/- Agent #121: operational environment census only; no proof oracle. -/
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, info) in env.constants.toList do
    match info with
    | .thmInfo _ =>
      let n := name.toString
      if n.startsWith "Agent109." || n.startsWith "Agent121.Review." then
        logInfo m!"AGENT121_THEOREM {n}"
    | _ => pure ()
