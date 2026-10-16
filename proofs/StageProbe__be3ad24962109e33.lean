import All
import Lean
open Lean Elab Command
run_cmd do
  let env ← getEnv
  for (n, ci) in env.constants do
    if n.toString.endsWith "_cstage1" then
      if let some idx := env.getModuleIdxFor? n then
        if env.header.moduleNames[idx]! == `ExteriorCharge then
          logInfo m!"{n}|unsafe={ci.isUnsafe}|partial={ci.isPartial}|theorem={ci.isTheorem}"
