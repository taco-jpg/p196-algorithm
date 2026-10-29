# Z11 audit report: omitted rank 30 of phase-zero J5 slice 6/12

**Status: EXHAUSTED-NONE.** Scope: the omitted U-rank-30 subcell, U=(18,9,0), phase zero, |J|=5, q=14,k=100, all 2,476,099 J words. This audit completes the U set for slice 6/12 but makes no global decimal Lychrel claim.

## Result

| U rank | U | J words checked | clock failures | unknown/short prefixes | W9 mismatches | W9 restorers | first W mismatch | offset from W cut |
|---:|---|---:|---:|---:|---:|---:|---|---|
| 30 | (18,9,0) | 2,476,099 | 0 | 0 | 2,476,099 | 0 | 135–150 | -25…-10 |

Complete first-mismatch histogram:

| Index | Count |
|---:|---:|
| 135 | 28,165 |
| 136 | 58,177 |
| 137 | 1,161,954 |
| 138 | 982,445 |
| 139 | 113,837 |
| 140 | 112,551 |
| 141 | 8,853 |
| 142 | 8,357 |
| 143 | 0 |
| 144 | 924 |
| 145 | 761 |
| 146 | 56 |
| 147 | 15 |
| 148 | 0 |
| 149 | 0 |
| 150 | 4 |
| **Total** | **2,476,099** |

Every candidate has the exact (1000)^30 overflow clock, the known endpoint prefix remains valid through coefficient 159, and every candidate mismatches inside W^14. The AVX2 search enumerates every base-19 code from 0 through 19^5-1; SIMD masks only batch 32 candidates and do not prune any active lane. The C++ selftest compares the SIMD carry/validity cone against the full pairword recurrence for 32 J samples, four legal even/odd centres, and all 120 phases.

The independent replay runs 10 genuine decimal controls: q=14,20,40,80,160 with k=100,100,200,400,800, one even-centre sample and one odd-centre sample. At every step, arbitrary-precision integer reverse-and-add, a separate LSD-first digit-array adder, and the folded pairword recurrence agree. The clock and odd-pair guard hold through 120 steps, and the W mismatch offset stays -25 or -10 as q grows.

## Completeness correction

This closes the missing rank-30 member of phase-zero slice 6/12. The other two ranks were previously reported as ranks 6 and 18; the correct full slice is ranks 6, 18, and 30. T12's protected-cut insertion theorem lifts the omitted fixed-seam mismatch to all independent q>=14,k>=100 and all legal palindromic centres. This is a scoped correction to census coverage, not an all-time decimal Lychrel certificate.

## Reproduction

From the repository root, run bash calculation/new_structures/Z11/slice06_rank30/run.sh (C++17 with AVX2 and OpenMP), then python3 calculation/new_structures/Z11/slice06_rank30/independent_replay.py.
