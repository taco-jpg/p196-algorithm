# Arbitrarily many active seams can disappear before a palindrome

The one-step seam and unequal-overflow safety criteria do not persist
automatically. In every base at least three there are canonical three-block
words with unequal isolated overflow bits and an arbitrarily large active
seam mass, yet their second ordinary reverse-and-add output is a palindrome.
The following larger family makes the obstruction explicit.

## A high-coefficient interval with exact first palindrome time

Let the base be an integer \(b\ge3\), and put
\(h=\lfloor(b-1)/2\rfloor\). Let \(Q=(q_0,\ldots,q_{L-1})\)
be a nonempty canonical symmetric pair word in base \(b\), with

\[
b-1\le q_i\le b+h-1\quad(0\le i<L),\qquad q_0\ge b.
\tag{1}
\]

Canonical includes the even central coefficient when \(L\) is odd. Let
\(n\) be any ordinary positive integer realizing this pair word. The first
positive palindrome time of its ordinary reverse-and-add orbit is

\[
\begin{cases}
1,&q_i=b+1\text{ for every }i,\\
2,&\text{otherwise}.
\end{cases}
\tag{2}
\]

The first case can occur only when \(b+1\) lies in the interval (1).
Here "positive" excludes time zero: the pair word alone does not decide
whether the original realizing seed was already a palindrome.
In decimal, (1) says that all coefficients are in \([9,13]\) and the
outside coefficient is at least 10. The unique immediate-palindrome type
inside this interval is the constant word 11.

**Proof.** At column zero, the carry becomes one because
\(b\le q_0\le b+h-1<2b\). At every subsequent column it stays one,
because \(b\le q_i+1\le b+h<2b\). The normalized output \(D\)
therefore has actual width \(L+1\) and digits

\[
d_0=q_0-b,\qquad d_i=q_i+1-b\ (1\le i<L),\qquad d_L=1.
\tag{3}
\]

Every digit is at most \(h\), since \(h\ge1\). Thus the reflected
digit sums in the next reverse-and-add step are at most
\(2h\le b-1\). That addition has no carries, and its symmetric
coefficient word is already an ordinary palindrome with positive endpoints.

It remains to decide whether \(D\) was already palindromic. Equality
of its endpoints forces \(q_0-b=1\), or \(q_0=b+1\). For
\(1\le i<L\), reflection at the actual width \(L+1\) gives
\(d_i=d_{L-i}\). By symmetry of the original width-\(L\) word,
\(q_{L-i}=q_{i-1}\). Equation (3) therefore gives
\(q_i=q_{i-1}\). All coefficients must be \(b+1\).
Conversely, that constant word yields digits 1 at both endpoints and 2
at every internal position, so it is palindromic. This also handles
\(L=1\), where there are no internal equalities. This proves (2).

## Canonical collisions with unbounded active-seam mass

For every \(m\ge1\), take

\[
B=(b,b),\qquad H=(b-1)^{2m},\qquad Q=BHB.
\tag{4}
\]

These blocks and the whole word have even width and positive endpoints.
Their coefficients lie in the allowed pair-word range \(0\) through
\(2b-2\), so every base \(b\ge3\) satisfies the canonical domain.
The isolated final carry of \(B\) is one, whereas the isolated final
carry of \(H\) is zero. The actual carry entering \(H\) is one,
and it propagates across all \(2m\) middle columns.

For either the three-block partition \(B|H|B\) or the singleton
partition, the active-seam polynomial is exactly

\[
K(x)=x^2+x^3+\cdots+x^{2m+1},\qquad K(1)=2m.
\tag{5}
\]

If \(E\) is the sum of isolated block normalizations and \(D=N(Q)\),
the exact seam identity gives

\[
D(1)=E(1)-2m(b-1).
\tag{6}
\]

The corresponding reflected-pair mass deficit is \(4m(b-1)\).
Nevertheless (1) holds and \(q_0=b\ne b+1\), so the first output
is nonpalindromic and the second is a palindrome. In fact \(D\) uses
only the digits zero and one; its next pair word has coefficients at most
two. Every isolated interval in that next pair word therefore has zero
carry, and every block partition has zero active-seam polynomial.
The whole witness vanishes in one update.

An explicit realizing seed is

\[
n_{b,m}=b^{2m+4}-b^{m+2}+b+1.
\tag{7}
\]

Its base-\(b\) digits, from most to least significant, are
\((b-1)^{m+2}0^m11\). Reversing them verifies (4), and the first
output is

\[
N(Q)=b^{2m+2}(b^2+b+1)+b.
\]

