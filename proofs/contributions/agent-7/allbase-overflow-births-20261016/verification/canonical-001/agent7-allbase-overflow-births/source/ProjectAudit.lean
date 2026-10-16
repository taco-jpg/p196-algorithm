import CanonicalOverflowBirths
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#check P196.Agent7.AllBaseOverflow.residue_zero_iff
#check P196.Agent7.AllBaseOverflow.residue_max_iff
#check P196.Agent7.AllBaseOverflow.adjacent_residues_zero_iff
#check P196.Agent7.AllBaseOverflow.adjacent_residues_max_iff
#check P196.Agent7.AllBaseOverflow.adjacentPair_zero_iff
#check P196.Agent7.AllBaseOverflow.adjacentPair_max_iff
#check P196.Agent7.AllBaseOverflow.adjacent_new_extreme_neutral
#check P196.Agent7.AllBaseOverflow.adjacent_without_neutral
#check P196.Agent7.AllBaseOverflow.ordinary_terminal_take_succ
#check P196.Agent7.AllBaseOverflow.incoming_succ
#check P196.Agent7.AllBaseOverflow.incoming_predecessor
#check P196.Agent7.AllBaseOverflow.incoming_mirror_predecessor
#check P196.Agent7.AllBaseOverflow.actual_overflow_body
#check P196.Agent7.AllBaseOverflow.actual_overflow_length
#check P196.Agent7.AllBaseOverflow.overflow_length_pos
#check P196.Agent7.AllBaseOverflow.actual_overflow_at
#check P196.Agent7.AllBaseOverflow.actual_overflow_last
#check P196.Agent7.AllBaseOverflow.actual_overflow_pair_at
#check P196.Agent7.AllBaseOverflow.actual_overflow_pair_getD
#check P196.Agent7.AllBaseOverflow.actual_overflow_endpoints
#check P196.Agent7.AllBaseOverflow.actual_overflow_zero_iff
#check P196.Agent7.AllBaseOverflow.actual_overflow_max_iff
#check P196.Agent7.AllBaseOverflow.actual_overflow_new_extreme_neutral
#check P196.Agent7.AllBaseOverflow.actual_overflow_without_neutral
#check P196.Agent7.AllBaseOverflow.endpoint_residue_positive
#check P196.Agent7.AllBaseOverflow.endpoint_residue_below_max
#check P196.Agent7.AllBaseOverflow.endpoint_residue_max_iff
#check P196.Agent7.AllBaseOverflow.overflow_head_coefficient_bound
#check P196.Agent7.AllBaseOverflow.actual_overflow_endpoints_pos
#check P196.Agent7.AllBaseOverflow.actual_overflow_endpoints_nonzero
#check P196.Agent7.AllBaseOverflow.actual_overflow_endpoints_max_iff
#check P196.Agent7.AllBaseOverflow.actual_overflow_endpoints_nonextreme
#check P196.Agent7.AllBaseOverflow.canonical_reverse_add_overflow_theorem
run_cmd do
  let env ← getEnv
  let selected : List String := ["BaseBirths", "SignedDigitUniqueness", "BaseReflection", "ResetNormalization", "AdjacentBirths", "PhysicalWidth", "SeamSafety", "ReverseAdd", "ActualBaseBirths", "OverflowDigits", "ActualOverflowBirths", "OverflowEndpoints", "CanonicalOverflowBirths"]
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
