# X11 phase-0 cell: U=(9,12,6), |J|=3..4, even C=14..24

**Status: EXHAUSTED-NONE**  
**Label: COMPUTED**, lifted to all independent q>=14,k>=100 by the T12 cut/insertion theorem.  
**Scope:** rooted p12/m9 phase 0; fixed oriented U=(9,12,6); all junction words J of length 3 or 4 over coefficients 0..18; even palindromic centres of lengths 14,16,18,20,22,24.

## Result

No candidate restores the required rooted B ++ W^q prefix after 120 genuine decimal reverse-and-add steps. The failure occurs inside W9, before the seam, for all 137,180 junctions at the exact reference width q=14,k=100. Thus no first epoch edge stays in this fixed-U cell, so no same-cell fixed point or longer cycle satisfying W9 preservation exists here. This is a scoped exclusion, not a global no-go or existence proof.

## Completeness and centre reduction

The exact J domain is 19^3+19^4=6,859+130,321=137,180. The six requested even centre lengths have 19^7,19^8,19^9,19^10,19^11,19^12 choices, respectively; their total is 2,336,276,809,354,740, so the raw (J,C) product has 320,490,452,707,283,233,200 members.

For U=(9,12,6), the 120-phase U3 carry cycle closes after 30 distinct states. Its T12 reset cones are 152 coefficients from the junction side and 121 from the centre side. U^100 has 300 coefficients, leaving 27 between the cones. The required rooted B/W endpoint is therefore independent of every admissible finite palindromic centre; C=0^14 is a valid representative. T12's paired-insertion theorem then reduces any fixed-J,C return for any independent q>=14,k>=100 to the literal reference width (14,100). We enumerate every J word directly in base 19, without mod-11 gates or the R02 MDD.

## Exhaustive result

Commands:

    g++ -O3 -std=c++17 -fopenmp calculation/new_structures/agent-X11/cell_search_u_9_12_6.cpp -o /tmp/x11-u126-pairword
    OMP_NUM_THREADS=5 /tmp/x11-u126-pairword 14 100 14
    g++ -O3 -std=c++17 -fopenmp calculation/new_structures/agent-X11/cell_search_digits_u_9_12_6.cpp -o /tmp/x11-u126-digits
    OMP_NUM_THREADS=5 /tmp/x11-u126-digits 14 100 14

Both independent full-domain engines checked 137,180 junctions, found the exact overflow clock (1000)^30 in every case, and found zero rooted-prefix restorations. Their first-mismatch histograms agree exactly:

| First mismatch | Junction count |
|---:|---:|
| 135 | 1,490 |
| 136 | 3,276 |
| 137 | 64,369 |
| 138 | 54,506 |
| 139 | 6,308 |
| 140 | 6,241 |
| 141 | 423 |
| 142 | 507 |
| 144 | 29 |
| 145 | 26 |
| 146 | 5 |
| **Total** | **137,180** |

The target B ++ W^14 prefix ends at coefficient index 159, so every mismatch is at index 135..146, 14..25 positions before the W9 cut.

## Genuine decimal and R30 controls

    python3 calculation/new_structures/agent-X11/independent_replay_u_9_12_6.py
    python3 calculation/new_structures/agent-X11/r30_crosscheck_u_9_12_6.py

The Python arbitrary-precision n+reverse engine, fresh-buffer decimal digit vector, and pairword recurrence agree for 96 cases at (q,k)=(20,80),(40,160),(80,320),(160,640), four junction controls (0^3,18^3,0^4,18^4), and all six centre lengths 14..24. All have the exact clock (1000)^30, overflow sum 30, no palindrome in states 0..120, and a mismatch inside the rooted prefix. The R30 C++ verifier independently agrees on 32 controls spanning all four widths, all four junction controls, and centre lengths 14 and 24; first mismatch, all overflow bits, palindrome guard, and final digit count match exactly.

The R30 symbolic control at qmin=kmin=512 also returns false with complete odd-pair witnesses and clock (1000)^30. It gives first mismatch 9q+12 for J=0^3, 9q+11 for J=18^3, 9q+12 for J=0^4, and 9q+11 for J=18^4, using centre [0,2,4,6,8,10,12,12,10,8,6,4,2,0].

**REDIRECT:** skip this fixed U orientation for |J|=3..4; move to |J|>=5, a phase-changing/moving seam, or a distinct architecture. This says nothing about other U words, other phases, or global decimal Lychrel existence.