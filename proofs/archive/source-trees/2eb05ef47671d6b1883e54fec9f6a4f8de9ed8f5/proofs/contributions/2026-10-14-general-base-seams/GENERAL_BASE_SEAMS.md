# The seam symmetry theorem holds in every base at least three

The independent decimal proof in
[`../2026-10-14-seam-review/RAW_SYMMETRY_REVIEW.md`](../2026-10-14-seam-review/RAW_SYMMETRY_REVIEW.md)
extends to every integer base \(b\ge3\). The restriction on the base is
essential: the corresponding implication fails in base two.

Let \(Q(x)=\sum_{i=0}^{L-1}q_i x^i\) be symmetric, with positive outside
coefficient and \(0\le q_i\le2b-2\). When interpreting \(Q\) as the pair
word of an ordinary integer, additionally require its odd center to be
even. Let \(D\) be its ordinary base-\(b\) normalization, let \(e\) be
the final carry, and let \(n=L+e\) be the actual output width.

Partition the original columns into any nonempty consecutive blocks.
Normalize each block independently from incoming carry zero and include
its terminal carry at its original offset. Their raw sum is \(E\).
Reflection throughout this statement is at the actual width \(n\), even
if \(E\) has leading zero coefficients there:
\(R_nF(x)=x^{n-1}F(x^{-1})\).

**Theorem.** For every such partition and every \(b\ge3\),

\[
E=R_nE\quad\Longleftrightarrow\quad D=R_nD.
\]

Either condition forces \(E=D\). Equivalently, normalization is
palindromic precisely in these two cases:

1. Every \(q_i\le b-1\); there is no final overflow.
2. Every \(q_i\in\{0,b+1\}\) and \(q_0=b+1\); there is final overflow.

## Proof

Let \(c_i\in\{0,1\}\) be the outgoing carry at column \(i\) in its
isolated block normalization, and put \(C(x)=\sum_i c_i x^i\). The
normalization equations telescope to

\[
E=Q+(x-b)C. \tag{1}
\]

All coefficients of \(E\) are nonnegative and \(E(b)=D(b)<b^n\), so
there is no nonzero coefficient of \(E\) beyond width \(n\).

Suppose first that \(E\) is symmetric. If \(e=0\), reflect (1) at
width \(L\). Since \(Q\) is already symmetric, subtraction yields

\[
(x-b)C(x)=(1-bx)x^{L-2}C(x^{-1}).
\]

Evaluate at the nonzero number \(x=1/b\). The right side vanishes,
while \(1/b-b\ne0\), so \(C(1/b)=0\). Its coefficients are
nonnegative; hence \(C=0\). No isolated column carries, so every
\(q_i\le b-1\). Actual normalization also has no carry, and \(D=Q=E\).

If \(e=1\), reflection is instead at width \(L+1\), where
\(R_{L+1}Q=xQ\). The same calculation gives

\[
(1-x)Q(x)+(x-b)C(x)=(1-bx)x^{L-1}C(x^{-1}).
\]

At \(x=1/b\), this becomes

\[
Q(1/b)=(b+1)C(1/b). \tag{2}
\]

Let \(a_i\in\{0,1\}\) be the isolated incoming carry at column
\(i\), reset to zero at each block start. Since
\(c_i=\lfloor(q_i+a_i)/b\rfloor\),

\[
q_i-(b+1)c_i\in
\begin{cases}
[0,b-1],&c_i=0,\\
[-2,b-3],&c_i=1.
\end{cases}
\]

Thus every coefficient of \(Q-(b+1)C\) lies in \([-2,b-1]\).
Multiply (2) by \(b^{L-1}\) and reduce modulo \(b\). Because
\(b\ge3\), zero is the only multiple of \(b\) in that interval.
The highest-index coefficient is therefore zero. Remove it, divide by
\(b\), and repeat. This proves \(Q=(b+1)C\) coefficientwise.

Consequently every coefficient is zero or \(b+1\), and the positive
outside coefficient is \(b+1\). In this case the actual outgoing
carry equals one exactly at the \(b+1\) columns, independently of the
incoming bit. Actual and isolated carries agree. Equation (1) gives
\(D=E=(1+x)C\), symmetric at width \(L+1\).

Applying this implication to the one-block partition \(E=D\) proves
the stated two-case palindrome classification. Conversely, in either
classified case the actual and isolated carries agree for every
partition, giving \(E=D\) and hence the reverse implication. This
completes the proof without assuming the classification in advance.

## Active seams and their mass deficit

For a block starting at column \(s_j\), let \(u_j\) be its actual
incoming carry and let \(\ell_j\) be its initial run of coefficients
equal to \(b-1\), including the whole block if applicable. Define

\[
K(x)=\sum_j u_j x^{s_j}(1+x+\cdots+x^{\ell_j-1}).
\]

The first block contributes zero because its actual incoming carry is
zero. Increasing a block's incoming carry from zero to one propagates
the carry difference through exactly this initial \(b-1\) run; the
first other coefficient resets it. If \(N_u(W)\) includes the terminal
carry of the block normalized with incoming bit \(u\), the exact identity is

