# Growing anti-complement walls, collisions, and a precise renewal criterion

Continuation update, 14 October 2026: the all-time finite embedding with
fixed C is now proved impossible for every finite C. It would have constant
digit sum 9*C, contradicting the unbounded digit-sum theorem proved in
`continuation/UnboundedDigitSums.pdf` and formalized in
`continuation/LychrelDigitSums.lean`. The wall identities below remain valid.
Increasing-C renewals are studied in the continuation, but no all-time
renewal construction or decimal Lychrel witness has been obtained.

Status: no finite decimal Lychrel witness and no all-time closure instance.
This note proves exact identities for an aperiodic, growing boundary. It
continues the boundary through arbitrary overlap when an explicit ordering
condition holds. The proof below is algebraic; it is not a Lean formalization.
The accompanying independent decimal-integer controls are finite checks of
the implementation, not an extrapolation to infinite time. No novelty claim
is made.

## 1. One wall that really can grow forever

All digit indices increase from the low end. Let W have length w, entries
in 0,...,18, and satisfy

    W[i] + W[w-1-i] = 18.

W may be empty; otherwise require W[0]>0. Extend it to a two-sided profile

    f_i = 0 (i<0), W[i] (0<=i<w), 18 (i>=w).

Thus f_i+f_(w-1-i)=18 at every integer index. The wall separates a constant
0 background from a constant18 background. Its width and its entire word
are allowed to change at every step; no temporal clock is prescribed.

Let a_i be the usual carry entering column i in a left-to-right scan of f,
with a_i=0 sufficiently far to the left. Put

    a_(i+1) = floor((f_i+a_i)/10),
    r_i = f_i+a_i-10*a_(i+1).

The r profile is0 far left and9 far right. Let b_i be the carry leaving
column i toward the left in the opposite scan, with b_i=1 sufficiently far
right. Let u_i=f_i+b_(i+1)-10*b_i and h=b_0.

The ordinary complementary-column identity gives, at all indices,

    b_i = 1-a_(w-i),
    u_i = 9-r_(w-1-i),
    a_w = 1-h,       r_w = 9-h.

This follows by scanning the complementary coefficients from opposite ends:
coefficients adding to18 and incoming carries adding to1 have total input19,
so their outgoing carries add to1 and output digits add to9.

Define the exact wall update by

    f'_i = r_i+u_(i-h)
         = 9+r_i-r_(w+h-1-i).                       (1)

Then f' is again a wall, of width **exactly w+h**, with entries0,...,18 and
the same anti-complement relation. Its first entry is positive. To check
the endpoints: if h=0, the first output is the sum of the two positive
outer column digits; if h=1, it is r_0+1. Outside the stated interval the
two tails in (1) give0 and18. Anti-complementation gives the other endpoint.
For the empty wall, h=1 and W'=(9).

This defines an unconditional infinite wall orbit from every admissible W.
It is an infinite-background object, **not an ordinary finite integer**.
The finite embedding in the next sections is the essential extra condition.

## 2. Exact transfer with a finite18 reservoir

Take the symmetric finite q word

    q = W ++ 18^M ++ reverse(W),       M>=1.

Every such word has a positive decimal realization, including odd lengths
(the central coefficient is18). The actual finite reverse-and-add update is

    G(q) = W' ++ 18^(M-h) ++ reverse(W'),
    |W'|=|W|+h.                                    (2)

The output width grows by h, while the two walls together grow by2h.
Consequently one reservoir coefficient is consumed at every overflow.
Equation (2) follows either by the carry matching at the two18 ends or by
the finite-difference proof below. It holds for arbitrary W and every M>=1,
including M=1,h=1 when the reservoir vanishes exactly.

This gives a genuine all-length moving-boundary transfer, but cannot renew
a finite reservoir while keeping M>=1. The exact balance is

    M_t = M_0 - number of overflows before t.

The width of an actual positive reverse-and-add orbit is unbounded (in
particular, the existing formalized width theorem in the archive applies).
Thus eventually this representation must reach a collision. Merely choosing
a larger initial M only postpones it.

## 3. Continue through collision by taking a fixed-distance difference

Fix one positive integer C and define

    q_i = f_i-f_(i-C),           0<=i<L=w+C.          (3)

The infinite extension of this q is zero outside these indices. Formula
(3) is symmetric because f_i+f_(w-1-i)=18. Its odd center, when present, is
even. Its first entry is positive. Therefore it is a valid finite q word
exactly when

    f_i >= f_(i-C) at every i.                      (F)

The upper bound q_i<=18 is automatic. For every residue class j modulo C,
telescoping also gives

    sum_(i congruent j mod C) q_i = 18.              (4)

