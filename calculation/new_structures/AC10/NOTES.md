# AC10 running notes
2026-10-29: Read AGENTS.md, OPEN_PROBLEMS.md, docs/CELL_LEDGER.md, AUDIT_N/AUDIT_Nseries, lattice_formats/FORMATS.md, p12/m9 lattice data, R30 independent checker, and issue #476 tail. Registered CLAIM AC10 on #476.
Derived an exact sparse-difference carry algorithm; built prototype and dense per-time audit; caught and fixed one reference-timestep indexing bug.
Recomputed all three U at |C|=7,8. Completed |C|=9,10 in disjoint chunks, tally 11,934,660 center-word endpoints, zero positive, zero gamma divergence. Independent Python bigint 120 samples, five width settings, all 120 phases.
Lengths 11..14: first and last 25k index samples for every U/length; zero returns, NOT an exhaustive cell.
No strict-W9 phasewise pruning, no odd-centre mod-11 pruning of even C, no false decimal-certificate claim.
