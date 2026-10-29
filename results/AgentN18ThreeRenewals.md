# AgentN18ThreeRenewals
**COMPUTED:** three consecutive 88-step decimal lattice-band renewals, from a 87-coefficient palindromic centre; NOT an infinite Lychrel proof.
Use width-39 B and period-20 W from `calculation/new_structures/agent-N18/lattice.txt`; `T_q(C)=B ++ W^q ++ C ++ reverse(W^q) ++ reverse(B)` (pair coefficients low-first).
Let U have forty entries 1, except `U[13]=7,U[20]=7,U[30]=6` (indices 0-based); `C=[8,0,0] ++ U ++ [16] ++ reverse(U) ++ [0,0,8]`.
For each q=1,2,3,4, the exact decimal coefficient dynamics satisfy `G^88(T_q(C))=T_q(C1)`, `G^176(T_q(C))=T_q(C2)`, `G^264(T_q(C))=T_q(C3)`, with identical q-independent centres `|C1|=131,|C2|=175,|C3|=219` (initial length 87).
Every intermediate t=0..352 matches the eight temporal B exterior rows; overflow follows 10101010; exterior contains an odd pair coefficient, giving a certified non-palindrome witness for these finite steps.
Fourth macrocycle cannot renew: at t=352, after removing B and q-1 W bands, the new centre (length 303) matches only first 2/20 W coefficients.
Fixed two-parameter 19x19 constructive grid of `U[20],U[30]` with other U fixed finds exactly four triple-renewal hits: (7,6),(7,15),(16,6),(16,15); no global exclusion claimed.
Independent Python *ordinary decimal integers*, separate from coefficient normalization: seeds with 205,245,285,325 digits each replay 352 operations; 0 palindromes, all exteriors valid and all three entire pairword templates/corresponding q-independent C1,C2,C3 match.
Reproduce from `calculation/new_structures/agent-N18`: `g++ -std=c++17 -O3 three_renewal.cpp -o three_renewal && ./three_renewal && python3 check_three_renewal.py`.
This realizes a finite glider-like repair across THREE successive lattice periods. Next construct a fourth by synthesizing a deeper backward preimage with a nonuniform exterior phase slip.
Scope strictly finite: q=1..4 and 352 operations; no universal-q closure, Lean result or decimal Lychrel certificate.
