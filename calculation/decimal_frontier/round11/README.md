# Round 11 (2026-11-03 .. 2026-11-04)

Seven routes, run on one machine. Each directory has its own report. Labels: PAPER PROOF / COMPUTED / UNDECIDED.
Large log sets are packed (`periods33to48/logs.tar.gz`, `p8_stack_centres/runs.tar.gz`).

| dir | route | result | report |
|---|---|---|---|
| `premiseB/` | premise (B) of ReachDiskRounds6to8 | WIRE reach histories of height H are in bijection with exteriors of width <= H (Theorem B, PAPER PROOF; lemmas checked exhaustively, COMPUTED). Bands: template => reachable at height H or H+1 (Theorem B'), band exclusion at T covers lcm(left-end period, band period) = T | `PROOF.md`, results/PremiseBReachEqualsAgent120 |
| `p8_stack_centres/` | p8 rec0/rec1 and the PRO-R03-e stack | rec1 has no fixed-centre 80-step return for \|C\| <= 16 (27,286,610,980 centres at L13..16, no pruning); thresholds q0 = 8 / 11 for periods 160 / 240; stack S(s) for s <= 16 reduces to rec1 (COMPUTED + PAPER PROOF) | `FINAL.md`, results/P8Rec1FixedCentreLen16 |
| `t12_seam/` | T12 route | every witness needs \|C\| >= 13 and \|J\| >= 10 (COMPUTED); centre and seam are independent (PAPER PROOF); full route UNDECIDED | `FINAL.md`, results/T12CentreLen12SeamLen9 |
| `periods33to48/` | new exteriors, periods 33..48 | no 9-wire stream and no uniform band for T = 33..40 and imprimitive clocks at T = 42..48, except 110 wire / 1,475 band words capped (COMPUTED); primitive clocks at T = 41..48 not run | `FINAL.md`, results/ExteriorPeriods33to40 |
| `chain6_chain8/` | chain 6 (clock 01, P32/P96), chain 8 (clock 110001001000, PR381) | P32 none; chain 8 none at T = 12, 24, 48 and none of width <= 22 at root [9,17,5] (COMPUTED); P96, T = 72, all-k UNDECIDED | `FINAL.md`, results/Chain6P32Chain8T48 |
| `chain1_3divr/` | chain 1, branch 3 \| r (lemma "only N12") | three PAPER PROOF reductions; the lemma itself UNDECIDED | `PROOF.md` |
| `clock01_T32/` | (32, 01) with w = 11 windows | windows prune < 6 %; forward run interrupted at height 58; UNDECIDED | `README.md` |

Nothing here is about 196 itself, and no Lychrel number is claimed.
