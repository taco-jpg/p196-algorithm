import NoAlternatingReturn
import Lean
open Lean Elab Command
set_option pp.all true
set_option pp.universes true
set_option pp.proofs true
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let names : List Name := [`P196.Agent4.TemporalStrip.left_scalar, `P196.Agent4.TemporalStrip.right_scalar, `P196.Agent4.TemporalStrip.left_backward, `P196.Agent4.TemporalStrip.right_backward, `P196.Agent4.TemporalStrip.cyclic_successor_onto, `P196.Agent4.TemporalStrip.no_alternating_six_twelve_strip, `P196.Agent4.TemporalStrip.no_finite_alternating_six_twelve_strip]
  for name in names do
    let some info := env.find? name | throwError m!"MISSING_EXPORT {name}"
    logInfo m!"STATEMENT_BEGIN {name}"
    logInfo m!"{info.type}"
    logInfo m!"STATEMENT_RAW {name} {repr info.type}"
    logInfo m!"STATEMENT_END {name}"
