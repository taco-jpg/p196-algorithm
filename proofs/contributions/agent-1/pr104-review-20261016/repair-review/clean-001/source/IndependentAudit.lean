import Agent114ShortRFirst11
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#check @Agent114.ShortR.common_first_step
#print axioms Agent114.ShortR.common_first_step
#check @Agent114.ShortR.r1_to_r4_initial_not_palindrome
#print axioms Agent114.ShortR.r1_to_r4_initial_not_palindrome
#check @Agent114.ShortR.r1_first_eleven
#print axioms Agent114.ShortR.r1_first_eleven
#check @Agent114.ShortR.r2_first_eleven
#print axioms Agent114.ShortR.r2_first_eleven
#check @Agent114.ShortR.r3_first_eleven
#print axioms Agent114.ShortR.r3_first_eleven
#check @Agent114.ShortR.r4_first_eleven
#print axioms Agent114.ShortR.r4_first_eleven
run_cmd do
  let env ← getEnv
  let selected : List String := ["LychrelDigitSums", "SafeDelay", "DecimalSafeRuns", "DecimalDelayBridge", "PairDelayBridge", "DelayedOverlapGate", "Agent114ShortRFirst11"]
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  let mut safeDefs := 0
  let mut safeOpaques := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        match info with
        | .axiomInfo v =>
          if v.isUnsafe then logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {mod} {name}"
          else throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .defnInfo v =>
          if v.safety != .safe then logInfo m!"NON_SAFE_DEFINITION {mod} {name} {repr v.safety}"
        | .opaqueInfo v =>
          if v.isUnsafe then logInfo m!"UNSAFE_OPAQUE {mod} {name}"
        | _ => pure ()
        let kind : Option String := match info with
          | .thmInfo _ => some "THEOREM"
          | .defnInfo v => if v.safety == .safe then some "SAFE_DEFINITION" else none
          | .opaqueInfo v => if !v.isUnsafe then some "SAFE_OPAQUE" else none
          | _ => none
        if let some kind := kind then
          if kind == "THEOREM" then count := count + 1
          else if kind == "SAFE_DEFINITION" then safeDefs := safeDefs + 1
          else safeOpaques := safeOpaques + 1
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then throwError m!"DISALLOWED_AXIOMS {kind} {mod} {name} : {axl}"
          logInfo m!"AUDIT_{kind} {mod} {name} : {axl}"
  logInfo m!"SAFE_DEFINITION_AUDIT definitions={safeDefs} opaque={safeOpaques}"
  logInfo m!"FULL_MODULE_AUDIT theorems={count} union={union}"
