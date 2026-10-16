import Agent101WidthFiberBounds
import Lean

open Lean Elab Command
run_cmd do
  let env ← getEnv
  let selected := ["Agent101ProfileExtraction", "Agent101WidthFiberBounds"]
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        if info.isUnsafe then
          throwError m!"UNEXPECTED_UNSAFE {mod} {name}"
        else
          match info with
          | .axiomInfo _ => throwError m!"CUSTOM_AXIOM {mod} {name}"
          | .thmInfo _ =>
            logInfo m!"MODULE_THEOREM {mod} {name}"
            elabCommand (← `(command| #print axioms $(mkIdent name)))
          | .defnInfo _ =>
            logInfo m!"MODULE_DEFINITION {mod} {name}"
            elabCommand (← `(command| #print axioms $(mkIdent name)))
          | .opaqueInfo _ =>
            logInfo m!"MODULE_OPAQUE {mod} {name}"
            elabCommand (← `(command| #print axioms $(mkIdent name)))
          | _ => pure ()
