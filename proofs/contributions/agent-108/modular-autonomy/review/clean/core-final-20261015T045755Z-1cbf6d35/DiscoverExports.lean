import AutonomyDefs
import AutonomyBasic
import DigitPerturbation
import LeadingWitness
import Necessity
import ModularAutonomy
import Lean

open Lean Elab Command

run_cmd do
  let wanted : Array Name := #[`Lychrel196Research, `AutonomyDefs, `AutonomyBasic, `DigitPerturbation, `LeadingWitness, `Necessity, `ModularAutonomy]
  let env ← getEnv
  for (name, info) in env.constants do
    if let some idx := env.getModuleIdxFor? name then
      let moduleName := env.header.moduleNames[idx.toNat]!
      if wanted.contains moduleName then
        match info with
        | .axiomInfo _ =>
          throwError "Unexpected locally declared axiom: {name}"
        | .thmInfo _ =>
          let visibility := if isPrivateName name then "private" else "exported"
          liftIO <| IO.println s!"THEOREM|{moduleName}|{name}|{visibility}"
          let axioms ← collectAxioms name
          let allowed : Array Name := #[`propext, `Classical.choice, `Quot.sound]
          for ax in axioms do
            unless allowed.contains ax do
              throwError "Forbidden axiom {ax} in {name}"
          liftIO <| IO.println s!"AXIOMS|{name}|{axioms}"
        | _ => pure ()
