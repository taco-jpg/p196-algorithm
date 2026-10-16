# Zero-spacer collision: exact carry response, locality, and closure classification

This note treats the boundary omitted by the separated-block theorem:

\[
Q=BHB,
\]

where \(B,H\) are canonical symmetric decimal pair words and no zero spacer
remains. It proves an exact all-length collision formula and a necessary
and sufficient condition for independent pair updates to remain exact.
It does not claim a repeatable reset, infinite safety, or a result for 196.

All coefficient words are ordered from least to most significant position.
Write \(N(W)\) for complete decimal normalization, including final overflow,
and \(G(W)=N(W)+\operatorname{rev}(N(W))\).

## 1. Fixed-width incoming-carry response

For a word \(W\) of width \(w\), let \(D_W^c\) be its \(w\) retained decimal
digits when normalized with incoming carry \(c\in\{0,1\}\), and let
\(f_W(c)\) be its outgoing carry. Define \(k_W\) to be the length of its
initial run of coefficient 9, allowing \(k_W=w\). Put

\[
S_k(x)=\sum_{i=0}^{k-1}x^i,\qquad
I_W=\begin{cases}1&\text{if every coefficient of }W\text{ is }9,\\0&\text{otherwise.}\end{cases}
\]

Then exactly

\[
\begin{aligned}
f_W(c)&=f_W(0)+cI_W,\\
R_W(x):=D_W^1(x)-D_W^0(x)
&=1+(x-10)S_{k_W}(x)-I_Wx^w.
\end{aligned}
\tag{1}
\]

Equivalently, when \(k_W<w\), the changed digits are -9 at every initial
9, +1 at the first non-9 coefficient, and zero thereafter. If \(W\) is all
9s, every retained digit changes from 9 to 0 and the outgoing carry changes
from 0 to 1.

**Proof.** At a coefficient 9, the two possible incoming carries produce
digits 9 and 0, and outgoing carries 0 and 1. At any other coefficient in
\(\{0,\ldots,18\}\), the outgoing carries agree, while the retained digit
for incoming 1 exceeds that for incoming 0 by 1. Once the carries agree,
all subsequent outputs agree. Summing the digit changes gives (1).

Thus every block's carry map is constant 0, identity, or constant 1. The
identity case occurs exactly for an all-9 block. For a symmetric block,
the first non-9 coefficient also determines the constant case: at most 8
gives constant 0, and at least 10 gives constant 1, because the last non-9
coefficient is its mirror. This last observation is convenient but is not
needed for the algebra below.

The coefficientwise response and its connection to actual interval carries
are separately formalized in
[`IncomingCarry.lean`](../2026-10-14-collision-formal/IncomingCarry.lean).
No Lean verification of the complete theorem below is claimed here.

## 2. Exact zero-spacer normalization defect

Let \(b=|B|\), \(m=|H|\), \(K=b+m\), and \(L=2b+m\). The actual boundary
carries are

\[
0\ \longrightarrow\ e=f_B(0)\ \longrightarrow\ h=f_H(e)
\ \longrightarrow\ j=f_B(h).
\]

The actual normalized whole digit width is **\(n=L+j\)**. Define the
formal sum of the separately normalized complete blocks at their original
physical positions:

\[
P(x)=(1+x^K)N(B)(x)+x^bN(H)(x).
\]

This is a redundant coefficient polynomial: an outgoing carry of one
block may overlap a digit of the following block. It is not asserted to
be a decimal digit word. Pad it to width \(n\) for reflection if necessary.
Define the nonnegative propagation polynomial

\[
\boxed{F(x)=e\,x^bS_{k_H}(x)+h\,x^KS_{k_B}(x).}
\tag{2}
\]

Then the exact normalization identity is

\[
\boxed{N(Q)(x)-P(x)=(x-10)F(x).}
\tag{3}
\]

This includes an all-9 core, an all-9 exterior, and a final carry that
creates a new leading digit.

**Proof.** Write \(U=D_B^0\), \(V=D_H^0\), and \(a=f_H(0)\). Direct block
normalization gives

\[
N(Q)=U+x^b(V+eR_H)+x^K(U+hR_B)+jx^L.
\]

On the other hand,

\[
P=U+x^bV+x^KU+ex^b+ax^K+ex^L.
\]

Equation (1) gives \(h=a+eI_H\) and \(j=e+hI_B\). Subtract the preceding
two expressions and substitute
\(R_W=1+(x-10)S_{k_W}-I_Wx^{|W|}\). The terms
\(-eI_Hx^K\) and \((h-a)x^K\) cancel, as do
\(-hI_Bx^L\) and \((j-e)x^L\). What remains is precisely (3).
\(\square\)

### Exact locality, including neutral blocks

Let \(E=(x-10)F\). Its support is contained in the following intervals;
omit an interval whenever its multiplier or its prefix length is zero:

\[
[b,b+k_H]\quad\text{if }e=1,\ k_H>0;
\qquad
[K,K+k_B]\quad\text{if }h=1,\ k_B>0.
\tag{4}
\]

