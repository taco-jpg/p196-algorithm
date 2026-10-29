# Agent N19: synchronized-counter centre and a six-phase decimal clock

**Labels:** PAPER PROOF for the conditional counter-certificate soundness and the six-cycle central light-cone lemma; COMPUTED for the explicit six-step decimal family at the listed widths and for 20,000-step independent replays; UNDECIDED for an infinite decimal orbit or universal six-edge instance proof.

## Nonregular certificate format (new search space)

A state is `(q,k)` with finite clock q and unbounded integer counter k>=k0. Its *folded* palindromic pairword is `H_q(k)=L_q ++ U_q^(k-a_q) ++ J_q ++ V_q^(k-b_q) ++ R_q` (coefficients in 0..18), and the actual pairword is `H ++ reverse(H)` for even length, or `H ++ reverse(dropLast(H))` for odd length. Every odd-length centre entry must be even; the leading coefficient is positive. The two different repeat blocks share the *same* counter, enforcing equal increments: for distinguishable letters, `{a^k c^k}` is not regular and cannot be represented by a finite DFA over folded pairwords. A clock edge may update k to k+d_q (including d_q=1), with whole-word length changing only by the ordinary decimal overflow 0 or 1. If every edge satisfies the **universal** arithmetic relation `step(P_q(k))=P_{q'}(k+d_q)` for all k>=k0, if every phase has an odd coefficient (a sufficient nonpalindrome guard), and if one actual integer has the initial pairword, then the integer is a base-10 Lychrel number. **PAPER PROOF:** induct on steps; pairword normalization depends only on the previous pairword; an odd pair coefficient excludes a palindrome because a palindromic number's pair coefficients are all even. This theorem is conditional: no base-10 cycle is asserted.

**Finite verification format:** for fixed blocks and fixed offsets, all synchronized convolutions of an input/expected output edge have form `X0 (X1)^k X2 (X3)^k X4` after finitely many boundary alignments. Reverse-add on folded pairwords is an exact finite-state *two-ended carry relation*: each folded column has low incoming carry `l`, high outgoing carry `r`, guesses high incoming carry `r'`, and must satisfy `l'=floor((x+l)/10)`, `r=floor((x+r')/10)`. Its output letters are determined by low/high remainder digits and at most a one-digit delay when the overflow is 1; terminal states enforce centre parity and matching carries. Product with a proposed output-word recognizer gives an NFA of **bad** edges. The number of Boolean transition matrices is finite; powers of both repeating-block matrices are eventually periodic. Therefore testing finitely many k (preperiod plus lcm of matrix periods) decides the universal edge assertion. This is a sound finite-counter-certificate FORMAT, even if the matrix period is computationally enormous. No executable all-k matrix checker is claimed for the example below. Unlike a regular-language certificate, its invariant can be nonregular.

## Explicit decimal two-counter propagation

Set folded `H0(k) = [10] 8^k [5,11] 16^k [8]` for k>=5, with full even-length pairword `P0(k)=H0(k)++reverse(H0(k))`. A concrete positive-leading seed N is obtained by splitting each coefficient x into a low digit `max(0,x-9)` and opposite high digit `min(9,x)`; concatenate the low half and reversed high half (LSB first). This gives genuine decimal integers, all nonpalindromic by the coefficient 5 or 11.

The observed exact time-t folded words for t=0..6 are parameterized by `L_t u_t^(k-a_t) J_t v_t^(k-b_t) R_t`:

|t|L|u|a|J|v|b|R|
|---|---|---:|---:|---|---:|---:|---|
|0|10|8|0|5,11|16|0|8|
|1|1,9|16|1|13,7,9|14|1|15,16|
|2|3,9,13|14|2|7,16,9,9|10|2|12,14|
|3|7,9,7|10|3|9,16,13,0,0|2|2|6,10|
|4|14,18,15,1|2|4|0,14,7,1,0|4|2|13,0|
|5|5,14,15,7,3|4|5|2,5,12,8,1,4|8|2|4|
|6|11,9,11,15,6|8|5|4,11,4,17,2,8|16|2|8|

The six-step phase **resets the bulk symbols (8,16)** but **unbalances the synchronized counter**: the first bulk has k-5 columns, the second k-2, an emergent skew of +3. This is a concrete positive two-counter memory mechanism, not a periodic bounded kink. Exact pairword computation verifies all seven forms at k=5..200 and at k=201,333,500,750,1000,2000, with additional independent Python big-integer arithmetic for k=5..20. The identity for *all* k is still UNDECIDED in this report (a finite transfer-matrix certificate, rather than extrapolation from tested widths, is needed). It is not a closed orbit: the exterior L/J/R changes, and the two counters diverge.

## Separate long-lived six-cycle central corridor

For any even coefficient x in `S=(8,16,14,10,2,4)`, carrying through a block of repeated x resets the carry after its first letter to `c*=[x>=10]`. Each subsequent normalized digit is `(x+c*) mod 10`; the next pair coefficient in the *interior* is twice this digit. Hence a symmetric central block of k>=2 equal pair coefficients maps, regardless of the surrounding coefficients and overflow, to a central block of at least k-1 equal pair coefficients, with cycle `8->16->14->10->2->4->8`. **PAPER PROOF:** both sides of the symmetric block settle to the constant carry after one uniform cell; the possible overflow shifts pair matching by at most one position, so at most the outermost paired coefficient is lost. The odd-length centre has even coefficient, giving the same terminal carry. This is finite-speed shielding, not an infinite certificate; k may decrease.

For `L=22000` choose the actual decimal seed whose most-significant-first digits are `9 8^L 0^L 1`, of 44002 digits. The entire reverse-add trajectory was computed to step **20,000 inclusive** by (i) a direct C++ least-significant-first digit-vector engine and (ii) an **independent GMP integer** engine that converts each actual integer to decimal, reverses its string, parses it as a new integer and adds. All 20,001 states were nonpalindromic in both; both complete values agree at all seven reported hash checkpoints, and both have the same final central uniform halfwidth **15,411** and final digit count **52,235**. The theorem independently guarantees at least 2,000 central columns at step 20,000 (initial 22,000 minus 20,000); observed shrinkage is slower.

The six-cycle corridor is **not** an infinite Lychrel proof: a finite initial corridor may eventually be consumed by the advancing outside disturbances. To turn the counter format into a certificate, search for a time-periodic pair of exterior emitters that replenish the two counter bands at least as fast as their distinct erosion speeds, and certify the synchronized transfer edges by matrix semigroup rather than fixed-width SAT. This is the explicit search redirection.

## Exact reproduction

From repo root, with Python 3 and a C++17 compiler plus GMP development libraries:

```
python3 calculation/new_structures/agent-N19/counter_six.py
python3 calculation/new_structures/agent-N19/fold_check.py
g++ -O3 -std=c++17 calculation/new_structures/agent-N19/replay_digits.cpp -o /tmp/n19_digits
/tmp/n19_digits 22000 20000
g++ -O3 -std=c++17 calculation/new_structures/agent-N19/replay_gmp.cpp -lgmpxx -lgmp -o /tmp/n19_gmp
/tmp/n19_gmp 22000 20000
```

Compare the FNV64 checkpoints and minimum width with `calculation/new_structures/agent-N19/checkpoints.csv`. All claims are decimal-only where marked COMPUTED, all parameter-wide theorem claims are conditional or labelled PAPER PROOF above. No Lean verification is claimed.