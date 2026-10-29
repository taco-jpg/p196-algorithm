# X11 cell report: phase 0, |J|=3..4, U=(9,10,8), even C=14..24

**Status: EXHAUSTED-NONE**  
**Label: COMPUTED**, with the existing T12 all-width cut/insertion theorem.  
**Scope:** rooted decimal p12/m9 phase 0; fixed oriented U=(9,10,8); all J over 0..18 of length 3 or 4; even palindromic coefficient centres of lengths 14,16,18,20,22,24; independent q>=14,k>=100.

## Decided statement

No member of this cell can complete a 120-step epoch with the required rooted B ++ W^q prefix restored. Hence there is no first edge of the requested epoch seam map that remains in this cell, and no fixed point or multi-epoch cycle satisfying the cell's W9-preservation requirement. This is a scoped cell exclusion, not a proof that base-10 Lychrel numbers exist or do not exist.

## Complete finite reduction

There are 19^3=6,859 length-3 junctions and 19^4=130,321 length-4 junctions, for exactly 137,180 J words. For the requested centre lengths, the numbers of palindromic coefficient centres are 19^7=893,871,739, 19^8=16,983,563,041, 19^9=322,687,697,779, 19^10=6,131,066,257,801, 19^11=116,490,258,898,219, and 19^12=2,213,314,919,066,161. Thus the raw requested (J,C) domain has 320,490,452,707,283,233,200 pairs.

No enumeration of centres is needed. T12's reset-cone theorem for this exact U orientation gives the 120-phase U3 bulk a maximum 152-site disturbance cone from the junction side and 121 from the centre side. The U band has 300 coefficients at k=100, leaving 27 coefficients outside both cones. Therefore the tested endpoint B/W prefix is independent of all admissible finite centres, including both parities and every requested centre length. The canonical source is realizable because the pairword is symmetric, all coefficients lie in 0..18, the centre is even, and the rooted leading pair coefficient is 10.

T12's paired-insertion theorem states that for fixed J,C,U, a genuine return at any independent q>=14,k>=100 is equivalent to a return at (q,k)=(14,100). It is therefore enough to exhaust the 137,180 junctions at that reference width and one representative centre C=0^14. The search uses no mod-11 pruning and no R02 MDD pruning: every junction word is enumerated directly in base 19. A second exhaustive program, cell_search_digits.cpp, independently realizes each source as a canonical decimal integer and iterates with fresh-buffer ordinary digit addition; it independently reproduces the exact same 137,180-case histogram.

## Exact search result

Commands:

    g++ -O3 -std=c++17 -fopenmp calculation/new_structures/agent-X11/cell_search.cpp -o /tmp/x11-cell-search
    OMP_NUM_THREADS=5 /tmp/x11-cell-search 14 100 14
    g++ -O3 -std=c++17 -fopenmp calculation/new_structures/agent-X11/cell_search_digits.cpp -o /tmp/x11-cell-digits
    OMP_NUM_THREADS=5 /tmp/x11-cell-digits 14 100 14

Both independent full-domain engines report all 137,180 candidates with the exact physical overflow clock (1000)^30. Zero restored the required prefix B ++ W^14; the engines agree on every histogram bin:

| First mismatch | Junction count |
|---:|---:|
| 135 | 1,547 |
| 136 | 3,205 |
| 137 | 64,455 |
| 138 | 54,397 |
| 139 | 6,161 |
| 140 | 6,367 |
| 141 | 529 |
| 142 | 452 |
| 144 | 33 |
| 145 | 16 |
| 146 | 10 |
| 147 | 8 |
| **Total** | **137,180** |

The required rooted prefix has length 160, so every first mismatch is 13..25 coefficients before the W9 cut. Because a full template return necessarily restores this prefix, none of these junctions can return; the mismatch is in W9, not merely a different seam label.

## Independent genuine-decimal controls

Run:

    python3 calculation/new_structures/agent-X11/independent_replay.py
    python3 calculation/new_structures/agent-X11/r30_crosscheck.py

The replay covers 96 cases: (q,k)=(20,80),(40,160),(80,320),(160,640); J=0^3,18^3,0^4,18^4; and each centre length 14,16,18,20,22,24 with centre coefficients all zero. Every case compares all 120 transitions using Python arbitrary-precision n+reverse(n), a fresh-buffer decimal digit-vector implementation, and the folded pairword recurrence. r30_crosscheck.py additionally compiles and invokes the repository's calculation/new_structures/R30/verify.cpp for each case and compares the exact mismatch index, full 120-bit overflow string, overflow sum, palindrome guard, and final digit count. All 96 controls pass: exact clock (1000)^30, sum of overflows 30, no palindrome at any state 0..120, no full target return, and first mismatch in the rooted prefix. The mismatch range is 191..1452 across these scaled widths.

R30 symbolic control command (run four times with J=0,0,0; 18,18,18; 0,0,0,0; and 18,18,18,18):

    python3 tools/parametric_verify_r30.py --lattice calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt --J 0,0,0 --U 9,10,8 --C 0,2,4,6,8,10,12,12,10,8,6,4,2,0 --qmin 512 --kmin 512 --only-symbolic

The symbolic transducer reports return=false, complete (1000)^30 clock and odd-pair witnesses, and first mismatch 9q+12 for J=0^3, 9q+11 for J=18^3, 9q+12 for J=0^4, and 9q+11 for J=18^4.

## Redirect and scope boundary

**REDIRECT:** skip fixed U=(9,10,8), |J|=3..4 at phase 0; do not spend time expanding its centre length. The result does not exclude |J|>=5, any moving/phase-changing seam, other U orientations, other rooted phases, U6 mixed words, or another template architecture. No global impossibility claim and no decimal Lychrel certificate is made.