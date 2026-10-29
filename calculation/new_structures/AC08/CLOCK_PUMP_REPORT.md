# AC08: centre-length-uniform physical overflow clock

**PAPER PROOF** of a mask-insertion pumping lemma plus **COMPUTED** 120-phase finite abstract-state verification. This is a theorem about a necessary component of T*, **NOT an all-time Lychrel certificate**, and does not give an identical-J/C endpoint return.

## Exact statement

Fix the canonical rooted phase-0 p12/m9 B34, W9^14, J=[5], k=100; choose **any of the 30** charge-zero U3 rotations of (9,a,18-a) for even a=0..18. Let C be **any finite palindromic coefficient centre**, with symbols 0..18 and even midpoint (if odd length), including empty C. Realize H++C++reverse(H) canonically as the ordinary decimal integer N0. Then for **all C lengths and all C values**, 120 genuine decimal reverse-and-add steps have exactly the overflow bitstream **(100010001000)^10 = (1000)^30**, i.e. exactly 30 true digit-growth events at t=0,4,8,...,116. No per-phase W9 preservation assumption is used.

The statement is pinned to q=14,k=100,rooted phase 0,J=[5]; it is uniform in centre length and coefficients and all 30 U words, **not** yet uniform in the two band exponents.

## Abstract semantics and soundness

Represent each possible decimal digit by a nonempty bitmask in {1,...,1023}. A concrete digit d has singleton mask 1<<d. Let ALL=1023 represent all digits 0..9. A possible input carry is bitmask 1 (carry 0), 2 (carry 1), or 3 (either). The abstract transfer at column i enumerates all x in mask[i], y in mask[n-1-i], c in carry and unions (x+y+c)%10 and floor((x+y+c)/10). This is a sound overapproximation even at the middle and with correlated source digits: ignoring correlations can only add possible outputs. If the terminal carry mask is singleton, its overflow decision is therefore exact for every represented concrete integer.

For the canonical pairword, all digit positions OUTSIDE C are determined by min(9,P_i) and max(0,P_i-9) in the usual two-ended canonical realization. Inside C, replace every position with ALL. Call this abstract input S_L for a centre of length L. It overapproximates **every** admissible C of that length.

## Midpoint insertion lemma (paper)

Define I(A) by inserting one ALL at the midpoint floor(len(A)/2). Suppose (i) n odd and A[mid]=ALL, or (ii) n even and A[mid-1]=A[mid]=ALL. Then a full abstract reverse-add step F has **the same terminal carry mask** on A and I(A), and the output is I(F(A)), with the insertion at the new midpoint after handling any forced growth digit.

Proof: before the midpoint the paired mirrored columns and their input carry masks agree; after the midpoint they agree with indices shifted by one. At the midpoint the only new pair is ALL with ALL, and **T(ALL,ALL,c)=(ALL,{0,1}) for every nonempty c**, so its output is ALL and its carry after the centre is identical to the saturated carry in the shorter word. The output at the original central column is ALL. When an overflow changes midpoint parity by one, moving insertion one position across that adjacent ALL changes no mask. This establishes the exact abstract relation for either parity. The central FULL condition is retained by inserting another ALL. No assumed spatial-radius bound is used.

## Finite certificate and induction

The executable proof checker CLOCK_PUMP.py (file clock_pump.py) evaluates the exact bitmask transfer for **121 states** (time 0 through 120) at base C length L=2, independently for each of the 30 U words. At every state it checks the midpoint-insertion premise. Every terminal carry is singleton, with gamma exactly (1000)^30. It also compares all 121 frames of L=3 with a centre insertion into the L=2 frame (independent implementation sanity check). By the lemma and induction on L-2, the same gamma holds for **every L>=2**, with no finite bound on L. L=0 and L=1 are separately checked by the exact abstract transfer for all 30 U words.

This is a parameter-uniform proof from a finite carry-mask certificate, rather than a finite sample of centre words. The finite checker itself has not been formally verified in Lean; label therefore **PAPER PROOF + COMPUTED**, not LEAN-VERIFIED.

## Independent arithmetic controls

210 physical Python-unbounded-integer runs (30 U x lengths C=0,1,2,7,14,50,301), each for 120 genuine decimal additions, independently confirmed the exact overflow clock. Also checked 23,000 random central-saturated mask words for midpoint-insertion commutation and terminal carry-mask equality. Those tests support the implementation; the universal-length claim relies on the paper insertion proof and base-state certificate.

## Remaining open obligation

The 120-step pairword must still restore the **same W9, J, C and two carry ports** with U exponent +5, guard all intermediate palindromes, and be pumped over all sufficiently large q,k. None of these follows from the overflow clock theorem. A correct clock does not repair the empirically eroding W9 frontier.