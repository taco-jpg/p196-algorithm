import Agent106CongruenceControls
import Lean

open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Agent30IndependentAudit

def selectedModules : List String :=
  ["LychrelDigitSums", "Agent106CarryBudget", "Agent106CongruenceSeed",
   "Agent106SparseTarget", "Agent106CongruenceObstruction", "Agent106CongruenceControls"]

def allowedAxioms : List Name := [``propext, ``Classical.choice, ``Quot.sound]

def endpointNames : List Name :=
  [`Agent106.CongruenceBudget.wordSum_le_constant,
   `Agent106.CongruenceBudget.carryCount_le_width,
   `Agent106.CongruenceBudget.digitSum_step_budget_of_canonical,
   `Agent106.CongruenceBudget.digitSum_step_budget,
   `Agent106.CongruenceBudget.not_step_of_digitSum_budget,
   `Agent106.CongruenceBudget.denseOutput_digitSum,
   `Agent106.CongruenceBudget.denseOutput_decimalLength,
   `Agent106.CongruenceBudget.denseOutput_canonical,
   `Agent106.CongruenceBudget.denseOutput_reverse,
   `Agent106.CongruenceBudget.denseOutput_step,
   `Agent106.CongruenceBudget.denseOutput_step_digitSum,
   `Agent106.CongruenceBudget.finitePrefix_first_step,
   `Agent106.CongruenceBudget.rho_le,
   `Agent106.CongruenceBudget.sparse_tail_bound,
   `Agent106.CongruenceBudget.target_digitSum_le_of_lt_pow,
   `Agent106.CongruenceBudget.target_digitSum_pow_add,
   `Agent106.CongruenceBudget.sparse_digitSum_bound,
   `Agent106.CongruenceBudget.sparse_eight_digitSum,
   `Agent106.CongruenceBudget.familyIndex_ge_two,
   `Agent106.CongruenceBudget.dense_step_digitSum_lower,
   `Agent106.CongruenceBudget.sparse_family_digitSum_gap,
   `Agent106.CongruenceBudget.congruence_sparse_jump_separation,
   `Agent106.CongruenceBudget.sparse_family_violates_actual_budget,
   `Agent106.CongruenceBudget.congruence_sparse_jump_ne_actual,
   `Agent106.CongruenceBudget.familyIndex_ge_four,
   `Agent106.CongruenceBudget.familyWidth_ge_six,
   `Agent106.CongruenceBudget.sparse_entry_tail_bound,
   `Agent106.CongruenceBudget.sparse_entry_bounds,
   `Agent106.CongruenceBudget.sparse_decimalLength,
   `Agent106.CongruenceBudget.denseOutput_mod99,
   `Agent106.CongruenceBudget.sparse_mod99,
   `Agent106.CongruenceBudget.familySource_mod99,
   `Agent106.CongruenceBudget.familySource_decimalLength,
   `Agent106.CongruenceBudget.sparse_family_entry_growth,
   `Agent106.CongruenceBudget.sparse_family_entry_width,
   `Agent106.CongruenceBudget.congruence_sparse_entry_controls]

def kind : ConstantInfo → String
  | .axiomInfo _ => "axiom"
  | .defnInfo _ => "definition"
  | .thmInfo _ => "theorem"
  | .opaqueInfo _ => "opaque"
  | .quotInfo _ => "quotient"
  | .inductInfo _ => "inductive"
  | .ctorInfo _ => "constructor"
  | .recInfo _ => "recursor"

def origin (env : Environment) (name : Name) : String :=
  match env.getModuleIdxFor? name with
  | some idx => env.allImportedModuleNames[idx.toNat]!.toString
  | none => "<current-or-kernel>"

/-- Includes projection structure names, unlike foldConsts in Lean 4.19.0. -/
def expressionNames (e : Expr) (acc : NameSet := {}) : NameSet :=
  match e with
  | .const n _ => acc.insert n
  | .app f a => expressionNames a (expressionNames f acc)
  | .lam _ t b _ => expressionNames b (expressionNames t acc)
  | .forallE _ t b _ => expressionNames b (expressionNames t acc)
  | .letE _ t v b _ => expressionNames b (expressionNames v (expressionNames t acc))
  | .mdata _ b => expressionNames b acc
  | .proj n _ b => expressionNames b (acc.insert n)
  | .sort _ | .bvar _ | .fvar _ | .mvar _ | .lit _ => acc

