# P8SccLatticesNoCentreAllPeriods

**Claim (COMPUTED + PAPER PROOF (Theorem A, Theorem F); 2026-11-11).** On the decimal clock 10101010, 55 of the 83 symmetry classes of
period-8 lattices whose bulk word is a primitive closed walk of length 61..159 of the 1,056-node SCC of IF(8) have no centre of any
depth and any time period; and no lattice of that SCC other than rec2 has a centre of exact depth 1..21, of any period.
- Theorem A: if the all-period closure Cyc_acc(K0) is empty and the exact fold map F_K has no periodic orbit inside Cyc_acc(K) for
  K < K0, there is no centre of any period on that phase orbit. Closed classes: K0 = 16..39, peak |Cyc_acc| 57,808,125 per job,
  0 exact orbits in 8,979 level lines; depth 0 by plain addition (258 cases, none possible).
- Theorem F (family): over all closed walks of the SCC at once, rec2 carved out, 0 exact fold cycles at every K <= 21.
Controls: second pipeline (own carries, Kosaraju) identical up to the EMPTY level on 5 orbits (K0 = 18..31); plain Python equals
the C++ counts at K = 1..21 on w61_0 orbit 0 (stopped there); base-9 Lean lattices b9r0/b9r1 give exact orbits and do not die, p12m9
dies at K = 6 as in round 13; 173 symmetric pairs, 0 violations; rule self-tested against big-number addition on all 85 classes.
**Not claimed:** the 28 budget-limited classes (UNDECIDED); bulk words longer than 160 beyond depth 21; the family at depth >= 22
(K = 22 exceeded 75 GB); rec0, rec1, rec2 for all periods (task K1); left parts that are not lattices; anything about 196.
Code: `calculation/decimal_frontier/round14/r14a_lattices/` (FINAL.md, class/table.md, src/, logs/).
