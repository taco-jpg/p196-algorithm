# AC11 running log

- Read AGENTS.md, OPEN_PROBLEMS.md, docs/CELL_LEDGER.md, docs/FOCUS_SWARM.md, S08 verifier, rooted p12/m9 lattice data and #476 current coordination.
- Claimed exact phase-2 J3/J4 all-30-U endpoint-only cell (prior AB15 was PARTIAL); premises: (a) T12 width reduction, (r) even-centre correction, (t) temporary W9 healing allowed.
- Python physical pairword replay reproduced W9 failures. Fast last-non-nine carry cone agreed with independent two-seed propagation on 500 random examples x120=60,000 transitions.
- Exhaustive C++ disjoint intervals 0:27436, 27436:54872, 54872:82308, 82308:109744, 109744:137180 yielded 4,115,400 total cases, no unresolved/invalid, min known t120 prefix 172 and first W9 mismatch 135..149.
- Independently replayed 168 Python arbitrary-precision integers, genuine decimal reverse-and-add for 120 steps each, checking schoolbook normalization, pairword, phase clock and centre parity at widths q=14/20/40/80/160.
- Avoided strict-phase pruning and did not extrapolate random q controls into a universal-q proof. Negative result is specific to stationary short junctions at phase 2.
