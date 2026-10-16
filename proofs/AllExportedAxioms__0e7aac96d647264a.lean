import OuterBlock
import ModulusSplit
import PeriodExistence
import ModularSpan
import ArithmeticCRT
import Lychrel196Research
import PalindromeDigits
import PairWeights
import DigitPools
import ResidueOrbit
import Saturation
import ExplicitBound
import All
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let selected : List String := ["OuterBlock", "ModulusSplit", "PeriodExistence", "ModularSpan", "ArithmeticCRT", "Lychrel196Research", "PalindromeDigits", "PairWeights", "DigitPools", "ResidueOrbit", "Saturation", "ExplicitBound", "All"]
  for mod in env.allImportedModuleNames do
    logInfo m!"AUDIT_IMPORT {mod}"
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        match info with
        | .axiomInfo value =>
          if value.isUnsafe then
            logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {mod} {name}"
          else
            throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          logInfo m!"AUDIT_THEOREM {mod} {name}"
          elabCommand (← `(command| #print axioms $(mkIdent name)))
        | _ => pure ()
