# Exponentially many distinct decimal seeds coalesce at the third reverse-add step

**PAPER PROOF.** This is an exact all-parameter `k >= 1` construction of a *three-step ordinary-integer collision fibre*, not an infinite non-palindromic orbit, periodic centre, or decimal Lychrel certificate. It is stronger than the already committed `Agent5P12OneStepExponentialFiber` in the essential way that the target is a **single identical integer**, not merely a common pairword.

## Statement and concrete construction

The committed `lattice_input.txt` records the reachable absorbing-lattice bulk with base 10, exterior width 34, time period 12, spatial period 9, overflow schedule `100010001000`. Use temporal phase `t=3`; its bulk row is `W3=(4,0,17,11,9,12,2,9,2)` and the successor phase-4 bulk row is `W4=(8,1,15,4,0,5,5,18,4)`. Notably, `W3` has no adjacent nines and `W4` has no nines. Fix any integer `k>=1` and let `n=200+18*k`, an even length. Define the symmetric pair-coefficient word `P` of length n by taking the phase-3 34-column exterior at the low end, then periodic `W3[(i-34) mod 9]` on the rest of the lower half and reflecting it to the upper half. Every coefficient lies in 0..18 and the outermost coefficient is positive.

For `i=0,...,k-1`, let `j_i=52+9*i`; these are separated by nine columns, their three-cell intervals are disjoint, and `j_(k-1)+30 < n/2`. On any subset `S` of the k indices, replace the three coefficients at lower-half positions `j_i,j_i+1,j_i+2`, together with their reflected upper mates, from baseline `(4,0,17)` to `(8,10,12)` whenever `i in S`. Each is a **connected** three-site change; the three new coefficients all differ from their old values. Let `P_S` be the resulting palindromic coefficient word.

Convert `P_S` into a canonical n-digit positive decimal integer `N_S` by splitting a reflected pair coefficient q at lower index `i` into the high mirrored digit `u=max(q-9, 1 if i=0 else 0)` and the low digit `q-u`. This makes both end digits nonzero and lies in the decimal digit alphabet. The map S -> P_S -> N_S is injective. Then for **every** S, `R^3(N_S)` is a single fixed integer, where `R(N)=N+reverse_digits(N)`. Moreover the 2^k integers `N_S`, `R(N_S)` and `R^2(N_S)` are each pairwise distinct. Thus the common integer is reached for the first time at the third reverse-add step, simultaneously by 2^k distinct orbits.

## Exact finite response and all-k induction

A symmetric pair coefficient word P determines its next integer exactly: normalize P from the least significant column with the usual base-10 carry; this produces the actual decimal digits of `R(N)` for *every* N realizing P. A new symmetric pairword is formed by adding reflected digits. There is no arbitrary template assumption in this step. For the phase-3 `gamma=0` lattice, the exact normalized one-switch successor pairword equals the phase-4 baseline pairword except for the lower-half changes

```
index:          j      j+1      j+2
new minus old: +9        0       -9
```

and exactly the reflected changes at the upper-half sites. The identities follow from the ordinary column carry formulas `c_(i+1)=floor((P_i+c_i)/10)` and `digit_i=(P_i+c_i) mod 10`, checked by `composition_certificate.py` on both source length parities and six translated positions, and previously established in the independent two-step connected local-cone theorem `Agent5P12TwoStepConnectedCoalescence`. The phase-3 word has no consecutive 9 coefficients, so an incoming carry discrepancy resets as soon as it encounters a non-9 column, never requiring more than two unchanged cells. The changed coefficient intervals are separated by six unchanged columns. In particular **each input switch has the same first-step response irrespective of the other switches**, with no cross-switch carry interference. The infinite number of translations is justified algebraically by spatial period nine, and all interfaces retain at least 30 columns of margin from the centre.

Likewise, the phase-4 next pairword contains no coefficient 9; every phase-4 column resets the carry independent of its incoming bit. Therefore a pairword whose first-step perturbation consists of any number of disjoint translated `(+9,0,-9)` triples has the *exact same second-step pairword* as the baseline. This is simply local finite-cone cancellation copied across the independent blocks, not an induction assumption about the centre. The next overflow bit is 1 for every constructed word because the exterior and its final carry are unchanged; the first overflow bit is zero for the same reason. `composition_certificate.py` independently recomputes both full-word successor pairwords, verifies the additive first-step response and zero second-step response on every subset up to k=8 and selected subsets at k=12,20,40, and checks the actual carried spatial rows and the no-nine reset premises. Period-nine invariance and reset outside the local cone are the finite proof that lifts these checks to *all* k.

Let S != T, and let `j` be their smallest differing switch position. Before j their first-successor pairwords agree, and at j they differ by +9 or -9. Thus the weighted integer values of those first-successor pairwords are **different modulo `10^(j+1)`**. Since the **second-step integer** is exactly the numeric value of the first-successor pairword, `R^2(N_S) != R^2(N_T)`. The first-step integers also differ: their pairwords are different. The initial integers are different by explicit digit construction. But the complete **second-step pairwords** coincide; the reverse-and-add operation is determined by that pairword, so all the **third-step integers** are identical. This proves both the size `2^k` and exact first coalescence time three, not just a lower bound on fibres with possible early collisions.

## Independent reproduction and controls

Run from repository root (standard Python only):

```
python3 calculation/decimal_frontier/lattice_kinks/three_step_fibre/run_checks.py
```

All necessary source, input and checkers are in the same commit under `calculation/decimal_frontier/lattice_kinks/three_step_fibre/`: `composition_certificate.py` independently normalizes complete coefficient words and checks every first-step delta and second-step output; `independent_integer.py` independently constructs actual n-digit integers, performs ordinary Python big-integer reverse-add through step 3, tests complete pairword realization, verifies all second-step integers are distinct, and asserts common third-step integer. Exhaustive subset checks for k=1,2,3,4,8,12 cover `2+4+8+16+256+4096=4382` positive seeds; the largest, 4096 separate 416-digit integers, all coalesce at step3. The primary checker tests all subsets through k=8, and random/extreme subsets at k=12,20,40 to exercise nonadjacent and long translated configurations. The strong mathematical conclusion comes from exact carry-reset/periodic-block identities, not from treating these finite tests as proof by extrapolation.

All supporting files are small. This construction makes no assertion that the common third-step integer, any source integer, or any later iterate avoids palindromes; no base-10 Lychrel number is claimed.
