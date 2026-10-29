# AC36: phase-3 junction audit (COMPUTED; not a decimal certificate)

## Proof-relevant correction
The previously reported AB36 claim that *every* phase-3 |J|=6 endpoint first differs at LSD-first coefficient **7** is false. The actual published phase-3 root is
B3=[5,2,3,12,16,2,15,10,9,7,18,8,15,9,1,14,0,3,10,0,17,17,9,3,3,15,8,7,9,4,3,3,9,2],
W3=[4,0,17,11,9,12,2,9,2].
For J=(0,0,0,0,0,0), U=(0,9,18), C=(4,4), q=14,k=100, the genuine 120-step decimal orbit has 30 overflows, clock (0001)^30 (zero-based t=1 mod 4) and first endpoint mismatch **135**, not 7. Indices 0..134 match the target, including coefficient 7. Correcting the erroneous early gate prevents unsound elimination of potentially repairing junctions.

## Exhausted only for explicit fixed-suffix subcells
For EACH U rank in {1,13,25}, in the lexicographically sorted 30 U words (U=(0,9,18),(9,4,14),(14,4,9)), fix J[0]=0, let J[1],J[2],J[3] independently cover 0..18, and fix (J[4],J[5]) to one of (0,0),(0,1),(1,0),(1,1). Both C=(4,4) and C=(4,14,4) are included.
Each of 12 subcells has exactly 19^3 * 2 = 13,718 distinct cases. Total **164,616**. Endpoint-only: no strict intermediate W9 condition; all 164,616 have the expected 30-overflow phase-3 clock; **zero** W9-restoring endpoints and zero full returns. First W9 mismatches lie in absolute LSD-first indices [134,146], against W9 range [34,159]. This is 164,616 / 2,822,752,860 of the 30-U, 19^6, two-fixed-C phase-3 cell, or 164,616 / 14,856,594 of the claimed J[0]=0, three-U slice. Neither denominator covers arbitrary C.

## Reproduction and independent check
Compile `g++ -O3 -std=c++17 census.cpp -o census`. Run `./census control`, then for each `rank in 1 13 25` and each `suffix in (0,0),(0,1),(1,0),(1,1)`, run `./census rank suffix0 suffix1 0`. Each call enumerates precisely 13,718 cases. Independent true-integer Python verification: `python3 verify_bigint.py` (90 explicitly specified controls, five widths); a separate local differential run tested 600 ordinary-bigint cases against the C++ implementation, including (14,100),(20,80),(40,160),(80,320),(160,640), with no disagreement. Ordinary bigint uses a canonical integer realizing the palindromic pairword; C++ uses exact schoolbook decimal normalization of pair coefficients.

## Scope / missing lemma
Label **COMPUTED** for the explicit finite subcells and counterexample; **UNDECIDED** for the complete phase-3 |J|=6 cell, all centres, parametric uniformity and all-time decimal existence. A proof-relevant next lemma is an endpoint-only, carry-sound reduction covering all J[4:6] and J[0] choices without strict-W9 pruning. No claimed Lychrel number or all-time T* return.
