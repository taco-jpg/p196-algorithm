import FiniteOverflow
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#check P196.Agent5.General.InitialValidity.band_digit_bounds
#check P196.Agent5.General.InitialValidity.phase_step
#check P196.Agent5.General.InitialValidity.boundary_digit_bounds
#check P196.Agent5.General.InitialValidity.normalize_digits_bounded
#check P196.Agent5.General.InitialValidity.zip_add_bounded
#check P196.Agent5.General.InitialValidity.append_digit_bounded
#check P196.Agent5.General.InitialValidity.rawExterior_bounded
#check P196.Agent5.General.InitialValidity.stripSuffix_bounded
#check P196.Agent5.General.InitialValidity.nextExterior_bounded
#check P196.Agent5.General.InitialValidity.valid_step
#check P196.Agent5.General.InitialValidity.valid_orbit
#check P196.Agent5.General.InitialValidity.overflow_bit_orbit
#check P196.Agent5.General.InitialValidity.orbit_add
#check P196.Agent5.General.InitialValidity.residue_zero_orbit
#check P196.Agent5.General.InitialValidity.residue_zero_after_overflow
#check P196.Agent5.General.InitialValidity.decimal_valid_orbit
#check P196.Agent5.General.InitialValidity.decimal_residue_after_overflow
#check P196.Agent5.General.InitialValidity.neutral_counterexample
#check P196.Agent5.General.InitialValidity.neutral_not_bounded
#check P196.Agent5.General.InitialValidity.odd_base_phase_counterexample
#check P196.Agent5.General.InitialValidity.normalize_append
#check P196.Agent5.General.InitialValidity.normalize_reverse_cons
#check P196.Agent5.General.InitialValidity.headD_append_replicate
#check P196.Agent5.General.InitialValidity.headD_stripSuffix
#check P196.Agent5.General.InitialValidity.head_step_raw
#check P196.Agent5.General.InitialValidity.raw_head_nil
#check P196.Agent5.General.InitialValidity.raw_head_cons_no_overflow
#check P196.Agent5.General.InitialValidity.raw_head_cons_overflow
#check P196.Agent5.General.InitialValidity.head_no_overflow
#check P196.Agent5.General.InitialValidity.head_positive_step
#check P196.Agent5.General.InitialValidity.head_positive_orbit
#check P196.Agent5.General.InitialValidity.head_powTwo_lower_bound
#check P196.Agent5.General.InitialValidity.overflow_by_power_bound
#check P196.Agent5.General.InitialValidity.decimal_overflow_before_five
#check P196.Agent5.General.InitialValidity.overflow_in_every_window
#check P196.Agent5.General.InitialValidity.decimal_overflow_every_five
#check P196.Agent5.General.InitialValidity.decimal_overflows_arbitrarily_late
#check P196.Agent5.General.InitialValidity.residue_zero_from_power_bound
#check P196.Agent5.General.InitialValidity.decimal_residue_zero_from_five
#check P196.Agent5.General.InitialValidity.sharpStart_valid
#check P196.Agent5.General.InitialValidity.sharp_no_earlier_overflow
#check P196.Agent5.General.InitialValidity.sharp_fifth_transition
#check P196.Agent5.General.InitialValidity.sharpAbsorptionStart_valid
#check P196.Agent5.General.InitialValidity.sharpAbsorption_not_at_four
#check P196.Agent5.General.InitialValidity.sharpAbsorption_at_five
#check P196.Agent5.General.InitialValidity.zeroHeadStart_valid
#check P196.Agent5.General.InitialValidity.zeroHead_not_absorbed_at_five
run_cmd do
  let env ← getEnv
  let selected : List String := ["ExteriorClock", "GeneralCarryMass", "GeneralMomentAbsorption", "InitialValidity", "FiniteOverflow"]
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
