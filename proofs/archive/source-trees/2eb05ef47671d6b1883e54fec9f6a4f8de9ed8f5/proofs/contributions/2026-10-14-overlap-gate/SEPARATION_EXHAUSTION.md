# Exact separated-block dynamics and finite spacer exhaustion

The remaining delayed-gate core \((u,v)=(1,7)\) admits an exact reduction
while its exterior and central blocks remain separated. The reduction
does **not** remain valid indefinitely for any fixed finite spacer: the
spacer reaches zero within a proved linear bound. This is an obstruction
to permanent separation as a proposed invariant, not a proof that the
whole orbit eventually reaches a palindrome.

The earlier finite-lifetime results in `EXACT_GATE_LIFETIMES.md` remain
unchanged. The all-time status of the remaining family is **UNKNOWN**.

## Exact block theorem

Let \(B,H\) be canonical symmetric pair words, of lengths \(b,m\), and let
\(g\ge1\). Write their coefficient polynomials in low-to-high order and set

\[
Q=B\,0^g\,H\,0^g\,B^R.
\]

Here \(B^R=B\), but the superscript records the reflection in the whole
word. Let \(D_B=N(B)\), \(D=N(H)\), including their final overflow digits.
Let \(e,h\in\{0,1\}\) be their final overflow bits, so their lengths are
\(b+e,m+h\). Set \(\delta=\max(e,h)\). Then exactly

\[
\begin{aligned}
B'&=G(B),\\
H'(x)&=x^{\delta-e}D(x)+x^{m+\delta-1}D(x^{-1}),\\
g'&=g-\delta,\\
G(Q)&=B'\,0^{g'}\,H'\,0^{g'}\,(B')^R.
\end{aligned}
\]

The new block lengths are

\[
|B'|=b+e,\qquad |H'|=m+2\delta-e.
\]

