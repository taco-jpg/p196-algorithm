import Lean
import Agent107TransducerDefs
import Agent107TransducerPath
import Agent107TransducerInput
import Agent107TransducerBoundary
import Agent107TransducerTablesData
import Agent107TransducerTablesChecks
import Agent107TransducerTables

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let mut count := 0
  for (name, info) in env.constants do
    if "Agent107.".isPrefixOf name.toString then
      if let .thmInfo _ := info then
        count := count + 1
        elabCommand (← `(command| #print axioms $(mkIdent name)))
        let axioms ← collectAxioms name
        for ax in axioms do
          unless #[``propext, ``Classical.choice, ``Quot.sound].contains ax do
            throwError "Unapproved axiom: {name} uses {ax}"
  logInfo m!"Audited {count} Agent107 theorem declarations, including generated proof lemmas."
