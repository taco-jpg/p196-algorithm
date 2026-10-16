import FourColumnConclusion
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let selected : List String := ["Rank4Data", "Rows4_000", "Rows4_001", "Rows4_002", "Rows4_003", "Rows4_004", "Rows4_005", "Rows4_006", "Rows4_007", "Rows4_008", "Rows4_009", "Rows4_010", "Rows4_011", "Rows4_012", "Rows4_013", "Rows4_014", "Rows4_015", "Rows4_branches", "AllRows4", "FourColumnAncestry", "Short4", "ThreeDigitBridge", "Table4", "FourColumnConclusion"]
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        match info with
        | .axiomInfo v =>
          if v.isUnsafe then logInfo m!"UNSAFE_IMPL {mod} {name}"
          else throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          logInfo m!"AUDIT_THEOREM {mod} {name}"
          elabCommand (← `(command| #print axioms $(mkIdent name)))
        | _ => pure ()
#print axioms SevenColumnProjection.actual_mem_prefixPredecessors
#print axioms SevenColumn.mem_prefixPredecessors_iff
#print axioms SevenColumn.Certificate.checkedRows_closed
#print axioms SevenColumn.Certificate.checkedRows_fast_to_long
#print axioms SevenColumn.ShortBoundary.rawWords_complete
#print axioms SevenColumn.ShortBoundary.nextWord_wordOf
#print axioms SevenColumnKernel.PalindromeBridge.canonical_last_step
#print axioms SevenColumnKernel.PalindromeBridge.no_196_target_of_ancestry_bound
#print axioms Lychrel196.no_palindrome_through_100
#print axioms DecimalDigits.step_palindrome_iff_overflow
