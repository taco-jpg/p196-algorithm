# AC40 running computation log

2026-10-29: Read AGENTS, OPEN_PROBLEMS, FOCUS_SWARM, audit N/Nseries, CELL_LEDGER, R30 checker and canonical lattice fixture. Filed CLAIM in issue #476 (id 6502677735), expanding AB40's 1,900-case partial (including its first 50 tails with J[0]=0).

2026-10-29: C++ LSD-first pairword schoolbook normalization compared against independent Python `n + int(str(n)[::-1])` for six junction identifiers including 0,19,361,123456,999999,2476098 with both centre parities. At each control both engines gave exactly the same coefficients at indices 136/137 and exactly 30 overflows.

2026-10-29: Python independent verifier replayed 10 junction words x 2 centres x 5 width pairs (14/100,20/80,40/160,80/320,160/640), 100 distinct 120-step controls. All showed 30 true overflows, no pairword return; first mismatches were the width-shifted W9 cut positions. These controls do NOT prove the complete cell; the separate full enumeration does.

2026-10-29: `exhaust.cpp` designed as an *unpruned* full census in batches of 100,000: for each J identifier base-19 decode j[5]..j[1], two centres, true 120-step pairword additions, inspect endpoint site 137. No strict-phase assumptions, no mod-11 pruning, no sampling.

2026-10-29: The 25 disjoint 100,000-J chunks finished: 4,952,198 paths, no endpoint value 9 at W9 site 137, zero overflow totals other than 30. Exact histogram recorded in REPORT.md. No T* certificate claimed.