This explicit seed is itself nonpalindromic, since its outside digits
are \(b-1\) and 1. Thus its first palindrome time is two even when
time zero is included in the convention.

For example, in decimal with \(m=1\),
\(999011\to1110010\to1210121\).

The shorter family \((b,(b-1)^{2m},b)\) also satisfies (1), and is
realized by \(b^{2m+2}-b^{m+1}+1\). Its output sequence is
\((b+1)b^{2m+1}\) followed by the palindrome
\((b+1)(b^{2m+1}+1)\). This whole word is canonical in every base,
but its singleton exterior \((b)\) is itself a canonical pair word
only for even bases. Family (4) avoids that independent-block parity
restriction entirely.

## Exact second-step criterion on the larger high-coefficient region

There is also an exact local test, without the smaller upper bound in (1).
Suppose instead

\[
b-1\le q_i\le2b-2,\qquad q_0\ge b,
\]

and set \(r_i=q_i-b+1\). The same carry induction gives (3), now
with \(0\le r_i\le b-1\) and \(r_0\ge1\). Pairing those digits
at their actual width gives the exact updated pair word

\[
G(Q)=\bigl(r_0,\ r_0+r_1,\ r_1+r_2,\ldots,
             r_{L-2}+r_{L-1},\ r_0\bigr).
\tag{8}
\]

For \(L=1\), this means \((r_0,r_0)\), with no internal terms.
For an internal position \(i\), the reflected index in the normalized
output is \(L-i\), and original symmetry gives
\(r_{L-i}=r_{i-1}\), proving (8).

Consequently the second ordinary output is palindromic **if and only if**

\[
q_{i-1}+q_i\le3b-3\qquad(1\le i<L).
\tag{9}
\]

Indeed, if (9) holds, all coefficients in (8) are at most \(b-1\),
so normalization has no carry and is already symmetric. If (9) fails,
some internal coefficient in (8) is at least \(b\), whereas the positive
outside coefficient \(r_0\) is at most \(b-1\). These two singleton
intervals have isolated carries one and zero. The previously proved
positive-terminal interval criterion therefore certifies a nonpalindromic
second output. Equivalently, the exact palindrome-predecessor classification
excludes its overflow case because the outside coefficient is below \(b+1\).

Thus, on this entire high-coefficient region, renewal of an unequal-carry
certificate at the very next word is exactly the adjacent-sum failure of
(9). The size of the current seam deficit does not decide it. This is a
one-step formula for the updated word and its next output, not an invariant
keeping future words in this region.

## Consequence for a persistence proof

The external collision criterion and the all-base seam theorem remain
valid one-step results. Equations (4)--(6) show that neither unequal block
overflow bits nor any lower bound on active-seam count or mass deficit
implies safety of the following output. A repeating certificate must also
control the updated word, excluding entry into the low-digit regime in
(3); counting current seam activity alone does not supply that control.

This is an obstruction to a proposed general closure mechanism. It is not
a claim about the future trajectory of 196 or about every active-seam word.

`check_obstruction.py` retains a small exact set of controls, including all
two-column words in the interval (1) for bases 3 through 12, and the explicit
collision families for several widths. It verifies ordinary seeds and both
integer steps, the stated first palindrome times, isolated carry bits, both
partition defects, and mass identities. The all-parameter conclusion follows
from the proof above, not from that finite set.

An independent mathematical review confirmed the carry induction, the
canonical parity conditions, and the exact polynomial (5).

```sh
python -B proofs/contributions/2026-10-15-seam-persistence-obstruction/check_obstruction.py
```

## Coordination with the independently published intrinsic-seam result

While this package was being reviewed, the other stream published commit
`e52125515490b668d14e95b0cf8d31767bcde7c4`. Its
[`intrinsic-seam handoff`](../../coordination/2026-10-15-intrinsic-seam-and-quantifiers.md)
proves the decimal shorter family `(10,9^k,10)`, exact defect mass k,
annihilation in one update, and first palindrome time two for even k>0.
It also gives an intrinsic adjacent high/9 characterization of whether any
partition can have a defect, together with 31 supporting Lean declarations.
The handoff was read at that exact commit. We acknowledge this independently
convergent result rather than claiming the decimal annihilation example as
a separate discovery.

This package supplies the all-base extension with independently canonical
even-width B,H blocks, the broader high-coefficient adjacent-sum iff, and
its separately reviewed 185 controls. The next decimal formal modules
formalize the high-column interval and larger adjacent-sum criterion. The
external finite-seed quantifier analysis is complementary; this package does
not claim a fresh audit of it or of the new external 31 declarations.
The earlier reviewed proof bytes are retained under `review_snapshots/`;
this appended coordination note changes no mathematical statement or control.
