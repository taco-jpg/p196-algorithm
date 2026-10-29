# X30: a 5,632-letter two-step decimal preimage fibre

**PAPER PROOF** (all lengths and all independent symbol choices) with a **COMPUTED** complete four-digit alphabet and independent big-integer controls. This generalizes the preceding two-letter anti-mirror dipole construction to a genuinely independent alphabet on each mirrored pair.

## Finite, explicit template family

Write blocks most-significant first. Let Q>=2 and X0=("5346")^Q. Let M=floor(Q/2). For each index a with 0<=a<M, write b=Q-1-a, and independently choose a symbol (U,V,k) satisfying

    k in {0,1}; 1000<=U<=9999; 0<=V<=9999;
    U + rev4(V) = 11781 + 90*k;
    V + rev4(U) = 11781 + 900*k;
    floor(U/1000) != V mod 10.

Here rev4 reverses four digits, preserving zeros; replacing a four-digit block by V uses zero padding. Replace the original block at a with U and at b with V. All block pairs are disjoint. If Q is odd, its middle block remains 5346.

An independent exhaustive 9,000-U enumeration with exact decimal Q=2 replay yields exactly 4096 symbols of colour k=0 and 1536 of k=1. There are exactly 5632^M distinct canonical Q-block initial numbers; no leading zero is introduced because U>=1000, and different choices change different block pairs.

## All-Q two-step coalescence theorem (PAPER PROOF)

Write R(n)=n+rev(n) using actual decimal integer reversal (not padded reversal). The reference one-step integer, for Q>=2, has exactly the digit expansion

    X1 = "1" ++ ("1782")^(Q-1) ++ "1781"    (length 4Q+1).

At a chosen pair a<b, note that a 4-digit block initially 5346 has local reversed block 6435. Relative to the original input, the full first reverse-add contribution is

    (U-5346+rev4(V)-6435)*10^(4b)
      + (V-5346+rev4(U)-6435)*10^(4a)
    = k*(90*10^(4b)+900*10^(4a)).

This expression sums over a independently, because reversing an input of fixed length 4Q permutes block positions and reverse4 is applied to each block exactly. The baseline X1 has legal decimal digits. At each chosen a with k=1, its digit changes are only
    MSB positions p=4a+2 and p+1: (7,8) -> (8,7);
    MSB positions r=4b+1 and r+1: (1,7) -> (2,6).
k=0 makes no first-step change. All sites are disjoint and none creates a carry or borrow: therefore this digit-edited word is the unique canonical expansion of Y1. With n=4Q+1, reflection interchanges p with r+1 and p+1 with r. Its signed edits (+1,-1) at each site add to zero at mirror positions. Thus Y1+rev(Y1)=X1+rev(X1), and Y2=X2 for ANY mixed choice of 5632 symbols at all M sites. If no k=1, Y1=X1; if any k=1, Y1 != X1 since all integer differences are positive. No information about t>2 is necessary for the exact identity.

Y0 is not a palindrome: its first and last digits differ by the last condition when a=0, and the untouched pair (5,6) differs if a=0 is left at its reference value. Under the specified construction every a is replaced, so the displayed condition is sufficient. Y1 also is not a palindrome, because the second and second-last digits of the baseline X1 are (1,8), and the four-digit edits never touch them. For t>=2 the integer equals the reference orbit, so every known finite nonpalindrome stage transfers.

## Controls and scope

Python multicolour_counts.py exhausts all 5632 admissible pairs and independently checks both Q=2 palindrome witnesses and Y2=X2 by full schoolbook decimal addition. C++ multicolour_dipoles.cpp uses a deterministic xorshift32 choice over all Q=8000 mirrored block positions, compares every full resultant integer from ordinary decimal schoolbook RAA with independent base-10^9 limb addition for each t=0..20000, checks no palindrome, and checks all t>=2 equal the evolving uniform reference. It prints 1000-step FNV64 MSB-decimal checkpoints in multicolour_checkpoints.csv. At Q=8000, initial length 32000; final length 40323; overflows 8323; final FNV64 33f8ce7f29c9f033.

The uniform Q=8000 reference's palindrome-free orbit is a preexisting 20,000-step COMPUTED result, not an infinite proof (results/AgentW10CyclicCarryMoat20k.md). This paper proof creates 5632^4000 initial seeds inheriting that **FINITE** trajectory, and does not close a template cycle, exhibit a self-renewing centre, prove an infinite decimal Lychrel orbit, or claim Lean verification.
