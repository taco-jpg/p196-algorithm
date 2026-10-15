import Lean
import ExteriorFactorizationProof
import ExteriorObservationInjective
import ExteriorUpdateLaw

open Lean Elab Command in
#eval show CommandElabM Unit from do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut names : Array Name := #[]
  for (name, ci) in env.constants.toList do
    if (name.toString.splitOn "Agent115").length > 1 then
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
