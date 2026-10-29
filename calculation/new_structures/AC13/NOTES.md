# AC13 running log

- Read AGENTS.md, OPEN_PROBLEMS.md, docs/FOCUS_SWARM.md, docs/CELL_LEDGER.md, B4/W4 lattice data, S08/verify.py and issue #476. AB13 phase4 J3/J4 remained PARTIAL at 12,000 fixed-centre trials.
- Naive 0/1 incoming-high-carry branch enumeration hit 185,139 prefixes at phase 31. Retaining only their common prefix prevents combinatorial explosion and remains sound.
- Starting from B4++W4^14 alone, a 160-coefficient prefix shrinks to length 70 by phase 120; insufficient. Adding U^50 retains >=183, covering the entire target 160-cell W9 prefix even for unknown centre.
- Full 30 U rotations x (19^3+19^4) J tested: 4,115,400 exact, 0 unresolved; certified first mismatch 134..151, 0 high-overflow ambiguities. No strict-phase-W9 filter.
- Independent Python bigint replay: 30 deterministic U/J controls, 5 q/k widths, alternating even/odd C, 120 genuine additions; 150/150 full prefix checks passed. Additionally 60 q14 controls tested both parities; 1,000 randomized carry-lemma/real-bigint crosschecks passed locally.
- No decimal all-time certificate; longer/moving seams, other phases and q-uniform exclusion undecided.
