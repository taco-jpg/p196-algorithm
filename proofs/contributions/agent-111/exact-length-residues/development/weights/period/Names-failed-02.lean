import Lean
open Lean in
run_elab do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    let s := name.toString
    if (s.startsWith "Nat." && (s.hasSubstring "gcd" || s.hasSubstring "mod") && (s.hasSubstring "mul" || s.hasSubstring "pow" || s.hasSubstring "cancel")) || (s.startsWith "Fin." && (s.hasSubstring "inject" || s.hasSubstring "surject")) then
      logInfo m!"{name}"
