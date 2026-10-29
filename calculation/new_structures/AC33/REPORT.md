# AC33 phase-0, six-column junction, fixed-prefix subcell
**Label: COMPUTED. Not a decimal Lychrel certificate.**

## Exact decidable predicate
Published rooted phase-0 B34/W9, 120 genuine decimal reverse-and-add steps, q=14, k=100, canonical symmetric coefficient source H C reverse(H), H=B W^q J U^k. Fixed |J|=6 and J[0]=J[1]=0, all J[2:6] in {0,...,18}^4, U in {(9,0,18),(9,8,10),(9,16,2)} (1-based U ranks 1/13/25), C in {[4,4],[4,14,4]}. Only endpoint-only restoration is tested, not phasewise strict W9; target is B W^q J U^(k+5) C reverse(...). No early pruning.

## Exact counts
Six configurations, each 19^4=130,321 distinct junction words; **781,926 ordinary-decimal trajectories**, 120 steps each. Every endpoint has +30 digits (the total is reported, not a proof of per-phase gamma for all cases). **0 W9-prefix restorations, 0 full template returns.** First disagreement is always coefficient 137 or 138, strictly before the W9 protected cut at 160. Combined histogram: index 137: 56,820; index 138: 725,106. U-wise histograms per centre: (9,0,18): (9,442,120,879), (9,8,10): (9,507,120,814), (9,16,2): (9,461,120,860).

This **exhausts only J[0:2]=(0,0)** for those three U and two fixed C, not the claimed full J[0]=0 slice (fraction 1/19 of that slice), not all 30 U, and not all palindromic centres. Reproduction uses true decimal digits, never in-place overwrite; compare every endpoint coefficient. Cross-checked 48 specified C++ singleton cases against independent Python unbounded-integer n+reverse(n), including the exact first mismatch. At q,k=(14,100),(20,100),(40,160),(80,320),(160,640) the independent implementation checked 30 additional U/C controls, all with gamma=(1000)^30, no intermediate palindrome and no return.

## All-width logical consequence and remaining lemma
By the **existing** T12Rooted120CutPumping theorem (PAPER PROOF, not independently reproved here), failure at (14,100) excludes a uniform same-J/C phase-0 120-step T* return for each listed fixed interface at **all q>=14,k>=100**. This is a finite reference-cell decision supplying an exact restricted no-go for the required physical fixed-seam return lemma. It does not exclude J[1]!=0, other U/C, mutable seams or q-changing returns, and does not establish any Lychrel number.

Odd-centre mod-11 only (existing R33/T12 gate): A([4,14,4])=-6=5 mod 11, so U=(9,8,10) has A(U)=0 and U=(9,16,2) has A(U)=6 and cannot support a uniform odd-C return even for arbitrary J. U=(9,0,18) has A(U)=5; its J[0:2]=0,0 gate admits 11,844/130,321 J words, all included in the unpruned census. **The even centre has no mod-11 pruning.** These observations were not used to prune any run.

## Reproduce
```bash
g++ -O3 -std=c++17 calculation/new_structures/AC33/census.cpp -o /tmp/ac33-census
for u in 0 1 2; do for c in 0 1; do /tmp/ac33-census "$u" "$c" 0 0; done; done
python3 calculation/new_structures/AC33/independent.py
```
Run intervals `lo hi` partition 0..130321 without overlap, summing histograms. Link: docs/CELL_LEDGER.md for scope discipline; calculation/new_structures/T12/NOTES.md for the independent-width theorem. No claims beyond the stated finite predicate and its T12 implication.
