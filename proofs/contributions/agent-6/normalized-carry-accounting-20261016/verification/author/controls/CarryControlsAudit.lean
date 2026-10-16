import CarryControls
import Lean

open Lean Elab Command

set_option maxRecDepth 100000
set_option maxHeartbeats 0

run_cmd do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut theoremCount := 0
  let mut definitionCount := 0
  let mut unsafeImplementationCount := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if mod.toString == "CarryControls" then
        match info with
        | .axiomInfo v =>
          if v.isUnsafe then
            unsafeImplementationCount := unsafeImplementationCount + 1
            logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {mod} {name}"
          else throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ | .defnInfo _ =>
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          if info.isUnsafe then
            unsafeImplementationCount := unsafeImplementationCount + 1
            logInfo m!"UNSAFE_IMPLEMENTATION_DEFINITION {mod} {name} : {axl}"
          else
            match info with
            | .thmInfo _ => theoremCount := theoremCount + 1
            | _ => definitionCount := definitionCount + 1
            for ax in axl do
              if !(union.contains ax) then union := ax :: union
            if axl.any (fun ax => !(allowed.contains ax)) then
              throwError m!"DISALLOWED_AXIOMS {mod} {name} : {axl}"
            logInfo m!"AUDIT_DECLARATION {mod} {name} : {axl}"
        | _ => pure ()
  logInfo m!"FULL_MODULE_AUDIT theorems={theoremCount} safeDefinitions={definitionCount} unsafeImplementations={unsafeImplementationCount} union={union}"
