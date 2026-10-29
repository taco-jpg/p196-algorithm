# AC35 phase-2 J6 / J0=0

**COMPUTED, restricted endpoint census; no decimal Lychrel certificate.** Phase-2 rooted B2/W2, q14/k100, J=(0,j1,...,j5), U3 rotations, 120 genuine reverse-add steps, endpoint P(14,105). No strict intermediate W9 pruning.

Even C=(4,4), U=(9,0,18): all 19^5=2,476,099 J tails scanned; 0 W9-prefix restorations and 0 whole returns, all 30 overflows.

Odd C=(4,14,4): an all-width literal return requires A(U)=A(C)=5 and A(J)=3 modulo 11 (alternating sums), by the odd-centre mod-11 gate. Only U zero-based ranks 0 and 28 are eligible; for J0=0 exactly 225,077 tails per U satisfy the J gate. Both complete 225,077-tail physical 120-step scans (450,154 total) give 0 W9-prefix restorations and 0 returns. This does NOT claim fixed-reference-width failure for mod-11-rejected cases.

Reproduce: compile census.cpp with g++ -O3 -std=c++17 -fopenmp. Run census for arguments (Urank,J0,Ctype,limit,q,k,oddgate) = (0,0,0,2476099,14,100,0), (0,0,1,2476099,14,100,1), (28,0,1,2476099,14,100,1).

Independent controls: Python bigint reverse-add vs separate LSD-first digit-array exact at all 120 steps for 7 J x3 U x2 centres x5 widths (25,200 steps). Best odd candidates J=[0,3,7,16,5,12], U=(9,0,18) and J=[0,0,5,16,2,10], U=(18,0,9) were checked at q20,40,80,160 as well; first mismatches remain W9 cut minus 11/14. Control gamma=(001000100010)^10.

**Scope:** no all-time witness, no even-centre all-U result, no arbitrary-centre or moving seam no-go. The published T12 is phase-0; a phase-2 all-width lift is not assumed without proof. This is a partial negative cell only.