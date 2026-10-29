# AC24: rooted phase-3 J5 endpoint obstruction

**Label: COMPUTED** (with a carry-prefix soundness lemma proved below).  
**Missing lemma supplied:** the rooted phase-3 stationary five-site junction branch of `PHYSICAL_TSTAR_RETURN_AT_REFERENCE_WIDTH` cannot satisfy its necessary W9 endpoint restoration, for any of the 30 charge-zero U3 rotations or any physically realizable palindromic centre.

## Exact scope and conclusion

Take the actual decimal p12/m9 row of `lat_p12m9.txt` at temporal phase 3:
`B3=[5,2,3,12,16,2,15,10,9,7,18,8,15,9,1,14,0,3,10,0,17,17,9,3,3,15,8,7,9,4,3,3,9,2]` and `W3=[4,0,17,11,9,12,2,9,2]`. For `J in {0,..,18}^5`, any of the 30 ordered rotations `U=rotate(9,a,18-a)`, `a=0,2,...,18`, any `k>=40`, and **any finite realizable palindromic centre C**, form the symmetric LSD-first coefficient word
`P=(B3++W3^14++J++U^k)++C++reverse(B3++W3^14++J++U^k)`.

**EXHAUSTED-NONE:** none of these `30*19^5=74,282,970` distinct J/U pairs can produce after 120 genuine ordinary decimal reverse-and-add steps the required fixed-interface return `P(14,k)->P(14,k+5)`. In every case, the final pairword already differs from `B3++W3^14` within a proved, centre-independent prefix. There are **0 unknown carry cases, 0 W9 endpoint restorations, and no first mismatch at or beyond the W9/J cut (index 160)**. The first mismatch indices are 134..154. The exact histogram, broken down by **every U rotation**, is in `HIST.csv`.

By the separately published phase-rotated T12 carry insertion/reset-cone theorem (`results/T12Rooted120CutPumping.md`, `results/V16Phase3EndpointNoReturn.md`), this rules out the **same literally fixed interface** for every independently large `q>=14,k>=100`. The direct enumeration at `q=14` is stronger in `k`, applying already to `k>=40`.

This is a restricted no-return result, **not a proof that a base-10 Lychrel number exists or does not exist**. Moving or growing junctions, q-changing returns, different intermediate seams, mixed U words, other clock phases, and 240-step cycles with changed intermediate seams remain outside its scope.

## Carry-universal prefix lemma (PAPER PROOF)

Let a symmetric pair-coefficient word of length `N>=2L` have known least-significant prefix `A` of length `L`, with coefficients 0..18. Its high `L` coefficients are necessarily `reverse(A)`, regardless of the unknown centre. Decimal normalization of the low prefix begins with carry zero; normalization of the high reversed prefix begins with an unknown carry `c in {0,1}`. The one-letter carry transfer `T_x(c)=floor((x+c)/10)` differs between 0 and 1 **if and only if `x=9`**. Consequently, the last non-nine letter at index `r` of A resets the unknown high inlet, and every high-side normalized digit paired with a low index `i<r` is identical for both inlets. The final high overflow `gamma` is also identical.

For `gamma=0`, the next pairword coefficient at index `i` is `lowDigit[i]+highDigit[i]`. For `gamma=1`, the new leading 1 shifts the opposite partner by one: coefficient zero is `lowDigit[0]+1`, and for `i>0` it is `lowDigit[i]+highDigit[i-1]`. Therefore the sound prefix transformer **retains** `r+gamma` universally forced coefficients (indices `0..r+gamma-1`), without claiming this is the maximal possible retained prefix. The rule can be iterated by induction without any assumptions about intermediate W9 integrity. It is an endpoint-only sound relaxation, **not** the strict-per-phase W9 MDD.

Start with `A=B3++W3^14++J++U^40` (285 letters). The physical paired length is at least 570. True reverse-and-add never decreases the digit length, whereas each abstract prefix length `r+gamma<=L`; thus opposite retained portions never overlap throughout 120 steps. Every J/U computation has a non-nine reset at every phase, so both possible high inlets give the same overflow and a sound retained prefix throughout. The independent B3W3-root prefix calculation gives phase-3 overflow `(0100)^30`, exactly 30 true length gains; it retains 70 unchanged root coefficients at step 120 even **without** a junction. With J/U^40, the complete exhaustive run finds a mismatch before index 160 and before the **individual candidate's** retained-prefix boundary in all 74,282,970 cases. This proves exclusion for every centre and `k>=40` without sampling those quantities.

## Reproduction and independent physical checks

Compile `g++ -O3 -std=c++17 centre_free_fast.cpp -o centre_free_fast`. For each `a=0,2,...,18` and `r=0,1,2`, run `./centre_free_fast 0 2476099 $a $r`. The code enumerates each J as five LSD-first base-19 digits, performs **all 120 sound carry-prefix transitions**, and rejects only a mismatch in the guaranteed endpoint W9 prefix, never an intermediate W9 mismatch. Every run reports `provedMismatch=2476099`, `UNKNOWN=0` and `clockBad=0`; the 30 per-U histograms and aggregate are in `HIST.csv`. `parse_logs.py` checks the exact intervals and histogram sums from saved `U0_full.log` through `U29_full.log`.

**Survivors by stage:** this engine deliberately makes no earlier rejection (temporary W9 damage alone is not a sound endpoint exclusion). Thus all 74,282,970 candidates are retained through phases 0..119, and **zero remain at the actual 120-step endpoint**. `HIST.csv` instead tabulates the more informative exact **first endpoint-mismatch position** (indices 134..154), not a misleading strict-W9-survival time.

`phase3.py` implements a separate schoolbook complete-pairword normalizer and arbitrary-precision Python `n+reverse(n)`. `abstract.py` implements the independent two-inlet prefix map. `validate.py` checks 125 true-decimal complete 120-step orbits (15,000 individual transitions) across five distinct q/k widths, verifying **each** predicted prefix and overflow. Another 900 stratified schoolbook/bigint 120-step controls span all 30 U, both odd/even C, and widths `(14,100),(40,160),(160,640)`; additional controls include centres of length 1..401 and `k=40`. A rare deepest mismatch `U=(6,12,9), J=(0,10,8,14,13)` occurs at index 154, still within a proved prefix, and matches both independent engines at q=14,20,40,80,160. These controls corroborate arithmetic; the centre-universal quantifier follows from the proof, not sampled widths.
