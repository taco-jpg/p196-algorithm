import Lean
import Agent121CertificateContracts

/- Agent #121: operational census, including generated and private local theorems. -/
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, info) in env.constants.toList do
    match info with
    | .thmInfo _ =>
      let n := name.toString
      let localName := ["Agent109.", "P196.Agent7.Finite.", "Agent116.", "Agent121.Review116."].any
        (fun prefix => n.startsWith prefix ||
          (n.startsWith "_private." && decide ((n.splitOn prefix).length > 1)))
      if localName then logInfo m!"AGENT121_THEOREM {n}"
    | _ => pure ()
