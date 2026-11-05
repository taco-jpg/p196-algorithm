# r11c FINAL — T12 route (phase-0 B34/W9, U3), 2026-11-04

## Results
1. **Centre C length 7..12 excluded — COMPUTED** (two-inlet cone soundness: AC46 PAPER PROOF).
   `census.cpp` (AC46 two-inlet central cone, K=47, K=100 retry), all 30 U, all admissible palindromic C:
   L7 2,057,700 / L8 3,909,630 / L9 39,096,300 / L10 74,282,970 / L11 742,829,700 / L12 1,411,376,430 cases,
   **0 survivors**; first mismatch radius always 0..2 (`census_L*.txt`). With AC46 (L1..6): every C with |C|<=12 fails, for every J.
2. **Role of J — PAPER PROOF** (from the T12/AC46 cone radii). For k>=100 the centre cone (<=122) and junction cone (<=152) never
   meet inside the 300-column U band, so the return splits into two independent conditions:
   (a) centre return of U^inf C U^inf, independent of J (AC46); (b) seam return of W0^14 | J | U^inf, independent of C.
   J can never repair a failing C; it only has to repair the seam.
3. **Seam census |J|=0,1 — COMPUTED** (`seam.cpp`: rooted prefix, both unknown centre-side carry inlets; cross-checked by
   `seam_check.py`: Python cone and real big-integer n+rev(n), 8 random full 120-step replays agree). All fail; the first mismatch
   is on the **W side, 18..25 columns before J**: the U3 band feeds a wrong high-carry sequence into W9.
4. **W-side inlet analysis — COMPUTED** (`seamsat.py W`). W region [64,160) depends on J,U only through the 120-bit high-carry
   inlet sigma_t at column 160. SAT found >=30 distinct sigma != sigma_W that still return W exactly (cap reached), so W itself is
   not rigid; J must act as a carry-sequence adapter turning the U3 sigma into a W-acceptable one.
5. **Targeted seam SAT, |J|<=9 excluded — COMPUTED.** Exact folded two-carry encoding of window [64, 160+|J|+170) over 120 steps:
   left inputs = exact rooted rows, right inlet = determined U background carry (beyond the 152 junction cone), forced clock
   (1000)^30, J free in 0..18, full final window = B0 W0^14 J U^(k+5). 30 U x |J| in {7,8,9}: **90/90 UNSAT** (cadical195,
   4..9 min each, logs in `sat/`). Since J++U^m gives the same seam as J, lengths 7,8,9 cover every |J|<=9.
   Controls: fixed census J gives UNSAT in agreement with seam.cpp; target = exact cone image gives SAT.

## Status
- No witness found, so no candidate to replay. Every phase-0 witness needs **|C|>=13 and |J|>=10** (both COMPUTED).
- Full T12 return for free-length J/C: **UNDECIDED**. No Lychrel number; nothing about 196.

## Next
Seam SAT |J|=10..12 (~6 min and ~6.5 GB RSS per instance); centre SAT (`satc.py`) for |C|=13..15.
