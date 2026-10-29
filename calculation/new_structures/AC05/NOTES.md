# AC05 notebook, 2026-10-29

- Reviewed AGENTS.md, OPEN_PROBLEMS.md, docs/FOCUS_SWARM.md, docs/CELL_LEDGER.md, audits N/Nseries, R30's independent verifier, and rooted p12/m9 lattice data. Posted CLAIM #476 comment 6502496718.
- Corrected an initial harness bug: the first mismatch may lie left of the centre and have a negative offset; success must be tested by a sentinel, not `offset < 0`. All reported census runs used the corrected code.
- The cut-port accelerated evaluator is exact when its external carry ports match the baseline; otherwise it switches to the uncompressed full digit-array engine. Full-vs-port agreement: 5,760 stratified generated cases, 0 mismatches and 0 port fallbacks.
- Independent Python bigint and schoolbook decimal digit-array checks: 120 complete trajectories (3 U words, 8 centre lengths, 5 q/k width pairs), 14,400 transitions, identical state after each transition, 30 genuine overflows in each trajectory. These are controls, not an all-time certificate.

- Corrected an initial invalid centre-only use of the FULL-return mod-11 gate A(C)=(1,4,8). The sound CENTRE-only test instead uses T12's protected centre cone, baseline outside invariance, and A(P_120)=0 mod11 to require A(C)=(0,7,9) mod11. The former criterion was discarded completely from the reported centre census. At t=1 the physical length is even and step 2 puts N in 11Z; all later states stay there. No even centre is pruned.
- Independently checked exact centre-gate survivor counts for length 11: (2,251,022; 2,251,022; 2,251,028), each of 24,760,990. Complete actual clock-preserving endpoint scans of all survivors found zero radius-170 returns. Tested the direct alternating sum of 12,000 random target coefficient words against the specialized gate.
- Additional cross-width C++ port-versus-full checks: 2,400 controls, 0 errors/port fallbacks, with q/k=(14,100),(20,80),(40,160),(80,320),(160,640).

- Exact unpruned radius-5 centre scan L7,L8: 596,733 cases, zero matches; L9: 3,909,630 cases, exactly ONE radius-5 match at U2, C=[2,1,13,4,2,4,13,1,2], and it fails radius-6 at offset -6 (physical coefficient 5 vs target 9). Independent Python-bigint replay at q/k=(14,100),(20,80),(40,160),(80,320),(160,640) reproduces that precise near miss. Any all-J exclusion at L9 MUST use radius>=6.
- Python-bigint junction independence check for 864 controls, all three U, L7..14, arbitrary junctions J=[0],[17,18],[5,4,2,13,0,3],[0]*7 and q/k=(14,100),(20,80),(40,160): all 10 central coefficients on each side agree with fixed J=[5], confirming T12's predicted separation.
