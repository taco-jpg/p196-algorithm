# Z11 phase-zero J5 slice 5/12 census report

**Status: EXHAUSTED-NONE.** Scope: rooted p12/m9, phase zero, |J|=5, lexicographic U ranks 5, 17, 29, q=14,k=100, all 2,476,099 junction words per U.

## Result

| U rank | U | J words checked | clock failures | unknown/short prefixes | W9 mismatches | W9 restorers | first W mismatch | offset from W cut |
|---:|---|---:|---:|---:|---:|---:|---|---|
| 5 | (4,9,14) | 2,476,099 | 0 | 0 | 2,476,099 | 0 | 135–147 | -25…-13 |
| 17 | (9,12,6) | 2,476,099 | 0 | 0 | 2,476,099 | 0 | 135–149 | -25…-11 |
| 29 | (18,0,9) | 2,476,099 | 0 | 0 | 2,476,099 | 0 | 135–149 | -25…-11 |
| **Total** | | **7,428,297** | **0** | **0** | **7,428,297** | **0** | | |

Every case has the exact (1000)^30 clock, an exact known prefix through coefficient 159 at t=120, and a mismatch inside W^14. The complete first-mismatch histogram is:

| Index | U rank 5 | U rank 17 | U rank 29 |
|---:|---:|---:|---:|
| 135 | 28,451 | 27,875 | 27,667 |
| 136 | 57,936 | 58,619 | 58,429 |
| 137 | 1,161,840 | 1,159,544 | 1,161,352 |
| 138 | 983,208 | 985,181 | 983,470 |
| 139 | 114,090 | 113,981 | 113,714 |
| 140 | 113,127 | 112,305 | 112,649 |
| 141 | 7,840 | 8,161 | 9,240 |
| 142 | 8,140 | 8,539 | 7,779 |
| 143 | 0 | 0 | 0 |
| 144 | 801 | 937 | 1,123 |
| 145 | 607 | 731 | 548 |
| 146 | 51 | 158 | 99 |
| 147 | 8 | 56 | 23 |
| 148 | 0 | 2 | 0 |
| 149 | 0 | 10 | 6 |
| **Total** | **2,476,099** | **2,476,099** | **2,476,099** |

## Completeness and independent checks

- The AVX2 program enumerates every base-19 code from 0 through 19^5-1 for each U. SIMD masks only batch 32 candidates; no active lane is pruned. It fails closed unless all expected counts, clocks, known-prefix lengths, and W9 mismatches agree.
- The carry cone computes the nearest known non-9 carry from each candidate's own valid prefix. Its validity mask is valid[i] AND seen[i+1], retaining exactly the coefficients strictly before the last known non-9. The terminal 9-run is lane-specific, so no candidate's carry state is borrowed from another.
- The C++ selftest compares the SIMD cone to the full symmetric pairword recurrence for all three U words, 32 J samples each, four legal even/odd centres, and all 120 phases.
- The independent replay script runs 30 genuine decimal cases for q=14,20,40,80,160 and k=100,100,200,400,800. For every step, arbitrary-precision integer reverse-and-add, an independent LSD-first digit-array adder, and the folded pairword recurrence agree. Both centre parities are represented; the clock and odd-pair guard hold throughout each 120-step replay. The W-mismatch offset is invariant under q growth.
- T12's protected-cut insertion theorem lifts each fixed-(J,U,C) mismatch from the reference width to every independent q>=14,k>=100 and every legal palindromic centre.

## Missing-lemma contribution

This closes the phase-zero length-five fixed-seam cells for U ranks 5, 17, and 29, redirecting remaining fixed-seam work to other U ranks/phases and the main constructive effort to moving/growing seam repair. It does not supply the epoch-map fixed point or an all-time decimal Lychrel certificate.

## Reproduction

From the repository root, run bash calculation/new_structures/Z11/slice05/run.sh (C++17 with AVX2 and OpenMP) for the regression and exhaustive census, then python3 calculation/new_structures/Z11/slice05/independent_replay.py for the 30-case genuine-big-integer/digit-array/pairword replay.
