import TemplateStep
import ReturnCertificate
import CertificateAccounting
import ExteriorCharge
import CertificateCharge
import LychrelDigitSums
import CertificateCarryBudget
import CertificatePhases
import CertificateConsequences
import PrefixModel
import CertificatePrefix
import SaturationCertificate
import SaturationTheorem
import CertificateSaturation
import AdmissibleCenters
import SymbolicGrowth
import AdmissibleHeads
import CertificateChecked
import SmallPeriodObstruction
import Lean
open Lean Elab Command

run_cmd do
  let modules : Array Name := #[`TemplateStep, `ReturnCertificate, `CertificateAccounting, `ExteriorCharge, `CertificateCharge, `LychrelDigitSums, `CertificateCarryBudget, `CertificatePhases, `CertificateConsequences, `PrefixModel, `CertificatePrefix, `SaturationCertificate, `SaturationTheorem, `CertificateSaturation, `AdmissibleCenters, `SymbolicGrowth, `AdmissibleHeads, `CertificateChecked, `SmallPeriodObstruction]
  let endpoints : Array Name := #[`Agent112.SmallPeriod.two_phase_next, `Agent112.SmallPeriod.two_code_step, `Agent112.SmallPeriod.valid_two_phase, `Agent112.SmallPeriod.parity_telescope, `Agent112.SmallPeriod.valid_two_period_even, `Agent112.SmallPeriod.checked_positive_exterior, `Agent112.SmallPeriod.checked_saturated_period_mod8, `Agent112.SmallPeriod.checked_period_ne_four, `Agent112.SmallPeriod.valid_phase_class, `Agent112.SmallPeriod.period_six_overflow_mod3, `Agent112.SmallPeriod.checked_period_ne_six, `Agent112.SmallPeriod.checked_period_even, `Agent112.SmallPeriod.checked_period_at_least_eight]
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
