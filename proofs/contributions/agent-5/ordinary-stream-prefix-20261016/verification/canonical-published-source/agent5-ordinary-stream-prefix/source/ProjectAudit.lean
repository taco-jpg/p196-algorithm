import OrdinaryStreamStep
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#check Agent5.OrdinaryStreamPrefix.normalize7_eq_norm6
#check Agent5.OrdinaryStreamPrefix.nonneutralPhase_nonneutral6
#check Agent5.OrdinaryStreamPrefix.ordinary_raw_prefix_from_normalized_streams
#check Agent5.OrdinaryStreamPrefix.ordinary_raw_prefix_from_streams
#check Agent5.OrdinaryStreamPrefix.ordinary_raw_prefix_from_streams_quotient
#check Agent5.OrdinaryStreamPrefix.ordinary_reverse_add_from_streams
run_cmd do
  let env ← getEnv
  let selected : List String := ["OuterFinite", "TARGET", "ExteriorFactorizationProof", "DigitDefinitions", "AdicDigits", "FractionDigits", "CoordinateStreams", "CoordinateThreshold", "CoordinateOnlyStreams", "ExteriorCore", "ExteriorBridge", "ExteriorProjection", "ExteriorArithmetic", "RawPrefixStreams", "OrdinaryStreamStep"]
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
