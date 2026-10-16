import CoordinateCycle
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let selected : List String := ["OuterFinite", "TARGET", "ExteriorFactorizationProof", "ExteriorObservationInjective", "ExteriorUpdateLaw", "CoordinateThreshold", "CoordinateDynamics", "CoordinateSign", "CoordinateCycle"]
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  for mod in selected do
    if !(env.allImportedModuleNames.toList.any (fun n => n.toString == mod)) then
      throwError m!"MISSING_PROJECT_MODULE {mod}"
    logInfo m!"AUDIT_MODULE {mod}"
  let mut count := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        let kind := match info with
          | .axiomInfo _ => "axiom"
          | .thmInfo _ => "theorem"
          | .defnInfo _ => "definition"
          | .opaqueInfo _ => "opaque"
          | .quotInfo _ => "quotient"
          | .inductInfo _ => "inductive"
          | .ctorInfo _ => "constructor"
          | .recInfo _ => "recursor"
        logInfo m!"AUDIT_CONSTANT {mod} {kind} {name}"
        match info with
        | .axiomInfo v =>
          if v.isUnsafe then logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {mod} {name}"
          else throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          count := count + 1
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then throwError m!"DISALLOWED_AXIOMS {mod} {name} : {axl}"
          logInfo m!"AUDIT_THEOREM {mod} {name} : {axl}"
        | .defnInfo _ =>
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          if info.isUnsafe then
            logInfo m!"UNSAFE_IMPLEMENTATION_DEFINITION {mod} {name} : {axl}"
          else
            if axl.any (fun ax => !(allowed.contains ax)) then throwError m!"DISALLOWED_DEFINITION_AXIOMS {mod} {name} : {axl}"
            logInfo m!"AUDIT_SAFE_DEFINITION {mod} {name} : {axl}"
        | _ => pure ()
  logInfo m!"FULL_MODULE_AUDIT theorems={count} union={union}"
