import LocalSmoke
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let selected : List String := ["LocalSmoke"]
  let exports : List String := ["Agent13SafeWeights.predecessor_le", "Agent13SafeWeights.mem_safeFiber_iff", "Agent13SafeWeights.full_safe_fiber_finite", "Agent13SafeWeights.incoming_nonneg", "Agent13SafeWeights.family_sum_le_incoming", "Agent13SafeWeights.finite_family_weight_lower", "Agent13SafeWeights.incoming_weight_lower", "Agent13SafeWeights.incoming_weight_ratio", "Agent13SafeWeights.no_uniform_multiplier", "Agent13SafeWeights.not_exists_uniform_bound", "Agent13SafeWeights.target_size_bound_nat", "Agent13SafeWeights.target_size_bound_real", "Agent13SafeWeights.family_size_scaled_power", "Agent13SafeWeights.sqrt_scale_lt_family_size", "Agent13SafeWeights.incoming_weight_sqrt_lower"]
  for mod in env.allImportedModuleNames do
    let path ← liftIO <| findOLean mod
    logInfo m!"AUDIT_IMPORT {mod} {path}"
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        match info with
        | .axiomInfo v =>
          if v.isUnsafe then
            logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {mod} {name}"
          else
            throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          logInfo m!"AUDIT_THEOREM {mod} {name}"
          if exports.contains name.toString then
            logInfo m!"AUDIT_EXPORT_TYPE {name}
{info.type}"
            logInfo m!"AUDIT_EXPORT_RAW_TYPE {name}
{repr info.type}"
          elabCommand (← `(command| #print axioms $(mkIdent name)))
        | _ => pure ()