/-- Kernel-expression dependencies. It includes opaque values, inductive
    families/constructors, and recursor rule bodies, not implementation hooks. -/
def directDependencies (info : ConstantInfo) : NameSet := Id.run do
  let mut refs := expressionNames info.type
  if let some value := info.value? (allowOpaque := true) then
    refs := expressionNames value refs
  match info with
  | .inductInfo v =>
      for n in v.all ++ v.ctors do refs := refs.insert n
  | .ctorInfo v => refs := refs.insert v.induct
  | .recInfo v =>
      for n in v.all do refs := refs.insert n
      for rule in v.rules do
        refs := expressionNames rule.rhs (refs.insert rule.ctor)
  | _ => pure ()
  return refs

def sortedNames (ns : NameSet) : Array Name :=
  ns.toList.toArray.qsort (fun a b => a.toString < b.toString)

def namesJson (ns : Array Name) : Json :=
  toJson (ns.map Name.toString)

def bannedName (n : Name) : Bool :=
  ["sorryAx", "admitAx", "Lean.ofReduceBool", "Lean.ofReduceNat",
   "Lean.reduceBool", "Lean.reduceNat", "Lean.trustCompiler"].contains n.toString ||
  (n.toString.splitOn "native_decide").length != 1 ||
  (n.toString.splitOn "nativeDecide").length != 1

