# AC01: exact endpoint-only centre census (rooted decimal p12/m9)

**Status: UNDECIDED.** No decimal Lychrel certificate or 120/240-step regenerative centre was found. No negative statement is made for untested candidates. This note corrects AB01's census cardinality and provides a sound endpoint-only window evaluation with automatic full-replay fallback; it is not an all-time no-go theorem.

## Predicate
Use the canonical phase-0 B34/W9 from `lat_p12m9.txt`, J=[5], q=14, k=100 and U in { (9,0,18), (0,18,9), (18,9,0) }. A centre C is a coefficient palindrome over {0,...,18}; at odd length its middle entry is even (physical realizability). Realize P=H+C+rev(H) as canonical decimal source, where H=B+W^q+J+U^k; take 120 **ordinary** reverse-and-add steps. The *necessary centre-only predicate* is agreement with H'=B+W^q+J+U^(k+5) on every pair coefficient in a radius `122+|C|+30` from the centre, including length/overflow consistency and carry ports. Exact full template return additionally requires W9 and J and all intermediate non-palindrome guards and is **not** claimed.

## Algorithm and soundness
`census.cpp` performs unpruned full ordinary-decimal digit-array replay. `window.cpp` accelerates centre-only checking by choosing a reference C=0 centre, then updating only the central radius-80 pair coefficients. At every step it uses the reference carry entering the window, checks the outgoing carry against the reference, computes guard coefficients beyond the next window and checks them against reference, and if **any** condition fails runs the unpruned full replay instead. By induction, outside-window pair coefficients and their carry inputs are identical to reference at every accepted fast step. The recurrence `d'_i=(p_i+c_i) mod 10`, `c_(i+1)=floor((p_i+c_i)/10)` and (for overflow g) `p'_i=d'_i+d'_(N-1-i+g)` is ordinary reverse-and-add, so fast and fallback paths compute the same necessary centre predicate. No *strict-phase W9* condition is used: endpoint healing remains allowed.

## Count correction
For centre length n, valid palindromic coefficient-centres number `19^(floor(n/2)) * (10 if n odd else 1)`. For n=7..14 the eight counts per U are 68,590; 130,321; 1,303,210; 2,476,099; 24,760,990; 47,045,881; 470,458,810; 893,871,739. Sum **1,440,115,640 per U** and **4,320,346,920 across three U**. AB01's reported denominator 66,660,000 is not the true full census size; its PARTIAL result remains a PARTIAL result.

## Completed and partial runs
- Full length-7 cell: all `3*68,590=205,770` C/U tuples, zero centre returns, zero fallback escapes. (Already within AB01's reported length-7..10 scope; this is an independent recheck, not a new exclusion.)
- For each U and each n=11,12,13,14: 5,000 distinct cyclic-stride indices starting at 15,313 with stride 123,457 modulo the per-U centre count. Total **60,000/4,308,412,260**, zero centre returns, zero fallback escapes; **PARTIAL**. This is a sampled test and cannot be promoted to exhaustive.
- 90 independent Python arbitrary-integer vs schoolbook digit-array controls (three U, six centre lengths 7/8/11/12/13/14, five widths (14,100),(20,80),(40,160),(80,320),(160,640)), all agree at every one of 120 steps; all had 30 overflows and no centre return. Additional 100 C11 candidates cross-checked between the local window and unpruned C++ engine.

## Reproduce
`g++ -std=c++20 -O3 -o census calculation/new_structures/AC01/census.cpp`
`g++ -std=c++20 -O3 -o window calculation/new_structures/AC01/window.cpp`
`./window 0 7 0 68590` (repeat for U=1,2)
`./window 0 11 15313 5000 14 100 123457` (repeat U=0,1,2; n=11..14)
`python3 calculation/new_structures/AC01/verify_independent.py`

**Remaining missing all-time lemma:** an exact physical T* epoch return with replenishing U-band and a non-palindrome guard for all q,k, including a returning junction, not just centre-side feasibility.
