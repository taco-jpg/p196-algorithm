# AC42 NOTES, 2026-10-29

- Read AGENTS.md, OPEN_PROBLEMS.md, docs/FOCUS_SWARM.md, docs/CELL_LEDGER.md, FORMATS.md, AUDIT_N.md, AUDIT_Nseries.md, the phase-9 lattice and R30 verifiers, and issue #476 page 2. Registered an explicit nonduplicated claim in #476.
- Ran 1,200 sampled genuine phase-9 J0=0 cases at q14/k100, both centre parities, with first endpoint mismatch at indices 135..143; these samples do **not** exclude any complete cell.
- Rejected an unsound strict-phase W9 MDD endpoint exclusion; no claim of a J/C-independent cone was proved.
- Proved exact two-epoch odd-centre mod-11 feasibility gate; DP enumerates 19^5 and 19^6 residue classes; direct independent 19^5 enumeration agrees. Posted FEED in #476.
- Cross-checked 20 true-bigint vs schoolbook cases across five widths for 240 steps apiece; 4,800 steps agree. Does not prove a 120-step fixed-seam return. Even centre not pruned.
