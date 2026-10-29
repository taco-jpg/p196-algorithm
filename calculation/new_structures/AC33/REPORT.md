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

## 2026-10-29 extension: complete J0=0 odd centre, additional even-centre slice

**Label: COMPUTED** (plus previously published PAPER-PROOF mod-11 and T12 gates). The fixed phase-0 120-step same-J/C/U return is impossible for **all 7,428,297** junction/U combinations J[0]=0, J[1:6] in {0..18}^5, U=(9,0,18),(9,8,10),(9,16,2), with the odd palindromic centre C=[4,14,4]. This is a completed restricted cell, *not* a decimal Lychrel certificate or an exclusion for other centres.

**Sound exact pruning:** For odd C, A(C)=4-14+4=-6=5 mod 11. The known parity-complete mod-11 all-width return gate requires A(U)=A(C), and for |J|=6 requires 2A(J)+A(C)=0 mod 11. The U alternating residues are 5,0,6 respectively. Thus U=(9,8,10) and U=(9,16,2) each fail for **all 19^5 J suffixes** (4,952,198 exact cases). U=(9,0,18) passes the U gate; with J0=0, the J gate becomes -J1+J2-J3+J4-J5=3 mod 11. Independent residue DP and direct 2,476,099-word enumeration both give **225,077 survivors** and **2,251,022 gate failures**. Every survivor was then replayed by genuine two-buffer ordinary-decimal arithmetic, 120 full steps, canonical source and endpoint-only W9 test, without intermediate strict-phase pruning; **0/225,077** restored the W9 prefix. Total arithmetic gate failures: **7,203,220**, true-decimal replays: **225,077**, sum = **7,428,297**. The T12Rooted120CutPumping theorem supplies the independently variable width equivalence from (14,100) to all q>=14,k>=100. The all-width no-return applies ONLY to these fixed interfaces and this centre; other C, U and moving seams remain open.

The physical first-mismatch histogram for the 225,077 gate survivors (W9 prefix cut=160): index 135:9,170; 137:9,611; 138:202,105; 139:3,737; 140:282; 141:122; 142:44; 144:3; 145:3. All 225,077 gained exactly 30 digits. The **six farthest-mismatch cases** were rechecked at five widths with an independent Python big-integer engine (30 exact replays), all with (1000)^30 overflow and nonpalindrome guard:
- index 145: J=[0,18,4,11,0,5], [0,9,4,1,17,8], [0,18,13,1,17,8].
- index 144: J=[0,9,9,5,0,14], [0,18,18,5,0,14], [0,18,18,14,9,14].
The mismatch position at other widths is the listed index + 9(q-14). No W9 restoration or second-epoch candidate was found.

**Additional unpruned fixed-centre subcell:** J[0:2]=(0,1), U all three, C=[4,4] (even) or [4,14,4] (odd), each of the 6 choices times 19^4 junction suffixes. All **781,926/781,926** physically replayed reference cases fail W9 at coefficients 137..140, independent of any strict-W9 phase pruning. In combination with the original J[0:2]=(0,0) six-cell exhaust, the remaining even-centre portion has **781,926** decided cases. Consequently the parent **J[0]=0, 3 U, 2 fixed C** cell is now **PARTIAL(8,210,223/14,856,594)**, with exactly 6,646,371 even-C cases J1=2..18 still open. Do not call that parent EXHAUSTED.

Reproduce from repository root:
```bash
g++ -O3 -std=c++17 calculation/new_structures/AC33/census_gated.cpp -o /tmp/ac33-gated
/tmp/ac33-gated 0 1 0 -1
for u in 0 1 2; do for c in 0 1; do /tmp/ac33-gated "$u" "$c" 0 1; done; done
python3 calculation/new_structures/AC33/audit_gate.py
```
The J1=-1 mode applies the proven odd-C mod-11 gate **only** when U=(9,0,18), C=[4,14,4], J0=0; other U ranks are eliminated algebraically as above. For even centre no mod-11 pruning is sound. The existing `independent.py` is a separately coded arbitrary-precision `n+int(str(n)[::-1])` implementation; `audit_gate.py` checks all six near-misses at five widths. These are all restricted necessary-condition decisions, not an all-time decimal certificate.
