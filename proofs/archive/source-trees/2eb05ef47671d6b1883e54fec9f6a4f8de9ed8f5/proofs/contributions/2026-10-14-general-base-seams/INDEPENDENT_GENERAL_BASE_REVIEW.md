# Independent review of the general-base seam theorem

**Verdict: the written theorem is valid for every integer base
\(b\ge3\), with the stated actual-width reflection.** The base-2
counterexample is valid, and the independent bounded replay passes.
No modification of the producer's proof, source, report, or catalog
was needed.

This review separates the all-base/all-width argument from the finite
arithmetic controls. The catalog alone would not prove the theorem.

## 1. Domain and physical width

The proof assumes a symmetric word \(Q\) of represented width \(L\ge1\),
positive outside coefficient, and coefficients in \([0,2b-2]\).
Column carries are then always 0 or 1. The positive highest original
coefficient ensures normalization has width \(L\) when the terminal
carry is 0 and width \(L+1\) when it is 1. Thus the stated actual width
\(n=L+e\) is correct, including width-1 inputs.

Each isolated block normalization includes its terminal carry at the
next original offset. Its coefficients, and hence those of the raw sum
\(E\), are nonnegative. Since isolated normalization preserves value,
\(E(b)=D(b)<b^n\). A nonzero coefficient of \(E\) at any index at least
\(n\) would contradict that inequality. Reflection at width \(n\) is
therefore well-defined for both words. Leading zero coefficients of
\(E\) inside that width must remain present: trimming them before
reflection would change the assertion.

Odd-center parity is necessary to interpret a symmetric coefficient
word as the digit-pair word of an ordinary integer. It is not used in
the algebraic symmetry argument, so the written theorem correctly
requires it only for that interpretation.

## 2. Reflection and the residual uniqueness step

Let \(c_i\) be the isolated outgoing carry at original column \(i\).
At a seam the raw coefficient includes the preceding block's terminal
carry; away from a seam it includes the ordinary preceding carry.
Consequently, uniformly at every column,

\[
E_i=q_i+c_{i-1}-bc_i,
\qquad E=Q+(x-b)C.
\]

For \(e=0\), symmetry of \(E\) and \(Q\) gives

\[
(x-b)C=(1-bx)x^{L-2}C(x^{-1}).
\]

Evaluation at \(x=1/b\) forces \(C(1/b)=0\); all its coefficients
are nonnegative, so \(C=0\). The calculation remains valid at \(L=1\):
one may regard the displayed reciprocal expressions as Laurent
polynomials evaluated at the nonzero number \(1/b\). Alternatively,
support at actual width already forces the possible terminal carry
to vanish in this case.

For \(e=1\), the longer reflection sends \(Q\) to \(xQ\), giving

\[
(1-x)Q+(x-b)C=(1-bx)x^{L-1}C(x^{-1}).
\]

At \(1/b\), cancellation of the nonzero factor \((b-1)/b\) yields
\(Q(1/b)=(b+1)C(1/b)\).

The isolated incoming bit \(a_i\) is either 0 or 1, including its
reset to 0 at block starts. If \(c_i=0\), then
\(q_i-(b+1)c_i\in[0,b-1]\). If \(c_i=1\), then
\(b-1\le q_i\le2b-2\), so
\(q_i-(b+1)c_i\in[-2,b-3]\). The common interval is therefore exactly
the sufficient bound \([-2,b-1]\).

For \(b\ge3\), no nonzero multiple of \(b\) lies in that interval.
Multiplying the evaluation identity by \(b^{L-1}\) makes the
highest-index residual coefficient the only term visible modulo
\(b\). It must be zero. Removing it and dividing by \(b\) repeats
the argument, so every residual coefficient vanishes. This is a
finite integer argument, with no uniqueness assumption about signed
base expansions beyond the proved interval restriction.

Thus \(Q=(b+1)C\), with coefficients only 0 or \(b+1\). At a zero
coefficient the outgoing carry is 0 regardless of the incoming bit;
at a \(b+1\) coefficient it is 1 regardless of that bit. Actual and
isolated carries coincide for every partition. Since \(C\) is symmetric
at width \(L\), \((1+x)C=D=E\) is symmetric at width \(L+1\).

Using the one-block partition to deduce the complete palindrome
classification is logically sound: that partition has \(E=D\) by
definition, so the implication just established applies directly.
Conversely, each of the two classified cases makes every partition's
raw sum equal to the actual normalization. There is no circular appeal
to an unproved palindrome classification.

## 3. Active-seam cancellation and pair mass

Increasing an isolated block's incoming carry from 0 to 1 changes
outgoing carries exactly through its initial run of \(b-1\)
coefficients. At the first other coefficient, both incoming choices
give the same outgoing carry. This includes the case in which the
entire block is a \(b-1\) run, because its terminal carry is retained.
The stated local identity

\[
N_u(W)-N_0(W)=u+(x-b)u\sum_{i<\ell}x^i
\]

is consequently exact for both input bits.

