# AgentR33P12Mod11ParityCorrection
**PAPER PROOF:** For every palindromic pairword P=H C rev(H), A(P)=0 if |C| is even; if |C| is odd, A(P)=2A(H)+(-1)^|H| A(C), where A is the least-significant-first alternating sum.
**Correction:** Q39's rooted p12/m9 necessary mod-11 equations A(U)=A(C) and 2A(J)+(-1)^|J| A(C)=0 are equivalent to mod-11 zero for ALL independent q,k only with ODD |C|; they MUST NOT prune even-length centres.
**Concrete arithmetic control:** B34/W9 from lat_p12m9.txt, U=(9,2,16), J=(4), C=(12,4,4,12) violates both equations but P(q,k) is 0 mod 11 and physically realizable for every q,k.
**COMPUTED checks:** 16 q,k controls at 20/40/80/160, independent native integers/digit-list; 120 genuine overflow steps at four widths. The 12 outer root gates and 90 temporal-period-10 U3 words (30 complementary-nine) also independently reproduce.
**Scope:** A search-pruning bug fix and parity-complete modular necessary-condition lemma. NOT an actual 120-step return, a decimal Lychrel certificate, or a proof of the Q cut-charge no-go.
**Code/proof:** calculation/new_structures/R33/{audit.py,TARGET.md,NOTES.md,IDEAS.md}.
**Reproduce:** python3 calculation/new_structures/R33/audit.py
