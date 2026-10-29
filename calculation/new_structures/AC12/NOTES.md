# AC12 execution notes

- Read top AGENTS.md, OPEN_PROBLEMS.md, docs/FOCUS_SWARM.md, docs/CELL_LEDGER.md, both AUDIT_N reports and issue #476. Claim registered in #476 comment 6502534226, FEED in comment 6502734750. AB12's prior 12,000 / 8,230,800 cases were PARTIAL, so this is nonduplicate exhaustive completion.
- Published phase-3 rows: B3=(5,2,3,12,16,2,15,10,9,7,18,8,15,9,1,14,0,3,10,0,17,17,9,3,3,15,8,7,9,4,3,3,9,2), W3=(4,0,17,11,9,12,2,9,2).
- Physical gamma schedule phase3=(0100)^30. All counted 120-step trajectories gain exactly 30 decimal digits. Actual n+reverse10(n) implementation was independently checked against the carry-pairword C++ engine, not an in-place overwrite.
- The C++ engine enumerates base-19 J codes j0 fastest. J3 used [0,6859). J4 used disjoint [0,26065),[26065,52130),[52130,78195),[78195,104260),[104260,130321), all U/C combinations for each J. Results and histogram totals are in REPORT.md.
- Realizing the physical source: for each pair coefficient p_i use high=min(9,p_i), low=p_i-high, symmetric placement; odd centre midpoint half. Since B3[0]=5, source leading digit 5 is nonzero.
- Independent Python arbitrary-precision reverse10 addition and distinct schoolbook carry-normalization matched at every one of 120 transitions for both J lengths, both C parities and U examples at q/k=(14,100),(20,80),(40,160),(80,320),(160,640). The width sample is diagnostic; the published T12 paired insertion theorem supplies all-width implications.
- Further centre tests at lengths 1,2,5,6 reproduced identical W9-prefix mismatches on sampled J/U, consistent with T12's 26-position U reset separation. This scan does not solve the all-time decimal Lychrel problem.