When C=w+M with M>=0, (3) is the non-overlapping form in section2. When
w>C, (3) allows the walls to overlap: in the overlap it subtracts one
piece of W from another. This is an exact spatial ordering condition,
not a demand that a single marked defect survive.

Assume (F), and impose the additional carried-digit ordering

    r_i >= r_(i-C) at every i.                      (R)

Only finitely many comparisons are needed for one step: r is0 left of0
and9 strictly past w, so comparisons with i=0,...,w suffice.

**Finite-difference theorem.** Under (F) and (R), ordinary decimal addition
has output digits

    d_i = r_i-r_(i-C),       0<=i<L+h,               (5)

and its next q word is exactly

    q'_i = f'_i-f'_(i-C),    0<=i<L+h.               (6)

Thus the same C works after this step, even at arbitrary overlap. The new
word is valid because it is the q word of an actual integer.

Proof of (5): put K_i=a_i-a_(i-C). Condition (F), monotonicity of the
decimal carry function, and induction from the zero tail imply K_i in{0,1}.
Subtract the two carried-column equations to get

    q_i+K_i = (r_i-r_(i-C)) + 10*K_(i+1).            (7)

By (R), the displayed remainder is a digit0,...,9. Starting with K_0=0,
uniqueness of decimal division proves that K is the actual carry word.
At the far end K_L=a_L-a_w=1-(1-h)=h. The possible new leading digit is
therefore precisely h. This proves (5) without any approximation.

For (6), apply (1) twice and subtract:

    f'_i-f'_(i-C)
      = (r_i-r_(i-C))
        + (r_(w+C+h-1-i)-r_(w+h-1-i))
      = d_i+d_(L+h-1-i).

That is exactly the mirrored pair-sum definition of the next q word.

## 4. Safety is part of the theorem, not an additional empirical test

Telescoping (5) gives

    sum_(i congruent j mod C) d_i = 9               (every j),
    digit sum(output) = 9C,
    output = 0 modulo (10^C-1).                    (8)

Moreover K contains exactly C ones, one in each output-column residue
class modulo C. For example,

    sum_(i congruent j mod C) K_(i+1) = 1.

These facts rule out both exact decimal palindrome-predecessor cases from
the archive:

* If every q coefficient were<=9, all actual carries starting from0 would
  be0, contradicting the C>=1 carries just proved.
* The exceptional overflow predecessor has all coefficients in{0,11} and
  outer coefficient11. Equation (4) excludes it: a sum of multiples of11
  cannot equal18 in any residue class.

Hence every step satisfying (F) and (R) produces a **nonpalindrome**.

There is also a simpler scalar explanation, supplied by the root audit.
Write S(n) for decimal digit sum. If T(n) is a palindrome, the exact
predecessor criterion gives either S(T(n))=2*S(n) (no overflow and no
carries), or 11*S(T(n))=4*S(n) (the exceptional0/11 overflow word). In
the latter case, writing q_i=11*b_i gives 2*S(n)=11*sum(b_i) and
S(T(n))=2*sum(b_i). Neither equation allows S(T(n))=S(n)>0. Here (4)
gives S(n)=9C and (8) gives S(T(n))=9C, so preservation of digit sum alone
also certifies safety. It does not supply preservation at later steps.

**Concrete all-time sufficient condition.** Supply a finite W_0 and a finite
C>=1 satisfying (F), such that their deterministic wall orbit from (1)
satisfies (R) at every time. Then (6) inductively supplies a valid finite
decimal orbit, and every positive-time value is nonpalindromic. Any decimal
realization n of q_0 gives the actual Lychrel witness T(n).

There is no supplied W_0,C with this all-time property. In particular,
existence of the unconditional infinite wall orbit does not supply it.

## 5. The first collision is completely explicit

At w=C, condition (F) is automatic. In (R) the only possibly failing
comparison is

    r_w=9-h >= r_0.

Consequently closure at this first collision holds **if and only if**

    h=0, or W[0]>=10.                              (9)

For h=1, an outer9 has r_0=9 and fails, whereas an outer value10,...,18
has r_0<=8 and passes. This explicitly identifies the neutral-prefix
overflow branch that the earlier A/B language did not preserve.

For W[0]=9+x, 1<=x<=9, the new wall has width C+1 and starts with x.
The now overlapping central coefficient is

    q'_C = (18-x)-x = 18-2x.                       (10)

When C is even, the odd-width anti-complement wall has central symbol9;
folding (6) gives precisely the earlier B(x,V) relation. Thus the B family
is the first overlap layer of this larger moving-wall construction.

