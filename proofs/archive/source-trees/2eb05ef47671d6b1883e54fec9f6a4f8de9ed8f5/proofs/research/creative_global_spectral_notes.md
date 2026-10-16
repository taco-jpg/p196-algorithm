# A quadratic spectral coordinate retaining every carry

Research derivation. This does not prove decimal Lychrel existence, or the
196 conjecture, and no novelty claim is made.

Let q=(q_0,...,q_{L-1}) be the symmetric mirrored-digit-sum word of a
positive integer, in least-significant-first order. Let c_i be the carry
*leaving* column i, with the incoming carry to column 0 equal to zero.
Let h=c_{L-1}, Q(x)=sum q_i x^i and C(x)=sum c_i x^i. The output digit
polynomial, including the extra leading 1 when h=1, is exactly

    E(x) = Q(x) + (x-10) C(x).

Let Q' be the pair-sum polynomial of the output. Since Q is reciprocal
of degree L-1, reflection of E gives these exact identities:

    h=0: Q'(x) = 2Q(x)+(x-10)C(x)+(x^-1-10)C*(x),
    h=1: Q'(x) = (1+x)Q(x)+(x-10)C(x)+(1-10x)C*(x),

where C*(x)=x^(L-1) C(1/x). All expressions here are polynomials; in the
h=0 expression the apparent x^-1 term is harmless because c_{L-1}=0.

Now take beta=10+sqrt(99), so beta+beta^-1=20. The centered spectral
coordinate Q(beta)/beta^((L-1)/2) is an integer A for odd L and sqrt(22) A
for even L. A is computed entirely with integer recurrences:

    T_0=2, T_1=20, T_(k+2)=20 T_(k+1)-T_k;
    R_0=1, R_1=19, R_(k+2)=20 R_(k+1)-R_k.

For L=2m+1,
    A=q_m+sum_(i<m) q_i T_(m-i).
For L=2m,
    A=sum_(i<m) q_i R_(m-1-i).

This coordinate is lossless for a fixed length: each weight exceeds 18
times the sum of all smaller weights (including the central unit weight
in the odd case). Thus two different q words of the same length have
different A. It is not a fixed numerical residue discarding the interior.

The centered carry polynomial decomposes as follows:

    L odd:  C(beta)/beta^((L-1)/2) = H + sqrt(99) J;
    L even: C(beta)/beta^((L-1)/2) = (sqrt(22) H+sqrt(18) J)/2.

Here H,J are integers, explicitly computed in the companion script.
Reflection negates J and preserves H. Substituting into the polynomial
identities gives a four-case exact integer evolution law:

    L odd,  h=0: A' = 2A + 198J;
    L odd,  h=1: A' = A - 9H + 99J;
    L even, h=0: A' = 2A + 9J;
    L even, h=1: A' = 22A - 99H + 99J.

In particular, the unobstructed no-overflow dynamics is literal doubling
in this coordinate. The entire deviation is the antisymmetric carry
charge J, not an uncontrolled approximation.

A further exact observation isolates the source of J. If q_i != 9, the
carry leaving column i is forced by q_i alone: it is zero for q_i<=8
and one for q_i>=10. Therefore c_i-c_(L-1-i) is supported only at columns
where q_i=9. Neutral-nine runs between opposite carry reset types cause
the correction. There is no assumption that such runs can be ignored.

The integer weights defining J also dominate the sum of smaller weights,
so J=0 exactly when C=C*. In particular, the absence of any 9 entry
implies J=0, although the converse need not hold.

For 196 the initial state is L=3, A=158, H=1, J=0, h=0. The first
nonzero J occurs at n=187088, with L=6, A=3722, H=417, J=419 and h=1:

    A' = 22*3722 - 99*417 + 99*419 = 82082.

That exact correction is why a proof using uninterrupted spectral
doubling would already fail near the start of the 196 orbit.

The known one-step palindrome criterion becomes an algebraic target:

* If h=0, the output is palindromic exactly when C=0, equivalently H=J=0.
* If h=1 and L is odd, it is palindromic exactly when J=0 and A=11H.
* If h=1 and L is even, it is palindromic exactly when J=0 and 2A=11H.

For the overflow cases, J=0 makes C symmetric. Equality of the spectral
coordinates then forces Q=11C, since both q and 11c are admissible
symmetric coefficient words in [0,18], and the spectral map is injective.
The leading carry is one, hence q_0=11, giving exactly the exceptional
0/11 pattern.

The missing proof is an invariant excluding these targets along an
actual orbit. The four-case law is a full-coordinate reformulation, not
yet a closed recurrence on (A,H,J) independent of digit extraction. No
claim is made that it establishes the missing invariant.

Verification: creative_global_spectral.py exhaustively checks all
canonical symmetric q words of lengths 1 through 7 (with even central
coefficient when length is odd), plus 10,000 seeded random longer words.
All 85,447 cases satisfy the exact evolution and carry-support identities.
Those tests check the implementation; the algebra above justifies the
identities for arbitrary length. This result has not been formalized in
Lean in this file.
