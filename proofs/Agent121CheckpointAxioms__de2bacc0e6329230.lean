import Lean
import Agent121CertificateContracts

/-!
Agent #121: execute actual #print axioms commands with exact Lean Names.
mkIdent preserves numeric components in private declaration names, which
cannot safely be round-tripped through a naive string-to-source conversion.
The command-construction technique was also inspected in Agent #116's
checkpoint-01/AllExportedAxioms.lean. This file runs in our fresh build.
-/
set_option maxRecDepth 100000
set_option maxHeartbeats 0
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
        | .thmInfo _ =>
          logInfo m!"AGENT121_AUDIT {name}"
          elabCommand (← `(command| #print axioms $(mkIdent name)))
        | .axiomInfo v =>
          if v.isUnsafe then
            logInfo m!"AGENT121_UNSAFE_IMPL {name}"
          else
            throwError m!"Unexpected safe project axiom: {name}"
        | _ => pure ()
