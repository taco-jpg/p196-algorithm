# X30: exact all-length two-step anti-mirror dipole erasure

**PAPER PROOF (arbitrary Q and mask); COMPUTED controls.** This result is a new local two-step preimage mechanism around the W10 period-four decimal crystal, not an infinite-time proof.

## Construction and theorem

Let Q>=2, M=floor(Q/2). Digits here are written most-significant first. Define X0=("5346")^Q. For ANY subset A of {0,...,M-1}, obtain Y0(A) by replacing each chosen block a with U="2497" and its reflected block b=Q-1-a with V="4739". Every pair of positions is disjoint because a<b. There are exactly 2^M distinct canonical decimal numbers Y0(A).

**Theorem (exact, for every Q>=2, every A):**
(1) Y0(A) and R(Y0(A)) are not palindromes.
(2) R^2(Y0(A))=R^2(X0).
(3) If A is nonempty, R(Y0(A)) != R(X0). Here R(n)=n+rev(n), with ordinary decimal integer reversal. Consequently all 2^M seeds have the same subsequent orbit from time 2. This is an algebraic exact identity, not a bounded numerical extrapolation.

## Proof by signed decimal digit differences

The unmodified one-step word is exactly

    X1 = "1" ++ ("1782")^(Q-1) ++ "1781"        [length 4Q+1].

Let a be chosen and b=Q-1-a. In base-10 value, replacing the two original 4-digit blocks contributes to Y0-X0:

    (2497-5346)*10^(4b) + (4739-5346)*10^(4a)
     = -2849*10^(4b) -607*10^(4a).

After reversal of the original 4Q-digit input, U reverses to 7942, V to 9374, and the baseline block 5346 reverses to 6435. Thus

    rev(Y0)-rev(X0) = +2939*10^(4b) +1507*10^(4a),

and therefore the ONE-step integer difference is

    Y1-X1 = 90*10^(4b) +900*10^(4a).

Sum this formula independently over all chosen a. This change is realized in the base-10 digits of X1 by four legal digit edits for each a: at zero-based MSB positions p=4a+2,p+1, replace baseline (7,8) by (8,7); at r=4b+1,r+1, replace baseline (1,7) by (2,6). No other digit changes. Indeed each two-site edit contributes 9 times the corresponding base-10 power, and the baseline digits remain between 0 and 9; all altered sites are disjoint for all a<M. The resulting legal decimal digit word has exactly the integer value Y1, and hence is its unique canonical decimal expansion.

With n=4Q+1, reflection interchanges p with r+1 and p+1 with r. The signed digit changes are (+1,-1) at p,p+1 and (+1,-1) at r,r+1, so the signed changes at reflected positions sum to zero. Consequently

    Y1 + rev(Y1) = X1 + rev(X1),

which is R^2(Y0)=R^2(X0). Every nonempty A gives a nonzero one-step difference (positive sum above), so merger is genuinely delayed until step 2. Y0 has unequal outermost digits: (5,6) if a=0 is not chosen and (2,9) otherwise. Y1 has unchanged second and second-last digits (1,8), so both are nonpalindromes. QED.

## Finite positive decimal descendants (not infinity)

W10 independently verified the unmodified X0=("5346")^8000 to be palindrome-free through t=20000 (see results/AgentW10CyclicCarryMoat20k.md). The theorem transfers that finite fact to EVERY Y0(A) for Q=8000, plus the first two nonpalindrome states. This gives 2^4000 individually specified seeds with 20,001 palindrome-free states. It does NOT give nonpalindromicity beyond t=20000, because the reference lacks an infinite certificate.

Independently replayed a deterministic xorshift32 subset of 4000 independent pair positions with ordinary decimal schoolbook addition AND arbitrary-precision base-10^9 limbs, comparing EVERY complete number and checking every palindrome. Entire states t>=2 were additionally compared to the original uniform crystal, not just lengths or hashes. Q=8000: 32,000 digits to 40,323 after 20,000 steps, 8,323 overflows, final FNV64 of MSB-first ASCII decimal digits 33f8ce7f29c9f033. Exact data: calculation/new_structures/agent-X30/dipole_checkpoints.csv. Exhaustively checked all 24,572 subsets with Q=2..26 (Python independent decimal algorithm), with zero failures.

## Reproduction and boundary

Compile calculation/new_structures/agent-X30/two_step_dipoles.cpp using g++ -O3 -std=c++17 and run with args "8000 2 20000"; its two arithmetic engines compare all 20,001 states. Run python3 calculation/new_structures/agent-X30/allmask_exhaustive.py for all masks Q=2..26. The PAPER PROOF is arithmetic and works for all Q>=2; no Lean theorem and no infinite decimal certificate are asserted. Unlike one-step gauge fibres and p8/m20 kink erasers, this is a two-step fibre of a four-digit ordinary decimal crystal.
