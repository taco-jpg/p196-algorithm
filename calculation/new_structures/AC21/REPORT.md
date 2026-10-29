# AC21 phase-0 |J|=5 final U-rank cells

**Label: COMPUTED.** No decimal all-time Lychrel certificate is claimed.

For rooted p12/m9 B34/W9 with q=14,k=100, all 19^5=2,476,099 five-coefficient junction words J were enumerated for each of the uncovered 1-based U ranks 4=(2,16,9), 16=(9,10,8), 28=(16,9,2). After 120 genuine decimal reverse-and-add steps, every one of the 7,428,297 cases has a mismatch inside the required W9 endpoint prefix, at coefficients 135..149 (W9/J cut =160). All cases have exactly 30 overflows, and zero unknown-carry or truncated-prefix cases. W9-restoration count: **zero** per U.

The two-ended SIMD carry/reset-cone engine is based on the previously audited Z11 program; it enumerates all 19^5 J codes WITHOUT filtering by intermediate W9 survival. An independent SIMD implementation produced the exact per-index histogram in endpoint_mismatch.tsv and the 121-row strict-W9 survivor diagnostic in strict_survivors.tsv. The strict-phase diagnostic was NEVER used for endpoint pruning. Python bigint, independent out-of-place digit arrays, and folded pairwords agreed at every step for 90 controls spanning 3 U ×3 J ×2 palindromic centre parities ×5 width pairs (14,100),(20,100),(40,200),(80,400),(160,800). The two parity controls are [4,4] and [4,12,4].

At each step the validity mask for the known 340-coefficient root prefix records exactly whether a non-nine reset fixes the upper carry independently of the unknown centre. The protected 160-coefficient B34/W9 prefix remains determined through t=120 for EVERY enumerated J. This makes the observed W9 obstruction independent of arbitrary legal palindromic centres C. The previously published T12 cut/insertion theorem, used here as a premise, lifts these cut-relative mismatches to all independent q>=14,k>=100 for the same fixed J,C,U.

**Missing lemma supplied:** these last three phase-0 J5 ranks cannot produce a stationary fixed-J/C/U 120-step T* return; the 27 other reported ranks still require their own audits. This excludes no moving/growing seam, changing-q or 240-step repair and establishes no endless decimal orbit.

Reproduce: `g++ -O3 -mavx2 -fopenmp -std=c++17 calculation/new_structures/AC21/census.cpp -o /tmp/ac21 && /tmp/ac21`; independent cross-check: `python3 calculation/new_structures/AC21/independent_replay.py`.
