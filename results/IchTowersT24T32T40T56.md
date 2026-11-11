# IchTowersT24T32T40T56

**Claim (COMPUTED via Proposition C and round 13's Theorem B, both PAPER PROOF; 2026-11-11).** Every infinite closed history of
period 24, 32 or 40 on the decimal clock 01 is 8-periodic, and the clock word (00100101010101)^4 (T = 56) carries no infinite closed
56-history, hence no exterior (any width), uniform-band template or lattice with that clock.
- Proposition C: the relative tower above an interface J dies at level D(J) + 1, D = longest chain of closed L-columns over
  interfaces (infinite iff a cycle is reachable); decided by an exact DFS over interfaces, no K-head graph.
- Births die (rotation classes): T = 24: 38,546, deepest 3309; T = 32: 202,849, the 16 capped ones in single runs, deepest 17714;
  T = 40: 1,203,631, deepest 1670; T = 56: 207,280, deepest 742, and the root word (L = 14) dies at 15.
Checks: per-tower death levels equal r13c's K-head lists for N24/N36 (1,344,653 towers, 0 mismatches); memo DFS vs chunked tree DFS
identical histograms on sampled towers of six words and on all of T = 24; deepest T = 24 towers and T = 40 if=790 also by a second
code; controls re-run: N12, the period-8 lock and the base-9 Lean certificate survive as the single tower, p11 L = 22 and L = 16 die.
**Not claimed:** T = 48, 54, 60 (towers running or not run: UNDECIDED); a second code for the 16 capped T = 32 towers and the
deepest T = 56 tower (tree DFS only); any statement about centres; other clocks and periods; anything about 196.
Code: `calculation/decimal_frontier/round14/r14c_towers/` (FINAL.md, src/, scripts/, logs/, ctrl/).
