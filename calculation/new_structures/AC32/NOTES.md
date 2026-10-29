# AC32 working log

1. Registered CLAIM in #476, read AGENTS, problems, ledger, AB32 partial and R30 realization.
2. Built real decimal C++ reverse-add engine with canonical digit source; no strict-phase pruning.
3. Reproduced W9 first-mismatch band in 11,000 initial endpoint samples.
4. Computed correct phase-11 A(B)=6,A(W)=-12; phase-0 congruence is inapplicable.
5. Proved uniform odd-C necessary A(J)=2,A(U)=5 mod 11 and DP counted 450,234 admissible windows.
6. Scanned every one of 450,234 at (q,k)=(14,100): zero endpoint/W9 returns; first mismatch index 135..148.
7. Independent CPython bigint vs schoolbook verified all 120 transitions in 20 controls at five widths; 45 randomized Python digit-array vs C++ individual endpoint checks passed.
8. Even-centre and nonuniform endpoint-only domains explicitly left open.
