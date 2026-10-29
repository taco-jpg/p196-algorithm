# AC29 phase-8 fixed-seam odd-centre obstruction

**Label: COMPUTED** (exhaustive endpoint test with a PAPER PROOF carry-reset reduction). Not a decimal Lychrel certificate.

**Scope:** rooted p12/m9 phase 8; H=B8 W8^q J U^k, |J|=5, C=[4,14,4], 30 U rotations of (9,a,18-a) for even a, and the exact 120 genuine decimal reverse-and-add return H C reverse(H) -> H' C reverse(H') with q fixed, k increased by 5, and unchanged J/C. No such all-width return exists for independent q>=14,k>=100.

**All-width necessary gate:** A(X)=sum (-1)^i X_i; A(B8)=-42, A(W8)=40, A(C)=-6. The target is divisible by 11 after the first overflow and a subsequent even-length step. Comparing q even and k of both parities yields A(J)=6 mod11 and A(U)=5 mod11. Only U=(9,0,18) and (18,0,9) survive. This eliminates 73832756 of 30*19^5=74282970 J/U pairs from the all-width language. These are NOT sound exclusions for isolated single-width return without insertion equivalence.

**Phase-8 T12 lift:** exact two-carry protected-insertion analysis gives the 120 rooted B/W phase transitions with (1000)^30 clock. Relative to phase-0, the phase-8 W reset loss is 92 (rather than 91), leaving boundary index 68 beyond the protected cut 52. The 30 U3 cycles close with reset losses at most 152/122, inside insertion margins 165/135. Thus Return(q,k) for all independently large q,k is equivalent to Return(14,100) for each fixed J,C,U. The finite-kernel calculation and 120 genuine big-integer insertion controls corroborate this paper adaptation; not Lean-verified.

**Full endpoint census:** 450214 mod-11-admissible J/U pairs were all tested through 120 genuine folded-decimal steps at (14,100), without intermediate W9 pruning. Zero returned, zero clock violations, zero intermediate decimal palindromes. First endpoint mismatch indices and exact counts: 135:141966, 136:82087, 138:105734, 139:102512, 140:9970, 141:6525, 142:690, 143:633, 144:32, 145:62, 147:1, 148:2. Sum 450214, all strictly inside W9 (indices 34..159). Separate unbounded Python n+reverse(n) replay agreed with compiled engine on 35 candidate/width controls, q/k=(14,100),(20,80),(40,160),(80,320),(160,640).

**Nonclaims:** even C=[4,4] remains PARTIAL (30000/74282970 tested, 0 returns); no odd-centre theorem for other C; no moving/growing seams, other phase classes, or base-10 Lychrel existence resolved. Reproduce with local code in this directory and `odd_aggregate.json`.
