import Agent1PeriodicNinesExcursion
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let selected : List String := ["PeriodObstructions", "ActualWordBridge", "PrefixSemantics", "LychrelDigitSums", "IncomingCarry", "Agent1RepeatedBlock", "Agent1RepeatedBlockContext", "Agent1PeriodicDigits", "Agent1PeriodicSlices", "Agent1PeriodicGuard", "Agent1PeriodicGuardFacts", "Agent1PeriodicNines", "Agent1PeriodicOuterStrip", "Agent1PeriodicCenterStrip", "Agent1PeriodicQuotient", "Agent1PeriodicCenterWrap", "Agent1PeriodicNinesCenter", "Agent1PeriodicWidthPath", "Agent1PeriodicPhase", "Agent1PeriodicParity", "Agent1PeriodicPositivity", "Agent1PeriodicValidity", "Agent1PeriodicZeroPeriod", "Agent1PeriodicNinesPath", "Agent1PeriodicNinesLedger", "Agent1PeriodicSafetyAlphabet", "Agent1PeriodicOuter", "Agent1PeriodicReturnClock", "Agent1PeriodicNinesExcursion"]
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  let mut defs := 0
  let mut union : List Name := []
  let mut defUnion : List Name := []
  let mut seen : List String := []
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
          if !(seen.contains mod.toString) then seen := mod.toString :: seen
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then
            throwError m!"DISALLOWED_AXIOMS {mod} {name} : {axl}"
          logInfo m!"AUDIT_THEOREM {mod} {name} : {axl}"
        | .defnInfo v =>
          if v.safety != .safe then
            logInfo m!"NONSAFE_DEFINITION {mod} {name}"
          else
            defs := defs + 1
            let axs ← liftCoreM (Lean.collectAxioms name)
            let axl := axs.toList
            for ax in axl do
              if !(defUnion.contains ax) then defUnion := ax :: defUnion
            if axl.any (fun ax => !(allowed.contains ax)) then
              throwError m!"DISALLOWED_DEFINITION_AXIOMS {mod} {name} : {axl}"
            logInfo m!"AUDIT_SAFE_DEFINITION {mod} {name} : {axl}"
        | .opaqueInfo v =>
          if v.isUnsafe then
            logInfo m!"UNSAFE_OPAQUE {mod} {name}"
          else
            defs := defs + 1
            let axs ← liftCoreM (Lean.collectAxioms name)
            let axl := axs.toList
            for ax in axl do
              if !(defUnion.contains ax) then defUnion := ax :: defUnion
            if axl.any (fun ax => !(allowed.contains ax)) then
              throwError m!"DISALLOWED_OPAQUE_AXIOMS {mod} {name} : {axl}"
            logInfo m!"AUDIT_SAFE_OPAQUE {mod} {name} : {axl}"
        | _ => pure ()
  for mod in selected do
    if !(seen.contains mod) then throwError m!"MODULE_NOT_AUDITED {mod}"
  logInfo m!"FULL_MODULE_AUDIT theorems={count} union={union}"
  logInfo m!"FULL_DEFINITION_AUDIT definitions={defs} union={defUnion}"

#check Agent1.RepeatedBlock.terminalCarry_eq_carryIn

#check Agent1.RepeatedBlock.terminalCarry_idempotent

#check Agent1.RepeatedBlock.terminalCarry_pow_succ

#check Agent1.RepeatedBlock.fixedDigits_pow_succ

#check Agent1.RepeatedBlock.normalize_pow_succ

#check Agent1.RepeatedBlock.pow_length

#check Agent1.RepeatedBlock.bounded_pow

#check Agent1.RepeatedBlock.normalize_context

#check Agent1.RepeatedBlock.terminalCarry_context

#check Agent1.RepeatedBlock.terminalCarry_two_bands

#check Agent1.RepeatedBlock.terminalCarry_symmetric_bands

#check Agent1.RepeatedBlock.normalize_context_length

#check Agent1.RepeatedBlock.normalize_symmetric_bands_length

#check Agent1.Periodic.normalize_periodicWord

#check Agent1.Periodic.scan_carry_stable

#check Agent1.Periodic.scan_carry_eq

#check Agent1.Periodic.scan_carry_le_one

#check Agent1.Periodic.scan_block_lengths

#check Agent1.Periodic.periodicWord_one

#check Agent1.Periodic.take_outer_one

#check Agent1.Periodic.take_period_one

#check Agent1.Periodic.take_center_one

#check Agent1.Periodic.pow_append

#check Agent1.Periodic.pow_succ_right

#check Agent1.Periodic.pow_reverse

#check Agent1.Periodic.zipAdd_append_eq

#check Agent1.Periodic.zipAdd_length_eq

#check Agent1.Periodic.zipAdd_comm_eq

#check Agent1.Periodic.zipAdd_reverse_eq

#check Agent1.Periodic.zipAdd_pow

#check Agent1.Periodic.pow_rotate_append

#check Agent1.Periodic.pair_three_parts

#check Agent1.Periodic.pair_periodic_digits

#check Agent1.Periodic.zipper_block_lengths

#check Agent1.Periodic.stepWord_periodic_form

