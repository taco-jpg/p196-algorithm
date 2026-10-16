import Agent116All
import CanonicalityCounterexample
import Lean
open Lean Elab Command
set_option maxHeartbeats 0
set_option maxRecDepth 100000
run_cmd do
  let env ← getEnv
  let localModules : List String := ["TemplateStep", "ReturnCertificate", "OuterFinite", "OuterBounds", "OuterBridge", "CertificateRealization", "ExteriorNormalization", "CertificateExterior", "CertificateUnrestricted", "Cap3Base", "Cap3AllBase", "Cap3AllBatch000", "Cap3AllBatch001", "Cap3AllBatch002", "Cap3AllBatch003", "Cap3AllBatch004", "Cap3AllBatch005", "Cap3AllBatch006", "Cap3AllBatch007", "Cap3AllBatch008", "Cap3AllBatch009", "Cap3AllBatch010", "Cap3AllBatch011", "Cap3AllBatch012", "Cap3AllBatch013", "Cap3AllBatch014", "Cap3AllBatch015", "Cap3AllBatch016", "Cap3AllBatch017", "Cap3AllBatch018", "Cap3AllBatch019", "Cap3AllBatch020", "Cap3AllBatch021", "Cap3AllBatch022", "Cap3AllBatch023", "Cap3AllBatch024", "Cap3AllBatch025", "Cap3AllBatch026", "Cap3AllBatch027", "Cap3AllBatch028", "Cap3AllBatch029", "Cap3AllBatch030", "Cap3AllBatch031", "Cap3AllBatch032", "Cap3AllBatch033", "Cap3AllBatch034", "Cap3AllBatch035", "Cap3AllBatch036", "Cap3AllBatch037", "Cap3AllBatch038", "Cap3AllBatch039", "Cap3AllBatch040", "Cap3AllBatch041", "Cap3AllBatch042", "Cap3AllBatch043", "Cap3AllBatch044", "Cap3AllBatch045", "Cap3AllBatch046", "Cap3AllBatch047", "Cap3AllBatch048", "Cap3AllBatch049", "Cap3AllBatch050", "Cap3AllBatch051", "Cap3AllBatch052", "Cap3AllBatch053", "Cap3AllBatch054", "Cap3AllBatch055", "Cap3AllBatch056", "Cap3AllFinite", "Cap3Encoding", "Cap3Batch000", "Cap3Batch001", "Cap3Batch002", "Cap3Batch003", "Cap3Batch004", "Cap3Batch005", "Cap3Batch006", "Cap3Batch007", "Cap3Batch008", "Cap3Batch009", "Cap3Batch010", "Cap3Batch011", "Cap3Batch012", "Cap3Batch013", "Cap3Batch014", "Cap3Batch015", "Cap3Batch016", "Cap3Batch017", "Cap3Batch018", "Cap3Batch019", "Cap3Batch020", "Cap3Batch021", "Cap3Batch022", "Cap3Batch023", "Cap3Batch024", "Cap3Batch025", "Cap3Batch026", "Cap3Batch027", "Cap3Batch028", "Cap3Batch029", "Cap3Batch030", "Cap3Batch031", "Cap3Batch032", "Cap3Batch033", "Cap3Batch034", "Cap3Batch035", "Cap3Batch036", "Cap3Batch037", "Cap3Batch038", "Cap3Batch039", "Cap3Batch040", "Cap3Batch041", "Cap3Batch042", "Cap3Batch043", "Cap3Batch044", "Cap3Batch045", "Cap3Batch046", "Cap3Batch047", "Cap3Batch048", "Cap3Batch049", "Cap3Batch050", "Cap3Batch051", "Cap3Batch052", "Cap3Batch053", "Cap3Batch054", "Cap3Batch055", "Cap3Batch056", "Cap3Finite", "Cap3Bounds", "Cap3AllBounds", "CertificateCap3", "LychrelDigitSums", "PeriodObstructions", "Compat", "ActualCap3", "Agent116All", "CanonicalityCounterexample"]
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
