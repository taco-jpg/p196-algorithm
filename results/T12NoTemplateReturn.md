# T12NoTemplateReturn

**Claim (PAPER PROOF, with COMPUTED SAT inputs; 2026-11-08).** In the T12 family P(q,k) = B0 W0^q J U^k C mirror (B34/W9, U one of the 30 charge-zero U3 rotations (9,a,18-a)), Phi^(120m)(P(q,k)) != P(q,k+5m) for every m >= 1, q >= 0, k >= 90m+10 and all finite J, C. No chain P(q,k) -> P(q,k+5m) -> ... exists; this decides the T12 return left open by T12CentreLen12SeamLen9 (|C| >= 13, |J| >= 10).
- Lemma K (PAPER PROOF; potential 3 - floor(log2 P) on the column-0 automaton): leading + last digit = 10 at both ends and exactly N/4 overflows force the clock (1000)^(N/4), for every m and q.
- Theorem A (band erosion): with the standard clock the U band start moves right at every epoch, because the one-epoch restoration instance B_1 is UNSAT for ten group instances (two encodings x kissat404/cadical195, all four combinations). A+ (g = 45): the band loses >= 46 columns per epoch, so every standard-clock return with k >= 90*ceil(N/120)+10 has N = 120m and k' <= k - 31m/3.
- m = 1, second proof (r12a, q >= 14, k >= 100 via T12Rooted120CutPumping): seam sets D_12(V) and centre sets E_R(V) (R = 4, 6) empty for all 30 V (two encodings, two solvers); direct SAT |J| = 10..12 and |C| = 13..15: 180/180 UNSAT.
- m = 2, 3: multi-epoch seam sets also empty (two encodings), an independent check of Theorem A there.
Controls: both encodings run on genuine big-integer orbits (genuine dynamics SAT, one changed final value UNSAT), planted returns SAT, pure-band controls SAT, D_1(U5) = {6,7,15,16} reproduced by the m-epoch code.
**Not claimed:** returns with more than N/4 overflows ("fast"), cross-q cycles q' > q, other template shapes, single returns with k < 90m+10; not Lean-checked (a Lean proof of Lemma K exists but is not in this commit); anything about 196.
Code: `calculation/decimal_frontier/round12/t12_all_m/` and `round12/t12_m1/` (FINAL.md, section 8 / 8b: commands).
