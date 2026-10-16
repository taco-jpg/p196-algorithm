import Agent108WindowIncoming
import Lean

open Lean Elab Command

private def declarationKind : ConstantInfo → String
  | .axiomInfo _ => "axiom"
  | .defnInfo _ => "definition"
  | .thmInfo _ => "theorem"
  | .opaqueInfo _ => "opaque"
  | .quotInfo _ => "quotient"
  | .inductInfo _ => "inductive"
  | .ctorInfo _ => "constructor"
  | .recInfo _ => "recursor"

elab "audit_window_modules" : command => do
  let env ← getEnv
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let modName := env.header.moduleNames[idx.toNat]!
      if modName.toString.startsWith "Agent108Window" then
        logInfo s!"METADATA|{modName.toString}|{name.toString}|{declarationKind info}|{info.isUnsafe}|{info.isPartial}"
        if !info.isUnsafe && !info.isPartial then
          logInfo s!"AUDIT_BEGIN|{name.toString}"
          elabCommand (← `(command| #print axioms $(mkIdent name)))
          logInfo s!"AUDIT_END|{name.toString}"

audit_window_modules
