# AC16 notes
- Reviewed AGENTS.md, OPEN_PROBLEMS.md, FOCUS_SWARM.md, CELL_LEDGER.md, S08/verify.py, V16/strict_w9_cell_local.cpp, issue #476 AB16 PARTIAL and current CLAIMs. Phase 7 had AB16's 60,000 physical controls, not a complete cell.
- Five contiguous unpruned endpoint-only C++ batches, each 823,080 cases; aggregate 4,115,400 tested, zero restorations, zero clock failures.
- Independently recreated carry-collar arithmetic; random and true-bigint controls at five widths, both C parities, all passed. Cone bounds W=91 U={(149,120),(150,119),(151,121)} with positive 170-site guard margins.
- Failed idea: an 11th-coefficient outer-root obstruction arose from accidentally using phase-6 W with phase-7 B in an early scratch control. Corrected source shows intact early exterior; **that false argument was discarded and not committed**. The endpoint-only collar proof is the result.
