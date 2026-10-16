import Control
import Lean
open Lean Elab Command
run_cmd do
  let env ← getEnv
  let modNames := env.header.moduleNames
  for (n, ci) in env.constants.map₁.toList do
    match env.getModuleIdxFor? n with
    | some idx =>
      if modNames[idx.toNat]! == `Control then
        let kind := match ci with
          | .axiomInfo _ => "axiom" | .defnInfo d => s!"def({repr d.safety})" | .thmInfo _ => "thm"
          | .opaqueInfo _ => "opaque" | .inductInfo _ => "induct" | _ => "other"
        logInfo m!"CTRL {n} kind={kind} unsafe={ci.isUnsafe}"
    | none => pure ()
-- does a safe decl referencing an unsafe aux constant get rejected by the kernel?
run_cmd do
  let env ← getEnv
  let n := `List.mapTR.loop._at.Ctl.roots._spec_1
  match env.find? n with
  | some ci => logInfo m!"type of aux axiom: {ci.type} isUnsafe={ci.isUnsafe}"
  | none => logInfo "not found"
