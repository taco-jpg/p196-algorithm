# A collision closure defect certifies one safe ordinary step

This deduction combines the other research stream's exact collision
classification, published at commit
`a3914ba08e5facb59699d066fcb69f1bd37b6e6a`, with the exact
immediate-palindrome predecessor classification used in our decimal
formalization. It is an all-length written proof. The new combined
statement has not itself been formalized in Lean.

## Statement

Words below list coefficients from least to most significant position.
Let B and H be nonempty canonical symmetric decimal pair words, with
widths b and m, and let Q=BHB be the pair word of an ordinary integer n.
Canonical means coefficients in 0,...,18, positive outside coefficients,
and an even center coefficient when the width is odd. Let N be ordinary
decimal normalization, including a final carry when present. Define

\[
G(W)=N(W)+\operatorname{rev}N(W),\qquad
S=(1+x^{b+m})G(B)+x^bG(H).
\]

Both additions defining G and S are coefficientwise; S need not be a
canonical pair word. Reflection inside each G uses that block's own
normalized width. Then

\[
\boxed{G(Q)\ne S\quad\Longrightarrow\quad
n+\operatorname{rev}_{10}(n)\text{ is nonpalindromic}.}
\]

Equivalently, let e and a be the final carry bits when B and H are
normalized separately from incoming carry zero. Let k_B,k_H be their
initial runs of coefficient 9, and let h be the actual outgoing carry
from H when its incoming carry is e. Put

\[
F=e x^b\sum_{i<k_H}x^i+h x^{b+m}\sum_{i<k_B}x^i.
\]

Either **F nonzero** or **e different from a** is sufficient for the
next ordinary output to be nonpalindromic. F is the polynomial called K
in our arbitrary-block seam identity.

## Proof

For a canonical symmetric pair word Q, its normalized decimal output is
palindromic exactly in the following two classes:

1. Every coefficient of Q is at most 9.
2. Every coefficient is 0 or 11, and its outside coefficients are 11.

These are the exact no-overflow and overflow palindrome-predecessor
classes, respectively; this criterion includes the actual width and is
used by the ordinary-decimal theorems in `LychrelDigitSums.lean`.

Assume the next output is palindromic. In class 1, both B and H normalize
without overflow. In class 2, the positive outside coefficients of each
canonical block must be 11. Thus B and H both have outside coefficient
at least 10. In either case, the other stream's collision closure
theorem, equation (8) of `COLLISION_RESPONSE.md`, gives G(BHB)=S.
Contraposition proves the boxed statement.

Their equations (6)--(9) additionally give

\[
G(BHB)=S\quad\Longleftrightarrow\quad F=0\text{ and }e=a.
\]

This proves the equivalent sufficient conditions. The proof uses the
positivity of the blocks' outside coefficients; it does not silently
extend the statement to blocks padded by leading zeros. No finite
enumeration or probabilistic premise occurs in the argument. ∎

## Why the overflow mismatch adds information

Take B=(2,2) and H=(18). The whole pair word
Q=(2,2,18,2,2) is realized by the seed 22900. Its ordinary next output is
23822, which is nonpalindromic. Here e=0, a=1, and F=0, whereas

\[
G(Q)=(4,5,16,5,4),\qquad S=(4,4,9,13,4).
\]

Both words have coefficient mass 34. Thus a mass-loss test alone does
not certify this example; the different component overflow bits do.
The active-seam example 99900 -> 100899 has F nonzero and is already an
ordinary-decimal instance of the Lean theorem
`RawSymmetryObstruction.numeric_nonzero_defect_safe`.

This safety criterion is not necessary. For a counterexample, use
B=(1,1), H=(1,10,1): both
components have zero final carry, so closure holds, but normalization
of Q=(1,1,1,10,1,1,1) is nonpalindromic. The realizing seed 1115000
has next output 1120111. The exact example checker retains all inputs
and independently computes the pair words and literal integer steps.

The assumption that H has positive outside coefficients is essential.
If it is dropped, B=(11,11), H=(0) gives the canonical whole seed
99022 -> 121121, a palindrome, despite F=0 and isolated bits e=1,a=0.
Here the zero central normalization makes the unequal-width term vanish,
so G(Q)=S. This excluded-domain control was supplied by an independent
read-only review and is retained alongside the three in-domain examples.
It must not be used to reject the theorem with its stated hypotheses.

## Scope and shared work

This supplies two concrete sufficient causes of one-step safety. It
does not establish that at least one of them is present on every future
iterate, that the block partition regenerates, or that 196 is Lychrel.
Closure in a safe step is possible, as the last example shows. The
remaining all-time obligation is therefore not equivalent to merely
excluding independent closure forever.

The source collision report is published at:

https://github.com/taco-jpg/p196-algorithm/blob/a3914ba08e5facb59699d066fcb69f1bd37b6e6a/proofs/contributions/2026-10-14-collision/COLLISION_RESPONSE.md

The same stream's final finite-family report proves, using its independently
audited finite driver trace, safety through time 10000 for every explicit
seed n_r with r>=5078. The threshold permits zero remaining gap at the
last recorded state; the exact spacer loss there is S_9999=5077. That
finite-horizon theorem is compatible with this corollary and does not
supply its missing infinite-persistence argument.

That historical external handoff also proposed a seven-step return with boundary
carry pattern `00*0*01` and overflow schedule `0010101`. Its bundle labels
this forthcoming rather than certified and supplies no checked reset
source there. Applying this note to such a return requires a precise
definition of the blocks at each step, their positive boundary coefficients,
the actual boundary carries, and preservation of the resulting core
language under the full return. The finite carry pattern alone discharges
none of those all-time obligations.

**Subsequent update.** Commit `6889b717599343b6773d376e728ca5b03cf68527`
then supplied the exact conditional return, padded-middle map, safety
conditions and formal boundary bridge. The next coordination commit
`8a42fe14262fee12ce1c8b40bf25e97b94044742` announced an obstruction to
four consecutive returns. Our independent reconstruction now certifies
that obstruction, including actual overlapping boundaries; see
[`seven_step_graph/ACTUAL_ORBIT_INCLUSION.md`](seven_step_graph/ACTUAL_ORBIT_INCLUSION.md).
Thus this particular clock cannot be made into an indefinitely repeating
invariant. Its padded middle can have zero endpoints, so the positive
canonical-component hypothesis of the present collision corollary must
still not be silently imposed on that different decomposition.
