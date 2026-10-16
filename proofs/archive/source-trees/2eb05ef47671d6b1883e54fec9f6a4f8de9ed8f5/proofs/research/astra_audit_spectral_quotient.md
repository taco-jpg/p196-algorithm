# Independent audit: universal carry-defect ideal and target saturation

Date: 2026-10-13. Task 7 of the requested Astra research team.

**Verdict.** All three mathematical theorems in
`astra_spectral_carry_quotient.md` are correct. The exact ideal equality,
the ring quotient, and both target-saturation constructions have complete
unbounded proofs. No substantive gap was found. This is an obstruction to
one precisely defined class of algebraic certificates, not a proof of
decimal Lychrel existence or nonexistence.

I inspected the note, its standalone Python implementation, and its recorded
results. I did not modify the canonical files or rerun finite controls;
the audit below is a proof check independent of those controls.

## Canonical words and normalization are genuine finite arithmetic

For length \(L\), a canonical word has integer coefficients
\(0\le q_i\le18\), symmetry \(q_i=q_{L-1-i}\), positive outer
coefficient, and an even center coefficient at odd length. These conditions
are necessary and sufficient for the word to be the mirrored digit sums of
an ordinary positive \(L\)-digit decimal integer. Each pair sum can be
split into two digits in \(\{0,\ldots,9\}\); for the outer pair choose
the leading digit positive. The center condition permits division by two.

Let \(c_i\in\{0,1\}\) be the carry leaving column \(i\), with incoming
carry \(c_{-1}=0\), and let \(h=c_{L-1}\). With
\[
Q=\sum_{i=0}^{L-1}q_ix^i,\qquad C=\sum_{i=0}^{L-1}c_ix^i,
\]
the complete normalized digit polynomial is
\[
E=Q+(x-10)C.
\]
Its constant-through-\(x^{L-1}\) coefficients are ordinary digits, and its
\(x^L\) coefficient is \(h\). If \(h=0\), the top remaining digit is
positive because \(q_{L-1}>0\); hence its exact length is \(L\). If
\(h=1\), its exact length is \(L+1\).

Define \(C^*=x^{L-1}C(1/x)\). Folding the normalized digits at their
**actual output width** gives, respectively,
\[
Q_{\rm new}-2Q=(x-10)C+(x^{-1}-10)C^*,\qquad h=0,
\]
\[
Q_{\rm new}-(1+x)Q=(x-10)C+(1-10x)C^*,\qquad h=1.
\]
These follow directly by computing \(E+x^{L-1}E(1/x)\) or
\(E+x^LE(1/x)\). Thus the two defect formulas use the correct reflection
width; no normalization or overflow assumption is hidden.

## The ideal equality

Let
\[
p=x^2-20x+1,\qquad g=9(x+1),\qquad I=(p,g)
\]
in \(\mathbb Z[x,x^{-1}]\). Because \(C(1)=C^*(1)\), the polynomial
\(C-C^*\) is divisible by the monic polynomial \(x-1\) over
\(\mathbb Z\); write \(T=(C-C^*)/(x-1)\). The identity
\[
(x-10)(x-1)=p+g
\]
then gives the exact certificates
\[
\Delta_0=p(C^*/x+T)+gT,
\qquad
\Delta_1=pT+g(T-C^*).
\]
For the first identity, the remaining \(C^*\) coefficient is
\(x+x^{-1}-20=p/x\). For the second it is
\((x-10)+(1-10x)=-g\). If \(h=0\), the constant coefficient of
\(C^*\) is zero, so \(C^*/x\) is even an ordinary integer polynomial.
These identities prove that **every actual defect** lies in \(I\).
They do not require reciprocal carries or the absence of runs of nines.

The three reverse-inclusion witnesses are correct:

| Input | Mirrored sums | Carry polynomial | Overflow | Defect |
|---|---|---|---|---|
| \(150\) | \((1,10,1)\) | \(x\) | \(0\) | \(p\) |
| \(109\) | \((10,0,10)\) | \(1+x^2\) | \(1\) | \(-g(1+x^2)\) |
| \(159\) | \((10,10,10)\) | \(1+x+x^2\) | \(1\) | \(-g(1+x+x^2)\) |

All are ordinary nonpalindromic inputs. Subtracting the last two defects
gives \(-xg\); since \(x\) is a unit in the Laurent ring, the actual
defects generate \(g\) as well as \(p\). Consequently they generate
exactly \(I\), even if palindromic inputs are excluded.

An optional strengthening is available: the same equality holds in
\(\mathbb Z[x]\). Indeed \(p+x(20-x)=1\), so the presence of \(p\)
and \(xg\) already implies the presence of
\(gp+(20-x)xg=g\). The stated Laurent version requires no correction.

## Quotient ring and interpretation

The exact identity
\[
9p-(x-21)g=198
\]
places \(198=9\cdot22\) in \(I\). Since \(9\) and \(22\) are
coprime, coefficientwise Chinese remaindering decomposes the quotient.
Modulo \(9\), \(g=0\) and \(p=(x-1)^2\). Modulo \(22\), the
coefficient \(9\) is invertible, so \(g=0\) forces \(x=-1\), and
\(p(-1)=22=0\). Thus
\[
\mathbb Z[x,x^{-1}]/I
\cong (\mathbb Z/9)[\epsilon]/(\epsilon^2)\times\mathbb Z/22,
\qquad x\longmapsto(1+\epsilon,-1).
\]
Both displayed images of \(x\) are units, so Laurent localization causes
no further identifications. The ring has \(9^2\cdot22=1782\) elements.

