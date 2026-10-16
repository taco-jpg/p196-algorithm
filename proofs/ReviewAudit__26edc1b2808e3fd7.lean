import CertificateExterior
import CanonicalityCounterexample
import Lean
open Lean Elab Command
set_option maxHeartbeats 0
set_option maxRecDepth 100000
run_cmd do
  let env ← getEnv
  let localModules : List String := ["TemplateStep", "ReturnCertificate", "OuterFinite", "OuterBounds", "OuterBridge", "CertificateRealization", "ExteriorNormalization", "CertificateExterior", "CanonicalityCounterexample"]
  for (name, info) in env.constants.toList do
    if let some index := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[index.toNat]!
      if localModules.contains mod.toString then
        match info with
        | .thmInfo _ =>
          logInfo m!"REVIEW_DECL {name}"
          elabCommand (← `(command| #print axioms $(mkIdent name)))
        | .axiomInfo v =>
          if !v.isUnsafe then throwError m!"Custom axiom: {name}"
        | _ => pure ()
