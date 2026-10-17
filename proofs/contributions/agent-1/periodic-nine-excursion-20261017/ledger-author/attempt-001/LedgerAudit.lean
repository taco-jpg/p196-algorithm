import Agent1PeriodicNinesLedger
import Lean
open Lean Elab Command

run_cmd do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let required : List Name := [``Agent1.Periodic.ninesExtraStrips,
    ``Agent1.Periodic.ninesExtraSum, ``Agent1.Periodic.quotientCenter_nines_length_balance,
    ``Agent1.Periodic.quotient_path_nines_center_balance]
  let mut seen : List Name := []
  let mut count := 0
  let mut defs := 0
  let mut runtime := 0
  let mut union : List Name := []
  let mut defUnion : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      if env.allImportedModuleNames[idx.toNat]!.toString == "Agent1PeriodicNinesLedger" then
        seen := name :: seen
        match info with
        | .thmInfo _ =>
          count := count + 1
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then
            throwError m!"DISALLOWED_THEOREM_AXIOMS {name} : {axl}"
          logInfo m!"AUDIT_THEOREM {name} : {axl}"
        | .defnInfo v =>
          if v.safety != .safe then
            runtime := runtime + 1
            logInfo m!"GENERATED_RUNTIME {name}"
          else
            defs := defs + 1
            let axs ← liftCoreM (Lean.collectAxioms name)
            let axl := axs.toList
            for ax in axl do
              if !(defUnion.contains ax) then defUnion := ax :: defUnion
            if axl.any (fun ax => !(allowed.contains ax)) then
              throwError m!"DISALLOWED_DEFINITION_AXIOMS {name} : {axl}"
            logInfo m!"AUDIT_SAFE_DEFINITION {name} : {axl}"
        | _ => throwError m!"UNEXPECTED_NEW_CONSTANT {name}"
  for name in required do
    if !(seen.contains name) then throwError m!"MISSING_PUBLIC_CONSTANT {name}"
  logInfo m!"MODULE_AUDIT theorems={count} safe_definitions={defs} generated_runtime={runtime} custom_axioms=0 theorem_union={union} definition_union={defUnion}"

#check Agent1.Periodic.ninesExtraStrips
#check Agent1.Periodic.ninesExtraSum
#check Agent1.Periodic.quotientCenter_nines_length_balance
#check Agent1.Periodic.quotient_path_nines_center_balance
#print axioms Agent1.Periodic.ninesExtraStrips
#print axioms Agent1.Periodic.ninesExtraSum
#print axioms Agent1.Periodic.quotientCenter_nines_length_balance
#print axioms Agent1.Periodic.quotient_path_nines_center_balance
