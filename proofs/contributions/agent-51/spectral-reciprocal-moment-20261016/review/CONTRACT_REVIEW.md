# Independent contract review: reciprocal coefficient moment

## Verdict and role

**PASS — the proposed contract is mathematically correct and preserves the selected source claim, while giving a valid stronger coefficient-level statement. No mathematical correction is required before implementation.**

This is an independent, read-only semantic review of a proposed contract. The reviewer has not authored proof code, reserved this task, contacted remote coordination, or run a new Lean build. The coordinator is separately refreshing and publishing the protected claim. This review must not be interpreted as ownership publication or successful execution.

Task identifier: `A51-SPEC-RECIPROCAL-MOMENT`. The full dedicated-formalization safeguards continue to apply. The review keeps the existing overflow-saturation proof modules frozen, requires ordinary kernel-checkable proofs, and does not authorize custom axioms, proof holes, or `native_decide`.

## Source and dependency pins

The exact original source is `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/astra_spectral_carry_quotient.md`, Git blob `eac5b8f61385a615d9cc3e7796a4d698c66b716b`, at pinned source snapshot `54ac7c885e54ce74190b85ec82cceca2b23c2e38`. The selected passage immediately after the three quotient coordinates asserts:

    For a reciprocal polynomial of degree L-1,
    2 Q_derivative(1) = (L-1)Q(1).

It then states that the derivative component modulo 9 adds no information when the length is known, because 2 is invertible modulo 9.

The reviewer re-read the surrounding passage and confirmed that the retained source SHA-256 remains `d39212c9ab98f4c5b0fccb733d3b662e41a09804878178c82b8762684e97fb09`.

The reusable finite-sum and literal natural-coefficient polynomial definitions are in the frozen `ResidueSums.lean`, SHA-256 `1333e156e2da6f02a18ff67f83e8ce36955e93c00e425cf67aff713f916140d4`. Their definitions and bridge statements were inspected again for this review.

## Precise intended proposition

Let q be a function from natural indices to integers, let L be a natural number, and assume only

    for every i < L, q(i) = q(L - 1 - i).

Define the mass and first coefficient moment by the finite sums

    mass(q,L)   = sum_{0 <= i < L} q(i),
    moment(q,L) = sum_{0 <= i < L} (integer i) * q(i).

The proposed general theorem is

    2 * moment(q,L) = ((integer L) - 1) * mass(q,L).

The quantification is universal in q and L. Symmetry is a bounded premise, not a property required at every natural index. In particular q outside the finite interval is irrelevant. The multiplier must use integer subtraction `((L : Int) - 1)`, as proposed; the source polynomial degree convention must not silently become natural subtraction in the statement.

The theorem should also be exported in the literal `List.range L` form, using the established `finiteSum_eq_range` bridge. This ensures that the source claim is not confined to an unexplained recursive helper.

## Why the generalization is valid

For L > 0, the map i -> L-1-i permutes exactly the indices below L and is its own inverse. Reindexing the finite moment sum and applying bounded coefficient symmetry replaces the weight i by L-1-i. Adding the original and reflected sums makes every coefficient weight equal to L-1. This is the required identity over integers and does not require nonnegative coefficients, positive mass, or bounded decimal digits.

For L = 0, both sums are empty and equal to zero. The integer multiplier is -1, but the right side remains zero. No index below zero exists, so the symmetry premise is vacuous. The source's canonical positive-width setting is a specialization of this harmless extension, not a reason to exclude L = 0.

For L = 1, the moment is zero and the multiplier is zero; the sole coefficient is unrestricted. For odd L > 1, the central coefficient contributes once, with twice its index equal to L-1. No evenness assumption on that coefficient is needed for this algebraic identity. Such an assumption belongs to physical mirrored digit-sum realizability, a separate property.

The fixed reversal index L-1 is essential. A polynomial that happens to be reciprocal with respect to some different degree does not automatically satisfy this contract at an arbitrarily padded width. The proposed explicit symmetry hypothesis correctly fixes the relevant width and prevents that ambiguity.

The source has canonical natural coefficients and nonzero endpoints, so its actual polynomial degree is L-1. The generalization permits signed coefficients and vanishing endpoints; in those cases the result is an identity for a coefficient word symmetric relative to the specified width. It must not be advertised as a statement that all such words have actual polynomial degree L-1.

## Derivative interpretation

For the formal polynomial

    Q(x) = sum_{0 <= i < L} q(i) * x^i,

coefficientwise formal differentiation gives

    Q'(x) = sum_{1 <= i < L} (integer i) * q(i) * x^(i-1).

