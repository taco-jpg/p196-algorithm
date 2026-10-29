# Z11 phase-zero J5 slice 1/12 census report

**Status: EXHAUSTED-NONE.** Scope: rooted p12/m9, phase zero, |J|=5, lexicographic U ranks 1, 13, 25, q=14,k=100, all 2,476,099 junction words per U.

## Result

| U rank | U | J words checked | clock failures | unknown/short prefixes | W9 mismatches | W9 restorers | first W mismatch | offset from W cut |
|---:|---|---:|---:|---:|---:|---:|---|---|
| 1 | (0,9,18) | 2,476,099 | 0 | 0 | 2,476,099 | 0 | 135–149 | -25…-11 |
| 13 | (9,4,14) | 2,476,099 | 0 | 0 | 2,476,099 | 0 | 135–149 | -25…-11 |
| 25 | (14,4,9) | 2,476,099 | 0 | 0 | 2,476,099 | 0 | 135–151 | -25…-9 |
| **Total** | | **7,428,297** | **0** | **0** | **7,428,297** | **0** | | |

Every case has the exact (1000)^30 clock, an exact known prefix through coefficient 159 at t=120, and at least one mismatch inside W^14. The complete first-mismatch histogram is:

| Index | U rank 1 | U rank 13 | U rank 25 |
|---:|---:|---:|---:|
| 135 | 28,000 | 27,684 | 28,158 |
| 136 | 59,007 | 58,887 | 58,797 |
| 137 | 1,160,308 | 1,159,483 | 1,162,375 |
| 138 | 984,104 | 984,912 | 982,231 |
| 139 | 114,046 | 113,619 | 114,233 |
| 140 | 112,075 | 113,070 | 112,388 |
| 141 | 8,662 | 8,477 | 8,380 |
| 142 | 8,359 | 8,251 | 7,911 |
| 143 | 0 | 0 | 0 |
| 144 | 711 | 905 | 797 |
| 145 | 694 | 669 | 727 |
| 146 | 53 | 64 | 42 |
| 147 | 76 | 62 | 36 |
| 148 | 0 | 0 | 0 |
| 149 | 4 | 16 | 0 |
| 150 | 0 | 0 | 0 |
| 151 | 0 | 0 | 24 |
| **Total** | **2,476,099** | **2,476,099** | **2,476,099** |

## Completeness and independent checks

- The AVX2 program enumerates every base-19 code from 0 through 19^5-1 for each U. SIMD masks only batch 32 candidates; no active lane is pruned. It fails closed unless all expected counts, clocks, known-prefix lengths, and W9 mismatches agree.
- The carry cone computes the nearest known non-9 carry from each candidate's own valid prefix. Its validity mask is valid[i] AND seen[i+1], retaining exactly the coefficients strictly before the last known non-9. The terminal 9-run is lane-specific, so no candidate's carry state is borrowed from another.
- The C++ selftest compares the SIMD cone to the full symmetric pairword recurrence for all three U words, 32 J samples each, four legal even/odd centres, and all 120 phases.
- The independent replay script runs 30 genuine decimal cases for q=14,20,40,80,160 and k=100,100,200,400,800. For every step, arbitrary-precision integer reverse-and-add, an independent LSD-first digit-array adder, and the folded pairword recurrence agree. Both centre parities are represented; the clock and odd-pair guard hold throughout each 120-step replay. The W-mismatch offset is invariant under q growth.
- T12's protected-cut insertion theorem lifts each fixed-(J,U,C) mismatch from the reference width to every independent q>=14,k>=100 and every legal palindromic centre.

## Missing-lemma contribution

This closes the phase-zero length-five fixed-seam cells for U ranks 1, 13, and 25, redirecting remaining fixed-seam work to other U ranks/phases and the main constructive effort to moving/growing seam repair. It does not supply the epoch-map fixed point or an all-time decimal Lychrel certificate.

## Reproduction

From the repository root, run bash calculation/new_structures/Z11/slice01/run.sh (C++17 with AVX2 and OpenMP) for the regression and exhaustive census, then python3 calculation/new_structures/Z11/slice01/independent_replay.py for the 30-case genuine-big-integer/digit-array/pairword replay.