A polynomial maps to
\(Q(1)+Q'(1)\epsilon\pmod9\) and \(Q(-1)\pmod{22}\). Reciprocity
gives the exact integer identity
\(2Q'(1)=(L-1)Q(1)\). Canonical words have even \(Q(1)\) and even
\(Q(-1)\); the latter is zero identically at even length. Therefore at
fixed length the physically possible classes reduce to
\[
s=Q(1)/2\pmod9,
\qquad r=Q(-1)/2\pmod{11}
\]
at odd length, and just \(s\) with \(r=0\) at even length. Division by
two here means division of the known even integer before reduction; it is
well defined from an even class modulo \(22\).

For actual input digits, \(s\) is the digit sum modulo \(9\), and at odd
length \(r\) is the input value modulo \(11\). This establishes the
stated loss of extra spectral information on canonical words.

Multiplication by \(2\) or \(1+x\) gives the coordinate updates
\[
(u,v,w)\mapsto(2u,2v,2w)\quad(h=0),
\qquad
(u,v,w)\mapsto(2u,2v+u,0)\quad(h=1).
\]
The first overflow therefore kills the alternating component permanently.
This is a claim about the mirrored-sum polynomial; an arbitrary even-length
input need not itself be divisible by \(11\).

## Saturation of classes by palindrome-producing inputs

At odd \(L\ge5\), use \(1\le u\le10\), \(0\le b\le9\),
\(a=\min(u,9)\), \(c=u-a\), and
\[
Q=a(1+x^{L-1})+b(x+x^{L-2})+c(x^2+x^{L-3}).
\]
The only overlap is at \(L=5\), when the last pair contributes a center
coefficient \(2c\in\{0,2\}\). All coefficients are at most nine and
the outer coefficient is positive, so these are canonical carry-free
words with palindrome output. Their labels are
\[
(s,r)=(u+b\bmod9,\ u-b\bmod11).
\]
The stated count of classes is exact. Equal labels for two parameter pairs
require
\[
\delta u+\delta b=9k,\qquad\delta u-\delta b=11l,
\]
where \(|\delta u|,|\delta b|\le9\), \(|k|\le2\),
\(|l|\le1\), and \(k,l\) have the same parity. If \(l=0\), the
differences are \((0,0)\) or \((\pm9,\pm9)\). If \(l=\pm1\), then
\(k=\pm1\), forcing one difference to have absolute value ten, which is
impossible. Hence among the one hundred parameter pairs there is exactly
one duplicated class, from \((u,b)=(1,0)\) and \((10,9)\). There are
exactly ninety-nine distinct classes, covering all permitted labels.

At even \(L\ge2\), the words \(Q=a(1+x^{L-1})\),
\(1\le a\le9\), cover all nine labels and are also carry-free. Every
word in these two constructions has an actual **nonpalindromic** input:
use leading digit \(q_0\le9\) and units digit zero, split the other pairs
into digits, and halve any center coefficient.

For the overflow flag as well, let \(L\ge18\) be even or \(L\ge19\)
be odd. Put coefficient eleven in any \(k\in\{1,\ldots,9\}\) symmetric
pairs including the outer pair, zero elsewhere, and zero at any center.
There are at least nine pairs available. Write \(Q=11C\), where \(C\)
is the resulting reciprocal binary word. This is also the **actual** carry
polynomial: an eleven column always emits carry one, and a zero column
always emits carry zero, regardless of its incoming carry.

The normalized digit polynomial is
\[
E=Q+(x-10)C=(1+x)C.
\]
It has coefficients at most two, degree \(L\), nonzero outer digits, and
is reciprocal. Thus it is a genuine palindrome of length \(L+1\), not
merely a formal reciprocal polynomial. These targets have
\(s=11k\pmod9\), covering all nine classes, and \(r=0\): at even
length reciprocity makes the alternating sum zero; at odd length every
nonzero symmetric pair contributes a multiple of \(22\) to \(Q(-1)\).
Leading input digit nine and units digit two realize the outer sum eleven
and ensure a nonpalindromic finite input.

It follows that after the alternating component has vanished, every
retained class at all lengths at least nineteen has palindrome-producing
representatives for either value of the overflow flag. The proof does not
rely on finite enumeration of targets.

## Exact scope of the obstruction

The universal property classifies **commutative-ring homomorphisms** on the
Laurent polynomial ring that annihilate every actual carry defect. Such a
homomorphism factors through the displayed finite quotient, and every
retained physical class at the stated lengths has a next-palindrome
representative. Hence a predicate using only this class and length cannot
guarantee that the next output is nonpalindromic. The overflow-flag extension
holds after the alternating component has died.

This does not classify nonlinear maps, carry-dependent information,
digit-pattern restrictions, or relations holding only along a particular
orbit. It also does not prove that any one orbit visits the target
representatives. No finite decimal Lychrel seed, all-time safe orbit, or
Lean formalization is supplied by these results. These boundaries are
stated correctly in the source report.
