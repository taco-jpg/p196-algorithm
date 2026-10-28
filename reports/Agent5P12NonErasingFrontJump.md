# An unbounded one-step front jump with a nonzero successor defect

**PAPER PROOF.** The exact decimal p=12, m=9 absorbing lattice admits arbitrarily long *non-erasing* apparent defect-front jumps after one actual reverse-and-add step. In contrast to `Agent5P12InvisibleDefect`, where a near patch vanished completely, the successor pairwords in this theorem are **different** at exactly two reflected positions. The source defect is **disconnected**; this does not contradict any possible light-cone theorem restricted to a single connected component, nor prove or disprove a periodic centre or a base-10 Lychrel number.

## Entire family, for every k>=2

Use the published phase t=1 periodic-lattice exterior and bulk in `calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt` (overflow g_1=0). Let n=200+30k, so n is even; construct its symmetric pair-coefficient word P from the exterior B_1, followed by the spatial-period-9 row W_1 to the middle, and then the reflection. Entries are in [0,18] and the first/last coefficient is positive less than 9. Thus there is a canonical n-digit decimal seed realizing P, and normalizing P has terminal carry zero.

Let Q be the word obtained by two mirrored, disjoint changes to P:

1. At lower coordinates 59,...,65, replace the seven coefficients `[4,5,10,14,13,12,9]` by `[9,5,0,15,3,12,14]`, and make the corresponding seven symmetric changes in the upper half. This is the proved carry-return **invisible** seven-column motif from `Agent5P12BulkCollisionTransfer`: its exact two-sided carry path returns to the original carry state after seven cells, and the *entire* next pairword remains equal to baseline if no further change is made.
2. At lower coordinate J=59+9k, and the symmetric upper position n-1-J, replace only coefficient 4 by 5. Because the periodic phase-1 bulk has coefficient 4 and entering lower/upper carries respectively (1,0) at every J≡59 (mod 9), both normalized digits increase by exactly 1, without changing outgoing carries. Therefore the next pair-coefficient at J (and by reflection at n-1-J) increases by exactly 2, while all other successor pair coefficients agree.

For k>=2, J>=77, strictly beyond the first patch ending at 65. The centre boundary is n/2=100+15k, giving a margin `n/2-J=41+6k` after the distant perturbation. Thus both reflected patches lie entirely in a safe lattice bulk segment; the upper and lower carry-reset boundaries of the first patch are reached before the distant single-site perturbation, so their one-step effects concatenate without interference. Neither perturbation affects the exterior overflow or the centre, and both pairwords are realizable as canonical positive integers of the same length n.

The first mismatching lower coefficient of P and Q is 59. Write F(P) and F(Q) for the **complete** symmetric next pair-coefficient words obtained after ordinary decimal reverse-and-add. The exact carry arithmetic above gives

```
F(Q)[i] - F(P)[i] = 2  if i=J or i=n-1-J,
                   0  at every other index.
```

So `F(Q) != F(P)`, but the first mismatching lower index of the successor words is exactly J=59+9k. The first-defect front advances J-59=9k places in **one** step, an arbitrarily large value as k grows. This directly defeats an unconditional one-step front-speed bound even under the weak requirement that the successor pairwords actually differ. It **does not** defeat a bound with a carefully defined connected-component or persistent-ancestry hypothesis: the first changed component disappears, while the second persists, and the proof does not trace an individual component through multiple steps.

## Reproduction and independent controls

From the repository root:

```
python3 calculation/decimal_frontier/lattice_kinks/code/k2_delayed_front.py
```

The script uses existing checked-in lattice data, builds P and Q with both reflected changes, computes the true full successor pairwords and compares every output index, proving that the *only* differences are precisely J and n-1-J and that both have coefficient difference +2. It independently realizes each input word as a canonical decimal numeral, then checks ordinary digit-list schoolbook reverse-and-add. An additional Python big-integer implementation of `N + reverse(N)` independently recomputes both complete pairwords. Exact representative cases k=2,3,4,5,6,7,8,9,10,20,30,50,100 pass, including k=100 with initial first mismatch 59 and next first mismatch 959. The proof for **all k** uses the two local carry-reset identities and the exact periodic coefficients/carries, not any extrapolation from k<=100.

No part of this result constitutes a long-lived centre orbit, Lychrel certificate, or a statement about whether 196 ever becomes palindromic.