# W10 cell report

**Status: EXHAUSTED-NONE** for the exact shard phase=0, |J|=3-4, U=(4,9,14), even C length 2-12.

**Missing-lemma sentence:** This supplies a scoped non-return lemma: no rooted p12/m9 120-step return exists for U=(4,9,14), |J|=3-4, and even palindromic C of length 2-12, because every junction forces a W9 mismatch at (q,k)=(14,100) and the exact T12 insertion theorem propagates that failure to all q>=14,k>=100.

## Exact search-space accounting

- Junction coefficients range independently over 0..18.
- |J|=3: 19^3 = 6,859 junctions.
- |J|=4: 19^4 = 130,321 junctions.
- Total junctions exhausted: 137,180.
- Even palindromic centres: 19 + 19^2 + 19^3 + 19^4 + 19^5 + 19^6 = 49,659,540 distinct words across lengths 2, 4, 6, 8, 10, 12.
- The unreduced Cartesian domain has 137,180 * 49,659,540 = 6,812,295,697,200 (J,C) pairs. The centre is not brute-force enumerated: the exact absorbing-band reduction below proves the W9-prefix outcome is independent of every centre value and every allowed even centre length.

## Exact finite computation

exhaustive.cpp exhausts every J for the single representative C=(0,0) at q=14,k=100, using the exact decimal digit-vector implementation of 120 reverse-and-add steps. It checks the entire rooted overflow word 1000 repeated 30 times and then compares the resulting pairword against the required B34 and W9 prefix.

| J length | J count | correct 120-step clock | B34 restored | W9 restored | full B34+W9 prefix restored |
|---:|---:|---:|---:|---:|---:|
| 3 | 6,859 | 6,859 | 6,859 | 0 | 0 |
| 4 | 130,321 | 130,321 | 130,321 | 0 | 0 |
| **Total** | **137,180** | **137,180** | **137,180** | **0** | **0** |

For q=14, W9 has 126 coefficients. The first W9 mismatch is always at offset 101 through 111 from the start of W9, i.e. 15 through 25 coefficients before the W9|J cut. Exact offset histogram over all 137,180 junctions: 101:1505, 102:3210, 103:64368, 104:54565, 105:6191, 106:6270, 107:436, 108:523, 110:56, 111:56 (offset 109 has count zero). No mod-11 pruning was used; even centres are retained.

## Why one centre suffices

The exact two-sided cyclic-carry map in bulk_absorption.py gives 121 phase rows for the bulk orbit starting at (4,9,14). It returns to the initial row at phase 120, visits 30 distinct rows, and every row has exactly one coefficient 9 and two non-9 coefficients. For a coefficient x, the carry transfer is T_x(c)=floor((x+c)/10) for c in {0,1}. At every x!=9, this transfer forgets the inlet bit. Therefore each phase's three-coefficient U block resets a carry in at most one block, independent of the centre's digits or length.

For this rotation, the exact T12 reset-cone recurrence gives junction-side loss 150 and centre-side loss 120 over 120 steps. U^100 has 300 coefficients, leaving 30 coefficients between the two cones, so the junction and centre disturbances do not meet. Thus the entire outer B34/W9 prefix after 120 steps is identical for every allowed C to the representative C=(0,0) result. Since every J fails W9 restoration for that representative, every (J,C) in this shard fails.

Finally, results/T12Rooted120CutPumping.md proves for each fixed J,C,U that Return(q,k) for all independent q>=14,k>=100 is equivalent to Return(14,100). The finite obstruction therefore rules out a same-cell fixed point or cycle at any admissible width. This uses the existing T12 paper proof; it is not Lean-verified.

## Independent controls and limits

- bulk_absorption.py: exact carry-kernel phase and reset-cone checks.
- exhaustive.cpp: complete compiled enumeration, independent of the NumPy batch implementation used during development.
- replay_samples.py: 48 controls at q=20,40,80,160, k=5q, four representative J words, and even centres of lengths 2, 4, and 12. Python arbitrary-precision n + reverse(n) and an independently coded digit-list engine agree exactly; all controls have clock 1000^30 and a W9 mismatch.

**Label:** COMPUTED finite enumeration + exact carry-reset reduction using the existing PAPER PROOF T12 theorem; not Lean-verified. This is a scoped exclusion only, not a decimal Lychrel existence proof.
