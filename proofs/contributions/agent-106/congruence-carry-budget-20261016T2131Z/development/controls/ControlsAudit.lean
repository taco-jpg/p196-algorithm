import Agent106CongruenceControls
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#check Agent106.CongruenceBudget.familyIndex_ge_four
#check Agent106.CongruenceBudget.familyWidth_ge_six
#check Agent106.CongruenceBudget.sparse_entry_tail_bound
#check Agent106.CongruenceBudget.sparse_entry_bounds
#check Agent106.CongruenceBudget.sparse_decimalLength
#check Agent106.CongruenceBudget.denseOutput_mod99
#check Agent106.CongruenceBudget.sparse_mod99
#check Agent106.CongruenceBudget.familySource_mod99
#check Agent106.CongruenceBudget.familySource_decimalLength
#check Agent106.CongruenceBudget.sparse_family_entry_growth
#check Agent106.CongruenceBudget.sparse_family_entry_width
#check Agent106.CongruenceBudget.congruence_sparse_entry_controls
run_cmd do
  let env ← getEnv
  let selected : List String := ["Agent106CongruenceControls"]
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
          if axl.any (fun ax => !(allowed.contains ax)) then
            throwError m!"DISALLOWED_AXIOMS {mod} {name} : {axl}"
          logInfo m!"AUDIT_THEOREM {mod} {name} : {axl}"
        | _ => pure ()
  logInfo m!"FULL_MODULE_AUDIT theorems={count} union={union}"
