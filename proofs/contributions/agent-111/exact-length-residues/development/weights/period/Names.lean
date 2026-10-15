import Lean
open Lean in
run_elab do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    let s := name.toString
    if s.startsWith "Nat." || s.startsWith "Fin." || s.startsWith "List." then
      logInfo m!"{name}"
