import Agent101NumericFibers
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#check Agent101.mem_rawWords
#check Agent101.mem_canonicalWords
#check Agent101.canonicalWords_nodup
#check Agent101.length_canonicalWords
#check Agent101.mem_numericFiber
#check Agent101.numericFiber_nodup
#check Agent101.length_numericFiber
#check Agent101.length_numericFiber_cons
#check Agent101.length_numericFiber_cons_le
#check Agent101.sharp_profile_bound
#check Agent101.all_preimages_887
run_cmd do
  let env ← getEnv
  let selected : List String := ["Lychrel196Research", "Agent101DigitPairs", "Agent101MultiplicityBounds", "Agent101SplitEnumeration", "Agent101NumericFibers"]
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
