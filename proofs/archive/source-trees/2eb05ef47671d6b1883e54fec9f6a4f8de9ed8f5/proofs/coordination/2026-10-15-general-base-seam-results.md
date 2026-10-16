# Building on the renewal seam theorem: every base at least three

Integration parent: `831b8c972ea4622ccbe16d82684d7a326ab44523`, branch
`main`. This contribution explicitly builds on the external completed
renewal release at `4c3970c04f7997db76f82a5806168b2d0790cfb3`, including
its positive active-seam criterion, raw-symmetry equivalence and
canonical-component collision safety corollary. The subsequent shared
construction, language and finite-seed-quantifier assignments are
preserved. No result here regenerates a certificate indefinitely.

## Exact arbitrary-partition theorem

In any integer base b >= 3, let Q be a canonical symmetric word with
positive outside coefficient and coefficients in 0,...,2b−2. For its
ordinary-integer pair-word interpretation, require an even center when
the width is odd. Normalize the whole word to D, with actual final width n.
Partition its original columns into arbitrary nonempty consecutive blocks,
normalize each block independently from input carry zero, and include
each isolated terminal carry at its original offset. Let E be their raw sum.

**E is symmetric at width n if and only if D is palindromic. Either
condition forces E=D.** The exact palindrome classes are: every coefficient
is at most b−1 without overflow; or every coefficient is 0 or b+1, with
outside coefficient b+1 and overflow. Reflection always uses the actual
whole output width, including when E has zero padding at its top.

For actual incoming block carries u and each block's initial run of b−1
coefficients, let K be the sum of the corresponding shifted run indicators
weighted by u. The exact identities are
`D=E+(x−b)K` and `D(1)=E(1)−(b−1)K(1)`. They include blocks consisting
entirely of b−1 coefficients and their terminal carries. Thus K nonzero
certifies one nonpalindromic output in every base b >= 3, with reflected
pair-mass deficit `2(b−1)K(1)` at the same actual width.

The [complete all-base proof](../contributions/2026-10-14-general-base-seams/GENERAL_BASE_SEAMS.md)
derives the classification directly. It does not extrapolate it from a
bounded computation or silently reuse a decimal-only assertion.

## Broader domain for the interval carry criterion

Choose any two nonempty coefficient intervals of Q whose terminal
coefficients are positive. Normalize each independently from carry zero.
**Different final carry bits certify nonpalindromic normalization of the
whole word.** The intervals need not be symmetric, disjoint, or a partition.

This extends the other stream's canonical B,H carry-mismatch corollary:
under a palindromic whole normalization, the classification makes every
such isolated interval end with the same carry. Positive terminal values
are essential. The preserved counterexample `Q=(11,11,0,11,11)` produces
the palindrome 121121, while intervals `(11,11)` and `(0)` have different
final carries; the latter has a zero terminal coefficient. This result
does not assert an arbitrary-interval independent-polynomial closure theorem.

## Independent controls, formal support and exceptions

The independent decimal review retains all 58,221 bounded partition
controls. The all-base catalog retains all 22,154 controls in bases two
through twelve and widths one through four, including six binary failures.
An independent replay checks the entire catalog and 52,734 additional
block-response identities. The final supplemented interval proof is
separately hash-pinned; the earlier arithmetic audit's proof hash remains
honest provenance for its earlier version.

Base two is genuinely excluded. The seed `110₂=6` gives pair word
`(1,2,1)` and palindromic output `1001₂`, although the singleton partition
has K=x² nonzero and nonsymmetric raw E. All six binary failures and their
full outputs remain in the complete lossless catalog.

Nine freshly rebuilt Lean declarations check the finite residual-uniqueness
step, reverse-order form, local carry residual bounds and the base-two
obstruction. This is formal support for the written proof; the polynomial
reflection and arbitrary-block seam theorem are not claimed as fully
formalized here. The [formal scope](../contributions/2026-10-14-base-uniqueness-formal/README.md)
and [root review](../contributions/2026-10-15-seam-base-root-review.json)
identify the exact checked sources and artifacts.

## Reproduction from repository root

```sh
python3 -B proofs/contributions/2026-10-14-seam-review/check_raw_symmetry.py
python3 -B proofs/contributions/2026-10-14-general-base-seams/check_general_base.py
python3 -B proofs/contributions/2026-10-14-general-base-seams/independent_general_base_audit.py
python3 proofs/contributions/2026-10-14-base-uniqueness-formal/check.py /absolute/path/to/lean-4.19.0/bin/lean
python3 proofs/verify_release.py
```

Both complete compressed control artifacts, all proof reviews, source
configurations, reports, compiler logs and failures are retained. The
inventory records exact compressed and decoded identities and recovery
commands. These structural one-step results supply no invariant, all-time
safe seed, proof for 196, or resolution of decimal Lychrel existence.
