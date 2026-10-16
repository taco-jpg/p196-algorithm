# Existential interval certificates reduce to two singleton columns

Fix an integer base b>=2 and any finite coefficient word Q with entries in
[0,2b-2]. No symmetry, parity, or positive outside assumption is needed for
this reduction. Every interval is nonempty, lies within Q, is normalized
from carry zero, and has a positive terminal coefficient.

The following conditions are equivalent:

1. Two such intervals have different isolated final carry bits.
2. Q contains both a coefficient in [1,b-1] and a coefficient in [b,2b-2].
3. Two singleton intervals have different isolated final carry bits.

Proof. Carries are bits by induction from zero. Under condition 1, name the
intervals so that the first has final carry zero and the second has final
carry one. At the last column of the first interval,
q+incoming < b, so its positive coefficient lies in [1,b-1]. The second
interval must contain a coefficient at least b: if every coefficient were
at most b-1, induction from initial carry zero would keep every carry zero.
Thus 1 implies 2. Singleton normalization gives floor(q/b), so the two
coefficients in 2 witness 3, which directly implies 1.

Accordingly, allowing longer, overlapping, or nonsymmetric intervals gives
more ways to present a certificate, but does not enlarge the class of words
for which some unequal-carry certificate exists. The arbitrary-interval
formal theorem remains useful when a block decomposition already supplies
its carries. It should not be described as a stronger existential detector
than the two singleton condition.

## Every active-seam certificate is included

Suppose any consecutive partition has nonzero active-seam polynomial K,
as defined in the general-base seam theorem. A contributing block has
actual incoming carry one and a nonempty initial run of coefficients b-1.
Such a run supplies a positive coefficient in [1,b-1]. Since the actual
whole-word carry starts at zero, a carry one anywhere requires an earlier
coefficient at least b, by the same induction just used. Thus condition 2
holds, and two singleton intervals already have unequal isolated carries.

The inclusion is strict. In decimal take Q=(2,2,18,2,2), realized by seed
22900. The singleton coefficients 2 and 18 have carries zero and one.
But Q contains no coefficient 9, so every block's initial-nine run is empty
and K=0 for every partition. The next output is 23822, nonpalindromic.
This is the external renewal collision example, now interpreted as a strict
inclusion between the two existential safety criteria.

For a canonical symmetric whole pair word in every base b>=3, condition 2
excludes both immediate-palindrome classes: the high coefficient excludes
all coefficients<=b-1, while the positive low coefficient excludes the
{0,b+1} class. Therefore conditions 1--3 certify one nonpalindromic output.
The preceding algebraic reduction itself also holds in binary, but this
safety consequence does not: Q=(1,2,1) has the two singleton carries and
normalizes to the palindrome 1001 in base two.

Neither criterion is forward invariant. The all-base family
B=(b,b), H=(b-1)^(2m), Q=BHB from
`../2026-10-15-seam-persistence-obstruction/SEAM_PERSISTENCE_OBSTRUCTION.md`
has both criteria and arbitrarily large K(1), yet its second ordinary
output is a palindrome. Its updated pair word has no high coefficient,
so condition 2 vanishes immediately.

This proof uses only carry induction and the already established exact
palindrome classification. It introduces no additional finite search and
makes no claim about an infinite orbit or seed 196.

## Relation to the complete one-step classification

For canonical symmetric Q in base b>=3, the exact complete safety test is:
there is a coefficient at least b, and there is a coefficient outside
{0,b+1}. This is simply the negation of the two palindrome-predecessor
classes, not a new invariant. Mixed positive-low/high coefficients satisfy
that test, but are not necessary. For example, decimal Q=(12,12) normalizes
to 132, which is nonpalindromic, while every positive-terminal interval
has carry one and there is no active seam. Thus the containments are strict:
active-seam certificate implies existential interval mismatch, which implies
one-step safety; neither implication is an equivalence.
