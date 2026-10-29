# N28 carry-gauge quotient and exact two-step orbit coalescence

**PAPER PROOF** for the base-independent identity below. **COMPUTED** for the listed independent controls and 20,000-step decimal test. This does not prove a decimal Lychrel number.

## Universal symmetric carry-gauge statement

Fix radix b >= 3, length n >= 2, and symmetric words x[0..n-1] and z[0..n-1] (least significant first), where 1 <= x_i <= b-2 and z_i in {0,1}. Define symmetric pair coefficients P_i = x_i + (b-1) z_i. (For realizable seeds of odd length, central P must be even; all test seeds here have even n.) Let F(P) = pairs(normalize_b(P)), where normalize carries from right to left in the integer (low coefficients to high). Then:

**Overflow / gauge-erasure branch, z_0=1:**
- F(P) has length n+1,
- F(P)_0=F(P)_n=x_0,
- F(P)_i=x_{i-1}+x_i, for 1 <= i <= n-1.
- This result is completely independent of the n mask bits z_i, including how many domain boundaries exist.

**Non-overflow / discrete-Laplacian branch, z_0=0:**
- F(P) has length n,
- F(P)_i=2x_i+z_{i-1}+z_{i+1}-2z_i, for 0 <= i < n, with z_{-1}=z_n=0.
Thus the non-overflow mode carries mask information only through its discrete second difference, whereas overflow completely annihilates it.

## Elementary proof (sound for every b and length)

Let c_i be the carry entering position i and c_0=0. For any 1<=x_i<=b-2 and z_i in {0,1}, the coefficient P_i+c_i has quotient exactly z_i upon division by b, independent of c_i in {0,1}: if z_i=0 then x_i+c_i<=b-1; if z_i=1 then x_i+(b-1)+c_i>=b and <=2b-1. Thus c_{i+1}=z_i and the normalized digit at i is d_i=x_i+z_{i-1}-z_i, setting z_{-1}=0. The final carry is c_n=z_{n-1}=z_0. If z_0=1, append d_n=1. Reflection gives x_{n-i}=x_{i-1}, z_{n-i}=z_{i-1}, and z_{n-i-1}=z_i. Pair d_i with d_{n-i} for 1<=i<n: the mask differences cancel exactly, giving x_i+x_{i-1}. The end pair is (x_0-1)+1=x_0. If z_0=0 there is no additional high digit; pairing d_i with d_{n-1-i} gives 2x_i+z_{i-1}+z_{i+1}-2z_i (the outside z values are zero). This proves both cases.

This is a **local quotient transducer** suitable for a new certificate format: the non-neutral digit residue x is its observable state, and z is a carry gauge. At any overflow transition, all internal gauge bits can be forgotten without losing a single subsequent pairword. Interleaving non-overflow stages can regenerate mask gradients, but no closed decimal renewal cycle is claimed.

## Entire two-step funnel and its concrete decimal example

For constant x_i=x, the overflow image is [x] ++ [2x]^(n-1) ++ [x]. Therefore **every** decimal seed realizing such a pairword, independent of symmetric mask z with z_0=1, reaches after TWO ordinary reverse-and-add steps exactly

    x*(b+1)*(b^n-1)/(b-1).

In base 10 and x=8, this is 88 times the length-n repunit. For even n, there are 2^(n/2-1) distinct palindromic binary masks z with z_0=1. Choosing a deterministic nonzero-leading digit split gives the same number of distinct starting integers, all coalescing at step 2. The n=4 controls are:
- 9448 -> 17897 -> 97768
- 9988 -> 18887 -> 97768

Both seeds underwent 20,000 independent ordinary-digit reverse-and-add steps (using the already committed replay_int.cpp) without a palindrome. At step 20,000 the results agree bit-for-bit in a decimal digit-list representation, length 8283 and FNV-1a 64-bit digest 9656804610410818816. These are **finite observations**, not an infinite certificate. In particular the x=5,6,7 repunit-multiple controls turn palindromic very early, whereas x=8 deserves deeper constructive investigation.

## Reproducibility

From repo root:
- python3 calculation/new_structures/agent-N28/mask_gauge.py
- printf '9448\n' > /tmp/n28_a.seed
- printf '9988\n' > /tmp/n28_b.seed
- g++ -O3 -std=c++17 calculation/new_structures/agent-N28/replay_int.cpp -o /tmp/n28_digit_oracle
- /tmp/n28_digit_oracle /tmp/n28_a.seed 20000
- /tmp/n28_digit_oracle /tmp/n28_b.seed 20000

The Python program enumerates small cases and samples larger independent symmetric residue and mask profiles in bases 3..77, comparing direct radix digit-vector reverse-and-add, coefficient normalization, exact symbolic formulas and independent Python bignum arithmetic: 25,458 cases passed. It also tests both gamma=0 and gamma=1 and large high-entropy decimal masks. Control outputs are saved in mask_gauge_observations.json. No external libraries.

## Next task: an actual renewal cycle

A gamma=1 transition takes the quotient of an arbitrary masked block to an adjacent-sum word. Study the composition with the mandatory gamma=0 transition (the next low coefficient is x_0 <= b-2) and solve a **two-step renewal fixed-point / finite substitution** condition with a nonzero growing domain. A repeated overflow reset alone consumes stored mask information and is not itself a nonpalindrome-forever proof.
