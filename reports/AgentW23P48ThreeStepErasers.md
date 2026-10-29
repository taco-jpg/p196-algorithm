# W23: A non-gauge three-step eraser on the decimal period-48 lattice

**COMPUTED**, finite scope. No infinite decimal Lychrel number is proved. Unlike the period-3 four-step eraser of AgentN28, this is a two-cell eraser INSIDE the period-8 temporal/48 spatial absorbing lattice, precisely the unsolved decimal frontier. The construction is a discrete zero-arrival-time (absorbing front) rather than another passive receding boundary.

## Exact mechanism
All pair coefficients are least-significant-first, 0..18. Use the period-48 rec2 lattice `W` and depth-11 rooted exterior `B=(17,5,0,2,1,9,15,18,14,9,3)` from `calculation/decimal_frontier/lattice_formats/p8_scc.txt`. At spatial phase 20, replace `(13,9)` by `(8,5)` in a distant bulk interior. Differences are -5 and -4, neither divisible by 9, so this is not the one-cell ±9 carry-gauge erasure. Under actual overflow bits `gamma=1,0,1`, the local change supports at t=0,1,2,3 are respectively {0,1}, {0,1,2}, {0,2}, and empty. Direct finite-window table at the insertion position (two preceding cells through five following cells):

| t | untouched bulk | modified bulk |
|---|---|---|
| 0 | 5,17,13,9,7,3,13,10 | 5,17,8,5,7,3,13,10 |
| 1 | 11,13,12,3,17,10,7,5 | 11,13,16,13,12,10,7,5 |
| 2 | 3,8,5,8,15,1,15,10 | 3,8,14,8,6,1,15,10 |
| 3 | 7,11,13,13,14,7,7,7 | 7,11,13,13,14,7,7,7 |

The search enumerates 48 positions times (19² - 1) changes = 17,280, each with a 960-coefficient periodic window and 16 temporal steps. It computes ascending and descending binary carries independently and then forms the paired next coefficients with the prescribed gamma shift. The *complete* source/changed arrays (not only the table window) are compared each step. Exactly five non-gauge substitutions erase, all at t=3:
`(offset 20,13,9)->(8,5),(8,14),(17,5),(17,14)` and `(offset 23,3,13)->(7,9)`. There are 101 gauge-type one-step erasures. The m20 companion scan has no non-gauge eraser among 7,200 substitutions; that comparison motivates using the m48 component, not a general impossibility claim.

## Real, independent ordinary decimal verification
Let `H_q=B ++ W^q ++ [10,14,1,10]`, and `P_q=H_q ++ reverse(H_q[:-1])` (an odd-length symmetric coefficient word). Realize it as an ordinary canonical decimal number by assigning each noncentral coefficient p the low digit max(p-9,0), high digit min(p,9), and the central coefficient 10 to digit 5. For a patch at index `11+48*(2+6j)+20` of H, substitute (8,5) for (13,9), and reflect. With j=0..4, the five independent switches give 32 distinct q40 seeds, length 3,869. Plain Python built-in arbitrary-precision N+reverse(N) verifies 32 distinct integers at t=0,1,2,3, their complete pairwords all equal at t=3, and their **integers all identical at t=4**; no palindrome at t=0..4. It separately verifies every one of the five different patch types at q8.

For q100 (initially 9,629 decimal digits), the all-five-patch and unpatched seeds coalesce at step 4. Two independent ordinary-decimal engines (C++ digit vector and GMP mpz with decimal-string reversal) replay through t=20,000. Every state is nonpalindromic, actual length overflow is 1010... (10,000 overflows), and all first eight pair coefficients follow the known eight-phase rooted path. Final length 19,629 digits and both engines' low-first FNV-1a 64-bit digest `971e60282dc35bc9` agree. A 20,000-step finite orbit is **not** an infinite certificate.

## Precise implication and missing piece
The five patches are **self-repairing defects, not a self-replenishing centre**. This gives a positive, rooted decimal reset/alphabet primitive on the m48 lattice, and demonstrates that at least 32 different centre/bulk perturbations can collapse to a single future state after four updates. It is especially relevant to tropical first-arrival searches: local front lifetime is exactly 3 rather than an extrapolated speed. A successful next construction must *emit* these repairs at a sustained rate and prove a finite transition cycle with a nonpalindromic witness; a one-off eraser and arbitrary initial repetitions supply neither renewal nor infinity.

## Reproduction
From repository root:
```sh
g++ -std=c++17 -O3 calculation/new_structures/agent-W23/eraser_sweep.cpp -o /tmp/w23_sweep && /tmp/w23_sweep
python3 calculation/new_structures/agent-W23/bigint_short.py
g++ -std=c++17 -O3 calculation/new_structures/agent-W23/digit_replay.cpp -o /tmp/w23_digit && /tmp/w23_digit 100 20000
g++ -std=c++17 -O3 calculation/new_structures/agent-W23/gmp_replay.cpp -lgmpxx -lgmp -o /tmp/w23_gmp && /tmp/w23_gmp 100 20000
```
Compact expected values are in `expected.json`. No Lean verification, unrestricted-q erasure theorem, global stationary front, or decimal Lychrel certificate is claimed.
