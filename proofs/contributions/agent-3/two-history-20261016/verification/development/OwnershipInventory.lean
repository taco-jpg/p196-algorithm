import Lean
import TwoLayerCertificate

open Lean Elab Command
run_cmd do
  let env ← getEnv
  for (name, info) in env.constants.toList do
    if let some index := env.getModuleIdxFor? name then
      let owner := env.header.moduleNames[index]!
      if owner.toString == "TwoLayerCertificate" then
        let user := (privateToUserName? name).getD name
        let isPrivate := (privateToUserName? name).isSome
        liftIO <| IO.println s!"P196_AUDIT_DECL {owner} {name} {user} {isPrivate} {info.isUnsafe} {info.isPartial}"