run_cmd do
  let env ← getEnv
  let entries := env.constants.toList.toArray.qsort (fun a b => a.1.toString < b.1.toString)
  let mut roots : Array Name := #[]
  let mut rootRows : Array Json := #[]
  let mut unsafeRows : Array Json := #[]
  let mut implementationNames : NameSet := {}
  let mut unsafeCount := 0
  let mut partialCount := 0
  let mut violations : Array String := #[]
  let mut axiomUnion : NameSet := {}
  let mut theoremCount := 0
  let mut definitionCount := 0
  let mut otherSafeCount := 0
  for (name, info) in entries do
    let mod := origin env name
    if selectedModules.contains mod then
      if info.isUnsafe || info.isPartial then
        implementationNames := implementationNames.insert name
        if info.isUnsafe then unsafeCount := unsafeCount + 1
        if info.isPartial then partialCount := partialCount + 1
        unsafeRows := unsafeRows.push (Json.mkObj [
          ("module", toJson mod), ("name", toJson name.toString),
          ("kind", toJson (kind info)), ("unsafe", toJson info.isUnsafe),
          ("partial", toJson info.isPartial)])
        logInfo m!"IMPLEMENTATION_SELECTED_CONSTANT {mod} {name} kind={kind info} unsafe={info.isUnsafe} partial={info.isPartial}"
      else
        match info with
        | .axiomInfo _ =>
            violations := violations.push s!"SAFE_SELECTED_AXIOM {mod} {name}"
        | .thmInfo _ => theoremCount := theoremCount + 1
        | .defnInfo _ => definitionCount := definitionCount + 1
        | _ => otherSafeCount := otherSafeCount + 1
        roots := roots.push name
        let axs ← liftCoreM (Lean.collectAxioms name)
        let mut axset : NameSet := {}
        for ax in axs do
          axset := axset.insert ax
          axiomUnion := axiomUnion.insert ax
          if !allowedAxioms.contains ax then
            violations := violations.push s!"DISALLOWED_AXIOM {mod} {name} {ax}"
        let sorted := sortedNames axset
        rootRows := rootRows.push (Json.mkObj [
          ("module", toJson mod), ("name", toJson name.toString),
          ("kind", toJson (kind info)), ("axioms", namesJson sorted),
          ("direct_dependencies", namesJson (sortedNames (directDependencies info)))])
        logInfo m!"AUDIT_SAFE_CONSTANT {mod} {name} kind={kind info} axioms={sorted.toList}"
  let mut endpointRows : Array Json := #[]
  for name in endpointNames do
    match env.checked.get.find? name with
    | none => violations := violations.push s!"MISSING_ENDPOINT {name}"
    | some info =>
        if kind info != "theorem" then
          violations := violations.push s!"ENDPOINT_NOT_THEOREM {name}"
        if !(roots.contains name) then
          violations := violations.push s!"ENDPOINT_OUTSIDE_SELECTED_ROOTS {name}"
        let axs ← liftCoreM (Lean.collectAxioms name)
        let mut aset : NameSet := {}
        for ax in axs do aset := aset.insert ax
        endpointRows := endpointRows.push (Json.mkObj [
          ("name", toJson name.toString), ("module", toJson (origin env name)),
          ("axioms", namesJson (sortedNames aset))])
  if endpointNames.length != 36 then
    violations := violations.push s!"ENDPOINT_COUNT {endpointNames.length}"
  let mut pending := roots
  let mut visited : NameSet := {}
  let mut graphRows : Array Json := #[]
  let mut graphAxioms : NameSet := {}
  let mut unsafeDependencies : NameSet := {}
  let mut partialDependencies : NameSet := {}
  while !pending.isEmpty do
    let name := pending.back!
    pending := pending.pop
    if !visited.contains name then
      visited := visited.insert name
      match env.checked.get.find? name with
      | none =>
          violations := violations.push s!"MISSING_KERNEL_CONSTANT {name}"
      | some info =>
          if info.isUnsafe then
            unsafeDependencies := unsafeDependencies.insert name
            violations := violations.push s!"UNSAFE_LOGICAL_DEPENDENCY {name}"
          if info.isPartial then
            partialDependencies := partialDependencies.insert name
            violations := violations.push s!"PARTIAL_LOGICAL_DEPENDENCY {name}"
          if bannedName name then
            violations := violations.push s!"BANNED_LOGICAL_DEPENDENCY {name}"
          match info with
          | .axiomInfo _ =>
              graphAxioms := graphAxioms.insert name
              if !allowedAxioms.contains name then
                violations := violations.push s!"DISALLOWED_GRAPH_AXIOM {name}"
          | _ => pure ()
          let refs := sortedNames (directDependencies info)
          pending := pending ++ refs
          graphRows := graphRows.push (Json.mkObj [
            ("name", toJson name.toString), ("module", toJson (origin env name)),
            ("kind", toJson (kind info)), ("unsafe", toJson info.isUnsafe),
            ("partial", toJson info.isPartial), ("dependencies", namesJson refs)])
  if sortedNames graphAxioms != sortedNames axiomUnion then
    violations := violations.push "AXIOM_COLLECTOR_GRAPH_UNION_MISMATCH"
  let implementationReachable := (sortedNames implementationNames).filter visited.contains
  if !implementationReachable.isEmpty then
    violations := violations.push "SELECTED_IMPLEMENTATION_REACHABLE_FROM_SAFE_ROOT"
  let summary := Json.mkObj [
    ("status", toJson (if violations.isEmpty then "PASS" else "FAIL")),
    ("module_count", toJson selectedModules.length), ("endpoint_count", toJson endpointRows.size),
    ("selected_safe_constants", toJson roots.size), ("theorems", toJson theoremCount),
    ("safe_definitions", toJson definitionCount), ("other_safe_constants", toJson otherSafeCount),
    ("selected_implementation_constants", toJson unsafeRows.size),
    ("selected_unsafe_constants", toJson unsafeCount),
    ("selected_partial_constants", toJson partialCount),
    ("selected_implementation_dependencies", namesJson implementationReachable),
    ("reachable_kernel_constants", toJson visited.size),
    ("unsafe_logical_dependencies", namesJson (sortedNames unsafeDependencies)),
    ("partial_logical_dependencies", namesJson (sortedNames partialDependencies)),
    ("collectAxioms_union", namesJson (sortedNames axiomUnion)),
    ("independent_graph_axiom_union", namesJson (sortedNames graphAxioms)),
    ("violations", toJson violations)]
  liftIO <| IO.FS.writeFile "audit-summary.json" (summary.pretty ++ "\n")
  liftIO <| IO.FS.writeFile "audit-roots.json" ((toJson rootRows).pretty ++ "\n")
  liftIO <| IO.FS.writeFile "audit-unsafe-selected.json" ((toJson unsafeRows).pretty ++ "\n")
  liftIO <| IO.FS.writeFile "audit-endpoints.json" ((toJson endpointRows).pretty ++ "\n")
  liftIO <| IO.FS.writeFile "audit-dependency-graph.json" ((toJson graphRows).pretty ++ "\n")
  logInfo m!"AUDIT_SUMMARY {summary.compress}"
  if !violations.isEmpty then
    throwError m!"AUDIT_FAILED {violations}"

end Agent30IndependentAudit
