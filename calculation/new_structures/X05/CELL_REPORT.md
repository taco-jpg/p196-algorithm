# X05 phase-0 p12/m9 cell report

**Status: EXHAUSTED-NONE. Label: COMPUTED.** This is a scoped cell obstruction, not a decimal Lychrel existence or nonexistence theorem.

## Exact scope and claim

Use the physically rooted phase-0 B34 and W9 from calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt, fixed U=(9,6,12), junction J of length 3 or 4 over coefficients 0..18, and any canonical palindromic odd centre C of length 15, 17, 19, 21, or 23 with coefficients 0..18 and an even midpoint. For every independent q>=14,k>=100, the 120-step target P(q,k;J,C) -> P(q,k+5;J,C) is impossible because the required B34 W9^q prefix is not restored.

## Exhaustive finite search

The literal junction domain is 19^3 + 19^4 = **137,180** words: 6,859 of length 3 and 130,321 of length 4. search.cpp directly enumerates all of them at q=14,k=100, with the legal representative centre C of length 15 whose midpoint is 4 and all other coefficients are 0. No mod-11 gate is applied, so no centre or junction is discarded by a congruence filter. R02's 361-state MDD table is absent from main; direct enumeration of the entire J domain is used instead of relying on that unavailable prefilter.

Every one of the 137,180 candidates has the exact physical 120-step overflow clock (1000)^30, with 30 overflows. **Zero** restore the required prefix B34 W9^14. The first mismatch histogram is:

| Absolute index | Offset from W9/J cut (index 160) | Junction count |
|---:|---:|---:|
| 135 | -25 | 1,488 |
| 136 | -24 | 3,291 |
| 137 | -23 | 63,956 |
| 138 | -22 | 54,864 |
| 139 | -21 | 6,301 |
| 140 | -20 | 6,310 |
| 141 | -19 | 440 |
| 142 | -18 | 439 |
| 143 | -17 | 0 |
| 144 | -16 | 34 |
| 145 | -15 | 54 |
| 146 | -14 | 3 |
| **Total** | | **137,180** |

The W9 band occupies coefficient indices 34..159 at q=14, and the W9/J cut is index 160. Thus every candidate fails inside the final 14–25 coefficients of W9, before the junction itself.

## Why this is all-width and centre-independent

The exact 120-phase bulk carry map for U=(9,6,12) returns to U and has exactly one coefficient 9 in every phase. The independently implemented reset-cone recurrence gives a seam-side bound of 152 coefficients and a centre-side bound of 121. Since U^100 contains 300 coefficients, the cones leave 300-152-121 = **27 untouched coefficients** between them. Therefore changing the centre's coefficients or any of the claimed odd centre lengths cannot affect this epoch's W9/J endpoint.

T12's proved insertion theorem states that for each fixed J,C,U, a 120-step full return at any q>=14,k>=100 exists if and only if it exists at (q,k)=(14,100). At that reference width, the complete J scan shows the necessary B34 W9^14 prefix fails, independently of C by the cone separation above. This excludes the full return for every q>=14,k>=100 in the stated cell. The proof uses T12's all-width reduction plus an exact finite computation; it is not an inference from sampled widths.

The five centre lengths contain, respectively, 8,938,717,390; 169,835,630,410; 3,226,876,977,790; 61,310,662,578,010; and 1,164,902,588,982,190 canonical centres. That is 1,229,618,902,885,790 centre choices, or 168,679,121,097,872,672,200 raw (J,C) pairs. The reset-cone proof makes enumeration of those centres unnecessary.

## Independent controls and reproduction

independent.py independently checks the U3 cycle and the 152/121 reset cones, then constructs canonical source integers and compares Python's unbounded-integer n+reverse(n) against a fresh-buffer schoolbook digit-array engine. It checks 100 controls: four representative J words, all five centre lengths, and (q,k)=(14,100),(20,100),(40,200),(80,400),(160,800), each for 120 ordinary decimal steps. All 100 controls agree at every step, have the exact (1000)^30 clock, contain no palindrome among the checked states, and miss the target 14–25 coefficients before the W9/J cut. This independently cross-checks the canonical realization and ordinary-step semantics documented by R30.

Run from repository root:

    g++ -O3 -std=c++17 -Wall -Wextra -pedantic -fopenmp calculation/new_structures/X05/search.cpp -o /tmp/x05-search
    /tmp/x05-search
    python3 calculation/new_structures/X05/independent.py

The exact search state count is 137,180; there is no state cap or SAT/MDD-dependent pruning. The MDD is not treated as evidence.

**REDIRECT:** Skip this exact phase-0 cell U=(9,6,12), |J|=3–4, odd C lengths 15–23; investigate longer junctions, even centres, another U orientation, or a moving/phase-changing seam.
