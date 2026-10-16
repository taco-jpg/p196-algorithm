import Lean
import Agent107TransducerBoundary

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let mut count := 0
  for (name, info) in env.constants do
    let origin : Name := match env.getModuleIdxFor? name with
      | none => Name.anonymous
      | some idx => env.allImportedModuleNames[idx.toNat]!
    if origin == `Agent107TransducerBoundary then
      if let .axiomInfo _ := info then
        throwError "Boundary introduces an axiom: {name}"
      if let .thmInfo _ := info then
        count := count + 1
        logInfo m!"BOUNDARY_MODULE_ORIGIN {name}"
        elabCommand (← `(command| #print axioms $(mkIdent name)))
        let axioms ← collectAxioms name
        for ax in axioms do
          unless #[``propext, ``Quot.sound, ``Classical.choice].contains ax do
            throwError "Disallowed transitive axiom: {name} uses {ax}"
  logInfo m!"BOUNDARY_MODULE_ORIGIN_COUNT {count}"
