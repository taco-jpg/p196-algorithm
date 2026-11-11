# Round 12 (2026-11-07 .. 2026-11-08)

Seven agents (r12a..r12g) on the Studio; six are packaged here (routes T12, exteriors and K1), plus the final log of a round-11 run. Each directory has its own
report (`FINAL.md`, trimmed of working notes) with the commands that reproduce its numbers. Labels: PAPER PROOF / COMPUTED /
UNDECIDED. Nothing is LEAN-VERIFIED here (the Lean proof of Lemma K was written but is not in this commit).
Large log sets are packed (`*/logs*.tar.gz`, each under 1 MB). Binaries and big data (dumps, cyclic sets) are not included.

| dir | route | result | report |
|---|---|---|---|
| `t12_m1/` | T12, one period (r12a) | Phi^120(P(q,k)) != P(q,k+5) for every U, J, C, q >= 14, k >= 100: seam sets D_12(V) and centre sets E_R(V) empty for all 30 V (PAPER PROOF reduction + COMPUTED SAT, two encodings, two solvers) | `FINAL.md`, results/T12NoTemplateReturn |
| `t12_all_m/` | T12, every period (r12f) | Lemma K (column-0 clock) and band erosion (Theorem A, B_1 = empty): no m-return for any m >= 1, q >= 0, U, J, C, k >= 90m+10 (PAPER PROOF with COMPUTED inputs); fast and cross-q returns UNDECIDED | `FINAL.md`, results/T12NoTemplateReturn |
| `ext41to48/` | exteriors, periods 41..48 (r12b) | exact K-head filter, Theorem K (PAPER PROOF); census T = 41..48 and the round-11 capped words (COMPUTED); Theorem U: P(9), p11^m (m <= 5); Corollary T: 6,700 of 6,722 roots acyclic | `FINAL.md`, results/ExteriorPeriods41to56, results/ExteriorUniquenessP9P11m |
| `ext49to56/` | exteriors, periods 49..56 (r12e) | census T = 49..56 (5,460,044,533 words, COMPUTED + Theorem K), 12 words UNDECIDED (one, (00010010111)^5, since decided by round 13's BirthTowersT16T55); p47 and (p21)^2 die | `FINAL.md`, results/ExteriorPeriods41to56 |
| `k1_sat/` | K1 by SAT, fixed centres (r12d) | fixed-centre returns of period 80K excluded for the lengths of table 4.1, K = 1..6 (rec0, rec1) and K = 1..3 (rec2) (COMPUTED + PAPER PROOF reduction); K = 1 is superseded by round 13 | `FINAL.md`, results/P8FixedCentrePeriods160to576 |
| `k1_depth/` | K1 by relaxation, all periods (r12g) | no centre of depth <= 23 (rec0, rec1) / <= 27 (rec2), any period (COMPUTED + PAPER PROOF reduction) | `FINAL.md`, results/P8CentreDepthBound |
| `chain8_T72/` | round-11 chain 8, T = 72 | run stopped at height 34 (3,836,399,833 orbits, frontier non-empty): UNDECIDED | `README.md`, results/Chain6P32Chain8T48 |

Not packaged: r12c (chain 1, "only N12" for k >= 3 by tail cores). Its methods failed, and Theorem U of `ext41to48/` proves
k = 3 (P(9)) by another route; nothing it decided changes what is known.

Nothing here is about 196 itself, and no Lychrel number is claimed.
