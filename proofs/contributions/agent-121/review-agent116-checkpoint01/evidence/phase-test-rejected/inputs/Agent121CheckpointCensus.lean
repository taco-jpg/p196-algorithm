import Lean
import Agent121CertificateContracts

/-!
Agent #121: select theorem constants by their defining source module, rather
than by printed namespaces. This includes private and generated declarations.
-/
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let selected : List String := ["TemplateStep", "ReturnCertificate", "OuterFinite",
    "OuterBounds", "OuterBridge", "ExteriorNormalization", "CertificateRealization",
    "Agent121CertificateContracts"]
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        match info with
        | .thmInfo _ => logInfo m!"AGENT121_THEOREM {name}"
        | .axiomInfo _ => throwError m!"Unexpected project axiom: {name}"
        | _ => pure ()
