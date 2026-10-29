# Agent N26: decimal 20-column centre repair
- **COMPUTED**, exact finite-lifetime and replay claims only; no base-10 infinite Lychrel certificate.
- A deterministic local-search centre with 20 free pair coefficients, appended after the reachable period-8 rooted exterior and c repeats of its 20-column lattice, postpones the first mismatch in the 39-column exterior from 88c+92 (plain next bulk block) to 88c+252 (repaired block).
- The 160-step gain costs **zero additional digits**. Independently checked for c=0,1,2,3,5,10,20 and at c=225 through its first failure t=20052.
- c=225 gives a 9,118-digit decimal number surviving 20,000 true GMP integer reverse-add steps, nonpalindromic with all 39 outer pairword columns exact at every time 0..20000; final 19,118 digits.
- The 20-coefficient repair, deterministic search program, ordinary-integer GMP checker, independent digit-array checker, controls and commands are under calculation/new_structures/agent-N26/.
- Detailed mechanism and reproduction: reports/AgentN26CentralSeamRepair.md.
