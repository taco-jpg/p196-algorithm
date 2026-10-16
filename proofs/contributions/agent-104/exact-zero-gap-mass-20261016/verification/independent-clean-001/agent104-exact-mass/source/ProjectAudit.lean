import Agent104FiniteMassBound
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#check Agent104.ExactZeroGap.interval_nine_mass
#check Agent104.ExactZeroGap.zeroBound_next_nooverflow_exact
#check Agent104.ExactZeroGap.zeroBound_next_overflow_exact
#check Agent104.ExactZeroGap.zeroBound_next_preserved
#check Agent104.FiniteMass.bounded_prefix_width
#check Agent104.FiniteMass.bounded_prefix_time
#check Agent104.FiniteMass.digitSum_escape_of_canonical
#check Agent104.FiniteMass.digitSum_escape
#check Agent104.FiniteMass.widthBound_scaled
#check Agent104.FiniteMass.runningMax_square_bound_of_canonical
#check Agent104.FiniteMass.runningMax_square_bound
run_cmd do
  let env ← getEnv
  let selected : List String := ["LychrelDigitSums", "Agent104ExactZeroGap", "SharedProfile", "ProfileDynamics", "SharpProfileBounds", "Agent104FiniteMassBound"]
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
