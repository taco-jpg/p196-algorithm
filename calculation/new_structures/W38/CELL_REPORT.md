# W38 cell report: rooted phase-0, U=(9,16,2), odd centre

**Status: EXHAUSTED-NONE for this exact cell.** Label: **PAPER PROOF + COMPUTED**, not Lean-verified and not a decimal Lychrel certificate.

## Scope

Use the canonical phase-0 root B (length 34) and W (length 9) from calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt, with overflow clock g=(100010001000)^10. The exact words are:

- B = (10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5)
- W = (5,18,4,8,1,15,4,0,5)

Fix the exact oriented inner word U=(9,16,2), junction length |J|=3 or 4, and any legal palindromic odd centre C of length 3, 5, 7, 9, 11, or 13. Coefficients are in 0..18, and an odd-length centre has an even midpoint so a canonical decimal source exists. The result applies for independent q,k>=20.

**Claim.** No member of this cell preserves the rooted B W^q prefix after 120 genuine reverse-and-add steps. Therefore no fixed point or cycle of the 120-step epoch seam map exists in this cell, regardless of the centre's outer coefficients. This is a cell-local exclusion only; it does not rule out another U orientation, even centres, longer J, another root phase, or a moving seam.

## Exact search-space accounting

Let A(X)=sum_i (-1)^i X_i (LSD-first). Here A(U)=9-16+2=-5 = 6 (mod 11). For odd palindromic C of length 2r+1, mirrored terms cancel and A(C)=(-1)^r C[r]. The corrected odd-centre gate A(U)=A(C) (mod 11) forces the midpoint to be 16 when r is odd (lengths 3, 7, 11) and 6 when r is even (lengths 5, 9, 13). The other gate, 2A(J)+(-1)^|J|A(C)=0 (mod 11), then requires:

- |J|=3: A(J)=3 (mod 11), giving **626** words;
- |J|=4: A(J)=8 (mod 11), giving **11,844** words.

Thus the exact J quotient contains **12,470** candidates. Before applying the gates, there are 19^3+19^4 = 137,180 J words and 10 * sum(19^r, r=1..6) = 496,595,400 odd-centre words, for 68,122,956,972,000 raw (J,C) tuples. After the gates there are 49,659,540 centre words and 619,254,463,800 (J,C) tuples. We do not enumerate those centre combinations: the centre-independence lemma below proves that every one has the same W9-cut result as its J representative. The finite exhaustive search is therefore exactly the 12,470 J words, not a random sample. R02's MDD was not used as a prefilter: direct enumeration of the complete post-gate J quotient is small enough and avoids relying on an external filter for completeness.

## Why the reduced search is all-width

For a coefficient block w, the carry transfer through w is the identity only when every coefficient of w is 9; otherwise it is a constant map on incoming carry {0,1}. This follows coefficientwise from f_x(c)=floor((x+c)/10): f_9 is identity, while f_x is constant for x!=9. The exact R30 symbolic trace for this rooted W9/U3 bulk, over states t=0..120, has 242 repeated W-band run occurrences and 242 repeated U-band run occurrences; **none** is an all-9 word. This is checked phase-by-phase in verify_examples.py. Consequently each repeated bulk block erases its incoming carry after one copy.

The 120-step clock has exactly 30 overflows, so the paired-word alignment can move at most 30 coefficient positions in one epoch. The decisive W9 mismatch lies 15–25 coefficients before the W9|J cut. At q,k>=20, the cut is at least 180 coefficients from the root and at least 63 coefficients from the centre; hence the mismatch window is at least 155 coefficients from the root and 78 coefficients from the centre. Both distances exceed the 30-position light-cone bound. Carry reset plus this bound makes the W9-cut transition independent of both exponents and of every coefficient of C. The representative C=[0,16,0] is therefore sufficient for the entire allowed centre class.

## Exhaustive result

screen.cpp enumerates every J word passing the corrected odd-centre mod-11 gates and performs the exact 120 ordinary digit-array transitions at q=k=20,40,80,160. At every width:

- 12,470 / 12,470 have the exact overflow clock (1000)^30 (30 true overflows);
- 0 / 12,470 preserve B W^q;
- 0 / 12,470 return to B W^q J U^(k+5) C reverse(...);
- all 12,470 first mismatches occur strictly inside W9, at absolute coefficient index 9q+c, with c in {9,10,11,12,13,14,15,16,18,19}.

The relative-to-cut histogram is identical at all four widths:

| First mismatch offset relative to W9/J cut | J count |
|---:|---:|
| -25 | 123 |
| -24 | 283 |
| -23 | 5,909 |
| -22 | 4,921 |
| -21 | 570 |
| -20 | 557 |
| -19 | 53 |
| -18 | 44 |
| -16 | 5 |
| -15 | 5 |

Independent Python-bigint and fresh-buffer digit-array engines agree on 72 controls (3 representative admissible J words × all 6 allowed odd-centre lengths × q=k=20,40,80,160, 120 steps each). R30's all-parameter symbolic verifier independently confirms the mismatch expressions 9q+11 for J=[3,0,0] and J=[0,0,0,3], and 9q+12 for J=[0,0,3], with the exact clock and a phasewise odd-pair guard. For J=[3,0,0], the same symbolic 9q+11 mismatch is also checked at each of the six legal centre lengths. These controls audit the all-width reduction; the cell-wide exclusion itself follows from the carry-reset/light-cone lemma and exhaustive J enumeration.

## Reproduction

From repository root, run:

    g++ -O3 -std=c++17 -Wall -Wextra -pedantic calculation/new_structures/W38/screen.cpp -o /tmp/w38-screen
    /tmp/w38-screen
    python3 calculation/new_structures/W38/verify_examples.py

**Redirect for the swarm:** do not spend more effort on phase-0, |J|=3–4, U=(9,16,2), odd C lengths 3–13. This result does not exclude the other 29 charge-zero rotations or any neighbouring cell.
