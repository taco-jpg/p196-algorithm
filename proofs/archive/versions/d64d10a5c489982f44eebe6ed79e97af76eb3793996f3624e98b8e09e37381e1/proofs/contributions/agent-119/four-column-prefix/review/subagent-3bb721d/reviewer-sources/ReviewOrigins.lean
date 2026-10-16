import FourColumnConclusion
import Lean
open Lean Elab Command

/-! Reviewer check: defining module of every constant the headline statements
depend on, and every non-internal constant declared by an Agent #119 module
outside the `FourColumnKernel` namespace. -/

def agent119Modules : List Name :=
  [`FourColumnAncestry, `ThreeDigitBridge, `FourColumnConclusion, `Rank4Data,
   `Rows4_000, `Rows4_001, `Rows4_002, `Rows4_003, `Rows4_004, `Rows4_005,
   `Rows4_006, `Rows4_007, `Rows4_008, `Rows4_009, `Rows4_010, `Rows4_011,
   `Rows4_012, `Rows4_013, `Rows4_014, `Rows4_015, `Rows4_branches, `AllRows4,
   `Short4, `Table4]

run_cmd do
  let env ← getEnv
  let modNames := env.header.moduleNames
  let modOf (n : Name) : String :=
    match env.getModuleIdxFor? n with
    | some idx => toString modNames[idx.toNat]!
    | none => "<current/none>"
  -- 1. transitive constant dependencies of the headline statements (types only)
  let heads : List Name := [``FourColumnKernel.Certificate.ancestry_bound,
    ``FourColumnKernel.Certificate.no_196, ``FourColumnKernel.Certificate.no_196_listed_prefix,
    ``FourColumnKernel.Certificate.ancestry_bound_33, ``FourColumnKernel.Certificate.no_196_33,
    ``FourColumnKernel.Certificate.sharp_33, ``FourColumnKernel.Certificate.sharp_33_starts]
  let mut seen : NameSet := {}
  let mut todo : Array Name := #[]
  for h in heads do
    let some ci := env.find? h | throwError "missing {h}"
    for c in ci.type.getUsedConstants do todo := todo.push c
  while !todo.isEmpty do
    let c := todo.back!
    todo := todo.pop
    if seen.contains c then continue
    seen := seen.insert c
    let some ci := env.find? c | continue
    -- follow definitions' bodies (not theorem proofs) to see what the statement means
    match ci with
    | .defnInfo d => for x in d.value.getUsedConstants do todo := todo.push x
    | _ => pure ()
    for x in ci.type.getUsedConstants do todo := todo.push x
  let mut rows : Array String := #[]
  for c in seen.toList do
    let m := modOf c
    if m != "Init.Prelude" && !(m.startsWith "Init.") then
      rows := rows.push s!"{c} @ {m}"
  rows := rows.qsort (· < ·)
  for r in rows do logInfo m!"STATEMENT-DEP {r}"
  -- 2. non-internal constants from Agent #119 modules outside FourColumnKernel
  for (n, _) in env.constants.map₁.toList do
    match env.getModuleIdxFor? n with
    | some idx =>
      let mn := modNames[idx.toNat]!
      if agent119Modules.contains mn && !(`FourColumnKernel).isPrefixOf n && !n.isInternal then
        logInfo m!"FOREIGN-NAMESPACE {n} @ {mn}"
    | none => pure ()
  logInfo m!"ORIGINS-DONE statementDeps={rows.size}"