\[
N_u(W)-N_0(W)=u+(x-b)u(1+x+\cdots+x^{\ell-1}).
\]

Including terminal carries covers all-run blocks too. The sum of the
actual \(N_{u_j}\) includes each internal seam carry once extra, at
the next block's starting column. These extra terms cancel the
displayed \(u_j\) terms when summing the identities, giving

\[
D=E+(x-b)K,\qquad D(1)=E(1)-(b-1)K(1).
\]

The theorem shows that either symmetry forces \(E=D\), and therefore
\(K=0\), since multiplication by the nonzero polynomial \(x-b\) is
injective over the integers. In particular, **\(K\ne0\) certifies one
nonpalindromic output in every base \(b\ge3\)**. The deficit in the
mass of the next reflected pair word, compared at the same actual
width, is \(2(b-1)K(1)\). The decimal factor 18 is its \(b=10\) case.

## A further consequence of the other stream's new collision criterion

The external renewal release at commit
`4c3970c04f7997db76f82a5806168b2d0790cfb3` proves
[`COLLISION_SAFETY_COROLLARY.md`](../../research/main_existence_attempt/renewal_pass/external_review/COLLISION_SAFETY_COROLLARY.md):
for canonical symmetric decimal blocks \(B,H\), unequal isolated final
carry bits certify safety of the next ordinary output of \(BHB\).
Their positive-outside hypothesis is essential.

The classification above gives a more general interval form, in every
base \(b\ge3\). Choose any two nonempty coefficient intervals of
\(Q\), each with a **positive terminal coefficient**. Normalize each
interval independently from incoming carry zero. If their final carry
bits differ, the actual normalized whole output is nonpalindromic.
The intervals need not be symmetric, disjoint, or a full partition.

Indeed, if the whole output were palindromic, the first classified case
would make every isolated interval carry zero. In the second case a
positive terminal coefficient must be \(b+1\); its outgoing carry
is one for either incoming bit. Thus all such intervals would have
the same final carry. Contraposition proves the criterion.

The external canonical \(B,H\) case follows because their terminal
coefficients are positive. Its excluded-domain example explains the
restriction: in decimal, \(Q=(11,11,0,11,11)\) normalizes to the
palindrome 121121, but intervals \((11,11)\) and \((0)\) have
different isolated final carries. The zero terminal coefficient of the
second interval prevents application of the criterion.

This strengthens the domain of the one-step carry-bit criterion. It
does not assert an independent-block polynomial closure theorem for
arbitrary intervals or preserve the criterion through future updates.

## Why base two is excluded

Take \(Q=(1,2,1)\) in base two, with three singleton blocks. The
ordinary seed \(110_2=6\) has this pair word and

\[
110_2+11_2=1001_2.
\]

The actual output is palindromic, but at its actual width four,

\[
D=(1,0,0,1),\quad E=(1,0,2,0),\quad K=x^2\ne0.
\]

The exact identity \(D-E=(x-2)K\) still holds. Raw symmetry equivalence
and active-seam safety both fail here. In the proof above the residual
coefficient interval becomes \([-2,1]\), which contains the nonzero
multiple \(-2\) of the base; the uniqueness step genuinely fails.

These are one-step structural results. They provide no invariant
preserving active seams through an infinite orbit and no Lychrel witness.

## Bounded controls and reproduction

`check_general_base.py` exhausts all admissible pair words of widths
one through four in bases two through twelve and every consecutive
partition of each word. It checks 22,154 cases using literal integer
normalization, retains every case in `all_controls.json.gz`, and records
the catalog hash and six intentionally retained binary failures in
`verification.json`. It also constructs an ordinary positive seed for
every word and checks its reverse-and-add sum.

The controls check the two polynomial carry identities, the mass
identity, actual reflection width, and both directions of the symmetry
criterion at every base at least three. The all-base and all-width
conclusion follows from the proof above, not this finite catalog.

`independent_general_base_audit.py` independently replays every retained
record by sequential column normalization, with no producer import. It
also checks 52,734 block-response identities and verifies bounded catalog
completeness from closed counting formulas. Its verdict is
`PASS_GENERAL_BASE_REPLAY`; the complete mathematical review is retained
in `INDEPENDENT_GENERAL_BASE_REVIEW.md`.

The critical finite residual-uniqueness step, its reverse-order corollary,
the local carry residual bound, and the base-two obstruction are formally
checked in
[`../2026-10-14-base-uniqueness-formal/SignedDigitUniqueness.lean`](../2026-10-14-base-uniqueness-formal/SignedDigitUniqueness.lean).
All nine supporting declarations pass a fresh Lean 4.19.0 build and axiom
audit. This does not claim a full Lean formalization of the polynomial
reflection or arbitrary-block seam theorem proved above.

From the repository root:

```sh
python -B proofs/contributions/2026-10-14-general-base-seams/check_general_base.py
python -B proofs/contributions/2026-10-14-general-base-seams/independent_general_base_audit.py
```
