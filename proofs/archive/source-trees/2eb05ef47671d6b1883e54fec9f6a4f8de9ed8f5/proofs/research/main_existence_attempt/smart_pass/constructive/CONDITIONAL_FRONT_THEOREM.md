# The stated finite moving-front criterion is structurally impossible

**Corrected status: the implication below is sound but vacuous.** The
independent audit in `INDEPENDENT_CRITERION_AUDIT.txt` proves that its
hypotheses are inconsistent for every positive K and p. The specified local
operation cannot satisfy the upper potential in any nonempty finite graph
closed under both overflow values. The same obstruction excludes that
potential for a finite graph closed under the alternating N,O clock.

The original certificate definition and conditional orbit induction are
preserved below so that the failed criterion and its exact scope remain
reviewable. There is no missing certificate to find within this format;
increasing the suffix bound, changing the bulk, or completing a capped
search cannot repair it. A different local operation would be required.
This does not exclude decimal Lychrel numbers or moving-front methods in
general.

## All-K structural obstruction

Let s_v=|S_v|, b=j-s_v, j'=j+Delta, and b'=j'-s_u. In
`suffix_step`, the known output begins at `ns=start+h=b+h`. After deleting
the matching periodic tail, let m be the remaining output length. The code
sets `newcut=ns+m` and retains `out[-K:]`, of length min(m,K). Hence, with
D=m-min(m,K)>=0,

    b' = b+h+D,
    Delta-s_u+s_v = h+D.

This exact identity includes m=0 and an empty retained suffix. Removing
the periodic tail at the right changes m, but never recovers a coefficient
before b+h. Truncating to K can only discard further known coefficients
at the left.

Around any directed cycle C the suffix lengths telescope, so

    sum_C Delta = sum_C h + sum_C D,
    sum_C (2*Delta-h) = sum_C h + 2*sum_C D >= sum_C h.

The proposed upper-potential inequality instead makes the left-hand side
at most zero. Thus every cycle satisfying that potential would have h=0
and D=0 on every edge. No overflow cycle is possible.

Every vertex of the proposed finite nonempty graph has an outgoing h=1
edge for each incoming carry. Fix either carry and repeatedly follow h=1
edges. Finiteness forces an all-h=1 cycle, a contradiction. For the
alternating-clock variant, every clock-compatible cycle also contains
an overflow, giving the same contradiction. This is independent of the
bulk symbols, spatial period, suffix bound, center constraints, lower
potential, or safety witnesses.

Equivalently, any path satisfies

    j_t-j_0 = H_t+s_t-s_0+sum_(i<t) D_i,
    2*j_t-H_t >= 2*j_0+H_t-2K.

An upper potential with bounded range would therefore bound the total
number of overflows. The current operation loses at least one known
column at every overflow; the center moves only half a column. Its bounded
suffix cannot absorb this difference indefinitely. The lower potential
was unnecessary for physical containment: the operation already forces
b_t>=b_0+H_t.

This proof supersedes the *model-level* question whether a capped search
might eventually produce the desired potential. The original cap and
transient records remain unchanged historical execution results; the
proof does not reconstruct those unfinished graphs. Separate free-clock
finite-family SMT queries do not use this local operation and remain
UNKNOWN.

Write G for the exact map on full symmetric decimal pair-sum words, and let
h be its actual leading overflow, 0 or 1. Every coefficient is in 0,...,18.
For a nonneutral periodic row B of period p, let F_h(B) be its exact periodic
bulk update, using the unique carries fixed by its non-9 reset symbols.
All periodic rows below are indexed by absolute spatial index modulo p.

## Historical finite certificate data (inconsistent hypotheses)

Fix positive integers p and K. A vertex v of a finite nonempty graph carries:

- a nonneutral p-symbol row B_v;
- a suffix S_v of at most K coefficients;
- a cut residue r_v modulo p;
- a full-length residue ell_v modulo 2p.

All written coefficients must lie in 0,...,18. At each vertex require the
following center conditions:

    B_v[i] = B_v[(ell_v-1-i) modulo p]    for all i;

if ell_v is odd, also require

    B_v[((ell_v-1)/2) modulo p] is even.

These conditions make a finite central periodic band symmetric with a valid
even middle sum when its full length is odd.

For each vertex v, each h in {0,1}, and each entering low carry a in {0,1},
require an outgoing edge e to some vertex u. Its suffix and periodic row
must be exactly those obtained by the local construction below. It records
an integer cut displacement Delta_e, and must satisfy

    B_u = F_h(B_v),
    r_u = r_v + Delta_e modulo p,
    ell_u = ell_v + h modulo 2p.

Requiring both h values removes a prescribed-clock hypothesis. It is a
conservative condition: an actual finite exterior may permit only one of
those values. A clock-restricted graph instead needs a separate all-time
proof that the finite exterior supplies that clock.

At every vertex require a safety witness:

    some coefficient in S_v or B_v is greater than 9 and different from 11.

