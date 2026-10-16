import Agent10SixCarryCounterexample
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0

#check Agent10SixCarryCounterexample.left_canonical
#check Agent10SixCarryCounterexample.right_canonical
#check Agent10SixCarryCounterexample.left_widths
#check Agent10SixCarryCounterexample.right_widths
#check Agent10SixCarryCounterexample.widths_agree
#check Agent10SixCarryCounterexample.six_complete_carries
#check Agent10SixCarryCounterexample.initial_pair_sums_differ
#check Agent10SixCarryCounterexample.next_integer_values
#check Agent10SixCarryCounterexample.next_integers_differ
#check Agent10SixCarryCounterexample.numeric_orbit_representations
#check Agent10SixCarryCounterexample.seventh_carry_differs
#check Agent10SixCarryCounterexample.six_carry_counterexample

run_cmd do
  let env ← getEnv
  let selected := "Agent10SixCarryCounterexample"
  let allowed : List Name := [``propext, ``Quot.sound]
  let mut count := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if mod.toString == selected then
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
