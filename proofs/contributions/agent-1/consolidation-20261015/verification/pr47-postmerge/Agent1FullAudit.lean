import TwoDigitMain
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let selected : List String := ["LychrelDigitSums", "PalindromeBridge", "TwoDigitProjection", "TwoDigitGrowth", "TwoDigitNumeric", "TwoDigitCertificate", "TwoDigitCert10", "TwoDigitCert20", "TwoDigitCert32", "TwoDigitCert40", "TwoDigitCert41", "TwoDigitCert60", "TwoDigitCert64", "TwoDigitCert65", "TwoDigitCert76", "TwoDigitCert80", "TwoDigitCert81", "TwoDigitCert82", "TwoDigitCert83", "TwoDigitMain"]
  let mut count := 0
  let mut union : List Name := []
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
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
