# BirthTowersT16T55

**Claim (COMPUTED via Theorem B, which is a PAPER PROOF; 2026-11-08).** The decimal clock word (00010010111)^5 (T = 55) carries no
infinite closed 55-history, hence no exterior (any width), uniform-band template or lattice; and every closed 16-history of clock (01)^8 is 8-periodic.
- Theorem B: the interface set IF(d) of d-periodic heads is finite (BFS: 1,483 interfaces, a0 = 44 for 00010010111, d = 11; 22,601,
  a0 = 87 for 01, d = 8). If the relative tower above every closed non-d-periodic column ("birth") over IF(d) dies, every infinite closed
  L-history is d-periodic; exteriors, uniform-band templates and lattices with clock length L are such histories.
- T = 55: all 1,240,956 rotation classes of births die (deepest level 345) and the root word (L = 11) dies at level 45; this decides the
  capped census word of round 12 (r12e section 6). T = 16: all 68,520 births (8,565 rotation classes) die, deepest level 526.
- Also (r13c only): for (0001)^6 and (0001)^9 every closed history is 12-periodic (125,090 and 1,219,563 births die), a stronger form of
  the known T = 24 / 36 results (it also covers lattices and non-accepting histories).
Checks: the main session's mc13e (own code from the recurrences) reproduces |IF|, a0, the T = 16 and T = 55 tower outcomes and the root
death at 45; Python and kh3 tower rechecks; the plain K-head first non-periodic column equals the tower prediction (L = 16 to K = 120, L = 36 to K = 500). Controls: N12 (d = 4), the Lean base-9 certificate (d = 5), the period-8 lock (d = 4) each survive as the single surviving tower; p11 at L = 22, 33, 44 dies.
**Not claimed:** (01)^12, (01)^16, (01)^20, (0001)^12, (0001)^15, root-9 T = 54, root-14 T = 56 (capped towers listed: UNDECIDED); primitive capped words; all L at once; anything about 196.
Code: `calculation/decimal_frontier/round13/births_filter/` (FINAL.md, REPRODUCE.sh, main_check/).
