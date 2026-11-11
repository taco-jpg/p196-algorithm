# Round 14 (2026-11-08 .. 2026-11-11)

Three agent routes and the main-session checks, run on one machine. Each directory has its own report. Labels: PAPER PROOF /
COMPUTED / UNDECIDED. Builds on round 13 (r13b closures, r13c interface graph IF(d) and Theorem B), packaged separately.
Large log sets are packed (`r14a_lattices/logs/job_logs.tar.gz`, `r14a_lattices/latw.tar.gz`, `r14c_towers/logs/progress_err.tar.gz`).
Status as of 2026-11-11 (UTC); jobs still running are UNDECIDED.

| dir | route | result | report |
|---|---|---|---|
| `tails_no_centre/` | tails of IF(d), centres over every periodic left part | On clocks 00001110001 (d = 11) and (1000)^3 (d = 12) every d-periodic rooted history ends in a 9-wire or in W0 = p12m9 (COMPUTED); hence no d-periodic left part carries an eventually periodic centre, any width and period (PAPER PROOF + COMPUTED; the no-centre part for the census streams and for p12m9 was already on main). Clock 10, d = 8: tails rec0, rec1 or one 1,056-node SCC containing rec2 (COMPUTED) | `PROOF.md`, results/P11P12PeriodicLeftPartsNoCentre |
| `r14a_lattices/` | K1 for the other lattices of the d = 8 SCC | 55 of the 83 classes of lattices with bulk word a primitive closed walk of length 61..159 have no centre of any depth and any period (COMPUTED + PAPER PROOF, K0 = 16..39); 28 classes budget-limited (UNDECIDED); whole SCC except rec2: no centre of exact depth <= 21, any period (COMPUTED + PAPER PROOF) | `FINAL.md`, results/P8SccLatticesNoCentreAllPeriods |
| `r14c_towers/` | ICH on the open overflow clocks by interface chains | every ICH of period 24, 32, 40 on clock 01 is 8-periodic; no ICH of period 56 on (00100101010101)^4 (COMPUTED + PAPER PROOF + r13c Theorem B). T = 54 (tower CAP54a) and T = 60 (tower N60_2) running, T = 48 (8 towers) not run: UNDECIDED | `FINAL.md`, results/IchTowersT24T32T40T56 |
| `r14b_k1_lemmas/` | K1 for rec0/rec1/rec2, all periods | no centre found; K1 UNDECIDED. Lemma C (local CA form; known), Lemma H (healing offsets +-5 at g = 0, +-9 at g = 1; PAPER PROOF), rigidity of accepting walks and fragility (COMPUTED, finite K; main-session code agrees). Band-anchored walls (Theorem B of r14b): computed part disagrees with the main-session code, UNDECIDED. No results note | `FINAL.md` (section 12) |
| (main session) | moving walls (wallscan/wallsat) | exploratory SAT scan, K = 24, small wall periods (left tails W9 of clock 1000 and p11 against all census bands): 0 SAT; 6,123 + 10,447 UNSAT, 122 + 29 timeouts (300 s). Not a complete census; no soundness theorem for the format yet; nothing claimed, code not shipped | - |

Nothing here is about 196 itself, and no Lychrel number is claimed.
