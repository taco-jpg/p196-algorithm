# AC08 log (2026-10-29)
- Inspected AGENTS.md, OPEN_PROBLEMS.md, docs/FOCUS_SWARM.md, docs/CELL_LEDGER.md, phase-0 lattice, audit reports, #476 claims and prior AB08 claim. Registered AC08 CLAIM in #476.
- Implemented true-digit decimal checker. Fixed an initial output-buffer resizing bug before exhaustive scans and independently validated the corrected implementation.
- Exhaustive length-7/8 scans all U; exact odd-centre endpoint mod-11 filtering and exhaustive length-9 scans all U. No centre fixed points.
- Independent Python big-integer width controls and 168 C++/Python pointwise checks. Unfinished lengths are PARTIAL, never promoted to EXHAUSTED.
- Missing all-time lemma: a sound growing-band return with both boundary carry ports and same J/C.