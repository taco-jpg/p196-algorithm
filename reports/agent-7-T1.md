# Agent 7: neutral-interface normal form in every base (T1)

Status: **PAPER PROOF**, with independent **COMPUTED** finite checks and positive
checks against existing Lean-source certificates. The new theorem itself is
**NOT LEAN-VERIFIED**. This is a necessary structural restriction; **no base-10
Lychrel number or obstruction to all decimal certificates is claimed**.

Primary sources: lean/P196/Drafts/Agent120NeutralBandCalibration/{A120Base,
A120Template,A120Certificate}.lean; calculation/neutral_band/README.md.
Coordination and complete independent decimal proof: issue #289, review issue #301.

## Definitions and exact statement

Fix any base b >= 2. Set h=b-1. For a valid Agent120.Neutral.Hyp
interface, e=e1(B), f=e2(B,C)=1-e, and g=gam(B,C) are bits. Define

    P_a(C) = h^a ++ C ++ h^a
    Q_a(B) = B ++ h^a

The exterior coefficient list is least significant first. A checked
cycle has symmetric center states because each nextC is symmetric and
symmetric trims preserve symmetry. No valid center can consist only of
neutral coefficients h: an h-run transmits its entering carry and
therefore fails e!=f.

**Theorem A (padding conjugacy).** For every a>=0 and both possible
overflow bits,

    nextC(b,B,P_a(C)) = P_a(nextC(b,B,C))
    nextB(b,Q_a(B),C) = Q_a(nextB(b,B,C)).

The relevant carries e,f,g are unchanged by this padding.

**Theorem B (cycle normal form).** Every checked finite cycle is
equivalent to another checked cycle with the same number of phases,
the same carry/overflow stream, the same total u and v, and with
all of the following:

* No center state has neutral h coefficients at its first/last positions.
* No exterior state has a neutral h coefficient at its last position;
  an empty exterior state is permitted.
* Every overflow edge has **u=v=0**.

If the original source/target trims are u_i,v_i, writing each
B_i=Q_{q_i}(E_i) and C_i=P_{a_i}(D_i) with maximal neutral padding
gives new trims

    U_i = u_i + q_(i+1) - q_i >= 0
    V_i = v_i + a_(i+1) - a_i >= 0.

They telescope on a cyclic chain: sum U = sum u and sum V = sum v.

**Theorem C (precise normalized positive-trim gates).**
Define

    L = floor((b-2)/2)       tL = (b-2) mod 2
    H = floor((3*b-1)/2)     tH = (3*b-1) mod 2.

A normalized edge with positive exterior trim U>0 necessarily has
g=0, a nonempty exterior E, and either

    (e, E.last, carry into last E coefficient) = (0,L,tL), or
    (e, E.last, carry into last E coefficient) = (1,H,tH).

A normalized edge with positive center trim V>0 necessarily has g=0,
a nonempty symmetric center D, and either

    (e, D.head, carry into last D coefficient) = (0,H,tH), or
    (e, D.head, carry into last D coefficient) = (1,L,tL).

These are **necessary**, not sufficient, conditions. In base 10 the
first-trim thresholds are L=4, H=14, and tL=0, tH=1. Further
base-10-only double-trim restrictions appear in review issue #301;
do not extend the two-coefficient formula to all odd bases.

## Proof of Theorem A (arbitrary padding length)

The base-generic neutral-run lemma norm_replicate_neutral proves,
inductively for all a, that normalizing h^a with entering binary carry c
emits [h*(1-c)]^a and returns c unchanged. Put x=h*(1-e),
y=h*(1-f). Since f=1-e, x+y=h. The corresponding normalizations are

    DB(Q_a(B)) = DB(B) ++ x^a
    DR(Q_a(B)) = y^a ++ DR(B)
    DC(P_a(C)) = x^a ++ DC(C) ++ y^a.

For g=0, the mirrored pointwise additions defining nextB and nextC
put an identical x+y=h in every appended/outer padded position,
leaving the unpadded positions unchanged. For g=1, nextB zips
(DB++[x]) with (1::reverse DR), and nextC zips (DC++[y])
with its reverse. The extra terminal coefficient occupies the same
position before/after padding, and the a peripheral positions still
sum x+y=h. The final carry g remains the same because both padded
neutral runs transmit the entering carry. Both identities follow for
arbitrary a. These steps are purely list arithmetic, not heuristic
inferences about numeric reverse-and-add.

