import NoAlternatingReturn
import LychrelDigitSums
import ActualMapObligations
import ActualStrip
import AlternatingScalarBoundary
import ActualInfiniteStrip
import NumericStrip
import All
import Lean
open Lean Elab Command

run_cmd do
  let modules : Array Name := #[`NoAlternatingReturn, `LychrelDigitSums, `ActualMapObligations, `ActualStrip, `AlternatingScalarBoundary, `ActualInfiniteStrip, `NumericStrip, `All]
  let endpoints : Array Name := #[`Agent112.TwoPhase.admissible_at, `Agent112.TwoPhase.constant_cut_reset, `Agent112.TwoPhase.uniform_band_tail, `Agent112.TwoPhase.cyclic_even_value, `Agent112.TwoPhase.actual_prefix_transport, `Agent112.TwoPhase.no_actual_alternating_prefix_return, `Agent112.TwoPhase.orbit_slot_valid, `Agent112.TwoPhase.actual_tile, `Agent112.TwoPhase.actual_spatial_step, `Agent112.TwoPhase.actual_outside, `Agent112.TwoPhase.actual_six_tail, `Agent112.TwoPhase.actual_twelve_tail, `Agent112.TwoPhase.no_actual_persistent_alternating_band, `Agent112.TwoPhase.Numeric.numeric_representation, `Agent112.TwoPhase.Numeric.no_numeric_persistent_alternating_band, `Agent112.TwoPhase.Numeric.canonical15, `Agent112.TwoPhase.Numeric.canonical1330, `Agent112.TwoPhase.Numeric.finite_scope_control, `Agent112.TwoPhase.Numeric.phase_alone_not_overflow_alternation]
  let allowed : Array Name := #[`propext, `Classical.choice, `Quot.sound]
  let env ← getEnv
  for n in endpoints do
    match env.find? n with
    | none => throwError m!"MISSING_ENDPOINT|{n}"
    | some ci =>
        unless ci.isTheorem && !ci.isUnsafe do
          throwError m!"ENDPOINT_NOT_SAFE_THEOREM|{n}"
        logInfo m!"ENDPOINT|{n}|{ci.type}"
  let mut names : Array Name := #[]
  for (n, _) in env.constants do
    if let some idx := env.getModuleIdxFor? n then
      if modules.contains env.header.moduleNames[idx]! then
        names := names.push n
  let mut safeCount := 0
  let mut theoremCount := 0
  let mut unsafeCount := 0
  for n in names.qsort Name.lt do
    let ci := (env.find? n).get!
    let deps ← collectAxioms n
    if ci.isUnsafe then
      unsafeCount := unsafeCount + 1
      logInfo m!"UNSAFE_COMPILER_ARTIFACT|{n}|{deps.qsort Name.lt |>.toList}"
    else
      for ax in deps do
        unless allowed.contains ax do
          throwError m!"DISALLOWED_AXIOM|{n}|{ax}"
      let kind := if ci.isTheorem then "THEOREM" else "CONSTANT"
      if ci.isTheorem then theoremCount := theoremCount + 1
      safeCount := safeCount + 1
      logInfo m!"AUDIT|{kind}|{n}|{deps.qsort Name.lt |>.toList}"
  logInfo m!"AUDIT_TOTAL|{safeCount}|{theoremCount}|{unsafeCount}"
