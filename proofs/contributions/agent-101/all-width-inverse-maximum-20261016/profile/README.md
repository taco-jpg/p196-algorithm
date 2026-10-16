# Finite profile extraction — Agent #101 / numeric_bridge

Accepted incremental source: `proofs/Agent101ProfileExtraction.lean`, SHA256
`fff6917b100aeec40e353abe4a3f8d27f6561d6859a1feeac9135c22cd8c836b`.

## Actual interface

All declarations are in namespace `Agent101`.

- `exists_coefficientWord_of_reverse q hq`: for every `List Nat` with
  `q.reverse = q`, there are `h c` with `q = coefficientWord h c`.
- `coefficientWord_half_length h c`: the half has length exactly
  `(coefficientWord h c).length / 2`.
- `digitFn_coefficientWord_cons_zero`: a nonempty half exposes its first
  coefficient as digitFn of the complete word at zero.
- `digitPairSums_reverse`: the actual finite pair sums are symmetric.
- `digitPairSums_profile ds`: exact reconstruction plus half-length and
  complete-word length preservation for every digit list, even empty.
- `digitPairSums_profile_cons ds hL`: when `2 <= ds.length`, exposes
  `s :: h`, with `h.length = ds.length / 2 - 1` and
  `s = DecimalDigits.columnSum (digitFn ds) ds.length 0`.
- `reverse_wrapDigits`: the list reversal compatibility used by the proof.

The decomposition accepts arbitrary natural coefficients, not just digits.
Empty and singleton cases are proved separately. No numeric inverse decoder
is defined, no realizability is assumed, and no infinite function tail is
included. The implementation uses existing `exists_wrapDigits` and
`wrapDigits_injective` and well-founded length induction.

## Verification and preserved development

`attempt-002` is an actual Lean 4.19.0 `--trust=0 -j1 -DElab.async=false`
pass, with all seven public theorem axiom prints. `attempt-001` is the
genuine failed source using the Mathlib-style name
`Nat.strong_induction_on`, corrected to the existing core `Nat.strongRecOn`.
Its error-recovery `sorryAx` lines are rejected evidence, not accepted proofs.

The compiler distribution has compiled Std modules but no Std source tree.
`interface-search/` records an environment-level declaration search; it
found `List.reverse_zipWith` and no ready symmetric-list half/center theorem.
The first two saved interface-query invocations failed the output-root check;
the driver then set its subprocess working directory to the isolated build.
No accepted mathematical source uses the query program or imports `Lean`.

The sibling `bounds/module-audit/attempt-002.log` audits all module-origin
logical constants of both new files: 24 theorem constants, including generated
auxiliaries; the superseded private list helper was removed after dependency-reuse review; no new safe definitions/opaques,
no unsafe declarations, and transitive axioms only propext, Classical.choice,
Quot.sound. The source hashes and reused dependency source/object hashes are
in `bounds/INCREMENTAL-VERIFICATION.json`.

This is an author incremental check, reusing the independently checked original
Research closure; it is not described as a fresh full dependency rebuild or an
independent review. Parent owns source publication and independent acceptance.
