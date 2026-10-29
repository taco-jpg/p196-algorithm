# Z03 report: phase-0 |J|=5, lexicographic U slice 3/12

**Status: EXHAUSTED-NONE. Label: COMPUTED, with an all-width cut/insertion reduction.** This is a scoped obstruction, not a base-10 Lychrel nonexistence theorem.

## Exact claim

For each of U=(2,9,16), U=(9,8,10), U=(16,2,9), and for every one of the 19^5 = 2,476,099 length-5 coefficient words J, the exact rooted phase-0 120-step pairword transition at (q,k)=(14,100) fails to restore the W9 prefix. The first mismatch is always inside W9, at an offset from the W9-to-J cut between -25 and -11 inclusive. The exhaustive endpoint-restoration count is **0 / 7,428,297**; the independently tracked strict-per-phase W9 survivor count is also **0 / 7,428,297**.

A complete T* return P(q,k;J,U,C) -> P(q,k+5;J,U,C) must restore W9 at step 120. T12's rooted cut/insertion theorem reduces any fixed J,C,U return for independent q>=14,k>=100 to (14,100). The mismatch lies in the protected W9 cut cone and is independent of C; therefore this slice contains no fixed-J, fixed-C, fixed-U T* return for any admissible q,k. This does not decide other U ranks, other seam lengths/phases, or moving/phase-changing seams.

## Exact domain and cone justification

The 30 U3 words were sorted lexicographically; only 1-based ranks 3, 15, and 27 were assigned. Each of the three J domains was traversed in three disjoint contiguous code ranges [0,1000000), [1000000,2000000), and [2000000,2476099). The ranges cover all 19^5 words exactly once per U. No modular gate or candidate pruning was used in the endpoint census.

The local bit-sliced engine tracks 108 W coefficients (the last 12 W9 copies), all five J coefficients, and 180 U coefficients. At phase 0, the exact W-side cone loss is 91 columns; the 108-column W window therefore includes every seam-sensitive W coefficient, with 17 protected columns before its start at index 52. The U-side cone bounds for the three U rows are (150,120), (152,121), and (151,122); the 180-column U collar leaves at least 28 columns beyond the junction-side cone, while the far-side reset makes its exterior carry seed independent of the centre. The W9 endpoint test is consequently centre-independent for every admissible finite C. These bounds are checked in verify_bigint.py.

**MDD handling:** the R02/V48 strict-W9 MDD was not used to prune the endpoint-only domain. A strict-per-phase filter is stronger than the required endpoint property and would be unsound as a pruning rule if a candidate damaged W9 temporarily and repaired it at step 120. Instead, strict survival was tracked as a side lane while every J was retained in the endpoint census; both counts were zero.

## First endpoint mismatch histogram

Counts below are the first mismatching coefficient offset from the W9-to-J cut. Each row sums to exactly 2,476,099.

| U rank | U | -25 | -24 | -23 | -22 | -21 | -20 | -19 | -18 | -16 | -15 | -14 | -13 | -12 | -11 |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | (2,9,16) | 28,027 | 58,546 | 1,158,088 | 986,488 | 114,538 | 112,384 | 8,213 | 8,228 | 752 | 602 | 146 | 83 | 0 | 4 |
| 15 | (9,8,10) | 28,099 | 58,715 | 1,160,301 | 983,932 | 113,881 | 112,985 | 8,257 | 8,167 | 1,042 | 589 | 84 | 35 | 12 | 0 |
| 27 | (16,2,9) | 27,532 | 58,318 | 1,163,142 | 981,732 | 113,477 | 113,686 | 8,046 | 8,766 | 793 | 388 | 103 | 110 | 6 | 0 |

The complete compact table is census_summary.tsv.

## Independent validation

- The C++ bit-sliced engine checks selected J codes {0,1,2,19,361,123456,987654,2476098} against a separate scalar local carry recurrence at every one of the 120 phases for each assigned U row.
- verify_bigint.py checks the local-window recurrence against genuine arbitrary-precision decimal n + reverse(n) at every phase for 15 reference controls at (q,k)=(14,100), plus 36 controls at (q,k)=(20,100),(40,200),(80,400),(160,800). It checks the true overflow clock at every step, all 12 rooted W transitions, all 30 U3 120-returns from all 12 phases, and the exact cone bounds.
- No candidate survived the first-epoch W9 endpoint test, so there was no survivor to replay at the four larger widths or to advance through the conditional second-epoch seam-map lane.

**Scope caution:** this result rules out a 120-step T* return in this exact phase/U/J-length slice. It does **not** rule out a different 240-step family that intentionally damages W9 at step 120 and repairs it at step 240; that is a different route and was not searched here.

## Reproduction

From the repository root, run:

    python3 calculation/new_structures/Z03/verify_bigint.py
    g++ -O3 -std=c++20 -march=native -Wall -Wextra calculation/new_structures/Z03/census.cpp -o /tmp/z03-census
    bash calculation/new_structures/Z03/run_census.sh

The script runs all nine contiguous U/range shards and regenerates census_summary.tsv; the complete search-space accounting and zero-survivor assertions are enforced by summarize.py.
