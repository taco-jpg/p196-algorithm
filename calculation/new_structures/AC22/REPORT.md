# AC22 phase-1 five-site junction carry-cut result
**Labels:** PAPER PROOF (carry-cut rule); COMPUTED (complete one-U enumeration). **NOT a decimal Lychrel certificate.**
**Scope:** rooted B1/W1 in `lat_p12m9.txt`, q=14, U in {(9,0,18),(0,18,9),(18,9,0)}, every 5-site J with coefficients 0..18, all k>=52, every palindromic realizable C. Only same-J/W9/U endpoint after 120 real decimal steps is excluded. Other 27 U rotations, phases, moving seams, and variable q are not excluded.

## Exact lemma (centre-independent endpoint rejection)
At any time the pair-coefficient word P is symmetric. Given its LSD prefix P[0..L-1], select the largest r<L with P[r]!=9. In decimal normalization of P, the carry after high-side coefficient P[n-1-r]=P[r] is **1 iff P[r]>=10**, independently of the unknown middle: incoming carry is either 0 or 1 and P[r]!=9. Normalize the low r coefficients with carry 0, the high r mirrored coefficients with this fixed entering carry. This determines the actual overflow gamma and the first r coefficients of the next symmetric pairword, with the gamma=1 high-end index shift included. Iterate the cut for 120 steps; neither an intermediate W9 match nor a bound on the unknown centre is assumed. If a known final coefficient differs from the proposed target, no completion of the unknown middle can make the endpoint return. This rule holds for every step and every symmetric decimal pairword with length >=2L; it does not claim that all candidate orbits are nonpalindromic forever.

For q=14 and k>=52, the first 320 source coefficients coincide with the stored B1 ++ W1^14 ++ J ++ prefix(U^infinity,155), independent of centre and k. Initial symmetric pairword length is >=642, and true reverse-and-add never reduces length. Consequently every successful 320-cut rejection applies simultaneously to all k>=52 and all palindromic C. The target prefix through first mismatch is likewise independent of k,C.

## Complete restricted enumeration
`g++ -O3 -std=c++17 -o ac22_cut calculation/new_structures/AC22/carry_cut.cpp`
`./ac22_cut --ai 0 --rot 0 --start 0 --limit 2476099 --initial 320`
Enumeration of exactly 19^5=2,476,099 base-19-coded junctions, no strict-phase pruning, neither PRNG sampling nor inferred prefix counts: **0 returns, 0 undecided cuts**, smallest final certified prefix length 149, first mismatch in indices 135..149 (0-based).
Histograms (index: count): `135:194636 136:58846 137:1125643 138:912927 139:99123 140:72381 141:5479 142:6111 144:492 145:369 146:48 147:36 148:3 149:5`; sum 2,476,099.
Four disjoint exhaustive intervals: [0,619025), [619025,1238050), [1238050,1857075), [1857075,2476099). Each yielded zero undecided cuts.
Independent Python **actual arbitrary-precision n+reverse(n)** controls cover 30 stratified J/U/C cases across (q,k)=(14,100),(20,80),(40,160),(80,320),(160,640), plus 40 targeted (J=0,1,1234567,2476098; both C parities at all five widths). Ordinary digit-array control agrees in mismatch and all 120 overflow bits; 30 overflows in every control.

**Limitations:** Other 27 U words remain UNDECIDED, and all-width q renewal, altered/moving junctions, endpoint nonpalindrome guards, and an all-time growing-band cycle remain open. This is a reusable necessary-condition lemma plus a narrow negative cell, not a proof that decimal Lychrel numbers exist.

## Additional complete U rotations, same carry-cut
U=(0,18,9) [ai=0,rot=1]: exactly 2,476,099/2,476,099 J5 junctions, zero return, zero undecided cuts; min known terminal prefix 148, mismatch 135..149. Histogram: 135:194768 136:58775 137:1125425 138:912935 139:99151 140:72492 141:5537 142:6007 144:502 145:423 146:46 147:23 148:9 149:6.
U=(18,9,0) [ai=0,rot=2]: exactly 2,476,099/2,476,099 J5 junctions, zero return, zero undecided cuts; min known terminal prefix 146, mismatch 135..149. Histogram: 135:194504 136:58840 137:1126151 138:912487 139:98985 140:72524 141:5551 142:6123 144:491 145:361 146:37 147:42 148:2 149:1.
Reproduce independently: compile carry_cut.cpp with g++ -O3 -std=c++17 -o ac22_cut, then execute ./ac22_cut --ai 0 --rot 1 --start 0 --limit 2476099 --initial 320 and the identical command with --rot 2. No strict-phase W9 pruning or centre parity filtering.
**Completed aggregate:** 7,428,297/7,428,297 J/U windows over all 3 rotations of (9,0,18), q=14, every k>=52 and every palindromic realizable C by the proved exact cut. Independent arbitrary-precision true-decimal controls: an additional 60 full 120-step runs at q/k=14/100,20/80,40/160,80/320,160/640, both centre parities, three J values and both new U rotations, agreed with the digit-array model.
**Still open:** the other 27 charge-zero U rotations, variable q, growing/moving seams and the complete decimal all-time certificate.
