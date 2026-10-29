# AC15 phase-6 J3/J4 fixed-seam endpoint obstruction
**Label: COMPUTED (exhaustive at stated finite junction scope, with a paper carry-cone soundness argument). NOT a decimal Lychrel certificate.**

**Exact missing repair lemma decided:** No stationary junction of length 3 or 4 in the rooted phase-6 p12/m9 W9|J|U3 family can provide the necessary W9-preserving 120-step repair edge at q=14, for any charge-zero U3 rotation, any k>=100, and any realizable symmetric centre. This rules out this short fixed-seam route, not moving seams, q-changing returns, arbitrary q, or a base-10 Lychrel existence proof.

Data: phase-6 B6=(2,11,3,6,0,1,17,7,2,14,9,14,1,2,9,5,9,17,14,4,17,4,12,15,9,18,9,7,10,16,10,6,12,8); W6=(5,9,16,0,9,11,1,10,8); 120-clock starts at phase 6 of (100010001000)^10. The tested initial symmetric pairword is H ++ C ++ reverse(H), with H=B6 ++ W6^14 ++ J ++ U^k. All P coefficients 0..18; odd C must have even middle coefficient for decimal realization. The target has identical B6,W6,J,C,U and exponent k+5. Failure of the first 160 coefficients is sufficient to refute the full endpoint.

## Exact centre-independent carry-cone lemma (paper proof)
For any symmetric pairword P of length L with a known first N coefficients x (N<=floor(L/2)), decimal normalization of P has carries in {0,1}. The low-side digits for x are uniquely determined from incoming carry 0. On the high mirrored side, normalize x in reverse index order, with an *arbitrary* incoming bit from the unknown interior. A coefficient x_i<=8 resets the carry to 0 and x_i>=10 resets it to 1; only x_i=9 transmits the incoming carry. If j=max{i:x_i!=9}, then both high-side carry hypotheses agree after processing site j, the overflow gamma agrees, and all mirrored normalized digits at i<j agree. If gamma=0, the next symmetric pairword's first j coefficients are therefore exact; if gamma=1 its first min(N,j+1) coefficients are exact (the inserted leading digit shifts the high-side partner). Induction makes this an exact, endpoint-only exterior cone for **any** intervening centre and any additional U repetitions. The checker rejects if the certified prefix falls below 160; it does **not** assume W9 remains intact at intermediate phases.

## Exhaustive decision
- Every length-3 junction: 19^3=6,859 words per U; 30 U rotations; **205,770** independent J/U assignments.
- Every length-4 junction: 19^4=130,321 words per U; 30 rotations; **3,909,630** assignments.
- Total **4,115,400**, enumerated without strict-W9 phasewise pruning. **Zero** retain the exact B6||W6^14 endpoint prefix at t=120. All 4,115,400 had the correct 120-step phase-6 overflow clock, no unresolved carry hypothesis; minimum certified endpoint prefix length **341** > required **160**. First mismatch absolute index ranged **133..156**. Since the initial certified prefix contains 100 U copies, the statement holds for *every k>=100*, independently of C and its parity.
- No U word/centre fixes W9; therefore no exact T(q,k)->T(q,k+5) fixed-J return exists in this stated subcell. The numerical q=14 result is **not** promoted to all q without independently checking T12 insertion hypotheses.

## Reproduction and independent physical checks
```bash
c++ -O3 -std=c++17 calculation/new_structures/AC15/cone_census.cpp -o /tmp/ac15-cone
for j in 3 4; do
  if [ "$j" = 3 ]; then stop=6859; else stop=130321; fi
  for u in $(seq 0 29); do /tmp/ac15-cone "$j" "$u" 0 "$stop"; done
done
```
Sum the JSON cases, Wok, cone_error, clockbad values; check each of 60 outputs. Exact search took 182 seconds with five concurrent workers, clang++ -O3 on x86-64. Independent direct decimal digit-array enumeration over all 205,770 J3 assignments with two fixed C parities and 25 J4 U ranks matched **70 per-U/parity histograms exactly** to the cone. Another independently written Python arbitrary-precision n+reverse(n) engine checked **80 random distinct cases ×120 steps** with palindromic centre lengths 1..20, and **30 five-width controls** at (q,k)=(14,100),(20,80),(40,160),(80,320),(160,640), including each intermediate genuine digit result and the overflow clock; no disagreement. These controls are audits, not proof of parameter-uniform q dependence.

No ALERT: a negative short-seam exclusion is not an all-time certificate.