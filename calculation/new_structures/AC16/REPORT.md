# AC16: phase-7 rooted W9/U3 fixed-junction return obstruction

**Label: COMPUTED (exhaustive finite carry-collar census, with an all-width reduction).** This is **not** a base-10 Lychrel number, nor a complete T* no-go. It decides the following necessary condition for the exact phase-7, 120-step T* fixed-J return.

**Statement.** Let the initial decimal physical pair-coefficient word, LSD first, be
P(q,k)=H C reverse(H), H=B_7 W_7^q J U^k, where B_7 and W_7 are the phase-7 rows of lat_p12m9.txt, q>=14, k>=100, J is any length-3 or length-4 word over {0,...,18}, U is any of the 30 rotations of (9,a,18-a) with even a in [0,18], and C is any finite palindromic coefficient centre admitting a canonical decimal realization. Under the T12 phase-rotated insertion/reset-cone hypotheses, **no** 120 genuine reverse-and-add steps can restore the original B_7 W_7^q prefix. Consequently the fixed-J, fixed-q, k->k+5 return is impossible for this cell, for either C parity.

**Finite decision.** At (q,k)=(14,100), 30*(19^3+19^4)=**4,115,400** distinct (U,J) pairs. An endpoint-only scan of five disjoint half-open ranges [0,823080), [823080,1646160), [1646160,2469240), [2469240,3292320), [3292320,4115400) gives **0** W9 prefix restorations, **0** rooted-clock failures. All 4,115,400 cases are simulated for all 120 exact pair-coefficient steps. The temporary W9 mismatches are **never** used as pruning. This is not an enumeration of all C: the carry-reset cone removes C from the necessary prefix predicate.

**Why the collar is independent of C.** An exact symmetric pairword step normalizes from LSD with low carry; the opposite high carry is determined backwards by the first coefficient unequal to nine. The gamma=1 overflow shifts the upper paired digit by one. The shared V16 local-collar engine tracks both carries and the genuine gamma[(7+t)%12], using 170 sites after the W9 cut and the phase-t U3 bulk. All 30 U words have a non-nine in each three-site period. Direct enumeration of their 120 phase rows gives U-side cone-loss pairs exactly (149,120), (150,119), (151,121); W9 loss is 91. Hence the junction-side reserve 170-151=19 and the centre-side reserve (300+|J|-170)-121 >=12 are strictly positive. The W9 bulk retains 9*14-91=35 cells. These margins keep all altered J/C influences outside the projected collar and justify the endpoint-only cut. For larger q,k the published T12 two-ended insertion theorem, with the 19/12 and 35 guards and periodic U/W rows, transports these equalities to independent insertions of W9 and U3, preserving the actual overflow clock.

**Independent arithmetic audit.** AC16/verify.py replays 120 deterministic mixed J/U cases with odd and even C and compares every one of 120 full pairword steps with the 330-site local collar. It compares genuine unbounded Python n+reverse(n), an independent LSD-first schoolbook digit array, and the pairword/clock for q=14,20,40,80,160; all match. It also checks all 30 U3 bulk rows, 12 W9 row transitions, the cone values, and paired W9/U3 insertion identities at every step in both centre parities.

**Reproduction** (from repository root):
- python3 calculation/new_structures/AC16/verify.py
- python3 calculation/new_structures/AC16/census.py --full

The census reuses the published exact C++ engine calculation/new_structures/V16/strict_w9_cell_local.cpp with --endpoint-only --phase 7. No mod-11 odd-centre gate and no strict-W9 MDD prefix prune is applied. This result eliminates one short fixed-seam phase-7 T* cell; moving/growing junctions, other phases, and long J remain entirely open.
