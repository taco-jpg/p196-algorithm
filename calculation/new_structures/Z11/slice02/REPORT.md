# Z11 phase-zero J5 slice 2/12 census report

**Status: EXHAUSTED-NONE.** Scope: rooted p12/m9, phase zero, |J|=5, lexicographic U ranks 2, 14, 26, q=14,k=100, all 2,476,099 junction words per U.

## Result

| U rank | U | J words checked | clock failures | unknown/short prefixes | W9 mismatches | W9 restorers | first W mismatch | offset from W cut |
|---:|---|---:|---:|---:|---:|---:|---|---|
| 2 | (0,18,9) | 2,476,099 | 0 | 0 | 2,476,099 | 0 | 135–148 | -25…-12 |
| 14 | (9,6,12) | 2,476,099 | 0 | 0 | 2,476,099 | 0 | 135–148 | -25…-12 |
| 26 | (14,9,4) | 2,476,099 | 0 | 0 | 2,476,099 | 0 | 135–149 | -25…-11 |
| **Total** | | **7,428,297** | **0** | **0** | **7,428,297** | **0** | | |

Every case has the exact (1000)^30 clock, an exact known prefix through coefficient 159 at t=120, and a mismatch inside W^14. The complete first-mismatch histogram is:

| Index | U rank 2 | U rank 14 | U rank 26 |
|---:|---:|---:|---:|
| 135 | 28,004 | 27,739 | 28,183 |
| 136 | 59,271 | 58,755 | 58,461 |
| 137 | 1,159,867 | 1,160,128 | 1,164,428 |
| 138 | 983,941 | 984,265 | 980,256 |
| 139 | 114,190 | 114,114 | 114,974 |
| 140 | 113,053 | 112,819 | 111,317 |
| 141 | 8,053 | 8,054 | 8,568 |
| 142 | 7,850 | 8,344 | 8,042 |
| 143 | 0 | 0 | 0 |
| 144 | 985 | 994 | 801 |
| 145 | 720 | 705 | 825 |
| 146 | 15 | 100 | 60 |
| 147 | 126 | 66 | 120 |
| 148 | 24 | 16 | 32 |
| 149 | 0 | 0 | 32 |
| **Total** | **2,476,099** | **2,476,099** | **2,476,099** |

## Completeness and independent checks

- The AVX2 program enumerates every base-19 code from 0 through 19^5-1 for each U. SIMD masks only batch 32 candidates; no active lane is pruned. It fails closed unless all expected counts, clocks, known-prefix lengths, and W9 mismatches agree.
- The carry cone computes the nearest known non-9 carry from each candidate's own valid prefix. Its validity mask is valid[i] AND seen[i+1], retaining exactly the coefficients strictly before the last known non-9. The terminal 9-run is lane-specific, so no candidate's carry state is borrowed from another.
- The C++ selftest compares the SIMD cone to the full symmetric pairword recurrence for all three U words, 32 J samples each, four legal even/odd centres, and all 120 phases.
- The independent replay script runs 30 genuine decimal cases for q=14,20,40,80,160 and k=100,100,200,400,800. For every step, arbitrary-precision integer reverse-and-add, an independent LSD-first digit-array adder, and the folded pairword recurrence agree. Both centre parities are represented; the clock and odd-pair guard hold throughout each 120-step replay. The W-mismatch offset is invariant under q growth.
- T12's protected-cut insertion theorem lifts each fixed-(J,U,C) mismatch from the reference width to every independent q>=14,k>=100 and every legal palindromic centre.

## Missing-lemma contribution

This closes the phase-zero length-five fixed-seam cells for U ranks 2, 14, and 26, redirecting remaining fixed-seam work to other U ranks/phases and the main constructive effort to moving/growing seam repair. It does not supply the epoch-map fixed point or an all-time decimal Lychrel certificate.

## Reproduction

From the repository root, run bash calculation/new_structures/Z11/slice02/run.sh (C++17 with AVX2 and OpenMP) for the regression and exhaustive census, then python3 calculation/new_structures/Z11/slice02/independent_replay.py for the 30-case genuine-big-integer/digit-array/pairword replay.
