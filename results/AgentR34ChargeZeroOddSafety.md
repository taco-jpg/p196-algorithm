# AgentR34ChargeZeroOddSafety
**PAPER PROOF.** For the decimal cyclic two-sided absorbing-row map, let S be all 30 rotations of (9,a,18-a), with even a in {0,2,...,18}.
Each row contains exactly one 9, with its other two entries even and summing to 18.
Write F_g for the exact cyclic-carry bulk successor with arbitrary true overflow g in {0,1}.
For u=(9,a,18-a), F_0(u)=(9,b,18-b), b=(2a+2) mod 22, and F_1(u)=(c,18-c,9), c=(8-a) mod 20; both b,c are even in [0,18].
The reverse-direction cyclic carry and forward cyclic carry each reset within one three-letter block; spatial rotation commutes with F_g. Hence F_0(S)=F_1(S)=S, **for any binary overflow sequence and any number of phases**.
An actual palindrome has pair-coefficient word consisting entirely of even entries. Therefore **any genuinely protected complete U3 bulk row in S is an all-time nonpalindrome witness**, regardless of outer seam/centre details.
Scope: this proves *safety conditional on surviving a protected bulk block*, not that one survives forever, nor a complete 120-edge rooted decimal renewal.
Independent ordinary-bigint/digit-array controls at q=k=20,40,80,160, and exact 120-phase protected-interior checks for all 30 rows at q=20,k=160, pass.
Reproduce: `python3 calculation/new_structures/R34/odd_witness.py`.
Missing lemma it supplies to an all-time proof: **phase-independent nonpalindromicity of the protected charge-zero U3 band**; regenerative W9|U3 seam return remains UNDECIDED.