Thus Q'(1) is exactly `moment(q,L)`, since the omitted index-zero term would be zero. A direct derivative-at-one definition by the literal weighted coefficient sum is a valid transparent representation of this value. It should be explicitly documented as formal polynomial differentiation and tied to the finite-sum version by a proved equality.

An alternative acceptable representation defines derivative coefficient j as `(integer (j+1))*q(j+1)` and sums the first L-1 such coefficients. If that representation is chosen, the shift and the empty cases must be proved. No real or complex analytic differentiation is required for the source's integer-polynomial assertion.

The derivative must not be defined as half of `(L-1)*mass`, as that would build the desired theorem into the definition. Likewise a generic moment name with no coefficient-derivative interpretation is insufficient for the requested direct source mapping. The proposed explicit coefficient definition avoids both problems.

## Modulo-nine consequence

The proposed consequence is correct for all signed coefficient words satisfying the contract:

    moment(q,L) % 9 =
      (5 * (((integer L) - 1) * mass(q,L))) % 9.

Indeed 2*moment = (L-1)*mass, and 5 is the inverse of 2 modulo 9 because 2*5 = 10 is congruent to 1. This argument uses multiplication in the residue ring, not integer division of an arbitrary residue by 2. It remains valid for negative mass and moment values under Lean's integer remainder at the positive modulus 9.

The same-width determination corollary must quantify over two functions q and r, require bounded symmetry for both at the same L, and assume only

    mass(q,L) % 9 = mass(r,L) % 9.

It can then conclude

    moment(q,L) % 9 = moment(r,L) % 9.

This is exactly the source's claim that the derivative coordinate modulo 9 adds no information once the width and mass coordinate modulo 9 are fixed. Exact equality of the masses is unnecessary. Symmetry for just one of the two words, or equality at unrelated widths without an additional width congruence premise, would not give that result.

## Required natural-coefficient bridge

The existing `polynomialValue` accepts q : Nat -> Nat and is the literal integer sum of `(q(i) : Int) * x^i` over `List.range L`. The natural wrapper must prove, for the same q and L,

    finiteSum (fun i => (q(i) : Int)) L = polynomialValue q L 1.

This follows by the existing finite-list bridge and evaluation of 1^i, but it must be supplied as an actual checked equality. Bounded natural coefficient symmetry transfers by casting to the integer symmetry premise. The resulting source-facing theorem must state the derivative-at-one expression and the actual `polynomialValue q L 1`, rather than silently introducing a second mass semantics.

There is no need to assume decimal digit bounds, canonicality, or positivity in this wrapper. If a later theorem instantiates q with actual decimal column sums, it should use the existing bounded column-sum symmetry interface. That further decimal specialization is optional unless the final claim record adds it explicitly.

## Contract completeness and acceptance obligations

The final protected record should name the actual exported theorem identifiers before acceptance: the integer moment identity, literal finite-list identity, derivative-at-one source statement, modulo-nine formula, same-width determination corollary, and natural-coefficient source bridge. Exact identifiers have not yet been supplied to this reviewer; this is an administrative detail to record, not a mathematical defect in the proposed statements.

Final source review should verify all of the following:

1. The symmetry premise applies only below L, all sum limits agree, and arbitrary signed coefficients and L = 0 remain included.
2. Reindexing really is a finite-range permutation; natural subtraction is justified only at in-range indices.
3. The public derivative expression has the explicit formal coefficient interpretation described above.
4. The same-width result assumes symmetry for both words and equal mass residues at the same modulus.
5. The natural wrapper connects to the frozen literal `polynomialValue`, without changing its definition or any overflow-saturation file.
6. No circular hypotheses, proof holes, new mathematical axioms, or forbidden evaluation shortcuts occur.
7. Exact final sources and their entire local import closure are freshly compiled; the actual endpoint and transitive axiom output is retained and independently reviewed.

No finite computation over selected widths can replace the universal coefficient identity. Kernel-checkable arithmetic for the fixed inverse 5 modulo 9 is acceptable and does not restrict the width quantifier.

## Scope boundary

This task can close the reciprocal first-moment identity and the derivative-coordinate redundancy modulo 9 at fixed width. It does not establish the carry-defect ideal, the quotient-ring isomorphism, the quotient cardinality, all residue realizability claims, or any ordinary-orbit persistence or all-time 196 result. Those statements require their own exact proof chains.

The proposed contract is ready for proof implementation after the coordinator's separate ownership publication succeeds.
