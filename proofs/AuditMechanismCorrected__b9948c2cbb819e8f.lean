import TemplateStep
import ReturnCertificate
import CertificateAccounting
import ExteriorCharge
import CertificateCharge
import LychrelDigitSums
import CertificateCarryBudget
import CertificatePhases
import CertificateConsequences
import All
import Lean

open Lean Elab Command

run_cmd do
  let modules : Array Name := #[`TemplateStep, `ReturnCertificate, `CertificateAccounting, `ExteriorCharge, `CertificateCharge, `LychrelDigitSums, `CertificateCarryBudget, `CertificatePhases, `CertificateConsequences, `All]
  let allowed : Array Name := #[`propext, `Classical.choice, `Quot.sound]
  let env ← getEnv
  let mut declarations : Array Name := #[]
  let mut theoremCount := 0
  let mut safeCount := 0
  let mut unsafeCount := 0
  for (n, _) in env.constants do
    if let some idx := env.getModuleIdxFor? n then
      if modules.contains env.header.moduleNames[idx]! then
        declarations := declarations.push n
  for n in declarations.qsort Name.lt do
    let ci := (env.find? n).get!
    let deps ← collectAxioms n
    if ci.isUnsafe then
      unsafeCount := unsafeCount + 1
      logInfo m!"AUDIT_UNSAFE_COMPILER_ARTIFACT|{n}|{deps.qsort Name.lt |>.toList}"
    else
      for ax in deps do
        unless allowed.contains ax do
          throwError m!"DISALLOWED_AXIOM|{n}|{ax}"
      let kind := if ci.isTheorem then "THEOREM" else "CONSTANT"
      if ci.isTheorem then theoremCount := theoremCount + 1
      safeCount := safeCount + 1
      logInfo m!"AUDIT|{kind}|{n}|{deps.qsort Name.lt |>.toList}"
  logInfo m!"AUDIT_TOTAL|{safeCount}|{theoremCount}|{unsafeCount}"
