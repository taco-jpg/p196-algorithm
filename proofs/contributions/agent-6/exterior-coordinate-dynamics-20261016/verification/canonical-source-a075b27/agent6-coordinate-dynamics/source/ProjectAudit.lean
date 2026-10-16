import CoordinateCycle
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#check Agent6.ExteriorCoordinates.phaseCarry_le_one
#check Agent6.ExteriorCoordinates.phaseCarry_eq_div_nine
#check Agent6.ExteriorCoordinates.phaseDigit_identity
#check Agent6.ExteriorCoordinates.phaseDigit_le_eight
#check Agent6.ExteriorCoordinates.phaseDigit_pos
#check Agent6.ExteriorCoordinates.overflow_eq_highValue
#check Agent6.ExteriorCoordinates.overflow_eq_rho_quotient
#check Agent6.ExteriorCoordinates.overflow_le_one
#check Agent6.ExteriorCoordinates.overflow_eq_zero_iff
#check Agent6.ExteriorCoordinates.overflow_eq_one_iff
#check Agent6.ExteriorCoordinates.rhoNum_lt_twice_denominator
#check Agent6.ExteriorCoordinates.empty_word_coordinates
#check Agent6.ExteriorCoordinates.empty_word_quotient_iff
#check Agent6.ExteriorCoordinates.quotient_identity_forall_iff
#check Agent6.ExteriorCoordinates.excluded_phase_controls
#check Agent6.ExteriorCoordinates.unbounded_coefficient_control
#check Agent6.ExteriorCoordinates.betaNum_eq
#check Agent6.ExteriorCoordinates.betaNum_outerNext_raw
#check Agent6.ExteriorCoordinates.betaNum_outerNext
#check Agent6.ExteriorCoordinates.revN_lt_power
#check Agent6.ExteriorCoordinates.highContribution_emod_ten_of_overflow_ne_zero
#check Agent6.ExteriorCoordinates.highContribution_ne_zero_of_pos
#check Agent6.ExteriorCoordinates.highContribution_ne_zero_of_nonneutral
#check Agent6.ExteriorCoordinates.zero_phase_empty_control
#check Agent6.ExteriorCoordinates.zero_overflow_negative_control
#check Agent6.ExteriorCoordinates.zero_overflow_positive_control
#check Agent6.ExteriorCoordinates.one_overflow_negative_control
#check Agent6.ExteriorCoordinates.one_overflow_positive_control
#check Agent6.ExteriorCoordinates.both_signs_at_zero_overflow
#check Agent6.ExteriorCoordinates.both_signs_at_one_overflow
#check Agent6.ExteriorCoordinates.outerIter_zero
#check Agent6.ExteriorCoordinates.outerIter_succ
#check Agent6.ExteriorCoordinates.orbitSum_zero
#check Agent6.ExteriorCoordinates.orbitSum_succ
#check Agent6.ExteriorCoordinates.contributionSum_zero
#check Agent6.ExteriorCoordinates.contributionSum_succ
#check Agent6.ExteriorCoordinates.orbitSum_telescope
#check Agent6.ExteriorCoordinates.betaNum_outerIter
#check Agent6.ExteriorCoordinates.contributionSum_eq_betaNum_sub
#check Agent6.ExteriorCoordinates.contributionSum_eq_zero_of_beta_return
#check Agent6.ExteriorCoordinates.closed_orbit_contributionSum_eq_zero
#check Agent6.ExteriorCoordinates.contributionSum_eq_zero_of_padding_return
#check Agent6.ExteriorCoordinates.outerIter_eq_chain
#check Agent6.ExteriorCoordinates.contributionSum_eq_chain_betaNum_sub
#check Agent6.ExteriorCoordinates.orbitSum_eq_zero_of_nonneg
#check Agent6.ExteriorCoordinates.orbitSum_eq_zero_of_nonpos
#check Agent6.ExteriorCoordinates.orbitSum_zero_both_signs
#check Agent6.ExteriorCoordinates.closed_orbit_both_signs_of_initial_ne_zero
#check Agent6.ExteriorCoordinates.closed_orbit_both_signs_of_pos
#check Agent6.ExteriorCoordinates.closed_orbit_both_signs_of_nonneutral
#check Agent6.ExteriorCoordinates.overflowBit_le_one
#check Agent6.ExteriorCoordinates.carryScale_eq
#check Agent6.ExteriorCoordinates.overflowCount_zero
#check Agent6.ExteriorCoordinates.overflowCount_succ
#check Agent6.ExteriorCoordinates.overflowCount_le
#check Agent6.ExteriorCoordinates.highContribution_eq_weighted
#check Agent6.ExteriorCoordinates.contributionSum_eq_weighted
#check Agent6.ExteriorCoordinates.closed_orbit_weighted_balance
run_cmd do
  let env ← getEnv
  let selected : List String := ["OuterFinite", "TARGET", "ExteriorFactorizationProof", "ExteriorObservationInjective", "ExteriorUpdateLaw", "CoordinateDynamics", "CoordinateThreshold", "CoordinateSign", "CoordinateCycle"]
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