#check Agent1.Periodic.raw_blocks_eq_zipper

#check Agent1.Periodic.raw_guard_bounded

#check Agent1.Periodic.raw_guard

#check Agent1.Periodic.raw_block_lengths

#check Agent1.Periodic.raw_center_symmetric

#check Agent1.Periodic.raw_blocks_bounded

#check Agent1.Periodic.rightEntry_nines

#check Agent1.Periodic.nines_entry_bits

#check Agent1.Periodic.rawPeriod_nines

#check Agent1.Periodic.stripPeriodSuffixAux_spec

#check Agent1.Periodic.stripPeriodSuffix_spec

#check Agent1.Periodic.stripPeriodSuffix_maximal

#check Agent1.Periodic.stripPeriodSuffix_empty_block

#check Agent1.Periodic.stripPeriodSuffix_length

#check Agent1.Periodic.stripPeriodSuffix_bounded

#check Agent1.Periodic.stripPeriodMiddle_wrap

#check Agent1.Periodic.stripPeriodCenter_test_iff

#check Agent1.Periodic.stripPeriodCenter_empty

#check Agent1.Periodic.stripPeriodCenterAux_decomposition

#check Agent1.Periodic.stripPeriodMiddle_length_lt

#check Agent1.Periodic.stripPeriodCenterAux_maximal

#check Agent1.Periodic.stripPeriodCenter_decomposition

#check Agent1.Periodic.stripPeriodCenter_maximal

#check Agent1.Periodic.stripPeriodCenter_length

#check Agent1.Periodic.stripPeriodCenter_length_le

#check Agent1.Periodic.stripPeriodCenter_bounded

#check Agent1.Periodic.stripPeriodCenter_symmetric

#check Agent1.Periodic.periodicWord_absorb

#check Agent1.Periodic.periodicWord_length

#check Agent1.Periodic.raw_guard_of_stripped

#check Agent1.Periodic.stripped_width_balance

#check Agent1.Periodic.quotient_step_bounded

#check Agent1.Periodic.quotient_irreducible

#check Agent1.Periodic.quotient_width_balance

#check Agent1.Periodic.quotient_exponent_accounting

#check Agent1.Periodic.stripPeriodCenter_wrap

#check Agent1.Periodic.rawCenter_nines_mixed

#check Agent1.Periodic.quotientCenter_nines_mixed

#check Agent1.Periodic.centerPeriods_nines_mixed

#check Agent1.Periodic.quotient_path_width_balance

#check Agent1.Periodic.quotient_path_equal_width_clock

#check Agent1.Periodic.mem_nonNine_of_length_four

#check Agent1.Periodic.reverse_ne_nines

#check Agent1.Periodic.terminalCarry_eq_of_nonNine

#check Agent1.Periodic.rawPeriod_eq_phaseImage

#check Agent1.Periodic.pair_middle_even

#check Agent1.Periodic.middle_append_eq

#check Agent1.Periodic.stripPeriodCenter_even

#check Agent1.Periodic.raw_center_even

#check Agent1.Periodic.periodicWord_canonical

#check Agent1.Periodic.raw_outer_positive

#check Agent1.Periodic.stripPeriodSuffix_outside

#check Agent1.Periodic.raw_valid

#check Agent1.Periodic.strip_valid

#check Agent1.Periodic.quotient_valid

#check Agent1.Periodic.valid_quotient_transition

#check Agent1.Periodic.leftPeriodDigits_zero

#check Agent1.Periodic.rightPeriodDigits_zero

#check Agent1.Periodic.rawPeriod_zero

#check Agent1.Periodic.zero_quotient_valid

#check Agent1.Periodic.quotient_path_nines_phase

#check Agent1.Periodic.quotient_path_nines_entry_sum

#check Agent1.Periodic.quotientCenter_nines_length_balance

#check Agent1.Periodic.quotient_path_nines_center_balance

#check Agent1.Periodic.mem_pow_iff

#check Agent1.Periodic.mem_periodicWord_iff

#check Agent1.Periodic.periodicWord_head

#check Agent1.Periodic.mem_stripped_alphabet_iff

#check Agent1.Periodic.outside_bounds

#check Agent1.Periodic.quotient_outside_step

#check Agent1.Periodic.quotient_path_valid

#check Agent1.Periodic.quotient_path_closed_outside_clock_bounds

#check Agent1.Periodic.quotient_return_clock_gain

#check Agent1.Periodic.quotient_return_length_ge_sixteen

#check Agent1.Periodic.quotient_return_nines_center_excursion

#check Agent1.Periodic.quotient_path_nines_small_centers_no_return

#check Agent1.Periodic.ninesExtraStrips
#print axioms Agent1.Periodic.ninesExtraStrips

#check Agent1.Periodic.ninesExtraSum
#print axioms Agent1.Periodic.ninesExtraSum

#print axioms Agent1.Periodic.quotientCenter_nines_length_balance

#print axioms Agent1.Periodic.quotient_path_nines_center_balance

#print axioms Agent1.Periodic.quotient_return_nines_center_excursion

#print axioms Agent1.Periodic.quotient_path_nines_small_centers_no_return