## Proof of Theorem B (nonnegative trims, including empty B)

Every center C_i decomposes uniquely as P_(a_i)(D_i), where D_i is
nonempty, symmetric, and starts with a non-h coefficient. Using
Theorem A and the old edge equality,

    P_(a_i)(nextC(D_i)) = P_(v_i+a_(i+1))(D_(i+1)).

If a_i exceeded v_i+a_(i+1), the right side would have a non-h
coefficient exactly where the left side still has h. Contradiction.
Thus V_i>=0 and cancellation gives the normalized center edge.

Likewise B_i=Q_(q_i)(E_i) with E_i empty or ending in non-h, and

    Q_(q_i)(nextB(E_i)) = Q_(u_i+q_(i+1))(E_(i+1)).

If E_(i+1) is nonempty, a negative U_i would force its last
non-h coefficient to equal h. If E_(i+1) is empty, note that
nextB(E_i) cannot be empty: its length is |E_i|+g, and when
E_i=[] the flip gives g=1. Hence simply comparing lengths rules
out U_i<0. Cancellation yields the normalized exterior edge.
Both normalizations preserve all carry bits, so they can be
applied simultaneously and telescope around the cycle.
Everything in the checker (including cycle gain) stays true.

## Proof of Theorem C (complete first trim gates)

For a normalized symmetric center D with c=D[0]=D[-1]!=h,
let t∈{0,1} be the carry entering the final coefficient. Its
outgoing carry f=1-e enforces either c+t>=b (e=0) or c+t<b
(e=1). Its first raw nextC coefficient is

    g=0: (c+e)%b + (c+t)%b
    g=1: (c+e)%b + h*e.

For g=1 this equals h only at c=h, excluded by normal form.
For g=0, setting it equal to h and excluding c=h gives

    e=0: 2*c+t = 3*b-1;
    e=1: 2*c+t = b-2.

Since t is a bit, the two stated (H,tH) and (L,tL) solutions
are forced.

For a normalized exterior E with z=E[-1]!=h, let t be the carry
entering its final coefficient, which exits with e. Its last raw
nextB coefficient is

    g=0: (z+t)%b + (z+1-e)%b
    g=1: h*(1-e) + (z+1-e)%b.

Again g=1 can give h only if z=h, excluded. When g=0,
the equation last coefficient=h gives

    e=0: 2*z+t = b-2;
    e=1: 2*z+t = 3*b-1.

This forces the corresponding thresholds. Empty E cannot trim
because its nextB under flip is [b], not [h].

Thus every normalized overflow edge has both trim counts zero.

## Numerical check, independently implemented

Reproduce from repository root:

    python3 calculation/agent-7/generic_trim.py

The script (standard library only) exhausts B widths <=3,
palindromic C widths <=4, bases b=2..12, and neutral padding
a=0,1,2. It tests conjugacy, carry/overflow preservation, and
the normalized first-trim necessary conditions.

Measured output in local computation:

    ALL CHECKS PASSED: general-base finite bound checks B_pad 123981 C_pad 14520

In a full repo checkout it additionally parses the actual existing
Lean-source cert11/cert17/cert26 edge lists from
lean/P196/Agent213KnownBaseMechanisms/KnownBases.lean. A separate
independent JS arithmetic implementation already replayed these exact
three original and normalized cycles with zero mismatches, with
normalized phase sequences (g,U,V):

    base11:  (0,0,0),(0,1,0),(1,0,0),(0,0,0),(0,1,1),(1,0,0)
    base17:  (1,0,0),(0,0,0),(0,0,0),(0,2,1),(1,0,0)
    base26:  (0,1,0),(1,0,0),(0,1,1),(1,0,0)

All three keep sum U=2 and sum V=1. These known certificates
are Lean-verified in the repository, **but the new normal-form
theorem and transformations here are not kernel-checked**.

On cyclic lengths, the established exact identities
|nextB|=|B|+g, |nextC|=|C|+g yield sum U=sum g,
2 sum V=sum g. Hence any certificate has even total overflow
count in every base; the normal form further puts every trim on
a non-overflow step.

## Limitations

No new decimal cycle was found. No assertion about unbounded
B/C cycle nonexistence, candidate 196, or an all-base negative
is made. Computed bounded tests only corroborate, not prove,
the width-free list identities. A new Lean theorem and verification
through python3 tools/verify.py --changed have not been run.
