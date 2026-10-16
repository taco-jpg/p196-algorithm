import Agent104620Witness
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#check Agent104.Prefix620Witness.exact_trajectory
#check Agent104.Prefix620Witness.twelve_steps
#check Agent104.Prefix620Witness.target_canonical
#check Agent104.Prefix620Witness.target_mem_family
#check Agent104.Prefix620Witness.first_hit_twelve
#check Agent104.Prefix620Witness.realized_depth12
#check Agent104.Prefix620Witness.any_uniform_bound_ge12
run_cmd do
  let env ← getEnv
  let selected : List String := ["LychrelDigitSums", "PrefixInverse", "ActualPrefix", "PrefixCertificate", "LongRowsBase", "FastInverse", "FastRowsBase", "PalindromeBridge", "ShortBoundary", "Agent124PrefixK", "Agent104620Witness"]
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
