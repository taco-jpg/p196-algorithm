# W26 cell report

Status: EXHAUSTED-NONE  
Label: COMPUTED, exact finite cell plus the previously established T12 all-width cut theorem.  
Scope: rooted p12/m9 phase 0; U=(9,4,14); seam length |J|=3 or 4; odd palindromic centre length 3,5,7,9,11,13; canonical coefficients 0..18 and an even centre coefficient.

## Statement decided

For every fixed J in the stated domain and every admissible odd centre C in the stated lengths, the exact 120-step return P_120(q,k)=P(q,k+5) is impossible for all independent q>=14,k>=100. The obstruction is already the necessary rooted prefix: B ++ W^q is not restored at the end of the first 120-step epoch.

## Completeness reduction

The full literal Cartesian domain has
- 19^3 + 19^4 = 137,180 junction words J.
- Centre counts by length: C3=190, C5=3,610, C7=68,590, C9=1,303,210, C11=24,760,990, C13=470,458,810.
- Total legal odd centres: 496,595,400, or 68,122,956,972,000 raw (J,C) pairs before modular gates.

Enumerating that Cartesian product is unnecessary. T12's proved 120-step cut bound gives U-side penetration at most 152 coefficients from the J boundary and 121 from the centre boundary for this specific U=(9,4,14). Since U^100 has 300 coefficients, 27 coefficients remain between the two disturbance cones. The actual phase-zero overflow clock is fixed by the rooted B prefix. Hence the endpoint B/W prefix for fixed J,q=14,k=100 is independent of the centre's coefficients and odd length. Any full return at any q>=14,k>=100 would, by T12's paired-insertion theorem, imply a return at (14,100); the prefix test therefore rules it out.

The search does not use the R02 MDD or any mod-11 pruning: it exhausts the complete J domain directly, and the C-independence reduction covers every admissible centre, including those outside the odd-only mod-11 gate.

## Exact exhaustive run

search.cpp constructs the genuine symmetric pair-coefficient word B ++ W^14 ++ J ++ U^100 ++ [0,0,0] ++ reverse(...), performs 120 exact LSD-first decimal normalizations and pairword reflections, and compares the final prefix with B ++ W^14. The J enumeration is the complete base-19 index interval 0..137179, with the first 6,859 indices representing |J|=3 and the next 130,321 representing |J|=4.

All 137,180 candidates had the exact overflow clock (1000)^30. Zero restored the B/W prefix. The first-mismatch histogram, zero-based coefficient index -> number of J words, was:

| Index | Count |
|---:|---:|
| 135 | 1,510 |
| 136 | 3,311 |
| 137 | 64,526 |
| 138 | 54,240 |
| 139 | 6,269 |
| 140 | 6,333 |
| 141 | 472 |
| 142 | 454 |
| 144 | 35 |
| 145 | 22 |
| 146 | 3 |
| 147 | 5 |
| Total | 137,180 |

The W prefix occupies indices 34..159 and its endpoint cut is 160. Thus every candidate's first mismatch lies in W's final 13..25 coefficients, not in the rooted B prefix.

Reproduce with:
- g++ -O3 -std=c++17 calculation/new_structures/W26/search.cpp -o /tmp/w26-search
- Run /tmp/w26-search on ranges (0,50000), (50000,50000), and (100000,37180), where the two arguments are start index and count.
- python3 calculation/new_structures/W26/independent.py

The independent script performs 60 genuine decimal 120-step replays at q=14,20,40,80,160 with k=100,100,160,320,640, two junction representatives, and all six centre lengths. It compares every step among the pairword recurrence, a fresh-buffer schoolbook digit-array engine, and Python arbitrary-precision n+reverse(n). All clocks are (1000)^30 and every replay fails the endpoint W-prefix equality. These controls validate the arithmetic engines; the exhaustive scope comes from the complete coefficient enumeration and the T12 reset-cone/insertion argument, not from sample extrapolation.

## Scope boundary and redirect

This excludes only the stated fixed-U, odd-centre, phase-zero, |J|=3..4 cell for q>=14,k>=100. It does not exclude |J|>=5, even centres, other U words, moving seams, other phases, or any different template architecture. It proves no global impossibility theorem for decimal Lychrel numbers.

REDIRECT: skip this exact shard and prioritize another unclaimed U/parity cell or a seam architecture with a different interface width.