Both new blocks are canonical symmetric pair words. The formula remains
valid at \(g=1\), where it may produce \(g'=0\). It asserts no further
independence once the spacer is zero.

**Proof.** Put \(s=b+g\), \(K=b+2g+m\), and \(L=2b+2g+m\). A positive zero
run absorbs any single outgoing carry before the next block begins.
Consequently the complete normalized whole digit polynomial is

\[
N(Q)(x)=(1+x^K)D_B(x)+x^sD(x),
\]

of length \(L+e\). This remains true for a one-zero gap: an outgoing carry
turns that zero into 1, then the outgoing carry resets to 0. The displayed
digit-block supports are disjoint.

Reflecting in degree \(L+e-1\) pairs the two exterior blocks to
\((1+x^K)G(B)\). The central terms sum to

\[
x^sD(x)+x^{L+e-1-s}D(x^{-1})
=x^{s+e-\delta}H'(x).
\]

The start of this new central block is
\(s+e-\delta=|B'|+g'\), proving the claimed placement and identity. The
three possibilities \((e,h)=(0,0),(0,1),(1,h)\) give the displayed central
width directly. Positivity of the two end coefficients also rules out
trimming the central block to manufacture a larger spacer:

- If \((e,h)=(0,0)\), the endpoints are positive as for an ordinary pair
  update.
- If \((e,h)=(0,1)\), both endpoints equal the final overflow digit 1.
- If \((e,h)=(1,0)\), both endpoints equal \(D(0)>0\). Symmetry and no
  final core overflow force its positive outside coefficient into
  \(\{1,\ldots,9\}\), so its units digit is nonzero.
- If \((e,h)=(1,1)\), both endpoints equal \(D(0)+1>0\).

The coefficients are sums of at most two decimal digits, and the middle
coefficient, when present, is even. These facts establish canonicality.
\(\square\)

## An exact palindrome test during separation

Under the same hypotheses,

\[
N(Q)\text{ is palindromic}
\quad\Longleftrightarrow\quad
e=h,\quad N(B)\text{ is palindromic},\quad N(H)\text{ is palindromic}.
\]

Indeed, in the comparison of the full digit polynomial with its reversal,
the exterior supports are disjoint from both possible central supports,
including when \(g=1\). Equality of the exterior pieces requires
\(D_B=x^{b+e-1}D_B(x^{-1})\). Equality of the central pieces requires

\[
D(x)=x^{m+e-1}D(x^{-1}).
\]

If \(h=1,e=0\), the reversed expression has a nonzero term of degree -1,
so this is impossible. If \(h=0,e=1\), its constant coefficient is zero,
whereas \(D(0)>0\): no final overflow forces the positive outside
coefficient of \(H\) to be at most 9, so its units digit is nonzero. If
\(h=e\), the equality is precisely ordinary palindromicity of \(D\).

This gives a concrete safety condition for the separated dynamics. It
does not establish that the condition continues to hold at every time.

## No fixed finite spacer remains positive forever

The spacer update \(g'=g-\max(e,h)\) is nonincreasing. More strongly, it
loses at least one zero for every exterior overflow. The exterior evolves
autonomously as \(B_{t+1}=G(B_t)\) until separation ends.

An elementary bound is **at most \(5g_0\) updates** before the first zero
spacer. To see this, write \(a_t\) for the exterior block's outside
coefficient. At a nonoverflow step,

\[
a_{t+1}=2a_t+c,\qquad c\in\{0,1\},\qquad 1\le a_t\le9.
\]

Four consecutive such steps force the next outside coefficient to be at
least 16; the following step must overflow. Every five consecutive steps
therefore include an exterior overflow. The initial \(g_0\) zeros cannot
survive \(g_0\) such overflows.

A sharper bound uses the existing lower-width potential from namespace
`DecimalWidthGrowth` in
[`LychrelDigitSums.lean`](../../research/continuation/LychrelDigitSums.lean):

\[
P(a)=
\begin{cases}
4 & a=1,\\
3 & a=2,\\
2 & a\in\{3,4,5\},\\
1 & a\in\{6,7,8,9,10\},\\
0 & a\in\{11,12,\ldots,18\}.
\end{cases}
\]

For every transition, \(P(a_{t+1})+1\le P(a_t)+4e_t\). This follows by
checking the 36 possibilities for \(1\le a\le18\) and incoming high-end
carry \(c\in\{0,1\}\), using the exact outer update

\[
e=\left\lfloor\frac{a+c}{10}\right\rfloor,\qquad
a'=
\begin{cases}
2a+c & e=0,\\
a+1-10\lfloor a/10\rfloor & e=1.
\end{cases}
\]

After \(T\) updates,

\[
T\le4\sum_{t<T}e_t+P(a_0).
\]

If the spacer were still positive at
\(T=4g_0+P(a_0)-3\), then
\(\sum_{t<T}e_t\le g_0-1\), giving \(T\le T-1\), a contradiction. Thus
the first time the spacer is zero is at most

\[
\boxed{\tau\le 4g_0+P(a_0)-3\le4g_0+1.}
\]

The potential is already present in the repository's Lean development.
The new block theorem and this particular separation corollary are not
asserted to have been formalized in Lean.

## Consequence for the \((1,7)\) gate and the remaining obligation

For \(r\ge2\), the gate's initial word has

\[
B_0=(1,1),\quad H_0=(1,8,14,8,1),\quad g_0=r-1.
\]

The formulas above describe its exact dynamics until the first zero
spacer. Since \(P(1)=4\), this occurs by

\[
\boxed{\tau\le4r-3.}
\]

For \(r=1\), the initial spacer is already zero. Increasing \(r\) postpones
interactions but cannot avoid them indefinitely for any fixed finite
member of this family. **Spacer exhaustion is not a palindrome event.**

A proposed infinite-orbit proof for one fixed member must therefore
control the zero-spacer carry interaction and all later iterations, or
prove an exact reset to another safe separated state. The present theorem
supplies no reset. A proof of perpetual safety for the independently
evolving blocks alone would still leave that finite-member obligation
unresolved.

## Controls and exploration record

Run from the repository root:

```sh
python -B proofs/contributions/2026-10-14-overlap-gate/separated_blocks.py
```

This checks all 36 potential transitions, 3,000 deterministic ordinary-
integer block examples (with heavy coverage of the one-zero boundary),
the exact palindrome criterion, and 18 full gate trajectories up to
spacer exhaustion. The latter are controls of the theorem, not all-time
palindrome claims.

`EXPLORATION_RECORDS.json` preserves the initial 96 finite discovery cases
(six gate cores and 16 spacer sizes, at most 300 iterations each), the
31 displayed separated-block states that motivated this reduction, and
the four 12-state samples at \(r=7\) used to discover the exact lifetime
formulas. The latter deliberately include iterations after a first hit;
those later iterations are not being counted as first hits.
Its `null` results mean only that no palindrome appeared within the
specified finite scan. Regenerate that record with:

```sh
python -B proofs/contributions/2026-10-14-overlap-gate/separated_blocks.py --record-exploration
```

No unbounded safety conclusion is inferred from those scans. In
particular, observing long survival for \((1,7)\) does not establish a
finite Lychrel witness.