The sum of actual block normalizations counts each internal seam
carry twice: as the previous block's terminal carry and already within
the next block's retained digits. The full word has only the latter
contribution. Thus this sum is
\(D+\sum_{j>0}u_jx^{s_j}\). These extra terms cancel the local
\(u_jx^{s_j}\) terms, leaving

\[
D-E=(x-b)K.
\]

Evaluation at 1 gives \(E(1)-D(1)=(b-1)K(1)\). Reflection at the same
physical width preserves coefficient sum, so the raw reflected pair
has mass exceeding the actual next pair by precisely
\(2(b-1)K(1)\). This is an exact deficit, not an inequality.

The symmetry theorem implies that either symmetry forces \(E=D\).
Injectivity of multiplication by \(x-b\) over integer polynomials
then forces \(K=0\). Hence \(K\ne0\) certifies a nonpalindromic
output for every base at least 3. It supplies a one-step certificate,
not an invariant for future iterations.

## 4. The binary obstruction is real

For \(b=2\), \(Q=(1,2,1)\), and singleton blocks, sequential carry
normalization gives

\[
D=(1,0,0,1),\qquad E=(1,0,2,0),\qquad K=x^2.
\]

The canonical seed is \(110_2=6\), and its reverse-and-add successor
is \(1001_2=9\). Thus \(D\) is palindromic while \(E\) is not,
and an active seam fails to certify safety in base 2. The carry identity
and its mass deficit still hold.

The same word with a single block makes the failure of the proof's
residual uniqueness step explicit. Its actual/isolated carry polynomial
is \(C=x+x^2\), giving

\[
Q-3C=1-x-2x^2\ne0,
\qquad (Q-3C)(1/2)=0.
\]

The highest residual coefficient is the allowed nonzero multiple
\(-2\) of the base. This identifies the precise reason the base
restriction is necessary, rather than merely displaying a failed
finite control.

## 5. Independent replay and completeness

`independent_general_base_audit.py` imports no producer code. It
normalizes the whole word and every block by the sequential
digit-and-carry recurrence, retaining the final carry even for padded
zero blocks. It checks the displayed polynomial identities
coefficientwise, the seam-term cancellation, the actual and raw
symmetry flags, the classification, the mass and doubled pair-mass
identities, and every supplied ordinary seed realization.

The replay covers all **22,154** retained word/partition controls,
bases 2 through 12 and widths 1 through 4. It also checks **52,734**
block input-response identities derived from those same cases, using
both incoming bits. No larger search is performed.

Catalog completeness is checked independently of the producer's
Cartesian-product enumeration. For fixed base \(b\), the admissible
word counts at widths 1 through 4 are

\[
b-1,\quad2b-2,\quad(2b-2)b,\quad(2b-2)(2b-1).
\]

Each width \(L\) has \(2^{L-1}\) partitions. Thus the total word count
is \((b-1)(6b+1)\) and the word/partition count is
\((b-1)(40b-11)\). Every retained key is valid and unique, and every
per-base/per-width count matches this full domain, proving that no
bounded case was omitted or duplicated.

The six binary failure indices are exactly
`11, 12, 41, 42, 43, 44`, matching the producer's report. All cases for
\(b\ge3\) pass the symmetry equivalence and active-seam implication.
`independent_general_base_audit.json` records the counts, binary
residual witnesses, source/catalog hashes, and final status
`PASS_GENERAL_BASE_REPLAY`.

Run from the repository root:

```sh
python -B proofs/contributions/2026-10-14-general-base-seams/independent_general_base_audit.py
```

The original complete catalog remains the retained record of every
bounded outcome; the audit avoids duplicating it.

## 6. Supplement: the arbitrary-interval carry criterion

The subsequently added interval corollary also passes independent
mathematical review. If the whole output is palindromic, classification
case 1 makes the isolated outgoing carry of every interval zero: with
input zero, coefficients at most \(b-1\) never create a carry. In
classification case 2, a positive terminal coefficient of an interval
must equal \(b+1\). That final column forces outgoing carry one for
either incoming bit, independently of the interval's earlier columns.

Thus any two nonempty intervals with positive terminal coefficients
have equal isolated final carries whenever the whole output is
palindromic. Their inequality certifies a nonpalindromic whole output.
No symmetry, disjointness, canonical leading digit, or partition
condition on the intervals themselves was used. The symmetry and
canonical-width hypotheses remain conditions on the original whole
word \(Q\).

Positivity is necessary for this statement: the decimal word
\((11,11,0,11,11)\) normalizes to 121121, while intervals \((11,11)\)
and \((0)\) have isolated final carries 1 and 0. The latter interval
ends in zero. This example does not contradict the positive-terminal
criterion.

The interval conclusion is a direct all-base consequence of the proved
classification, so no larger bounded catalog is required.
`independent_interval_review.json` pins the supplemented proof version;
the earlier arithmetic audit's recorded proof hash continues to
identify the version reviewed when that replay was performed. Producer
code and catalog bytes are unchanged.
