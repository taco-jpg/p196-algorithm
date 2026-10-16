# Independent review of the singleton reduction

PASS for `INTERVAL_REDUCTION.md`, SHA-256
`2e7e9d3597371f41a65f2d137c0fdba8171bdcb005a63c4fe8bab92603405e65`.

The three equivalent conditions are valid for every finite bounded
coefficient word in every base at least two. The zero-carry interval's
positive terminal coefficient supplies a coefficient in `1..b-1`.
Zero-start normalization of a word entirely below the base never creates
a carry, so the one-carry interval supplies a coefficient at least `b`.
The converse uses the two corresponding singleton intervals. No symmetry,
parity, or positive outside assumption enters this reduction.

An active seam supplies a coefficient `b-1` and an actual incoming carry
one. That carry requires a preceding coefficient at least `b`; hence the
singleton mismatch follows. The strict decimal example `(2,2,18,2,2)`
has no nine at any position, so no partition can have a nonempty
initial-nine run. The second strict example `(12,12)` is nonpalindromic
after normalization, while every nonempty interval has final carry one.
Both strict inclusions are therefore established with their stated domains.

For canonical symmetric whole words, positive outside coefficients make
the negation of the two palindrome classes exactly the final test stated
in the note. The safety implication needs base at least three; the binary
word `(1,2,1)` is a valid explicit counterexample, despite satisfying the
carry reduction. The distinction between the base-independent reduction
and the restricted safety consequence is maintained throughout.

This review introduces no new catalog or graph computation. It confirms
the reductions and their one-step scope, including the stated failure of
persistence shown by the separate all-base family.

## Coordination addendum

The final note has SHA-256
`c40185c3e4b692e11a03533b920f0bc5de29839ab6485ee43215e94cb009413a`.
Its complete previously reviewed bytes are preserved as an exact prefix
and in `review_snapshots/before_external_INTERVAL_REDUCTION.md`, whose
SHA-256 remains
`2e7e9d3597371f41a65f2d137c0fdba8171bdcb005a63c4fe8bab92603405e65`.
Only the coordination appendix was added; the mathematical proof is unchanged.

The appendix correctly distinguishes the external adjacent high-then-nine
condition for active-seam existence from the two arbitrary positive columns
used for isolated-carry mismatch here. An adjacent high-then-nine pair
satisfies the latter test, whereas the preserved strict example has no nine.
Thus the external intrinsic criterion agrees with the proved inclusion and
does not turn either criterion into a persistence theorem. This addendum
checks that reconciliation; it is not a separate audit of the external Lean
package.
