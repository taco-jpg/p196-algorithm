# Development and unsuccessful proof routes

All substantive results are in `DelayedOverlapGate.lean`. Nothing in this
directory asserts a recurrent gate or decimal Lychrel existence.

The following compiler attempts are retained in `development_checks/`:

1. Initial carry certificates failed because the arithmetic tactic saw
   the named `Domain` predicate as opaque. Unfolding that definition exposed
   its actual inequalities. This was a proof-script issue, not a numerical
   counterexample to the gate.
2. The corrected initial carry certificates compiled.
3. All four transitions, the p=1,...,4 extension, admissibility, and the
   returned overlap identity compiled.
4. The coefficient defect, normalized digit defect, cancellation, and
   two-step return statements elaborated, but three helper evaluations
   failed because `simp only` left trivial `if True` branches. These were
   resolved by explicitly simplifying `if_true`, `or_true`, and `true_or`.
5. The complete 49-theorem source, including actual ordinary decimal
   realization and safety, compiled. A source snapshot and source hash are
   retained for this attempt and all subsequent development attempts.

The implementation uses a finite carry-certificate theorem and sparse
column functions. It proves the recurrence at every index up to the
arbitrary symbolic width; it does not enumerate a bounded list of spacer
values. The six core pairs are handled simultaneously by inequalities
`u>=1`, `v>=5`, and `u+v<=8`, rather than separate computational instances.

The redundant intermediate comparison word has central coefficient 4v,
which exceeds 18. `redundant_not_admissible` explicitly proves that it is
not an admissible pair word. Its carry normalization is still a well-defined
arithmetic operation and is used only to explain the cancellation.

The constructive branch's p>=5 global-overflow transport identity was
communicated during this work but is not formalized here. This source
restricts the gate to p<=4 and proves all required final carries are zero.
The later first-hit 4/11 classifications and additional delayed-return
cores are separate contributions; no imported assertion about them is used.

The failure to iterate the gate is a checked mathematical result, not a
failed tactic: `return_not_in_domain` proves that the returned parameters
cannot satisfy the same gate's eligibility conditions. A later reset or
another compatible gate is still needed for any renewal construction.
The separate expanded twenty-core written construction does supply a
compatible second gate for the original (1,6) branch; it lies outside the
six-core `Domain` formalized here and does not contradict this theorem.
