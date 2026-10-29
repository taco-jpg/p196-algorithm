# AgentW17BinaryCentreAlphabet
**COMPUTED**: a 32,768-element explicit base-10 centre-alphabet family that restores a p8/m20 spatial band for three consecutive 88-step macros; NOT an infinite certificate.
From phase-0 entrance B (length 39) and W (length 20), let U be 40 coefficients initially all 1; independently change U at indices 0,2,4,6,8,10,12,14,16,18,22,26 from 1 to 10 (12 bits), U[13], U[20] from 7 to 16, and U[30] from 6 to 15 (3 bits).
Set C=[8,0,0] ++ U ++ [16] ++ reverse(U) ++ [0,0,8] and P_q=B ++ W^q ++ C ++ reverse(W^q) ++ reverse(B). All indices zero-based, coefficients least-significant first.
**Exhaustive exact arithmetic**: all 2^15=32,768 centres at q=1 survive 352 steps without palindrome, retain the 39-column p8 exterior and overflows 10101010, and have complete W renewals at steps 88,176,264 (core lengths 131,175,219).
At the fourth macro (352), after removing B and the q-1 spare bands, the attempted new W matches exactly 2/20 coefficients in all 32,768 cases; there is no closed cycle.
**Independent ordinary decimal-digit controls**: 8 centre selections, q=1..4 (32 seeds) through 352 steps agree at every full pairword; no palindrome.
**Independent long replay**: q=225, mask=4095, special=7 gives 9,165 to 19,165 decimal digits at step 20,000; GMP big integer, schoolbook digit list, and coefficient engine agree every step, with prescribed 39-column exterior and zero palindromes.
Reproduce: cd calculation/new_structures/agent-W17 && c++ -O3 -std=c++17 alphabet_renewal.cpp -lgmpxx -lgmp -o alphabet_renewal && ./alphabet_renewal lattice.txt 4096 && ./alphabet_renewal lattice.txt 1 --long
Code/data: calculation/new_structures/agent-W17/{alphabet_renewal.cpp,lattice.txt,observations.json}.
No all-2^40 theorem, no 4th renewal, no self-replenishing centre, no universal q, no Lean verification, and no decimal Lychrel claim.