# Agent W20: programmable decimal centre collision gate
**COMPUTED**, not a base-10 Lychrel existence proof. This builds on N18's three-renewal centre by making the *incoming central payload* variable and measuring its exact delayed scattering, not by repeating the earlier fixed-centre witnesses.

## Exact construction and semantics
All words are least-significant-first pair coefficients. Read the rooted 39-by-8 exterior and the phase-0 spatial period-20 band W from `calculation/new_structures/agent-N18/lattice.txt` (47 rows: 39 of length 8, then 8 of length 20). Let B be the time-zero exterior column, and let U be 43 coefficients equal to 1 except `U[13]=7, U[20]=7, U[30]=6, U[40]=x, U[41]=y, U[42]=z`. Define `C=[8,0,0] ++ U ++ [16] ++ reverse(U) ++ [0,0,8]` (length 93), and for q>=1 the symmetric pairword `P(q;x,y,z)=B ++ W^q ++ C ++ reverse(W^q) ++ reverse(B)`. This is a valid decimal integer using digit pairs `(min(P_i,9), P_i-min(P_i,9))` and central digit 8; its first high-end digit is 8, hence no initial leading zero.

A coefficient step normalizes `P` in base 10 with carry from the least significant end and pairs the resulting decimal digits against their reversal. This is exactly the pairword under true `N -> N+reverse(N)` (finite arithmetic identity). At time t, a full 20-column renewal is the exact equality of columns `[39..58]` to W (for q=1); for q>1 use the cut `39+20*(q-1)` to observe the centre-facing W after removing q-1 outer bands. The check also enforces all 39 time-phase exterior columns (index j, phase t mod 8). An odd exterior coefficient at every checked phase proves the ordinary integer cannot be palindromic.

## Exhaustive positive scattering table
A full deterministic scan of all 19^3=6,859 assignments `(x,y,z)` for q=1 uses exact coefficient transitions and checks the exterior at every time t=0..264. **Every payload** has a complete W prefix at t=88 and t=176. At t=264 the exact prefix length is: 8 for 64 cases (lexicographic example 4,0,3); 13 for 603 cases (example 8,1,8); 20 for 6,192 cases (example 0,0,0). For all 6,192 complete third renewals, t=352 returns prefix length 2 and the exterior still matches all 39 columns. The 667 non-full cases are not claimed to be palindromes or exclusion results; their 8/13-prefix outcomes give two reproducible, positive scattering channels, versus the full 20-column channel.

This is a **programmable delayed collision**: the last three digits of U control a spatially localized disruption of the third 88-step band return, while earlier returns are unaffected. The finite alphabet of observed output signatures `{8,13,20}` is a potential interface alphabet for assembling multiple centre-repair devices. It does not prove a composition law, eventual renewal, or any infinite-time invariant. Crucially, changes to deeper sites need not improve the fourth return: all full-third cases tested here have only a 2/20 fourth prefix when q=1.

## Independent checks
`ordinary_integer_oracle.py` advances genuine Python arbitrary-size integers by constructing `int(str(N)[::-1])`, separately from coefficient normalization. It checks the three lexicographic representatives at q=1,2,3,4, matching every full 39-column exterior at each step and comparing whole centre words (after stripping q-1 periods) at t=88,176,264 and t=352 when applicable. All 12 runs pass, with q-independent centre-return words. Exact scope: q=1..4 for **representatives only**, not all 6,859 payloads.

Two independently written C++ arithmetic paths also validate the (0,0,0) codeword at q=240 for 20,000 reverse-add updates: (i) direct decimal-digit vector addition plus separately recomputed pairwords, checked against the coefficient evaluator at every step; (ii) GNU GMP `mpz_class` ordinary integer addition with decimal-string reversal (does not use pairword dynamics). Both check nonpalindrome and 39-column shape at every time t=0..20000; seed has 9,771 decimal digits, final has 19,771, 10,000 length overflows, all first 39 columns remain exact, and the GMP step-20000 FNV64 (over most-significant-first decimal ASCII) is 16422078354326034688. There is no periodic-centre claim or extrapolation beyond t=20000.

## Reproduce (repository root)
```
g++ -std=c++17 -O3 -Wall -Wextra -Werror calculation/new_structures/agent-W20/renewal_gate.cpp -o /tmp/w20_gate
/tmp/w20_gate scan calculation/new_structures/agent-N18/lattice.txt
python3 calculation/new_structures/agent-W20/ordinary_integer_oracle.py calculation/new_structures/agent-N18/lattice.txt
/tmp/w20_gate long calculation/new_structures/agent-N18/lattice.txt 240 20000
g++ -std=c++17 -O3 -Wall -Wextra -Werror calculation/new_structures/agent-W20/independent_gmp.cpp -lgmpxx -lgmp -o /tmp/w20_gmp
/tmp/w20_gmp calculation/new_structures/agent-N18/lattice.txt 240 20000
```

## What remains open
The collision alphabet needs an **exact splicing or reset transfer law** between two gates such that the 20-column channel replenishes itself after each reflection. The present fourth return is only 2/20 for every full-third codeword with q=1; no finite cycle has been found. A productive next experiment is to optimize *earlier* (positions below 40) and permit nonuniform phase/width changes, rather than extending the independently invisible deeper suffix. This is a constructive search redirection, not a no-go theorem.
