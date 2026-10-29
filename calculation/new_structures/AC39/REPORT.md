# AC39: phase-6 outer-prefix shield; correction to AB39

**PAPER PROOF**, conditional on 120 explicitly checked finite carry transitions; **COMPUTED** physical independent controls. Not a decimal Lychrel certificate, no claim of a whole-word return or all-time nonpalindrome.

## Exact arbitrary-interior theorem

Let `n_0` be a canonical positive decimal integer with symmetric digit-pair coefficients `P_0[i] = digit_i(n_0) + digit_(N-1-i)(n_0)` (least-significant first), `N >= 320`. If its first 160 coefficients equal the canonical zero-based phase-6 rooted exterior `A_0=B_6 ++ W_6^14`, then **for every possible interior** its 120 ordinary reverse-and-add steps have exactly the phase-6 rotation of `g=(1000)^30` as their 120 actual digit-overflow bits, total 30, and `P_120[:70] == A_0[:70]`. In particular `P_120[12]=1`. The `B_6/W_6` are read directly from `calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt`, not phase-0 data.

All canonical `B_6 ++ W_6^q ++ J ++ U^k ++ C ++ reverse(...)` source words with `q>=14` satisfy the premise, regardless of J length, U word, and odd/even centre. This **contradicts AB39's reported phase-6/J6 universal first mismatch index 12** (observed 0 versus expected 1). Its observation is not sound for the canonical phase-6 template and cannot prune an endpoint-only search. This theorem decides *only the outer-prefix necessary boundary*; the junction/U/centre return and nonpalindrome guard are still missing.

## Sound two-ended carry induction

Suppose `P_t` is a symmetric length-`N` coefficient word, `N>=2w`, with known least-significant prefix `A` of width `w`. Because `P_t` is symmetric, its upper length-`w` suffix is `reverse(A)`. Ordinary decimal normalization has known lower inlet carry zero and unknown upper inlet `c in {0,1}`. These **exhaust** upper carry possibilities since every pair coefficient is between 0 and 18 and `c' = floor((coefficient+c)/10)` remains binary. Compute the lower `w` output digits `L` by normalizing `A` with carry zero, and the upper `w` digits `R_c` by normalizing `reverse(A)` with each upper inlet. Let `g_c` be the upper normalization overflow. The next coefficient prefix for `g_c=0` is exactly `L_i + R_c[w-1-i]`; for `g_c=1` it is `L_0+1` at index zero and `L_i+R_c[w-i]` at indices `1..w-1`. This shift accounts for the genuine newly added most-significant digit, not an assumed periodic clock.

For each step the certificate evaluates **both** inlet carries, confirms equal overflow bits, and retains their longest common output prefix. That prefix is valid for every unknown interior, by induction. Exactly 120 arithmetic iterations from the published 160 coefficients give lengths `160 -> 70`, losing one position on each of 90 non-overflow steps and zero on each of 30 overflow steps. The terminal 70 coefficients literally equal the initial first 70. Since reverse-and-add does not decrease decimal length, at each stage `N_t >= 320 >= 2w_t`. Thus the induction has no hidden centre, W9 strict-phase, mod-11 parity, or width hypothesis beyond the stated source.

The 90-position shield depletion is why the argument **does not** prove a periodic seam repair or all-time orbit. It neither excludes nor constructs any returning junction.

## Reproduction and independent decimal controls

`python3 calculation/new_structures/AC39/prefix_shield.py --check`

The program checks all 120 exact recurrence steps and independently realizes 68 canonical source numbers at q/k=(14,100) covering all 30 charge-zero U3 rotations and both fixed centre parities, plus q/k=(20,80),(40,160),(80,320),(160,640). Each transition is checked with BOTH Python arbitrary-precision integer reverse-add and an independent schoolbook decimal digit-array engine: 8,160 matched genuine steps. Every control has site 12=1 and the first 70 coefficients restored; none of the 68 whole words returns. The controls are examples only, not a full junction census.

**Missing all-time lemma to supply next:** a simultaneous carry-sound restoration of the full W9/J/U/centre interface (or provably closed moving-seam epoch map) for every length, plus intermediate nonpalindrome guards. This theorem supplies the exact uniform phase-6 outer-boundary condition for that interface calculation and corrects a false early-index no-go.
