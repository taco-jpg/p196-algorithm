import Agent1PeriodicZeroPrefix
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut theoremCount := 0
  let mut safeCount := 0
  let mut unsafeCount := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if mod.toString == "Agent1PeriodicZeroPrefix" then
        if info.isUnsafe then
          unsafeCount := unsafeCount + 1
          logInfo m!"UNSAFE_IMPLEMENTATION {name}"
        else
          match info with
          | .axiomInfo _ => throwError m!"CUSTOM_AXIOM {name}"
          | _ => pure ()
          safeCount := safeCount + 1
          if info.isTheorem then theoremCount := theoremCount + 1
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then
            throwError m!"DISALLOWED_AXIOMS {name} : {axl}"
          logInfo m!"AUDIT_SAFE_CONSTANT {name} theorem={info.isTheorem} : {axl}"
  if theoremCount == 0 then throwError "MODULE_NOT_AUDITED"
  logInfo m!"ZERO_PREFIX_MODULE_AUDIT theorems={theoremCount} safeConstants={safeCount} unsafeImplementations={unsafeCount} union={union}"

#print Agent1.Periodic.zeroExponent_guarded_prefix
#print Agent1.Periodic.zeroLiftWord_step_prefix
