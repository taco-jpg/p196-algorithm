import Agent1PeriodicZeroState
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#check @Agent1.Periodic.ZeroState
#print axioms Agent1.Periodic.ZeroState
#check @Agent1.Periodic.zeroNext
#print axioms Agent1.Periodic.zeroNext
#check @Agent1.Periodic.zeroStateOrbit
#print axioms Agent1.Periodic.zeroStateOrbit
#check @Agent1.Periodic.zeroStateOrbit_add
#print axioms Agent1.Periodic.zeroStateOrbit_add
#check @Agent1.Periodic.zeroStateOrbit_valid
#print axioms Agent1.Periodic.zeroStateOrbit_valid
#check @Agent1.Periodic.zeroStateOrbit_cycle_reduce
#print axioms Agent1.Periodic.zeroStateOrbit_cycle_reduce
#check @Agent1.Periodic.zeroStateMeasure
#print axioms Agent1.Periodic.zeroStateMeasure
#check @Agent1.Periodic.zeroStatePrefixBound
#print axioms Agent1.Periodic.zeroStatePrefixBound
#check @Agent1.Periodic.zeroStateMeasure_le_prefix
#print axioms Agent1.Periodic.zeroStateMeasure_le_prefix
#check @Agent1.Periodic.zeroStateOrbit_cycle_bounded
#print axioms Agent1.Periodic.zeroStateOrbit_cycle_bounded
run_cmd do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut theoremCount := 0
  let mut definitionCount := 0
  let mut opaqueCount := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if mod.toString == "Agent1PeriodicZeroState" then
        match info with
        | .axiomInfo v =>
          if v.isUnsafe then logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {name}"
          else throwError m!"CUSTOM_AXIOM {name}"
        | .defnInfo v =>
          if v.safety != .safe then logInfo m!"NON_SAFE_DEFINITION {name} {repr v.safety}"
        | .opaqueInfo v =>
          if v.isUnsafe then logInfo m!"UNSAFE_OPAQUE {name}"
        | _ => pure ()
        let kind : Option String := match info with
          | .thmInfo _ => some "THEOREM"
          | .defnInfo v => if v.safety == .safe then some "SAFE_DEFINITION" else none
          | .opaqueInfo v => if !v.isUnsafe then some "SAFE_OPAQUE" else none
          | _ => none
        if let some kind := kind then
          if kind == "THEOREM" then theoremCount := theoremCount + 1
          else if kind == "SAFE_DEFINITION" then definitionCount := definitionCount + 1
          else opaqueCount := opaqueCount + 1
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then throwError m!"DISALLOWED_AXIOMS {name} : {axl}"
          logInfo m!"AUDIT_{kind} {name} : {axl}"
  logInfo m!"MODULE_AUDIT theorems={theoremCount} definitions={definitionCount} opaque={opaqueCount} union={union}"
