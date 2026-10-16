import Agent101ProtectedFamily
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#check Agent101.Protected.mem_protectedSeeds_numeric
#check Agent101.Protected.protectedSeeds_nodup
#check Agent101.Protected.length_protectedSeeds
#check Agent101.Protected.protectedSeeds_palindrome_iff
#check Agent101.Protected.mem_protectedNonpalSeeds_numeric
#check Agent101.Protected.length_protectedNonpalSeeds
#check Agent101.Protected.protectedNonpalSeeds_nonempty
#check Agent101.Protected.protectedNonpalSeeds_second_value
#check Agent101.Protected.protectedNonpalSeeds_safe
#check Agent101.Protected.protectedNonpalFamily_exact
run_cmd do
  let env ← getEnv
  let selected : List String := ["LychrelDigitSums", "Lychrel196Research", "Agent101DigitPairs", "Agent101MultiplicityBounds", "Agent101SplitEnumeration", "Agent101NumericFibers", "Agent101PalindromeFibers", "Agent101NonpalindromicFibers", "PeriodObstructions", "ActualWordBridge", "FamilyDefinitions", "FamilyCardinality", "Agent101ProtectedMultiplicity", "Agent101ProtectedPalindrome", "Agent101ProtectedNonpalindromic", "DecimalSafeRuns", "SafetyBridge", "NormalizedSafety", "TemplateStep", "Compat", "IntegerInterfaces", "Agent101NormalizationValue", "FiniteHorizonOverflow", "FiniteHorizonTheorem", "Agent101ProtectedSafety", "Agent101ProtectedFamily"]
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
