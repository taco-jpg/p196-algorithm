# W10: a mod-9999 cyclic-carry clock lifted to a finite decimal zero moat

**Overall label: COMPUTED.** Every decimal orbit claim here concerns the single seed 5346 repeated 8,000 times. There is no infinite Lychrel claim, no claim about decimal 196, and no Lean theorem.

## Distinct constructions

Define the fixed-width toroidal map F4(u) = (u + rev4(u)) mod 9999, with rev4 reversing all four digits, including leading zeros. An exhaustive 0..9998 residue-graph scan gives exactly one recurrent directed cycle containing no four-digit palindrome: 5346, 1782, 4653, 8217. Every other recurrent cycle contains a four-digit palindrome. This is NOT ordinary reverse-and-add: reduction modulo 9999 folds overflow back to the low end. The cycle is only a seed-selection heuristic.

For the *ordinary decimal* seed N0 = int('5346' * 8000), compute canonical digits, unbounded integer addition and ordinary reversal at every step. Its number of digits increases from 32,000 to 40,323 in t=20,000 iterations, with exactly 8,323 length increases. None of the 20,001 states is palindromic.

Write n_t for the actual length and d for its LSB-first digits. Let a_t = t+64. At every state t=0..20000 the implementation checks d[i] == d[i+4] for every i in [a_t, n_t-a_t-4] and checks P_i == P_{i+4}, where P_i = d_i + d_{n_t-1-i}, when both pair indices lie in the lower half. At t=20000 there are 192 checked digit-period comparisons and 93 checked pair-period comparisons. The interior is thus nonempty and has period four at every step, but neither the full number nor the boundary words are periodic. This is a finite-horizon pair-word shape, not a closed certificate.

## Four-cell transducer

For a 4-periodic LSB-first central row r[0..3], let h=(n-1) mod 4. Its coefficient tile is p[j]=r[j]+r[(h-j) mod 4]. Define cyclic carries c[0],..,c[4] in {0,1} by c[j+1]=floor((p[j]+c[j])/10) with c[4]=c[0]. The successor row is r'[j]=(p[j]+c[j]) mod 10. At least one cyclic fixed carry exists because the carry return function on {0,1} is monotone; uniqueness fails exactly when every p[j]=9. This is a local steady-bulk rule, not a global digit-update rule.

The small transducer predicts the next observed central row in all 19,999 transitions having a unique cyclic fixed carry, and the one neutral/ambiguous transition is deliberately not counted. The observed central four-digit row first becomes 0000 at t=33. As the checked central region has period 4, that checked region is an all-zero moat thereafter, through t=20000. This does not imply the boundary defects remain separated forever.

## Independent reproducibility

All resources under calculation/new_structures/agent-W10/:
- cyclic_clock.py enumerates the entire 9,999-state toroidal graph, asserting its unique all-nonpalindromic four-cycle.
- period4_replay.cpp performs literal decimal least-significant-first carry addition, checks every state's palindrome status, checks every digit and paired-coefficient in its guarded interval, and validates the independent four-site carry predictor.
- gmp_replay.cpp uses GNU MP mpz_class for arbitrary-precision addition; it independently converts the full integer to decimal, reverses its canonical decimal string, parses that integer and adds it. It never uses the digit-array update or period assumptions.
- checkpoints.tsv has 21 checkpoints spaced 1,000 steps apart, each recording length, cumulative overflow count, central tile, per-step period errors, and an FNV-1a 64-bit hash over all decimal digits in LSB-first order.
- run.sh compiles both engines, runs the exact 20,000 transitions, compares both engines' whole-number hashes, length and overflow counts at all 21 checkpoints, and compares the digit results with the committed TSV fixture.

Execute: bash calculation/new_structures/agent-W10/run.sh (requires Python 3, C++17, g++, libgmpxx and libgmp). Palindrome checks do NOT depend on hashes; each implementation scans all decimal digits at every step. Hashes serve only as independent whole-number checkpoint comparisons.

## Positive research direction

The finite cyclic clock suggests a boundary-to-zero converter that might periodically renew the protected moat. An infinite base-10 certificate would require a return of both boundary defect states, carry and length-mod-4 phase, with nondecreasing interior protected length and a nonpalindrome guard at every edge. Neither the mod-9999 hint nor this finite replay proves such a return. This report states no new exclusion result.