Finally supply integer labels R_v and U_v such that every edge e:v->u obeys

    2*Delta_e - h <= R_u-R_v,                         (upper)
    Delta_e - |S_u| + |S_v| >= U_u-U_v.               (lower)

The upper inequality keeps the moving front away from the center. The
lower inequality keeps the retained suffix inside the actual finite word.
Both are finite edge checks. No asymptotic speed assumption is involved.

## The exact local edge operation

Choose any integer cut j congruent to r_v and put b=j-|S_v|. The known
infinite right profile is S_v on [b,j), followed by B_v on [j,infinity).
Its earlier wake is completely unspecified.

Scan from b with low incoming carry a. The high directional carry is fixed
by the periodic tail. The high scan through S_v is consequently exact too.
For nonoverflow, add the two directional output digits at each position.
For overflow, add the low digit at i to the high digit at i-1 and retain
only i>=b+1. This avoids the unspecified high digit just before b.

Only a finite window is needed: after p tail coefficients the low carry has
reset, and one additional column covers the overflow shift. The
implementation uses two periodic blocks plus two extra coefficients.
Beyond that window the output agrees exactly with F_h(B_v).

Starting from the known output interval [b+h,infinity), delete the matching
periodic tail at its right. Let j' be the end of the remaining finite
nonperiodic prefix, or b+h if no such prefix remains. Keep only its final K
coefficients. Those are S_u, and Delta_e=j'-j. Deleting earlier known
coefficients only weakens the description; it creates no constraint on the
unknown wake. An empty suffix is allowed and is handled by the same rule
at the next step.

Thus the edge is an identity for every compatible incoming carry and every
finite wake, as long as the finite central region contains enough of the
periodic tail to reset the carry from the opposite side.

## Historical conditional finite-seed recipe (no certificate can exist)

Pick any vertex v_0. Let R_max=max R_v and U_min=min U_v. Choose an integer
j_0 with the stated cut residue such that

    j_0-|S_(v_0)| >= max(1, U_(v_0)-U_min).

Choose L_0 congruent to ell_(v_0) modulo 2p and large enough that

    L_0-2*j_0 >= 2p+4 + R_max-R_(v_0).

These are explicit finite choices. Form a prefix P_0 of length j_0 that
ends in S_(v_0), begins with coefficient 1, and otherwise has coefficient 0.
There is room for that initial 1 by the first inequality. Define a full word
Q_0 of length L_0 by

    Q_0[i] = P_0[i]                              (i<j_0),
    Q_0[i] = B_(v_0)[i modulo p]                 (j_0<=i<L_0-j_0),
    Q_0[i] = P_0[L_0-1-i]                        (i>=L_0-j_0).

The center conditions make Q_0 symmetric, and its odd middle, if present,
is even. Its outer coefficient is 1. It therefore has an explicit positive
decimal realization n_0: for each opposed pair sum q, choose high digit
min(9,q) and low digit q-min(9,q), and halve the middle sum if necessary.
The proposed decimal witness is the concrete integer

    n_1 = n_0 + reverse(n_0).

## Proof of the sound but vacuous implication

Let n_t be the ordinary reverse-and-add orbit of n_0, Q_t its pair-sum word,
h_t its actual overflow, and H_t=sum_(i<t) h_i. Suppose Q_t has vertex v_t,
cut j_t, and the described central periodic band. Its retained suffix begins
at b_t=j_t-|S_(v_t)|. Let a_t be the actual carry entering that suffix. The
certificate includes an edge for this exact pair (h_t,a_t), so choose it.
No clock prediction or carry choice is imposed on the actual integer.

The upper edge inequality telescopes to

    2*j_t-H_t <= 2*j_0 + R_(v_t)-R_(v_0).

Since the actual length is L_t=L_0+H_t, this gives

    L_t-2*j_t >= 2p+4.

The lower edge inequality similarly gives

    b_t >= b_0 + U_(v_t)-U_(v_0) >= 0.

Thus the retained window always lies inside the physical word and remains
separated from its center by at least a full nonneutral block on either
side. The tail carry is reset before it can depend on the opposite finite
boundary. The local edge operation therefore gives the actual next suffix
and the actual next periodic central region. Reflection gives the other
side, and the center residue and parity conditions supply the middle. The
bounds also hold for the target edge, so this establishes the induction.

At every time Q_t contains the required coefficient greater than 9 and
unequal to 11: if it comes from B_(v_t), the central band contains at least
a complete period; otherwise it is in the retained suffix. Therefore Q_t
belongs to neither exact palindrome-predecessor class: the all-<=9 class,
or the class with outer coefficient 11 and every coefficient in {0,11}.
Hence n_(t+1) is not a palindrome for every t>=0. The finite positive integer
n_1 is consequently a decimal Lychrel witness.

The structural proof above shows that the finite graph cannot exist for
this local operation. The preserved implication is therefore vacuous; it
is not a viable construction criterion or a decimal Lychrel existence
proof. A future moving-front method would have to change the information
update, for example by recovering earlier known columns through additional
wake structure. No such repair is established here.
