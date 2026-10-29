# AgentN18TwoRenewals
**COMPUTED:** explicit base-10 centre that replenishes the period-20 band for TWO consecutive 88-step macrocycles; not an infinite Lychrel certificate.
Use B and W from `calculation/new_structures/agent-N18/lattice.txt`; for each q=1,2,3,4 let `T_q(C)=B ++ W^q ++ C ++ reverse(W^q) ++ reverse(B)`.
Set `U=[1]*20` with `U[13]=7` (zero-based), and `C=[8,0,0] ++ U ++ [16] ++ reverse(U) ++ [0,0,8]` (47 coefficients, palindromic).
For each q, `G^88(T_q(C))=T_q(C1)`, `G^176(T_q(C))=T_q(C2)`, where `|C1|=91`, `|C2|=135` and C1,C2 are *exactly independent of q=1..4*, checked at every step with expected temporal B and overflow word `10101010`.
The next 88-step output at t=264 has only the first 8 of 20 W coefficients: third renewal fails, but the 39-column exterior still matches throughout all 264 steps.
Small constructive parameter scan `U[13]=0..18` with all other U digits 1 finds precisely `7` and `16` giving two renewals (no all-centre exclusion claim).
Independent conventional Python arbitrary-size integers: each of four explicit seeds, 165/205/245/285 decimal digits, replayed exactly 264 steps (0 palindromes), exterior B checked EVERY step, t88 and t176 checked by whole pair words; all agree on C1,C2.
Reproduce: from `calculation/new_structures/agent-N18`, `g++ -std=c++17 -O3 two_renewal.cpp -o two_renewal && ./two_renewal && python3 check_two_renewal.py`.
Novel mechanism: backward target repair of an 88-step moving centre, realizing two positive lattice-band renewals rather than one; next task is synthesizing a third renewal via multiple separated centre defects and an exact cut-automaton.
Scope: finite q=1..4 and 264 steps; no universal q, third renewal, or infinite decimal certificate is proved.
