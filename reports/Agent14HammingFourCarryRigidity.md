# Agent14HammingFourCarryRigidity

**COMPUTED, exhaustive and uncapped.** For either existing reachable decimal period-eight / primitive-spatial-period-20 non-self-mirror absorbing lattice (rec0 and rec1, gamma=10101010), take the complete 320-bit itinerary of cyclic ascending and descending carry-in bits (8 times x 20 positions x 2 directions). There is NO physical eight-time-periodic coefficient lattice in ANY integer base b>=2 whose carry itinerary differs from the reference in exactly FOUR positions. With the previously published complete Hamming-radius-three result, any distinct physical itinerary must have Hamming distance at least FIVE. This is not a claim about centres, decimal Lychrel numbers, other bulk periods, or 196.

The exact bulk recurrence over spatial indices modulo 20 is:

    P_(t+1)[j] = P_t[j] + P_t[j-gamma_t] + a_t[j] + d_t[j-gamma_t]
                 - b*(a_t[j+1] + d_t[j-gamma_t-1]).

The eight-step linear part is 16*(I+S)^4, where S shifts the spatial index. Hence H=I-16*(I+S)^4 is invertible over the rationals (its determinant is odd because H=I mod 2). The source-committed twenty-integer inverse-kernel certificate, with common denominator D=4772995440505252811961825, yields each initial coefficient P0[j]=(A_j*b+B_j)/D. Each of 320 binary carry flips adds an exact independent affine impulse to A and B; every four-flip result is the sum of four such impulses. No floating-point arithmetic or finite search over bases is used.

For P0[0] and P0[1] to be integers, D must divide A0*b+B0 and A1*b+B1. Consequently D divides A0*B1-A1*B0. The code first checks this determinant, then solves the two congruences by generalized CRT, then enforces all remaining 18 coefficient-integrality congruences. It next enforces 0<=P_t[j]<=2(b-1) and the exact prescribed ascending/descending carry-in and carry-out inequalities at all eight temporal phases, for integer b>=2.

Complete exact counts:

| Lattice | Four-bit masks | Determinant survives | First 2 CRT survive | All 20 integral | Physically legal |
|---|---:|---:|---:|---:|---:|
| rec0 | 428,761,520 | 221,226 | 137,575 | 16,631 | **0** |
| rec1 | 428,761,520 | 219,985 | 137,013 | 16,631 | **0** |

Among the 16,631 integral candidates in EACH case, 16,630 have an explicit single carry/digit legality inequality s*b+c>=0 with s<0 and 2*s+c<0 (or s=0,c<0), impossible for every real b>=2. The two exceptions are rec0 mask (23,68,113,158) and rec1 mask (33,78,103,148). For rec0, descending upper gate (t=0,j=17,out=0) forces b<=13986001/4812871 while descending lower gate (t=1,j=9,out=1) forces b>=31706572/2202637. For rec1 the same fractions arise from descending upper gate (t=0,j=7,out=1) and lower gate (t=1,j=19,out=0). Since the lower bound exceeds the upper, both fail even over real bases. The committed exception.py independently rederives these two fractions from every indicated carry bit and affine coefficient; a memorized mask alone is not accepted.

The two stand-alone source implementations are distinct: primary.py uses the integer cyclic inverse-kernel convolution and independently recomputes 320 complete carry perturbation vectors; independent.py directly Gauss-Jordan-inverts the 20x20 rational matrix, derives the 320 unit impulse responses from the time recurrence, and performs its own CRT, carry, and source checks. Both are uncapped, and produce one checkable line for each of the 320 disjoint first-mask-position partitions (their sizes are binomial(319-i,3)). The source snapshots rows.txt, kernel.txt, the exact exceptional-pair checker and reproducible commands are in this same commit. The independent script also runs positive full 10-edge pairword normalizations for the existing base-9 SCC (m4, exterior width61) and both existing base-13 SCCs (exterior widths75 and55), using those already published repo control certificates.

To reproduce from the repo root:

    bash calculation/decimal_frontier/lattice_formats/hamming4/reproduce.sh

For restartable disjoint partitions, set environment P196_H4_START and P196_H4_STOP to any half-open interval of first indices in [0,320], then combine the printed count vectors. Full all-mask independent execution takes longer than the optimized C++ cross-check used during development but requires only Python 3 standard library. No source or data necessary for verification is sandbox-only. No Lean files changed; the full local tools/verify.py --changed cannot be run without a complete checkout, but this commit changes non-Lean files only.

This classification excludes ONLY four-bit changes of the 8x20x2 carry itinerary at temporal period eight and spatial period twenty. It does NOT exclude carry distance >=5, other lattice periods, other overflow schedules, root reachability or periodic centres; it does not prove existence or nonexistence of a decimal Lychrel number.
