import Lean
import FiniteHorizonTheorem

#check Lean.ConstantInfo.isUnsafe
#check Lean.ConstantInfo.isPartial

open Lean Elab Command

run_cmd do
  let env ← getEnv
  for (name, info) in env.constants.toList do
    if name.toString.startsWith "P196.Agent3.OverflowHorizon." then
      liftIO <| IO.println s!"P196_SAFETY {name} {info.isUnsafe}"
