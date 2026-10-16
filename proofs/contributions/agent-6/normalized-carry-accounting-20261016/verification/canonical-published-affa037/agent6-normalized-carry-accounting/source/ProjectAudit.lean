import CarryControls
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#check Agent6.NormalizedCarry.gam_eq_overflow
#check Agent6.NormalizedCarry.overflow_stripSuffix_of_le18
#check Agent6.NormalizedCarry.overflow_stripSuffix_of_bounded
#check Agent6.CertificateCarryAccounting.overflowBit_stateOuter
#check Agent6.CertificateCarryAccounting.rowOverflowSum_eq_totalGam_of_bounded
#check Agent6.CertificateCarryAccounting.valid_rowOverflowSum_eq_totalGam
#check Agent6.CertificateCarryAccounting.checked_rowOverflowSum_eq_totalGam
#check Agent6.CertificateCarryAccounting.checked_weighted_balance_totalGam
#check Agent6.CertificateCarryAccounting.checked_weighted_balance_gains
#check Agent6.CarryControls.phase19_carry_drift
#check Agent6.CarryControls.phase2_unbounded_indicator
#check Agent6.CarryControls.phase18_empty_boundary
#check Agent6.CarryControls.neutral_and_zero_boundaries
#check Agent6.CarryControls.bounded_phase19_boundary
#check Agent6.CarryControls.unrestricted_strip_carry_invariance_false
#check Agent6.CarryControls.indicator_eq_gam_without_bounded_false
run_cmd do
  let env ← getEnv
  let selected : List String := ["TemplateStep", "ReturnCertificate", "OuterFinite", "OuterBounds", "OuterBridge", "TARGET", "ExteriorFactorizationProof", "CoordinateThreshold", "NormalizedCarry", "CertificateRealization", "ExteriorNormalization", "CertificateExterior", "CertificateAccounting", "ExteriorObservationInjective", "ExteriorUpdateLaw", "CoordinateDynamics", "CoordinateSign", "CoordinateCycle", "CertificateCoordinates", "CertificateCarryAccounting", "CarryControls"]
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
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
        | _ => pure ()
  logInfo m!"FULL_MODULE_AUDIT theorems={count} union={union}"
