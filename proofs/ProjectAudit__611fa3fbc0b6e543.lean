import OuterOrbit
import AlternatingScalarBoundary
import HighBaseFirstHit
import DifferenceObservability
import TwoDigitMain
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#check Agent113.TwoDigit.no_196_thirteen_arith
#check Agent113.TwoDigit.startsTwo_iff
#check Agent113.TwoDigit.exact_depth_10
#check Agent113.TwoDigit.exact_depth_20
#check Agent113.TwoDigit.exact_depth_32
#check Agent113.TwoDigit.exact_depth_40
#check Agent113.TwoDigit.exact_depth_41
#check Agent113.TwoDigit.exact_depth_60
#check Agent113.TwoDigit.exact_depth_64
#check Agent113.TwoDigit.exact_depth_65
#check Agent113.TwoDigit.exact_depth_76
#check Agent113.TwoDigit.exact_depth_80
#check Agent113.TwoDigit.exact_depth_81
#check Agent113.TwoDigit.exact_depth_82
#check Agent113.TwoDigit.exact_depth_83
#check P196.Agent3.Charge.charge_zero_from_five
#check P196.Agent3.Charge.returned_outer_charge_zero
#check P196.Agent3.Charge.five_step_bound_sharp
#check Agent9.AlternatingScalarBoundary.no_six_boundary
#check Agent9.AlternatingScalarBoundary.no_twelve_boundary
#check Agent11HighBase.numeric_two_step_threshold
#check Agent11HighBase.numeric_interval_first_hit
#check Agent11HighBase.binary_threshold_counterexample
#check DifferenceObservability.nine_carry_words_determine_pair_sums
#check DifferenceObservability.nine_carry_words_determine_next_integer
run_cmd do
  let env ← getEnv
  let selected : List String := ["OuterCharge", "OuterOrbit", "AlternatingScalarBoundary", "SignedDigitUniqueness", "BaseReflection", "ResetNormalization", "PhysicalWidth", "SeamSafety", "ReverseAdd", "HighBaseNormalization", "HighBasePairs", "HighBaseThreshold", "HighBaseNumeric", "HighBaseFirstHit", "LychrelDigitSums", "Lychrel196Research", "PrefixCarryBound", "ActualCarryObservability", "DifferenceObservability", "TwoDigitProjection", "TwoDigitGrowth", "PalindromeBridge", "TwoDigitNumeric", "TwoDigitCertificate", "TwoDigitCert10", "TwoDigitCert20", "TwoDigitCert32", "TwoDigitCert40", "TwoDigitCert41", "TwoDigitCert60", "TwoDigitCert64", "TwoDigitCert65", "TwoDigitCert76", "TwoDigitCert80", "TwoDigitCert81", "TwoDigitCert82", "TwoDigitCert83", "TwoDigitMain"]
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
