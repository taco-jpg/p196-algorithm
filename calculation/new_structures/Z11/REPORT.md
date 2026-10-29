# Z11 |J|=5 phase-zero census report

**Status: EXHAUSTED-NONE.** Scope: rooted p12/m9, phase zero, |J|=5, U-order ranks 11 and 23, q=14,k=100, all 2,476,099 coefficient words per U. No claim about other U ranks, other phases, moving/growing seams, or the global decimal Lychrel problem is made.

## Result

| U rank | U | J words checked | wrong 120-clock cases | unresolved/short prefixes | W9 mismatches | W9-restoration candidates | first mismatch indices | offsets from W cut |
|---:|---|---:|---:|---:|---:|---:|---|---|
| 11 | (9,0,18) | 2,476,099 | 0 | 0 | 2,476,099 | 0 | 135–148 | -25…-12 |
| 23 | (12,6,9) | 2,476,099 | 0 | 0 | 2,476,099 | 0 | 135–149 | -25…-11 |
| **Total** | | **4,952,198** | **0** | **0** | **4,952,198** | **0** | | |

All candidates have the exact required (1000)^30 overflow clock. The known prefix after step 120 is valid through index 159 for every candidate. Thus every J has a concrete mismatch inside W^14; this is not an inference from the fact that a prefix survived a finite horizon. The first W mismatch histogram, with all counts included, is:

| Index | U rank 11 | U rank 23 |
|---:|---:|---:|
| 135 | 27,893 | 27,794 |
| 136 | 58,828 | 58,557 |
| 137 | 1,160,751 | 1,161,664 |
| 138 | 983,301 | 983,641 |
| 139 | 112,943 | 113,440 |
| 140 | 113,596 | 113,328 |
| 141 | 8,332 | 7,928 |
| 142 | 8,576 | 8,083 |
| 143 | 0 | 0 |
| 144 | 861 | 835 |
| 145 | 798 | 701 |
| 146 | 122 | 63 |
| 147 | 75 | 37 |
| 148 | 23 | 10 |
| 149 | 0 | 18 |
| **Total** | **2,476,099** | **2,476,099** |

## Completeness and independent validation

- **No search-space pruning:** the compiled program enumerates all base-19 codes from 0 through 19^5-1, decoding each into one five-coefficient J word. The only SIMD masking groups candidates for parallel evaluation; it does not discard any active candidate. The final assertions fail unless the tested count, clock, prefix-validity, and W-mismatch counts equal the complete expected totals.
- **Exact cone:** at each step, for every candidate lane and coefficient i, the high-side carry is determined by the first known non-9 coefficient at or to the right of the relevant index. The seen mask records whether such a coefficient exists inside the known prefix. The output-validity mask is valid[i] AND seen[i+1], which is exactly the two-sided reset-cone rule: retain only positions strictly before the last known non-9. A candidate's valid prefix is tracked independently, so lanes with different terminal 9-runs cannot contaminate one another.
- **C++ regression:** --selftest compares the SIMD carry/validity cone coefficient-by-coefficient with the full symmetric pairword recurrence for both U rows, 32 J samples per row, four legal even/odd centres, and all 120 phases.
- **Genuine decimal differential replay:** independent_replay.py performs 40 cases across (q,k)=(14,100),(20,100),(40,200),(80,400),(160,800), with both even and odd legal centres and two J samples per U (earliest and latest first-mismatch witnesses). At every one of 120 steps it cross-checks arbitrary-precision N + reverse(N), a separately written LSD-first digit-array adder, and the folded pairword recurrence. Every sample has exact clock, an odd pair coefficient at each of the first 121 states, and the expected W mismatch offset preserved as q grows.
- **All-width scope:** the committed T12 cut/insertion theorem transports the fixed-seam mismatch from (14,100) to all independent q>=14,k>=100: each protected W insertion shifts the mismatch and W cut together, while the protected U insertion is beyond the seam-side mismatch. The resulting offset from the W cut remains unchanged. This lifts the obstruction for each enumerated fixed (J,U) to all widths and all legal palindromic centres.

## Missing-lemma contribution

This closes the assigned phase-zero length-five fixed-seam cells for U ranks 11 and 23, redirecting any remaining fixed-seam census to the other U ranks/phases and the main search to moving/growing seam repair. It does **not** supply the epoch-map fixed point or an all-time decimal Lychrel certificate.

## Reproduction

From the repository root, run bash calculation/new_structures/Z11/run.sh (C++17 compiler with AVX2 and OpenMP) for the SIMD regression and full exhaustive census. Then run python3 calculation/new_structures/Z11/independent_replay.py (Python 3) for the separate 40-case genuine-big-integer/digit-array/pairword differential replay.