For a nonneutral block, this is its incoming-carry 9-prefix plus its first
non-9 column. For an all-9 core, the first interval includes the entire
core and the first column of the high exterior; the second interval
continues the response if that exterior also starts with 9s. For an all-9
high exterior, the last position is \(L\), the newly created leading digit.

With reflection defined using the **actual width \(n=L+j\)**, put

\[
\mathcal R_n(A)(x)=x^{n-1}A(x^{-1}),\qquad T=P+\mathcal R_n(P).
\]

The exact paired defect is

\[
G(Q)-T=E+\mathcal R_n(E).
\tag{5}
\]

Its support is confined to the intervals (4) and their reflections
\(i\mapsto n-1-i\). Overlapping support may cancel some individual
coefficients. It cannot erase the entire defect when \(F\ne0\).

### Mass rules out hidden one-step cancellation

Evaluation at \(x=1\) gives

\[
\begin{aligned}
\operatorname{mass}(N(Q))&=P(1)-9(ek_H+hk_B),\\
\operatorname{mass}(G(Q))&=2P(1)-18(ek_H+hk_B).
\end{aligned}
\tag{6}
\]

Since \(F\) has nonnegative coefficients,

\[
\boxed{G(Q)=T\quad\Longleftrightarrow\quad ek_H+hk_B=0.}
\tag{7}
\]

In particular, a nonzero boundary-carry response through 9s cannot become
an antisymmetric digit error that disappears under pairing in this same
step. The positive mass loss prevents that cancellation. This statement
does not exclude a later delayed repair after additional iterations.

## 3. Complete classification of independent pair-update closure

The natural independent target, formed from the three component pair
updates at the original physical starts, is

\[
S(x)=(1+x^{b+m})G(B)(x)+x^bG(H)(x).
\]

Again, this is a formal coefficient polynomial; at a seam its coefficients
need not themselves define a canonical pair word.

The following is an exact necessary and sufficient condition:

\[
\boxed{
G(BHB)=S
\quad\Longleftrightarrow\quad
\begin{array}{l}
\text{both }B\text{ and }H\text{ normalize without final overflow},\\
\text{or both outside coefficients }B_0,H_0\text{ are at least }10.
\end{array}}
\tag{8}
\]

Thus mixed independent overflow bits never give this closure. When both
bits are 1, an initial 9-prefix in either block is exactly the remaining
obstruction.

**Proof.** The target has mass \(S(1)=2P(1)\). Therefore (6) shows that
equality requires \(F=0\). This also forces \(j=e\): the only way
\(j-e=hI_B\) could be 1 is an all-9 exterior receiving carry 1, which
would contribute \(hk_B=b>0\) to \(F(1)\).

Let \(a=f_H(0)\). Under \(F=0\), equation (5) yields \(G(Q)=T\), and a
direct reflection of the three independently normalized blocks gives

\[
T-S=x^b\bigl(x^{m+e-1}-x^{m+a-1}\bigr)N(H)(x^{-1}).
\tag{9}
\]

The nonzero polynomial \(N(H)\) cannot cancel this difference in the
Laurent polynomial ring. Hence equality additionally requires \(e=a\).
If both bits are 0, then \(h=0\) and \(F=0\) automatically. If both bits
are 1, then \(h=1\), and \(F=0\) is equivalent to \(k_B=k_H=0\). For a
symmetric block with final overflow 1, absence of an initial 9 is equivalent
to its positive outside coefficient being at least 10: an outside
coefficient at most 8 would force final carry 0, and coefficient 9 would
give a nonempty 9-prefix. These observations prove (8) in both directions.
\(\square\)

## 4. Meaning for the unresolved gate orbit

At the first zero spacer in the \((1,7)\) family, this theorem supplies
the exact collision update, with no omitted dependence on the incoming
carry. It separates two concrete causes of failed independent closure:

1. A carry traverses a 9-prefix, producing the measured mass deficit (6).
2. No such propagation occurs, but the independent component overflow bits
   differ, producing the nonzero reflection displacement (9).

When closure does hold, it is a coefficient-polynomial identity. It does
not restore a positive spacer or return the blocks to the original gate
domain. A recurrence proof still needs an exact safe reset, or a different
invariant that remains valid through all subsequent collisions. No such
all-time claim is supplied here.

## 5. Controls and retained records

Run from the repository root:

```sh
python -B proofs/contributions/2026-10-14-collision/collision_response.py
```

The checker covers every ordered pair of canonical components of widths
at most three: 207 components and **42,849 pairs**. It also checks 3,000
deterministic longer pairs. In every case an actual ordinary seed realizes
\(BHB\), and literal integer reversal and addition verify the digit and
pair formulas, width, mass, and exact closure classification.

`COLLISION_CONTROLS.json` retains the case counts, one full representative
of every carry-type/defect/closure category, and explicit neutral-block
and 9-prefix examples. The checker reproduces the exhaustive catalog and
all longer controls deterministically. These finite controls audit the
implementation; equations (1)--(9) establish the unrestricted theorem.
