# Agent X19: two commuting decimal 99-reservoir increments (COMPUTED)

## Explicit finite four-orbit mechanism

Put `N(Q,R) = 12(99)^Q34(99)^R56(99)^Q78` (the parentheses denote repeated literal **two-digit decimal** `99` blocks), and write `F(n) = n + reverse_decimal(n)`. For every `t = 0,...,20000`, the four ordinary base-10 integers `F^t(N(Q+i,R+j))` for `(i,j) in {0,1}^2`, **with `Q=5500`, `R=6300`**, have all of these properties:

1. Each is nonpalindromic by direct decimal digits. Stronger: its symmetric pairword `P_t(k) = d_k + d_{len-1-k}` (LSD-first) has an odd coefficient; across all four orbits and all times, the minimum number of odd pairword entries is 2.
2. Along either Q-edge, the longer ordinary decimal digit word, grouped in LSD-first base-100 pairs, can be reduced to the shorter one by deleting exactly two `99` blocks, without changing another cell. Along either R-edge, exactly one `99` is deleted.
3. Independently of the preceding property, along each Q-edge the *full palindromic pairword* of coefficients 0..18 can be reduced to the shorter pairword by deleting exactly four `18` cells, and along each R-edge exactly two `18` cells. This explicitly tracks the shape of the pairword at **every** step. Insertion sites may depend on time and parameters; no permanent-site or global-Q,R statement is inferred.
4. The base corner is recomputed at every step using a separate **most-significant-first decimal string** arithmetic algorithm and compared digit by digit to the least-significant-first vector computation. The final base corner has 42,903 decimal digits (34,608 initially), and the running base-corner digest after all 20,001 states is `3b6facc7d66a409d` (FNV64, see source).

The four-edge square is a *positive* two-counter mechanism: the Q increment appears in two separate outer reservoirs, while the R increment is an independent central reservoir. Both increments survive simultaneously for at least 20,000 true decimal transitions; changing either parameter alone cannot account for this square. No time-cycle, recurrent return, or infinite-time theorem is asserted.

## Reproduction and independent controls

From repository root run:

```
bash calculation/new_structures/agent-X19/reproduce.sh
```

`dual_replay.cpp` is a standalone ordinary decimal digit-vector simulator. On each time slice it explicitly checks palindrome absence, a four-edge base-100 `99` insertion square, the independent pairword `18` square, and a separate MSB-first decimal-string reverse-and-add implementation for the base corner. The pairword insertion matcher uses greedy subsequence matching for an inserted *fixed* symbol (`18`); independently, 200,000 randomized small cases were differentially checked against exhaustive dynamic programming. `independent.py` uses Python arbitrary-precision integers and an independently implemented set-valued deletion automaton, checking `(Q,R,steps)=(5,5,13),(10,20,25),(20,20,50),(100,100,300)`, and a deliberate mutated-insertion negative control.

`first_break.cpp` independently scans Q,R in `{5,10,20,40,60,100}` using the same exact digit and pairword predicates and writes `first_break.csv`. For `(100,100)`, the pairword 18-insertion edge fails at 393 steps for the outer Q parameter and 337 for the centre R parameter. The displayed grid gives the *first failure of the stated insertion property*, not a palindrome or a first-collision theorem for all parameter values. Its near-separate dependence on Q and R is a constructive clue for a future product-of-renewal-clock template, but **not** an observed superlinear or exponential lifetime.

## What a sound infinite-time extension would require

A finite certificate can use the two-parameter template `T_t(Q,R)` with Q repeated symmetrically in the exterior and R central. To imply a never-palindromic decimal orbit, it must establish, using a bounded local carry interface rather than sampled values, exact one-step arithmetic for **all** permitted Q,R, an odd pairword coefficient at all times, and either a finite time-cycle or a well-founded indefinitely repeatable macro-renewal with all resource updates nonnegative. The present four-corner checks are deliberately not substituted for universal carry-interface quantification. The centre first loses the 18-insertion property at 337 for the finite `(100,100)` control, providing a concrete, exactly located failure to target with a phase-dependent repair.

**Label COMPUTED.** Not Lean-verified, not a base-10 Lychrel certificate, and not a claim about 196.
