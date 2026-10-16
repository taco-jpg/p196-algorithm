import Lean
open Lean in
run_elab do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    let s := name.toString
    if (s.startsWith "Nat." && (s.contains "gcd" || s.contains "mod") && (s.contains "mul" || s.contains "pow" || s.contains "cancel")) || (s.startsWith "Fin." && (s.contains "inject" || s.contains "surject")) then
      logInfo m!"{name}"
