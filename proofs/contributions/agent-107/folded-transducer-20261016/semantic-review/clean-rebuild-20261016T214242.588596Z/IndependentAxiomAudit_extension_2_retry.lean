import Lean
import Agent107TransducerDefs
import Agent107TransducerPath
import Agent107TransducerInput
import Agent107TransducerBoundary
import Agent107TransducerTablesData
import Agent107TransducerTablesChecks
import Agent107TransducerTables
import Agent107TransducerOutput
import Agent107TransducerNumeric
import Agent107TransducerReachable

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let mut count := 0
  for (name, info) in env.constants do
    let sourceModule : Lean.Name := match env.getModuleIdxFor? name with
      | none => Name.anonymous
      | some idx => env.allImportedModuleNames[idx.toNat]!
    if "Agent107Transducer".isPrefixOf (toString sourceModule) then
      if let .thmInfo _ := info then
        count := count + 1
        logInfo m!"DECLARATION_ORIGIN {sourceModule}: {name}"
        elabCommand (← `(command| #print axioms $(mkIdent name)))
        let axioms ← collectAxioms name
        for ax in axioms do
          unless #[``propext, ``Classical.choice, ``Quot.sound].contains ax do
            throwError "Unapproved axiom: {name} uses {ax}"
  logInfo m!"Audited {count} Agent107Transducer module-origin theorem declarations, including private and generated proof lemmas."
