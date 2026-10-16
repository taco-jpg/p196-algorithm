# Collision and regeneration components

Status: exact conditional local identities and an exact **safe two-step
mass-regenerating family**. No closed recurrent family or finite decimal
Lychrel witness has been obtained. These files do not assert existence.

Use least-significant-first pair sums q_i=d_i+d_(L-1-i), and let G be
the exact pair-sum update. N means no overflow; O means one new leading
digit. A power is a repeated q symbol. A bar means coefficientwise
complement x -> 18-x. All displayed integer parameters are finite.

## The neutral-gap collision state

Suppose a known window is

    x, 9^M, 18-x,        M>=1, x in {0,...,18}\{9}.

Its two inward carries are opposite: the low neighbor sends 0 and the
high neighbor sends 1. Under N, if the carries entering the two outside
neighbors are a and 1-a, then the exact window becomes

    f_a(x), 9^M, 18-f_a(x),

where

    f_a(x) = 2x+a+1        for 0<=x<=8,
             2x+a-20      for 10<=x<=18.

This condition on the two exterior carries is essential. If f_a(x)=9,
the known neutral gap gains two symbols; deciding how much farther it
extends requires more wake symbols.

Under O, the exact corresponding inner window is

    o(x), 9^(M-1), 18-o(x),

where

    o(x) = x+10           for 0<=x<=8,
           x-10           for 10<=x<=18.

This formula is independent of the two exterior carry bits. At M=1 the
neutral band disappears and leaves the complementary pair
(o(x),18-o(x)). It does **not** regenerate a long 18 band.

At M=0, an overflow of the complementary central pair creates a central
9, but the new neighbors depend on the next wake symbols. This is a
specific failure of the state consisting only of (x,M) and its current
inward carries. Genuine finite decimal examples have the same core
(2,16), inward carries (0,1), and an overflow, but produce different
fronts:

| seed | next integer | new local window |
|---|---|---|
| 91129910870001 | 101137712862120 | (3,9,15) |
| 91829910170001 | 101837012162820 | (10,9,8) |

The omitted left wake symbol is respectively 1 or 8; its incoming carry
is zero in both cases. Keeping that carry alone therefore does not fix
the new front. This does not exclude a richer correlated wake invariant.

## A corrected safe mass-regenerating gate

For every integer M>=1 let

    P_M = (1,2,4,9^M,14,2,6),
    A_M = P_M reverse(P_M).

Two nonoverflow updates give the exact global identities

    G(A_M) = (2,4,9^(M+1),8,5,12,12,5,8,9^(M+1),4,2),

    G^2(A_M) =
      (4,8,18^(M+1),16,11,5,5,11,16,18^(M+1),8,4).

The q masses are respectively

    18M+58,     18M+80,     36M+124.

Thus the corresponding digit sums are 9M+29, 9M+40, 18M+62. The mass
increase grows with M, so this is not a fixed-digit-mass wall update.

Safety through these two updates is also exact: all three q words have
an odd coefficient (respectively 1, 5, and 5 or 11). A palindrome has
only even pair sums, so every decimal realization of every displayed
state is nonpalindromic. The central 12,12 in the intermediate word also
gives the established high-column predecessor criterion for the second
update. For example M=1 has the finite canonical seed 12499260050000;
only this displayed finite segment, not its infinite continuation, is
certified here.

The center 6,6 is deliberate. The initially considered center 1,1 instead
passes through an all-<=9 q word and produces a palindrome at step 2.
That earlier variant is unsuitable for the existence construction.

The exterior carry requirement is visible in a companion identity.
Replace the second symbol 2 of P_M by 8, keeping the center 6. Calling
the resulting full symmetric word B_M, all the first three steps are N:

    G^2(B_M) =
      (5,12,9^(M+1),17,11,5,5,11,17,9^(M+1),12,5),

    G^3(B_M) =
      (11,5,0^(M+1),16,3,11,11,3,16,0^(M+1),5,11).

Initially A_M and B_M have the same nearest front 4|9^M|14 and the same
two carries entering that front. After one update the farther symbol 2
becomes 4 and sends carry 0, whereas 8 becomes 16 and sends carry 1.
That next carry determines regeneration versus continued neutrality.

## Why a bounded literal wake is not enough by itself

Let U=(14,14,4,4). For every k>=1 and M>=0, a known window

    U^k, 9^M, U^k

entered by carries 0 from the left and 1 from the right becomes exactly

    9^(M+8k)

under N. This is a local identity, conditional on those boundary carries.
For every 4 or 14 column, the base output is 8 and its two neighboring
outgoing carries sum to 1; the specified boundary carries continue this
period-four rule. The middle 9 run is entered by opposite carries and
therefore also becomes 9.

Consequently arbitrarily much prepared wake can disappear into the
neutral gap in one update. A bounded list of nearest wake digits does
not determine the new maximal-gap length or the next exposed front.
A run or substitution description could encode this wake, but no such
description closed under the actual collision dynamics has been found.

## Events in the original Q_m family

Here Q_m=V_m reverse(V_m) is the original 6m+3 wall family, not the gate
family A_M above. Tracking the inherited first 18 band and first neutral
9 band gives the following finite discovery data:

| m | inherited 18 band dies | neutral band dies | complementary collision pair | first loss of complementary center |
|---|---:|---:|---|---:|
| 8 | 27 | 50 | (5,13) | 68 |
| 16 | 58 | 87 | (2,16) | 150 |
| 32 | 107 | 178 | (13,5) | 273 |
| 64 | 219 | 359 | (15,3) | 555 |

At each listed neutral collision the exact O rule above applies. The
complementary region has respectively 7, 22, 37, and 76 surviving pairs
around its center at that moment. Thus the 18 collision does not destroy
all organization, but what survives is a long correlated wake, not a
regenerated long uniform band. These observations do not prove a formula
for the event times or a finite menu for the wakes.

At m=4 the neutral band instead turns into 18,18 at time 27 while its old
length is 2; its boundary neighbors are then 8 and 7, which both send
carry 0. This is a genuine local mass-regeneration event in Q_4, but no
closed return follows from it. The event script stops at these specified
events and does not repeat the earlier bounded balanced-return search.

## Verification and remaining proof obligation

`collision_gate.py` proves the two global family identities by exact
affine runs with M=k+1 for every k>=0. It also checks the general
neutral-gap formulas by exact affine runs for all 18 choices of x and
both carry choices (396 local checks including padding choices and all
four outside-carry combinations for O).
The column derivations above justify arbitrary k in the absorbing-wake
identity; its 16 finite controls are not the proof. Ordinary decimal
arithmetic independently checks 25 global family transitions and the
two collision examples. Results are in `collision_gate.json`.
`collision_events.py` and its JSON record the explicitly finite event
observations for m=4,8,16,32,64; they are not an all-parameter proof.

The unresolved requirement is a finite family whose evolving collision
wake recreates the safe gate with larger parameters, while supplying all
intermediate carries and nonpalindromicity. The gate only supplies one
mass increase. Neither it nor the neutral-front formulas supply a return
equation G^tau(m)(Q_m)=Q_f(m), and no all-time claim follows.
