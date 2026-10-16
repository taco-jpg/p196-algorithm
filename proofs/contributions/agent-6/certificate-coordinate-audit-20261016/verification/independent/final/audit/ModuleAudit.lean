import CertificateControls
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let selected : List String := ["TemplateStep", "ReturnCertificate", "OuterFinite", "OuterBounds", "OuterBridge", "CertificateRealization", "ExteriorNormalization", "CertificateExterior", "CertificateAccounting", "TARGET", "ExteriorFactorizationProof", "ExteriorObservationInjective", "ExteriorUpdateLaw", "CoordinateDynamics", "CoordinateThreshold", "CoordinateSign", "CoordinateCycle", "CertificateCoordinates", "CertificateFilter", "CertificateControls"]
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  for mod in selected do
    if !(env.allImportedModuleNames.toList.any (fun n => n.toString == mod)) then
      throwError m!"MISSING_PROJECT_MODULE {mod}"
    logInfo m!"AUDIT_MODULE_JSON {(Json.mkObj [("module", toJson mod)]).compress}"
  let mut count : Nat := 0
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
        let origin := [("module", toJson mod.toString), ("kind", toJson kind), ("name", toJson name.toString)]
        logInfo m!"AUDIT_CONSTANT_JSON {(Json.mkObj origin).compress}"
        match info with
        | .axiomInfo v =>
          if v.isUnsafe then
            logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM_JSON {(Json.mkObj origin).compress}"
          else throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          count := count + 1
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then throwError m!"DISALLOWED_AXIOMS {mod} {name} : {axl}"
          let record := origin ++ [("axioms", toJson (axl.map Name.toString))]
          logInfo m!"AUDIT_THEOREM_JSON {(Json.mkObj record).compress}"
          elabCommand (← `(command| #print axioms $(mkIdent name)))
        | .defnInfo _ =>
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          let record := origin ++ [("axioms", toJson (axl.map Name.toString))]
          if info.isUnsafe then
            logInfo m!"UNSAFE_IMPLEMENTATION_DEFINITION_JSON {(Json.mkObj record).compress}"
          else
            if axl.any (fun ax => !(allowed.contains ax)) then throwError m!"DISALLOWED_DEFINITION_AXIOMS {mod} {name} : {axl}"
            logInfo m!"AUDIT_SAFE_DEFINITION_JSON {(Json.mkObj record).compress}"
            elabCommand (← `(command| #print axioms $(mkIdent name)))
        | .opaqueInfo _ =>
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          if info.isUnsafe then throwError m!"UNEXPECTED_UNSAFE_OPAQUE {mod} {name}"
          if axl.any (fun ax => !(allowed.contains ax)) then throwError m!"DISALLOWED_OPAQUE_AXIOMS {mod} {name} : {axl}"
          let record := origin ++ [("axioms", toJson (axl.map Name.toString))]
          logInfo m!"AUDIT_SAFE_OPAQUE_JSON {(Json.mkObj record).compress}"
          elabCommand (← `(command| #print axioms $(mkIdent name)))
        | _ => pure ()
  logInfo m!"FULL_MODULE_AUDIT_JSON {(Json.mkObj [("theorem_count", toJson count), ("axiom_union", toJson (union.map Name.toString))]).compress}"
