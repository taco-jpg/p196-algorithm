import OuterBlock
import ModulusSplit
import PairWeights
import PeriodExistence
import Lychrel196Research
import PalindromeDigits
import DigitPools
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let selected : List String := ["OuterBlock", "ModulusSplit", "PairWeights", "PeriodExistence", "Lychrel196Research", "PalindromeDigits", "DigitPools"]
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        match info with
        | .axiomInfo ax =>
          if ax.isUnsafe then
            logInfo m!"UNSAFE_COMPILER_AXIOM {mod} {name}"
          else throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          logInfo m!"REVIEW_THEOREM {mod} {name}"
          elabCommand (← `(command| #print axioms $(mkIdent name)))
        | _ => pure ()
