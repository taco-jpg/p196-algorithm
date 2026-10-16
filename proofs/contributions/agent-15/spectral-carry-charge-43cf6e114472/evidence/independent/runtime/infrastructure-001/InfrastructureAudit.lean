import ReviewFixture
import Lean


open Lean Elab Command
set_option pp.universes true
set_option pp.fullNames true
set_option pp.explicit true
set_option pp.width 160
set_option maxRecDepth 100000
set_option maxHeartbeats 0

run_cmd do
  let env ← getEnv
  let selected : List String := ["ReviewFixture"]
  let required : List String := ["ReviewFixture.visible_eq", "ReviewFixture.sample_refl"]
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut names : List String := []
  let mut axiomUnion : List Name := []
  let mut count := 0
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let origin := env.allImportedModuleNames[idx.toNat]!
      if selected.contains origin.toString then
        unless (env.checked.get.find? name).isSome do
          throwError m!"UNCHECKED_DECLARATION {origin} {name}"
        if info.isUnsafe || info.isPartial then
          throwError m!"UNSAFE_OR_PARTIAL_DECLARATION {origin} {name}"
        let kind : String := match info with
          | .axiomInfo _ => "axiom"
          | .defnInfo _ => "definition"
          | .thmInfo _ => "theorem"
          | .opaqueInfo _ => "opaque"
          | .quotInfo _ => "quotient"
          | .inductInfo _ => "inductive"
          | .ctorInfo _ => "constructor"
          | .recInfo _ => "recursor"
        if kind == "axiom" then
          throwError m!"NEW_AXIOM {origin} {name}"
        let axioms := (← liftCoreM (Lean.collectAxioms name)).qsort Name.lt
        let axl := axioms.toList
        if axl.any (fun ax => !(allowed.contains ax)) then
          throwError m!"DISALLOWED_AXIOMS {origin} {name} : {axl}"
        for ax in axl do
          unless axiomUnion.contains ax do
            axiomUnion := ax :: axiomUnion
        names := name.toString :: names
        count := count + 1
        let record := Json.mkObj [
          ("module", toJson origin.toString),
          ("name", toJson name.toString),
          ("kind", toJson kind),
          ("private", toJson (Lean.isPrivateName name)),
          ("axioms", toJson (axioms.map Name.toString))]
        logInfo m!"AUDIT_DECL_JSON {record.compress}"
        logInfo m!"SIGNATURE_BEGIN {name}"
        logInfo m!"{name} : {info.type}"
        logInfo m!"SIGNATURE_END {name}"
        elabCommand (← `(#print axioms $(mkIdent name)))
  for name in required do
    unless names.contains name do
      throwError m!"MISSING_["ReviewFixture.visible_eq", "ReviewFixture.sample_refl"]_DECLARATION {name}"
  if count == 0 then
    throwError "EMPTY_PROJECT_DECLARATION_AUDIT"
  let summary := Json.mkObj [
    ("count", toJson count),
    ("axiom_union", toJson ((axiomUnion.toArray.qsort Name.lt).map Name.toString))]
  logInfo m!"AUDIT_SUMMARY_JSON {summary.compress}"
