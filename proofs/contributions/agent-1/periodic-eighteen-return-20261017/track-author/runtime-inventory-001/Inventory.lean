import Agent1PeriodicEighteenTrack
import Lean.Elab.BuiltinEvalCommand
open Lean Elab Command
run_cmd do
  let env ← getEnv
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      if env.allImportedModuleNames[idx.toNat]!.toString == "Agent1PeriodicEighteenTrack" then
        if let .defnInfo value := info then
          logInfo m!"DEFINITION {name} SAFETY {repr value.safety} TYPE {value.type}"
