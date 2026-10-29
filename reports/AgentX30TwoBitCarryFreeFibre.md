# X30: the two independent carry-free anti-mirror switches

**PAPER PROOF** for every length and independently selected symbol. **COMPUTED** exhaustive four-digit alphabet and full-state 20,000-step checks. This is an exact two-step reverse-and-add preimage structure, not a certificate of infinite nonpalindromicity.

## Symbol definition and all-Q theorem

Let Q>=2, M=floor(Q/2), X0=("5346")^Q, and R(n)=n+rev(n) in ordinary base-ten arithmetic. For every a=0,...,M-1, put b=Q-1-a and independently choose a four-digit pair (U,V) and two bits x,y satisfying:

    1000<=U<=9999, 0<=V<=9999, x,y in {0,1};
    U + rev4(V) = 11781 + 90*x + 900*y;
    V + rev4(U) = 11781 + 900*x + 90*y;
    floor(U/1000) != (V mod 10).

Here rev4 reverses four digits, padding with zeros, and V is written with four digits. Replace the original "5346" blocks at a and b by U and V. If Q is odd the middle "5346" is retained.

**Theorem:** EVERY resulting Y0 is a canonical nonpalindrome, R(Y0) is a nonpalindrome, and R(R(Y0))=R(R(X0)). All 7744^M seeds are different because each chosen pair changes disjoint block positions. At least one switch x=1 or y=1 forces Y1 != X1; if all bits are zero Y1=X1. At Q=8000 this is an enormous exact two-step fibre, but the orbit from t=2 is the already known finite W10 orbit, not a proven infinite Lychrel orbit.

## Proof: two independent signed anti-mirror swaps

For Q>=2, the reference has the exact length 4Q+1 digit word X1="1" ++ "1782"^(Q-1) ++ "1781". Relative to two original 4-digit blocks at positions a<b, the chosen pair changes Y1-X1 by

    (U+rev4(V)-11781)*10^(4b)
      + (V+rev4(U)-11781)*10^(4a)
    = (90*x+900*y)*10^(4b)+(900*x+90*y)*10^(4a).

The x switch makes the MSB-first digit changes in X1 at p=4a+2,p+1 (7,8)->(8,7) and at r=4b+1,r+1 (1,7)->(2,6), as in the preceding single-switch theorem. The y switch independently makes changes at p'=4a+1,p'+1 (1,7)->(2,6) and r'=4b+2,r'+1 (7,8)->(8,7). Within a single pair, x,y may both be one: the changes overlap at one digit but algebraically sum to legal digits: high block "1782" becomes "2772", and low block "1781" becomes "2771" when a=0 (or interior "1782" becomes "2772" for a>0). No carries or borrows occur. All distinct mirror pairs occupy disjoint four-digit blocks and the leading "1" remains fixed.

The signed digit edits are anti-mirror around the whole length-(4Q+1) integer: for each position i the increment is the opposite of the increment at n-1-i. Thus for the canonical digit words, Y1+rev(Y1)=X1+rev(X1) exactly. The t0 most/least significant digits differ by the last displayed inequality. At t1 the second and second-last digits also differ: the complete four-bit alphabet has these digits respectively 1 or 2 and 8 or 7, so no generated state at t=0 or 1 is palindromic. This proves the all-Q claim without a finite-length bound.

## Alphabet count and exact scope

The two bits provide four classes with computed counts:

    x,y     choices   local coefficients (A,B)
    0,0       4096    0,0
    1,0       1536    90,900
    0,1       1536    900,90
    1,1        576    990,990

Total 7744 = (64+24)^2. For each of the four coefficient classes, enumerating U=1000..9999 uniquely determines rev4(V) and hence V; testing the second equality plus the leading/trailing inequality yields the exact counts. The enumeration is *complete for these stated two-switch, carry-free coefficient classes*. It does not purport to enumerate every possible ordinary base-ten two-step preimage.

Python two_bit_counts.py checks all 7744 symbols against exact Q=2 schoolbook arithmetic, including the first two nonpalindromes and equality at step 2. C++ two_bit_dipoles.cpp independently replays a seeded choice at all 4000 mirrored positions for Q=8000 with two genuinely different arithmetic engines: normal decimal schoolbook and base-10^9 limb addition. It compares the COMPLETE integer at every one of 20001 steps, independently checks nonpalindromicity, and checks every state t>=2 equals the evolving uniform reference. Initial/final lengths 32000/40323, overflow 8323, initial FNV64 cfa92931c7ee87e3, final FNV64 33f8ce7f29c9f033.

## Limitation

This expands the previously published 5632-symbol alphabet by 2112 additional choices and splits a local delayed-erasure event into TWO independent switches. The fact that 7744^4000 seed choices merge by t=2 does not imply that the common orbit remains nonpalindromic for unbounded t. The proved part is the parameter-uniform finite two-step identity. No decimal infinite certificate, no Lean theorem and no result about 196 are asserted.
