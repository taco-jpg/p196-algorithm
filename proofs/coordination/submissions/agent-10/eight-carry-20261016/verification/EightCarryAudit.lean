import Agent10EightCarryCounterexample
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0

#check Agent10EightCarryCounterexample.left_canonical
#check Agent10EightCarryCounterexample.right_canonical
#check Agent10EightCarryCounterexample.left_widths
#check Agent10EightCarryCounterexample.right_widths
#check Agent10EightCarryCounterexample.widths_agree
#check Agent10EightCarryCounterexample.eight_complete_carries
#check Agent10EightCarryCounterexample.initial_pair_sums_differ
#check Agent10EightCarryCounterexample.next_integer_values
#check Agent10EightCarryCounterexample.next_integers_differ
#check Agent10EightCarryCounterexample.numeric_orbit_representations
#check Agent10EightCarryCounterexample.ninth_carry_differs
#check Agent10EightCarryCounterexample.initial_pair_difference_active
#check Agent10EightCarryCounterexample.first_separation_at_eight
#check Agent10EightCarryCounterexample.eight_carry_counterexample
#check Agent10EightCarryCounterexample.palindrome_values_at_four
#check Agent10EightCarryCounterexample.first_palindromes_at_four

run_cmd do
  let env ← getEnv
  let selected := "Agent10EightCarryCounterexample"
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
