import Lean
import Agent107TransducerBoundary

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let mut count := 0
  for (name, info) in env.constants do
    if "Agent107.FoldedTransducer.Boundary.".isPrefixOf name.toString then
      if let .thmInfo _ := info then
        count := count + 1
        elabCommand (← `(command| #print axioms $(mkIdent name)))
        let axioms ← collectAxioms name
        for ax in axioms do
          unless #[``propext, ``Classical.choice, ``Quot.sound].contains ax do
            throwError "Unapproved axiom: {name} uses {ax}"
  logInfo m!"Audited {count} boundary theorem declarations."
