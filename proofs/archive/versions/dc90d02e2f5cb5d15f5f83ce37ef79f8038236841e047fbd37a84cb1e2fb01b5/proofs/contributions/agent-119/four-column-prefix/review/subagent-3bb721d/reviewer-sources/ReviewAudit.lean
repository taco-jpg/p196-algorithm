import FourColumnConclusion
import Lean

/-!
Reviewer-written axiom audit (independent of the author's check.py).

1. Enumerates EVERY constant whose defining module is one of the 33 modules of
   the import closure of `FourColumnConclusion`, classifies it, and rejects any
   safe `axiom` declaration, any `opaque` constant, any user-visible (non-internal
   name) `unsafe` or `partial` definition, and any `implemented_by`/`extern`
   attribute.  Internal-name unsafe/partial constants and unsafe axiom stubs are
   the code generator's `_cstage`/`_spec`/`_unsafe_rec` auxiliaries; they are
   counted, and the kernel refuses any safe declaration that mentions them.
2. Runs `Lean.collectAxioms` (the engine behind `#print axioms`) on every
   theorem among them and accepts only `propext`, `Classical.choice`,
   `Quot.sound`.
3. Prints one line per theorem in the `FourColumnKernel` namespace.
Fails (throwError) on any violation.
-/

open Lean Elab Command

def reviewClosureModules : List Name :=
  [`LychrelDigitSums, `PrefixInverse, `FastInverse, `ActualPrefix, `ShortBoundary,
   `PrefixCertificate, `PalindromeBridge, `LongRowsBase, `FastRowsBase,
   `FourColumnAncestry, `ThreeDigitBridge, `FourColumnConclusion, `Rank4Data,
   `Rows4_000, `Rows4_001, `Rows4_002, `Rows4_003, `Rows4_004, `Rows4_005,
   `Rows4_006, `Rows4_007, `Rows4_008, `Rows4_009, `Rows4_010, `Rows4_011,
   `Rows4_012, `Rows4_013, `Rows4_014, `Rows4_015, `Rows4_branches, `AllRows4,
   `Short4, `Table4]

def reviewAllowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]

run_cmd do
  let env ← getEnv
  let modNames := env.header.moduleNames
  -- sanity: every closure module is actually loaded
  for m in reviewClosureModules do
    unless modNames.contains m do
      throwError "closure module {m} not loaded"
  let mut consts : Array (Name × Name × ConstantInfo) := #[]
  for (n, ci) in env.constants.map₁.toList do
    match env.getModuleIdxFor? n with
    | some idx =>
        let mn := modNames[idx.toNat]!
        if reviewClosureModules.contains mn then
          consts := consts.push (n, mn, ci)
    | none => pure ()
  consts := consts.qsort (fun a b => Name.lt a.1 b.1)
  let mut nThm := 0
  let mut nDef := 0
  let mut nInd := 0
  let mut nOther := 0
  let mut nAuxUnsafe := 0
  let mut nAuxAxiom := 0
  let mut nAuxPartial := 0
  let mut violations : Array String := #[]
  let mut axiomUnion : Array Name := #[]
  let mut fckThms := 0
  let mut fckUserThms := 0
  for (n, mn, ci) in consts do
    -- implemented_by / extern only matter for compiled evaluation; report any.
    if (Compiler.implementedByAttr.getParam? env n).isSome then
      violations := violations.push s!"implemented_by on {n} in {mn}"
    if isExtern env n then
      violations := violations.push s!"extern on {n} in {mn}"
    match ci with
    | .axiomInfo _ =>
        if ci.isUnsafe && n.isInternal then
          nAuxAxiom := nAuxAxiom + 1   -- compiler specialization stub; kernel forbids safe use
        else
          violations := violations.push s!"AXIOM DECLARATION {n} in {mn} (unsafe={ci.isUnsafe})"
    | .opaqueInfo _ => violations := violations.push s!"opaque constant {n} in {mn}"
    | .defnInfo d =>
        nDef := nDef + 1
        if d.safety == .unsafe then
          if n.isInternal then nAuxUnsafe := nAuxUnsafe + 1
          else violations := violations.push s!"user-visible unsafe def {n} in {mn}"
        if d.safety == .partial then
          if n.isInternal then nAuxPartial := nAuxPartial + 1
          else violations := violations.push s!"user-visible partial def {n} in {mn}"
    | .thmInfo _ =>
        nThm := nThm + 1
        if ci.isUnsafe then
          violations := violations.push s!"unsafe theorem {n} in {mn}"
        let axs ← collectAxioms n
        for a in axs do
          unless axiomUnion.contains a do
            axiomUnion := axiomUnion.push a
          unless reviewAllowed.contains a do
            violations := violations.push s!"theorem {n} ({mn}) uses axiom {a}"
        let sorted := axs.qsort Name.lt
        if (`FourColumnKernel).isPrefixOf n then
          fckThms := fckThms + 1
          unless n.isInternal do fckUserThms := fckUserThms + 1
          logInfo m!"AUDIT-THM {n} [{mn}] axioms={sorted.toList}"
        else
          logInfo m!"AUDIT-OTHER {n} [{mn}] axioms={sorted.toList}"
    | .inductInfo _ => nInd := nInd + 1
    | _ => nOther := nOther + 1
  logInfo m!"AUDIT-SUMMARY constants={consts.size} theorems={nThm} defs={nDef} inductives={nInd} other={nOther} fourColumnKernelTheorems={fckThms} fourColumnKernelNonInternalTheorems={fckUserThms} compilerAuxUnsafeDefs={nAuxUnsafe} compilerAuxUnsafeAxiomStubs={nAuxAxiom} compilerAuxPartialDefs={nAuxPartial} axiomUnion={(axiomUnion.qsort Name.lt).toList} violations={violations.size}"
  for v in violations do
    logInfo m!"AUDIT-VIOLATION {v}"
  unless violations.isEmpty do
    throwError "audit failed with {violations.size} violation(s)"

-- Explicit #print axioms on the theorems named in the review task.
#print axioms FourColumnKernel.Certificate.ancestry_bound
#print axioms FourColumnKernel.Certificate.no_196
#print axioms FourColumnKernel.Certificate.no_196_listed_prefix
#print axioms FourColumnKernel.Certificate.ancestry_bound_33
#print axioms FourColumnKernel.Certificate.no_196_33
#print axioms FourColumnKernel.Certificate.sharp_33
#print axioms FourColumnKernel.Certificate.sharp_33_starts
#print axioms FourColumnKernel.Certificate.table4_checked
#print axioms FourColumnKernel.Certificate.table4_length
#print axioms FourColumnKernel.Certificate.entry_sound
#print axioms FourColumnKernel.Certificate.allRows
#print axioms FourColumnKernel.Certificate.allRowsFast
#print axioms FourColumnKernel.Certificate.shortDescent4
#print axioms FourColumnKernel.Certificate.root33_checked
#print axioms FourColumnKernel.Certificate.table4_has_33
#print axioms FourColumnKernel.actual_iterPairs_rank4
#print axioms FourColumnKernel.overflow_palindrome_prefix
#print axioms FourColumnKernel.no_overflow_of_prefix
#print axioms FourColumnKernel.canonical_last_step3
#print axioms FourColumnKernel.last_step_root
#print axioms FourColumnKernel.time_bound_of_root
#print axioms FourColumnKernel.ancestry_bound_of_checks
#print axioms FourColumnKernel.no_196_of_checks
#print axioms FourColumnKernel.shortWords3_complete
#print axioms FourColumnKernel.shortDescentOK_sound
#print axioms FourColumnKernel.project4_short
#print axioms FourColumnKernel.project4_long
#print axioms FourColumnKernel.project4_congr

-- Exact elaborated statements with fully qualified names.
set_option pp.fullNames true in
#check @FourColumnKernel.Certificate.ancestry_bound
set_option pp.fullNames true in
#check @FourColumnKernel.Certificate.no_196
set_option pp.fullNames true in
#check @FourColumnKernel.Certificate.no_196_listed_prefix
set_option pp.fullNames true in
#check @FourColumnKernel.Certificate.ancestry_bound_33
set_option pp.fullNames true in
#check @FourColumnKernel.Certificate.no_196_33
set_option pp.fullNames true in
#check @FourColumnKernel.Certificate.sharp_33
set_option pp.fullNames true in
#check @FourColumnKernel.Certificate.sharp_33_starts
set_option pp.fullNames true in
#check @FourColumnKernel.Certificate.table4_length
set_option pp.fullNames true in
#check @FourColumnKernel.actual_iterPairs_rank4
set_option pp.fullNames true in
#check @FourColumnKernel.ancestry_bound_of_checks
set_option pp.fullNames true in
#check @FourColumnKernel.overflow_palindrome_prefix
set_option pp.fullNames true in
#check @FourColumnKernel.last_step_root
set_option pp.fullNames true in
#check @FourColumnKernel.time_bound_of_root
set_option pp.fullNames true in
#print FourColumnKernel.Starts3
set_option pp.fullNames true in
#print FourColumnKernel.PalindromeStarts3
set_option pp.fullNames true in
#print FourColumnKernel.Certificate.Starts2
set_option pp.fullNames true in
#print FourColumnKernel.GrowthPrefix
set_option pp.fullNames true in
#print FourColumnKernel.rootWords
set_option pp.fullNames true in
#print FourColumnKernel.project4
set_option pp.fullNames true in
#print FourColumnKernel.ShortDescent
set_option pp.fullNames true in
#print FourColumnKernel.shortDescentOK
set_option pp.fullNames true in
#print FourColumnKernel.shortWords3
set_option pp.fullNames true in
#print FourColumnKernel.Certificate.entryOK
set_option pp.fullNames true in
#print DecimalDigits.Canonical
set_option pp.fullNames true in
#print DecimalDigits.value
set_option pp.fullNames true in
#print Lychrel196.orbit
set_option pp.fullNames true in
#print Lychrel196.step
set_option pp.fullNames true in
#print Lychrel196.Palindrome
set_option pp.fullNames true in
#print Lychrel196.reverse10
set_option pp.fullNames true in
#print SevenColumn.Certificate.CheckedRows
set_option pp.fullNames true in
#print SevenColumn.Certificate.checkRow
set_option pp.fullNames true in
#print SevenColumn.Certificate.checkInitial
set_option pp.fullNames true in
#print SevenColumn.Certificate.longPred
set_option pp.fullNames true in
#print SevenColumn.Certificate.lookup
