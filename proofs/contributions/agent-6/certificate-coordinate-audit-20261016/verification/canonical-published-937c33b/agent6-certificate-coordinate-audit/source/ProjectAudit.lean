import CertificateControls
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#check Agent6.CertificateCoordinates.rowOuter_orbit
#check Agent6.CertificateCoordinates.rowOuter_orbit_of_lt
#check Agent6.CertificateCoordinates.rowOuter_closed
#check Agent6.CertificateCoordinates.rowSum_eq_orbitSum
#check Agent6.CertificateCoordinates.rowContributionSum_eq_contributionSum
#check Agent6.CertificateCoordinates.valid_row_contribution_sum_eq_zero
#check Agent6.CertificateCoordinates.checked_row_contribution_sum_eq_zero
#check Agent6.CertificateCoordinates.valid_row_both_signs
#check Agent6.CertificateCoordinates.checked_row_both_signs
#check Agent6.CertificateCoordinates.checked_coordinate_conditions
#check Agent6.CertificateCoordinates.checked_row_weighted_balance
#check Agent6.CertificateFilter.coordinateFilter_eq_true_iff
#check Agent6.CertificateFilter.checked_coordinateFilter
#check Agent6.CertificateFilter.check_eq_false_of_coordinateFilter_eq_false
#check Agent6.CertificateFilter.period_pos_of_coordinateFilter
#check Agent6.CertificateFilter.coordinateFilter_eq_false_of_period_zero
#check Agent6.CertificateFilter.filteredCheck_eq_check
#check Agent6.CertificateControls.cancellationCandidate_period
#check Agent6.CertificateControls.cancellationCandidate_link_count
#check Agent6.CertificateControls.cancellationCandidate_rows
#check Agent6.CertificateControls.cancellationCandidate_contributions
#check Agent6.CertificateControls.cancellationCandidate_sum_zero
#check Agent6.CertificateControls.cancellationCandidate_filter_passes
#check Agent6.CertificateControls.cancellationCandidate_first_phase_failure
#check Agent6.CertificateControls.cancellationCandidate_check_false
#check Agent6.CertificateControls.cancellationCandidate_filteredCheck_false
#check Agent6.CertificateControls.coordinateFilter_not_sufficient
#check Agent6.CertificateControls.emptyCandidate_boundary
#check Agent6.CertificateControls.zeroPhaseCandidate_boundary
run_cmd do
  let env ← getEnv
  let selected : List String := ["TemplateStep", "ReturnCertificate", "OuterFinite", "OuterBounds", "OuterBridge", "CertificateRealization", "ExteriorNormalization", "CertificateExterior", "CertificateAccounting", "TARGET", "ExteriorFactorizationProof", "ExteriorObservationInjective", "ExteriorUpdateLaw", "CoordinateDynamics", "CoordinateThreshold", "CoordinateSign", "CoordinateCycle", "CertificateCoordinates", "CertificateFilter", "CertificateControls"]
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
