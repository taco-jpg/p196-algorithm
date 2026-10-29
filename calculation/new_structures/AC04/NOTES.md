# AC04 work log

- Registered CLAIM in issue #476. Read AGENTS.md, OPEN_PROBLEMS.md, docs/FOCUS_SWARM.md, docs/CELL_LEDGER.md, lattice FORMATS.md, p12/m9 rooted input, R30 checker, AB04 coordination and #476 tail.
- Built exact coefficient normalizer and centre-only comparator, no strict W9 phasewise pruning; physical overflow clock checked.
- Complete unpruned C7/C8 for all three U rotations: 3*(68,590+130,321)=596,733 candidates, none restored the central U/C collar.
- Sound carry-set abstraction, allowing all inner C completions, excludes respectively 228/361,25/361,82/361 two-letter prefix classes for each C length 7..14; excludes 5237/6859,1638/6859,2633/6859 three-letter classes for C14.
- Crosschecked 14,400 individual decimal steps using independent Python true-bigint replay at five q,k choices, all U and lengths 7..14; no discrepancy.
- Local git DNS unavailable; GitHub connector used. No Lean files were changed. C9..14 remain UNDECIDED.
- Stronger symbolic carry-mask pumping theorem: ALL L>=7, not merely C7..14; finite 1,083 U/outer-two-letter runs, min core run K_t=2 across 120 phases, 335 excluded infinite centre-prefix cylinders, no ambiguous overflow. Proof and reproduction appended to REPORT.md; independent 60 physical bigint controls checked.