# An all-width forbidden-prefix theorem

`PrefixObstruction.lean` proves an exact obstruction for the actual decimal
pair dynamics. It imports only the unchanged standalone
`continuation/LychrelDigitSums.lean`; the finalized overlap-gate source and
its audit are untouched.

For an actual finite pair word, “prefix (a,b,c)” means that its width is
at least three and its full coefficients at indices 0,1,2 are a,b,c.
This includes a center coefficient when the actual width is five. It does
not require three strictly noncentral folded pairs.

## Main results

The checked assertions apply to every admissible finite pair word and
every actual overflow branch:

1. No output of G has prefix (1,6,2).
2. An output with prefix (2,12,4) must have arisen without overflow, and
   its input has prefix (1,6,2).
3. Consequently no two-step output G²(q) has prefix (2,12,4), at any
   finite width. Every fixed target with that prefix has no admissible
   two-step ancestor.

The ordinary-decimal bridge is also checked: for every positive integer n,
every time t>=2, and every canonical representation of T^t(n), its pair
coefficients cannot begin (2,12,4). After one step the pair prefix (1,6,2)
is excluded. These conclusions concern actual integer reversal and
addition, rather than an approximation to the symbolic dynamics.

## Exact local argument and centers

Symmetry rules out output widths three and four for either of these
triples. Therefore the output has width at least five and its input has
width at least four. The existing exact overflow-emission formula applies
at indices 0,1,2 throughout this range, including center positions.

Without overflow, a positive input has outer output coefficient at least
two. Hence outer output one forces overflow and outer input ten. If the
next output coefficient is six, the second input coefficient is five or
fourteen. Its delayed high output digit is at least four; the third
output coefficient, a sum of nonnegative digits, cannot be two.

For prefix (2,12,4), overflow would force outer input eleven. The delayed
high digit would then be at most two, making the second output coefficient
at most eleven, contradicting twelve. In the no-overflow branch, the
successive even emissions 2,12,4 and zero outside carries force input
coefficients 1,6,2 and zero succeeding carries. The first result then
excludes a second predecessor.

Canonical width and digit uniqueness transfer the symbolic obstruction
to any ordinary decimal representation. No leading-zero padding or
infinite-tail identification is used.

## Scope

This is an all-length theorem, with no bounded-search hypothesis. It can
be applied directly to the language branch's words beginning (2,12,4),
and to any later family with that prefix. It does not prove a safe
infinite forward orbit or decimal Lychrel existence.

## Reproduction and retained development

From the project root run:

    python main_existence_attempt/renewal_pass/lean/prefix/check.py /workspace/scratch/fe6abe1df721/lean-runtime/lean

The checker freshly compiles the decimal dependency, `PrefixObstruction`,
and generated `AllAxioms`, auditing all 16 new theorem declarations
transitively. Only `propext`, `Classical.choice`, and `Quot.sound` are
permitted. Custom axioms, placeholders, and `native_decide` are excluded.
`verification.json` is written only after compilation, audit, and source
hash comparisons all succeed. Compiler output is in `compile.log`.

Every development source snapshot and compiler log is retained in
`development_checks/`. The initial arithmetic tactic attempts could not
automatically split the binary backward-carry alternatives. Explicitly
splitting that carry into zero/nonzero cases proved the two possible
second input coefficients. Normalizing the index expression `L-(1+1)`
to `L-2` also made the third-digit bound visible to the arithmetic tactic.
These were proof-script refinements; no counterexample to the theorem
was found or discarded.

The fresh Lean 4.19.0 build and all 16 declaration audits completed with
PASS. The dependency compiled in 53.30 seconds, the new module in 2.05
seconds, and the generated audit in 0.66 seconds. The checked source
SHA-256 is
`1436c61c791f8bb2a982f86c7857c4a6cb70c80280dfdba1aaa4cdfeef2fd97d`.
