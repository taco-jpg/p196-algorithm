# AC18 dated research log (2026-10-29)

- Read AGENTS.md, OPEN_PROBLEMS.md, FOCUS_SWARM, CELL_LEDGER, audited N/Nseries summaries, and p12/m9 rooted data.
- Registered phase-9 |J|=3/4, 30 U, endpoint-only two-centre-parity task in #476.
- Found phase-9 B_9[0]=1. A physical realization must have a nonzero leading digit; choose the high partner of coefficient 1 to be 1, and its low partner 0. This is why a coefficient-10 mismatch inferred from an invalid leading-zero split is not a sound filter.
- Derived centre-independent carry collar: since every pair coefficient <=18, normalization carry is in {0,1}. Propagate both possible incoming carries at the high end of a known palindromic collar. Only emit prefix positions identical under both cases. The resulting prefix is exact for ANY palindromic interior.
- Wrote C++ exhaustive J/U search and Python independent schoolbook and unbounded-integer audit. Randomized 10,000 single-step collar cases matched full normalization. 96 full physical 120-step independent tests at q=14,20,40,80,160 (k=100,80,160,320,640) agree, both centre parities.
- Method intentionally does NOT enforce W9 at intermediate times, unlike strict-phase MDD.
- Exhaustive four-way split completed: 4,115,400/4,115,400 J/U pairs, no unresolved, min radius 163, mismatch indices 135..150 (all strictly within W9), 30 genuine overflows each. Independent centres therefore need no doubled enumeration.