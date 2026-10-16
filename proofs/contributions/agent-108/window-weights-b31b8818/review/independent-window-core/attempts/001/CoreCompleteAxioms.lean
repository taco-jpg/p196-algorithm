import Agent108WindowEndpoints
import Lean

open Lean Elab Command

elab "audit_window_core" : command => do
  let env ← getEnv
  for (name, info) in env.constants.toList do
    if name.toString.startsWith "Agent108.WindowWeights." then
      logInfo m!"DECLARATION {name} : {info.type}"
      elabCommand (← `(command| #print axioms $(mkIdent name)))

audit_window_core
