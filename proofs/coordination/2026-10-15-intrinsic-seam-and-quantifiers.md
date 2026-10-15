# Intrinsic seam safety, immediate extinction, and finite-seed quantifiers

Published checkpoint: 15 October 2026. This accepted continuation follows
the [division of work](2026-10-14-continuation-start.md). The observed shared
head advanced during preparation from `921e85d` through the component-bound
commit `831b8c972ea4622ccbe16d82684d7a326ab44523` to the general-base commit
`91e6443f04486b5cdff3ccde3938637ab32ad0e9`. Both new handoffs were read,
and every existing contribution and certificate is preserved. Coordination
uses repository artifacts, not private access to another agent's conversation.

The [component-specific bounds](2026-10-14-component-bounds-results.md)
sharpen the same hypotheses to 94 broader seven-step returns and 98 full
scalar periods. The [general-base seam contribution](2026-10-15-general-base-seam-results.md)
extends the arbitrary-partition theorem to every base at least three and
the carry-mismatch criterion to intervals with positive terminal coefficients.
Their complete supplied numerical certificates, written arguments and scoped
formal support remain intact. We acknowledge these contributions without
claiming a new local replay of their full numerical certificates.

Our complementary work builds on the decimal seam criterion through the
intrinsic high/9 characterization and annihilation below, variable-return
constructions, unrestricted correlated languages and finite-seed quantifiers.
Only the results explicitly audited and included in this checkpoint are
claimed here; later construction and language bundles retain their own scope.

**Decimal Lychrel existence and the 196 claim remain unproved.** These are
supporting theorems and limitations on proposed extraction arguments, not a
positive invariant, repeatable reset, or infinite safe decimal orbit.

## Exact one-step criterion

[IntrinsicSeam.lean](../research/main_existence_attempt/continuation_pass/lean/IntrinsicSeam.lean)
proves that for any finite coefficient word in 0..18, some partition has a
nonzero actual-minus-isolated outgoing-carry defect if and only if, in
least-significant-first order, a coefficient at least 10 is immediately
followed by 9. Equivalently a 9 receives actual incoming carry 1. Singleton
blocks simultaneously maximize every defect coefficient, so searching over
more complicated partitions adds no witnesses. The characterization needs
neither symmetry nor canonicality. The ordinary numeric safety bridge does:
for a canonical mirrored pair word the pattern certifies both a nonpalindromic
input and a nonpalindromic next output. This is one-step safety only.

## Arbitrarily large defect mass can vanish in one update

[SeamAnnihilation.lean](../research/main_existence_attempt/continuation_pass/lean/SeamAnnihilation.lean)
proves the exact family `Q_k=(10,9^k,10)`. Its singleton defect mass is `k`,
while every partition of the next pair word has zero defect. For `k>0`, that
next word is `(1,1,0^(k-1),1,1)`. For even `k=2r>0`, canonical positive decimal
realizations exist, and every realization first reaches a palindrome at time
2. The example `9901 -> 11000 -> 11011` illustrates the phenomenon. The
formal nonvacuity theorem uses constructive canonical realization; the paper's
explicit seed formula is not asserted as a separate Lean identity.

Thus nonzero initial seam mass, even any fixed lower bound on it, does not
give temporal persistence. A useful construction must supply additional
structure that regenerates safety. This does not exclude such stronger
families or alternative safety certificates.

The [formal status](../research/main_existence_attempt/continuation_pass/lean/STATUS.md)
records **31 supporting theorem declarations and 5 definitions** in two modules.
Both the branch clean build and a separate root clean build passed all six
stages and audited all 36 declarations, using only `propext`, `Classical.choice`
and `Quot.sound`. Original failed compiler attempts and their source snapshots
are retained. These counts describe audit coverage, not independent major results.

## What finite-delay evidence cannot extract by itself

The [finite-seed proof](../research/main_existence_attempt/continuation_pass/finite_seed/FINITE_SEED_OBSTRUCTIONS.md)
gives an artificial, fully terminating map that preserves the true immediate
palindrome-predecessor set, strict numeric growth, the stated width bounds,
and, in its strengthened version, complete pair-word equivalence classes.
For every prescribed finite horizon function there is such a terminating map
with asymptotically density-one survival through that horizon. The quantifiers
are **for every horizon, there exists a map**; this is not one fixed map
outlasting every horizon. The map is not actual reverse-and-add outside its
specified exact agreement set. It shows that these shared properties alone
do not extract one infinitely surviving finite seed.

For actual reverse-and-add, a written all-parameter safe-fiber construction
has `9*10^(m-2)` distinct safe predecessors for each stated target, `m>=2`.
Consequently no positive weight nonincreasing with seed size admits a uniform
finite incoming-fiber multiplier on the whole safe set. This leaves other
weights, restrictions and proof methods open. Fixed-target ancestry also has
the explicit bound `t <= min(p-1,5M-1)` for target `p` of width `M`.

The all-parameter arguments were read independently. The executable finite
audit was independently rerun, and the report, script and result hashes match
the [root review](../research/main_existence_attempt/continuation_pass/root_review/finite_seed_review.json).
These finite-seed arguments are written proofs with exact finite controls,
not new Lean formalizations and not a claim that actual reverse-and-add terminates.

## Reuse and remaining work

Use the intrinsic criterion directly when testing an expanding reset or a
correlated invariant language. A proposed all-time construction must explain
why its safety certificate persists at every future step and produce one
finite initial seed. The external stream's existing clock hierarchy and full
graph/kernel integration remain its complementary work; this checkpoint does
not claim to have independently replayed those broader hierarchy certificates.

Run the portable commands in [REPRODUCE.md](../REPRODUCE.md). Exact source,
development-history and build-product coverage is recorded in
[INVENTORY.json](../INVENTORY.json). The still-active `zero_exterior`, language
and other construction follow-ups are outside this accepted snapshot and will
be published in separately reviewed checkpoints, including failures and UNKNOWN.
