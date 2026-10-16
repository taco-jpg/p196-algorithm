import Lean
import TwoDigitMain

/-!
Exhaustive axiom audit (not part of the proof chain). Enumerates every
theorem constant whose name starts with `Agent113`, collects its transitive
axioms exactly as `#print axioms` does, prints one line per theorem, and
fails if any axiom outside `propext`, `Classical.choice`, `Quot.sound`
occurs (in particular `sorryAx` or `Lean.ofReduceBool`).
-/

open Lean Elab Command in
#eval show CommandElabM Unit from do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut names : Array Name := #[]
  for (name, ci) in env.constants.toList do
    if (`Agent113).isPrefixOf name then
      match ci with
      | .thmInfo _ => names := names.push name
      | _ => pure ()
  let sorted := names.qsort (fun a b => a.toString < b.toString)
  let mut bad : Array Name := #[]
  let mut union : List Name := []
  for name in sorted do
    let axs ← liftCoreM (Lean.collectAxioms name)
    let axl := axs.toList
    for ax in axl do
      if !(union.contains ax) then union := ax :: union
    if axl.any (fun ax => !(allowed.contains ax)) then bad := bad.push name
    logInfo m!"AUDIT {name} : {axl}"
  logInfo m!"AUDIT-SUMMARY theorems={sorted.size} bad={bad.size} union={union}"
  if bad.size > 0 then
    throwError m!"AUDIT-FAIL disallowed axioms in {bad}"
