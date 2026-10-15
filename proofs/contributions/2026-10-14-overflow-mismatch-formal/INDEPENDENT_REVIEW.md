# Independent review of the interval overflow criterion

The mathematical statement, Lean source, fresh-build checker, and saved
15-theorem axiom report pass independent review. This review did not repeat
the Lean compilation.

`isolatedCarry` starts its shifted coefficient word with carry zero.
`PositiveTerminalInterval` requires a positive length, containment in the
actual whole-word width, and a positive coefficient at the last column.
It does not require the first coefficient to be positive. The positive
length ensures that `start + (length - 1)` is the genuine terminal column;
the containment premise puts every column used by the shifted carry inside
the supplied whole-word bounds.

The proof separates the exact `BadWord` cases correctly. In the small case,
every zero-start isolated carry is zero by induction. In the zero/eleven
case, terminal positivity forces that terminal coefficient to be eleven;
the incoming carry is bounded by one, so the final carry is one. No interval
symmetry, independence, disjointness, equal length, or partition structure is
used. The proof also does not need whole-word admissibility merely to derive
the equality from `BadWord`.

The numerical bridge obtains `BadWord` from the canonical integer's actual
ordinary next palindrome. Agreement of `q` with the pair word is needed
only below its actual width. The orbit-time corollary obtains a canonical
representation at the requested time and applies the same theorem with
that time's changing width; it assumes the two certificates at that time
and does not assert their persistence.

The three checked examples match their stated roles: an ordinary mismatch,
a genuinely nonsymmetric interval, and an excluded zero-terminal example
whose ordinary output is palindromic. The last example shows why terminal
positivity cannot simply be dropped. The fresh checker audits every public
theorem and rejects proof placeholders or nonstandard axioms. Its saved
report contains 15 declarations and only the standard logical axioms;
the zero-terminal counterexample itself has no axiom dependencies.

Reviewed source SHA-256:
`5b985dad6fcd9a606973c239de5cf041b7bcbcd84542c755de2750f3bd292abc`.
The unchanged base dependency has SHA-256
`ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57`.

This validates the interval implication and its stated limits. It does not
claim a proof of the independent-block polynomial closure equivalence or
an all-time safety invariant.
