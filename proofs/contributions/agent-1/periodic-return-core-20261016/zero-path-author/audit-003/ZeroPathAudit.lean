import Agent1PeriodicZeroPath
import Lean.Elab.BuiltinEvalCommand
import Lean.Util.CollectAxioms
open Lean Elab Command

#check Agent1.Periodic.quotient_path_zeroStateOrbit
#check Agent1.Periodic.quotient_path_zero_interface_ne
#check Agent1.Periodic.quotient_path_zero_no_return

run_cmd do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      if env.allImportedModuleNames[idx.toNat]!.toString == "Agent1PeriodicZeroPath" then
        match info with
        | .axiomInfo _ => throwError m!"CUSTOM_AXIOM {name}"
        | .thmInfo _ =>
          count := count + 1
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then
            throwError m!"DISALLOWED_AXIOMS {name} : {axl}"
          logInfo m!"AUDIT_THEOREM {name} : {axl}"
        | _ => throwError m!"UNEXPECTED_NEW_CONSTANT {name}"
  if count != 5 then throwError m!"WRONG_DECLARATION_COUNT {count}"
  logInfo m!"MODULE_AUDIT theorems={count} exported_endpoints=3 generated_proofs=2 definitions=0 custom_axioms=0 union={union}"
