# AC26 work log
- Read AGENTS.md, OPEN_PROBLEMS.md, FOCUS_SWARM.md, CELL_LEDGER.md, lattice data and R30 verifier sources.
- Registered CLAIM in #476 for phase=5, |J|=5; compared AB26's reported index-7 mismatch.
- Derived unknown-inner-carry sound cone; fixed initial indexing of the high reversed suffix before validation.
- At q14, protected length 160->70 after 120 edges, g=(0001)^30, prefix equals target; all interiors universally covered.
- Tested 2000 randomized one-step symmetric pairwords; 150 T* controls across five q/k scales with independent bigint and every digit-array step.
- Tested 6,000 distinct J/U/C from first 100 base-19 J words per U/centre, C++ endpoint-only, zero returns; mismatches 134..144.
- Five additional distinct 6,000-tuple base-19 J slices (start 100,1000,10000,100000,1000000), zero returns and first mismatches >=134.
- Posted BREAK on #476 about AB26's false index-7 report. No all-time decimal Lychrel certificate or exhaustive J5 result.
