# AC29 notes

- Read AGENTS, OPEN_PROBLEMS, FOCUS_SWARM, CELL_LEDGER and AB29's issue #476 PARTIAL prior to CLAIM.
- Exact new cell: rooted phase8 J5 all30 U, fixed odd C=[4,14,4]. Used T12 protected-cut recurrence, even-centre parity correction and NO strict intermediate-phase W9 pruning.
- Phase8 W reset loss is 92, NOT phase0's 91. Protected cut 52 remains valid: endpoint cut 68. U losses <=152/122, smaller than margins 165/135; this supports the all-width-to-reference reduction for each J,C,U.
- A(B8)=-42, A(W8)=40, A(C)=-6: all-width odd-centre mod11 gate A(J)=6 and A(U)=5. Exact admissible J/U count 450214, 73832756 skipped as impossible all-width returns.
- Thirteen contiguous J-code windows [0,2476099) scanned over all U; all 450214 unpruned candidates tested for 120 exact decimal carries, 0 returns, no clock or intermediate digit-palindrome violations. No finite survival claim.
- Independent bigint replay: 35 C++ versus Python width/candidate controls; phase8 independent insertion bigints: 120 W/U comparisons across U/C.
- Even C has no mod11 gate; 30000 sampled endpoint cases found 0 returns; status PARTIAL only.
