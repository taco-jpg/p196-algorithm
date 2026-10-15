# Congruence-preserving delayed paths for the finite-prefix family

**Written proof and checked finite controls.** These are constructed
terminating paths, not actual reverse-and-add trajectories after their
first edge. No all-input countermap, pair-word quotient theorem, or
Lychrel witness is asserted here.

This note follows the external finite-seed obstruction at commit
[`e521255`](https://github.com/taco-jpg/p196-algorithm/commit/e521255),
`proofs/research/main_existence_attempt/continuation_pass/finite_seed/FINITE_SEED_OBSTRUCTIONS.md`.
The exact reviewed note has Git blob
`a56603a78845cb2371137050ea095a2a0d69adad`.
Its countermap preserves the exact immediate-palindrome predecessor set,
growth bounds, and the finite-prefix seed family, but does not preserve
every arithmetic property of true reverse-and-add.

The additional congruences considered here are

\[
 T(n)\equiv2n\pmod9,\qquad
 T(n)\equiv
 \begin{cases}0&\text{if the decimal width is even},\\
 2n&\text{if the decimal width is odd}\end{cases}\pmod{11}.
\]

They follow from (10\equiv1\pmod9) and (10\equiv-1\pmod{11}).
The existing `LychrelDigitSums.lean` already proves the stronger eventual
modulo-11 result `AstraModular.orbit_six_dvd11`: every actual positive orbit is divisible
by 11 after six steps, and this divisibility persists. No new proof of
that fact is claimed here.

## 1. The relevant family reaches residue zero immediately

Write

\[
 k=\lfloor7R/4\rfloor+1,\qquad C_R=2(10^k-1).
\]

Its decimal word is (1\,9^{k-1}\,8). Reversal gives

\[
 T(C_R)=11(10^k-1)=:y_k.
\]

Therefore (99\mid y_k). From this first genuine output onward, both
displayed congruence laws reduce to the same invariant (99\mid n).
This does not imply safety: 99 itself is a palindrome in that residue
class. In particular, these residues do not distinguish the long safe
segments in the finite-prefix construction from the terminating paths
below.

For (k\ge2), the word (y_k) is

\[
 1\,0\,9^{k-2}\,8\,9,
\]

so it has width (k+2), digit sum (9k), and outside pair coefficient
10. It is nonpalindromic and is outside both exact immediate-palindrome
predecessor classes.

## 2. Explicit arbitrarily delayed terminating paths

Fix integers (a\ge5) and (\ell\ge0), and define

\[
 \rho(e)=\begin{cases}89&e\text{ odd},\\989&e\text{ even},\end{cases}
 \qquad c(a,j)=10^{a+j}+990a+\rho(a+j),\quad0\le j\le\ell.
\]

Define the terminal predecessor, with (E=a+\ell+1), by

\[
 \beta(E)=\begin{cases}782&E\text{ odd},\\692&E\text{ even},\end{cases}
 \qquad b(a,\ell)=10^E+\beta(E).
\]

Every (c(a,j)) is divisible by 99: the leading power is congruent to
10 or 1, while the chosen tail is congruent to 89 or 98, respectively.
The term (990a) is divisible by 99. Similarly (b(a,\ell)) is divisible
by 99, because (10+782=792) and (1+692=693).

The inequality

\[
 990a+989<10^{a-1}\qquad(a\ge5)
\]

holds at (a=5) and propagates by induction: increasing its left side
by 990 multiplies it by less than ten. Thus (c(a,j)) has width (a+j+1),
starts with 1, and ends with 9. Its outside coefficient 10 excludes both
immediate-palindrome classes, independently of its interior digits.

The number (b(a,\ell)) starts with 1 and ends with 2. Its outside pair
coefficient is 3. Since (E\ge6), the three-digit tail is separated from
its reflected interior positions; all remaining pair coefficients are
individual digits from that tail or zero. Every coefficient is at most
9. Hence (b(a,\ell)) is nonpalindromic but its **true** next output is
palindromic.

For (R\ge2), set (a=k+2\ge6) and use the path

\[
 C_R,\ y_k,\ c(a,0),\ c(a,1),\ldots,c(a,\ell),\
 b(a,\ell),\ T(b(a,\ell)).
\]

Its first edge is the true reverse-and-add step. Its last edge is also
the true step. Every earlier vertex is nonpalindromic, and its exact
first positive palindrome time is (\ell+4). Thus for every (R\ge2)
and every prescribed finite horizon, choosing a sufficiently large
finite (\ell) gives a terminating constructed path from the same
(C_R) surviving that horizon. The choice (\ell=R) suffices to preserve
the asserted safety through index (R).

Each intermediate edge increases width by exactly one. On the entry
edge, (c(a,0)<11\cdot10^{a-1}\le11y_k). For consecutive chain nodes,
their tails satisfy

\[
 990a+\rho(e+1)<10(990a+\rho(e)).
\]

Thus (c(a,j+1)<10c(a,j)); the strict increase follows from the width
increase. The final edge to (b(a,\ell)) also lies below ten times its
source. The first and last genuine edges satisfy the ordinary bound
(n<T(n)<11n). Consequently every edge has strict numeric growth, the
bound (<11n), and a width increase of zero or one. Along the whole
finite path, width at time (t) is at least the starting width plus
\(\lfloor t/5\rfloor\).

Every edge satisfies both congruence laws. Every source before the last
edge is outside the exact immediate-palindrome predecessor set; the
last source belongs to it and uses its true output. Thus the exact
one-step palindrome predicate is respected on all displayed edges.

For completeness, (R=0) uses the genuine path (18,99). At (R=1),
use (198,1089,10989), followed by the same chain with (a=5) and its
terminal predecessor. It has first hit (\ell+5), and the two extra
entries obey all the stated inequalities and congruences directly.

These are pathwise quantifiers. We do not claim one resulting map on
all positive inputs, arbitrary prescribed delays simultaneously for all
inputs, or preservation of the external note's complete pair-word
quotient strengthening.

## 3. A stronger necessary condition still rejects the sparse jump

The congruences forget the magnitude of the carry count. The original
formal theorem `DecimalMass.digitSum_step_balance` states the exact
digit-sum balance

\[
 s(T(n))+9C(n)=2s(n),
\]

where (C(n)) is the number of outgoing carries. Each of the (L) source
columns contributes at most one, so every genuine transition necessarily
satisfies

\[
 s(T(n))\ge2s(n)-9L.
\]

For (n=y_k), put (a=k+2). This gives the useful bound

\[
 s(T(y_k))\ge9a-36.
\]

The sparse constructed edge (y_k\longmapsto c(a,0)) violates that bound
for every family parameter (R\ge3). At (R=3), (a=8), the target
is (100008909), with digit sum 27, below the required 36. For every
(a\ge9),

\[
 990a+989<10^{a-5}
\]

holds by induction starting from (9899<10000). The target therefore has
digit sum at most (1+9(a-5)=9a-44<9a-36). For the remaining family
parameters (R\ge4), (a\ge10), so this covers all of them.

This supplies a specific additional actual-map condition that defeats
the displayed congruence repair. It is a quantitative restriction, not
merely the modulo-9 consequence of the same identity. It neither proves
that every terminating countermodel preserving this restriction is
impossible nor supplies an infinite actual orbit. No all-time constant
digit-sum invariant is proposed; the original formal development also
proves eventual unbounded digit sum along actual positive orbits.

## 4. Retained finite controls

`check_congruence_paths.py` checks 134 explicit paths comprising 8,259
stored states and 8,125 edges. It covers (R=0,1,2,\ldots,64,128,256),
with the exact finite delays listed in `verification.json`. It checks
ordinary integer reversal on the genuine edges, both congruences on
every edge, growth and width bounds, the exact predecessor criterion,
the first positive palindrome time, and the asserted carry-budget
failure at the sparse jump for every tested (R\ge3).

All generated path states are retained losslessly in `paths.json.gz`;
the report records both compressed and recovered byte counts and
SHA-256 hashes. Recover them with:

```sh
gzip -dc paths.json.gz > paths.json
```

The finite audit passed. The all-parameter arguments above are written
proofs, not new Lean theorems. The parameter range does not stand in for
the written quantifiers, and neither is a proof of decimal Lychrel
existence or of the claim about 196.