There is an additional exact check one layer later. If w=C+1 and
1<=W[0]=x<=8, (R) holds exactly when x<=4. Indeed its only nontrivial
comparison is

    r_(w-1)=8-x+a_(w-1) >= r_0=x,

with a_(w-1) in{0,1}; this is equivalent to x<=4. The outer9 branches
depend on the next symbols and are not silently included in this rule.
Thus a nonzero marked interior V does not repair the small-root branch's
eventual loss of ordering.

## 6. What failure creates: exact missing carries and a possible renewal

Retain (F) but allow (R) to fail. The same K_i=a_i-a_(i-C) still lies
in{0,1} and has exactly one1 per column residue class. Equation (7) and
the bound r_i-r_(i-C)<=9 imply that the actual finite carry c_i satisfies

    0 <= c_i <= K_i                              (all i).       (11)

This is an induction: if c_i<=K_i, the next ordinary carry is at most
floor((q_i+K_i)/10), which is at most K_(i+1) by (7). In particular, failure
can remove carries from this comparison word; it cannot create extra ones.

Let e_j be the number of missing carries in column residue j. Since K has
one per residue, e_j is0 or1. Summing ordinary digit equations in each
residue class gives the exact output identities

    digit sum in class j = 9+10*e_j-e_(j-1),
    total digit sum = 9*(C+E),      E=sum_j e_j.       (12)

Condition (R) is equivalent to E=0. If E=0, (11) forces equality of both
carry words, and (7) has actual nonnegative digit remainders. If (R) holds,
section3 already proves equality. Thus every ordering failure increases
the digit sum by exactly9 for each missing carry.

This makes a growing-parameter renewal obligation concrete. At failure,
the only possible new balanced parameter is

    C_new = C+E.                                   (13)

To restart the wall model, the actual next q word must have residue sums18
modulo C_new, and its cumulative sums along those classes must define a
valid anti-complement wall with the required ordering. The residue sums
18 are sufficient for this representation when L_new>=C_new: set
f_i=sum_(k>=0)q_(i-k*C_new), using q=0 outside the finite word. Symmetry of
q and the residue sums imply the anti-complement relation about width
w_new=L_new-C_new; nonnegativity gives (F), and the sums18 bound f by18.

No automatic rebalancing theorem is available. Even when failure produces
a nonpalindrome, (13) need not restore the residue balance. A positive
construction could use repeated rebalancing events, but must prove their
occurrence and safety for one finite initial state at all times. Arbitrary
initial reservoirs, or successful finite event chains, do not do that.

## 7. Explicit failures and independent controls

Starting with the empty wall and C=2 gives the actual orbit

    99 -> 198 -> 1089 -> 10890 -> 20691 -> 40293 -> 79497.

The first five updates obey (R). At the final displayed update the wall
is (7,9,11), C=2, and its low digit profile is (7,9,1,9). The comparison
r_2>=r_0 fails. Both theoretical carries are missing; the digit sum rises
from18 to36 and the result79497 is a palindrome.

For C=3, the first failure occurs instead at

    1593405 -> 6637356.

The wall is (6,5,13,12), with low digits (6,5,3,3,9); r_3>=r_0 fails.
One carry is missing, so the digit sum increases from27 to36. The output
is not a palindrome. C_new=4 nevertheless does not re-establish balance:
its low-to-high digits have residue sums (9,11,9,7) modulo4, and its q word
has residue sums (18,22,18,14). Thus failure of this model is not proof
of palindrome attainment.

`astra_moving_boundary_check.py` realizes each admissible q by an ordinary
positive decimal integer, performs literal integer reversal and addition,
and checks the derived wall output. It uses exhaustive anti-complement
walls with half-width<=2 plus reproducibly sampled longer walls. Results:

* 10,555 exact ordered steps: 5,272 overflow and5,283 non-overflow;
* 8,155 positive-reservoir transfers;
* 1,445 first-collision cases, including every failed collision branch;
* 1,009 valid steps with already overlapping walls;
* 11,843 full carry-majorization and missing-carry identities;
* 1,288 valid-input ordering failures;
* 9,214 rejected non-admissible differences, never treated as integers.

The script also records the first failure for the empty initial wall at
C=1,...,24, and saves complete small traces for C=1,2,3. Those trajectories
are controls, not evidence for an all-time claim. No longer196 iteration
was used in this branch.

Reproduce from the parent directory with

    python research/astra_moving_boundary_check.py

Files: `astra_moving_boundary_check.py`, `astra_moving_boundary_results.json`,
and this note. The remaining positive task is exactly one of: preserve (R)
forever for one finite W,C; or give a safe all-time sequence of proved
rebalancing events (13). Neither is established here.
