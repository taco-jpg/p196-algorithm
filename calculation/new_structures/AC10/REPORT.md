# AC10 center-only T* fixed-point census (COMPUTED)

**Status: COMPUTED for |C|=7..10; PARTIAL for |C|=11..14. No decimal Lychrel certificate.**

## Exact predicate
Pairword P=H ++ C ++ reverse(H), H=B0 ++ W0^14 ++ [5] ++ U^100,
B0=(10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5),
W0=(5,18,4,8,1,15,4,0,5);
U=(9,18,0),(18,0,9),(0,9,18).
C is any palindrome with entries 0..18 and even midpoint when odd. The necessary center-return predicate compares the full interval of radius 122+|C|+30 about the center of the true 120-step pairword against P' with U^105 and *identical* C. The 120-bit clock must have 30 overflows, with both reflected sides driven by genuine decimal carries. This is endpoint-only; intermediate W9 damage is allowed. q=14,k=100,J=[5] are fixed.

## Exhaustive results
For each of the three U words: |C|=7: 68,590/68,590; 8: 130,321/130,321; 9: 1,303,210/1,303,210; 10: 2,476,099/2,476,099. **All 11,934,660 tests failed** center-return; zero clock divergences, zero survivors. A word of length L has 19^floor(L/2) times 10 (if L odd) or 1 (if even) possibilities. No pruning by mod-11 or strict-W9 intermediates; full lexicographic enumeration, split into disjoint 300,000-index chunks for lengths 9 and 10.

For each U, length 11: 50,000/24,760,990, length 12: 50,000/47,045,881, length 13: 50,000/470,458,810, length 14: 50,000/893,871,739; exactly the first and last 25,000 indices per cell. **PARTIAL, not exhausted**, zero observed returns. Total additionally sampled: 600,000.

## Exactness mechanism and verification
C++ stores a reference pairword trajectory (zero C). For each candidate it maintains changed coefficients and propagates a decimal carry until the carry equals the reference after the last changed coefficient. Digits beyond that point agree, and the next pairword difference is exactly the symmetric sum of the changed output digits. This elementary induction is an exact sparse-difference recurrence provided the overflow clock agrees; overflow divergence is flagged, never silently discarded. The center window is checked only at t=120, hence temporary mismatches are allowed.

The compiled implementation's in-run audit checks every coefficient after every time step against an independently executed dense pairword engine (150 diverse sample cases passed). A *separate* CPython arbitrary-precision n+reverse(n) verifier checked every phase for 120 controls spanning all U, all lengths 7..14 and (q,k)=(14,100),(20,80),(40,160),(80,320),(160,640); one common 120-bit clock, 30 overflows; all central windows failed. The original sparse code had an off-by-one baseline index, caught by this audit and corrected **before** the complete enumerations.

## Reproduction / scope
g++ -O3 -std=c++20 centre_sparse.cpp -o centre_sparse
For each u=0,1,2 and L=7,8,9,10 partition 0..count(L)-1 into successive chunks of <=300000; run "./centre_sparse u L chunk_size offset". Run "python3 verify_physical.py". Optional sixth argument "audit" after a dummy fifth argument cross-checks dense arithmetic on each candidate.

This is a finite missing-center-gate exclusion **within the specified T* ansatz**, not an all-time argument, not an exclusion of wider C, altered J or moving/growing seams, and not a proof of decimal Lychrel existence. Use T12's center-cut separation theorem only where its hypotheses are met; the scan alone does not establish independence from arbitrary junctions.
