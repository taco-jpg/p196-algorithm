# AC37 running notes, 2026-10-29

1. Read AGENTS.md, OPEN_PROBLEMS.md, FOCUS_SWARM, CELL_LEDGER, FORMATS, the phase-4 rooted rows and #476 AB37/AB25/AB13 coordination. AB37's earlier phase-4/J6 cell sampled only 2,280 tuples.
2. Registered J[0]=0 phase-4/J6 in #476. Built a direct decimal digit-array endpoint checker with no strict-phase pruning.
3. Exploratory partial: J=(0,0,0,j3,j4,j5), all 19^3 tails, all thirty U and both C=[4,4] and [4,14,4], gave 411,540 actual endpoints, zero full returns. This does NOT complete the even-centre cell.
4. Phase-4 alternating sums 31 and 4 yield A(J)=A(U)=5 mod11 for a UNIFORM odd-centre recurrence; only two of thirty U words remain.
5. Finished all nineteen J[1] partitions for J[0]=0 and fixed odd C: 2,476,099 visited, 225,107 pass the all-width mod11 gate, 450,214 genuine exact endpoint runs with zero returns/clock violations. Histogram in REPORT.md.
6. Independent Python bigint on 190 controls, both surviving U, 19 J[1] partitions and q/k pairs (14,100),(20,80),(40,160),(80,320),(160,640) agrees with direct C++ first mismatch, length and clock. No certificate.

7. Replaced brute-force continuation with a stronger sound two-carry construction. Outer prefix 160->70 proves 120 genuine overflows for every rooted q>=14; central cone U^100 C rev(U)^100 retains at least 328 protected sites, and 60/60 U,C centre flanks differ from the demanded target. No T12, no strict-phase filter. Independently checked every intermediate state in 18,392 genuine bigint states. Stopped redundant brute-force J[0]=1..18 scan.
