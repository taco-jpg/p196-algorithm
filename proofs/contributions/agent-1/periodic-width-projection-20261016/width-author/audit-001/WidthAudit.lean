import Agent1PeriodicWidth
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#check @Agent1.Periodic.widthResidue
#print axioms Agent1.Periodic.widthResidue
#check @Agent1.Periodic.widthResidue_lt
#print axioms Agent1.Periodic.widthResidue_lt
#check @Agent1.Periodic.periodicWord_length_mod_eight
#print axioms Agent1.Periodic.periodicWord_length_mod_eight
#check @Agent1.Periodic.quotient_width_mod_eight
#print axioms Agent1.Periodic.quotient_width_mod_eight
#check @Agent1.Periodic.quotient_widthResidue
#print axioms Agent1.Periodic.quotient_widthResidue
run_cmd do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut theoremCount := 0
  let mut definitionCount := 0
  let mut opaqueCount := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if mod.toString == "Agent1PeriodicWidth" then
        match info with
        | .axiomInfo v =>
          if v.isUnsafe then logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {name}"
          else throwError m!"CUSTOM_AXIOM {name}"
        | .defnInfo v =>
          if v.safety != .safe then logInfo m!"NON_SAFE_DEFINITION {name} {repr v.safety}"
        | .opaqueInfo v =>
          if v.isUnsafe then logInfo m!"UNSAFE_OPAQUE {name}"
        | _ => pure ()
        let kind : Option String := match info with
          | .thmInfo _ => some "THEOREM"
          | .defnInfo v => if v.safety == .safe then some "SAFE_DEFINITION" else none
          | .opaqueInfo v => if !v.isUnsafe then some "SAFE_OPAQUE" else none
          | _ => none
        if let some kind := kind then
          if kind == "THEOREM" then theoremCount := theoremCount + 1
          else if kind == "SAFE_DEFINITION" then definitionCount := definitionCount + 1
          else opaqueCount := opaqueCount + 1
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then throwError m!"DISALLOWED_AXIOMS {name} : {axl}"
          logInfo m!"AUDIT_{kind} {name} : {axl}"
  logInfo m!"MODULE_AUDIT theorems={theoremCount} definitions={definitionCount} opaque={opaqueCount} union={union}"
