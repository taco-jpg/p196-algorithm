import Lean
import TwoLayerCertificate

set_option pp.privateNames true
open Lean Elab Command
run_cmd do
  let env ← getEnv
  let targets := ["_private.TwoLayerCertificate.0.P196.Agent3.TwoHistory.jointData",
    "_private.TwoLayerCertificate.0.P196.Agent3.TwoHistory.jointData.match_1"]
  for (name, _) in env.constants.toList do
    if targets.contains name.toString then
      elabCommand (← `(command| #print axioms $(mkIdent name)))
