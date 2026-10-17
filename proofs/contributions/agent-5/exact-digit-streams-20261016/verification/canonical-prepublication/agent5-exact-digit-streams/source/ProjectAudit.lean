import CoordinateStreams
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#check Agent5.ExactDigitStreams.adicNumeratorDigits_length
#check Agent5.ExactDigitStreams.fractionDigits_length
#check Agent5.ExactDigitStreams.adicNumeratorDigits_bounded
#check Agent5.ExactDigitStreams.adicNumeratorDigits_prefix
#check Agent5.ExactDigitStreams.adicNumeratorDigits_column
#check Agent5.ExactDigitStreams.adicNumeratorDigits_constant
#check Agent5.ExactDigitStreams.adicNumeratorDigits_normalize
#check Agent5.ExactDigitStreams.adicNumeratorDigits_phase
#check Agent5.ExactDigitStreams.adicNumeratorDigits_exterior
#check Agent5.ExactDigitStreams.fractionDigits_scale
#check Agent5.ExactDigitStreams.fractionDigits_repeat
#check Agent5.ExactDigitStreams.highValue_cons_digit
#check Agent5.ExactDigitStreams.highValue_lt_pow
#check Agent5.ExactDigitStreams.fractionDigits_of_highValue
#check Agent5.ExactDigitStreams.normalize_value_conservation
#check Agent5.ExactDigitStreams.normalize_digits_lt_ten
#check Agent5.ExactDigitStreams.highValue_reverse_word
#check Agent5.ExactDigitStreams.phase_tail_digit
#check Agent5.ExactDigitStreams.fractionDigits_exterior
#check Agent5.ExactDigitStreams.fractionDigits_prefix
#check Agent5.ExactDigitStreams.fractionDigits_digits_lt_ten
#check Agent5.ExactDigitStreams.fractionDigits_exterior_digits_lt_ten
#check Agent5.ExactDigitStreams.strip_zip_append_replicate
#check Agent5.ExactDigitStreams.outerNext_from_streams
#check Agent5.ExactDigitStreams.outerNext_from_streams_of_cutoff
run_cmd do
  let env ← getEnv
  let selected : List String := ["OuterFinite", "TARGET", "ExteriorFactorizationProof", "DigitDefinitions", "AdicDigits", "FractionDigits", "CoordinateStreams"]
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
