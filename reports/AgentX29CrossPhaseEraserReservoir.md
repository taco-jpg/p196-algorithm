# X29: phase-shifted p8 exterior + p3 erasers + central-18 reservoir

**COMPUTED**: all stated 20,000-step physical decimal replay checks. **PAPER PROOF**: conditional central-18 insertion lemma and local four-step packet erasure. Neither is an infinite base-10 Lychrel certificate. There is no conclusion about the literal 196 orbit.

## Three compositions and cross-wave map
The N/W DONE inventory and result titles separate rooted p8/m20 and p8/m48 fronts (N01/N02/N10/N16/W06), p12/m9 packets (N05/N21/W02), folded languages/affine counters (N04/N07-N09/N19), coalescent interfaces (N28/W06/W07/W13), and pair-18 or 9 reservoirs (N23/N27/W18/W27). Here an N28 *period-three* eraser is embedded in a W06 *period-twenty* exterior, then a central-18 pumping reservoir is added. This is different from the existing same-species p8 erasers.

(A) Phase-one p8 + p3 non-gauge eraser: positive, exact P4/N5 merger. (B) W06 0/9 buffer next to p3 in four placements: zero one-step P1 resets among exactly 720 settings (6 lengths, 10 even centres, 3 inner periods), a failed combination only, not a no-go theorem. (C) Seven independently selectable p3 erasers + central pair-18 pump: positive 128-to-one coalescence and full 20k finite-horizon pump. B redirects to C.

## Constructed actual decimal integers
Pairword coefficients are least-significant-first. B1 and W1 are the 39/20-entry arrays in construct.py. That separate script derives their values from one genuine decimal reverse-add step of the established B0/W0 p8 root, and independently checks the entire 20-cell periodic prefix. The phase-one root has four initial real overflow bits 0101, compatible with the N28 period-three eraser (the original root had 1010).

For Q>=6500 define H_Q=B1++W1^300++(5,5,2)^80++18^Q, then P_Q=H_Q++[18]++reverse(H_Q). Split every mirrored coefficient p into low digit floor(p/2) and high digit ceil(p/2), with middle digit 9. Thus P_Q is a genuine canonical decimal integer's pairword; its leading digit is nonzero. For Q=6500 the seed has exactly 25559 decimal digits. Replacing the local [5,2,5] by [7,7,7] at p3 repeat index 50, and at the reflected right-hand position, produces a different decimal integer. The seven switches at repeat indices [8,16,24,32,40,48,56] are separated by 24 coefficients and have disjoint four-step causal cones. All 128 masks (including the empty mask) have exactly equal complete pairwords after four steps and equal ordinary integers after five, as checked with native Python bigint. The first six states of each mask are nonpalindromic (768 state checks). The local eraser rule is the established N28 four-step 0101 carry truth table, now occurring in the independently phased p8 exterior.

## Two independent 20,000-step computations
The standalone grade-school digit-vector program triple.cpp replays Q=6500 baseline, one packet mutation, and Q=6501 baseline simultaneously, asserting nonpalindrome at every t=0..20000. At every one of those 20001 states, it also checks whole-word central two-18 pairword insertion for Q+1, full pairword equality of the eraser variants for t>=4, identical decimal integers for t>=5, exact overflow bit gamma_t=t mod 2, and agreement with independently generated eight-phase p8 root rows up to their first mismatch. Initial length 25559, final length 35559; 10000 length overflows; minimum centered run of coefficient 18 is 1637; minimum rooted p8 phase-prefix match is 1496. Final FNV64 over big-endian decimal digit characters is 4a5b548aae4d2f9f.

Define trajectory fold F from 1469598103934665603 by F_next=(F xor FNV64(N_t))*1099511628211 modulo 2^64 for t=0..20000 inclusive. Result: 0542b847044b048d. The *separate* independent_gmp.cpp uses arbitrary precision GNU GMP integer addition and canonical decimal-string reversal at all 20000 steps, checks palindromes at all states and reproduces exactly this full-trajectory digest and final FNV64. Construct.py generates the same canonical decimal seed independently and checks the phase-one B1/W1 derivation; SHA256 digests for base, packet and plus seeds are in expected.json.

Lemma.py exhaustively tests all positive-leading flank words of lengths 1,2,3 for centred-18 runs of length 5,6,7 (20574 cases), and another 20000 random larger flanks. All pass the claimed pairword insertion identity.

## Conditional insertion lemma and scope
**PAPER PROOF:** Let a canonical decimal integer have palindromic pairword P with at least five centred 18 coefficients. Insert two more 18 coefficients at the middle, yielding P'. Realize that insertion by two ordinary digit-9 insertions at the middle of the integer; the resulting word remains canonical and has pairword P'. In normalizing P to compute the next reverse-add integer, the first 18 coefficient outputs 8 or 9, the carry becomes 1, and all subsequent 18 coefficients output 9 with carry 1. Hence adding two 18s in the interior of this band inserts two ordinary 9s, without changing any exterior digit or the final overflow. Reflective pairing shows that the successor pairword is exactly the successor of P with two more central 18s. Symmetrically adding two middle 9s preserves palindrome status or its negation, since the centre already consists of 9s. This is a finite, exact, length-independent one-edge fact.

The true Q=6500 orbit retains at least 1637 central 18 coefficients at every t<=20000. Induction using the insertion lemma therefore transfers its exact 20,001-state nonpalindrome conclusion to *every Q>=6500*, and similarly to each of the seven-switch variants, all of which coalesce at t=5 while remaining nonpalindromic earlier. This is a finite-horizon all-Q statement only. The centre 18 reservoir and rooted p8 prefix both shrink on this tested trajectory, and no perpetual renewal is proved.

## Reproduce
All commands from repository root:

1. g++ -O3 -std=c++17 calculation/new_structures/agent-X29/triple.cpp -o /tmp/x29_triple
2. /tmp/x29_triple 300 6500 20000 80
3. g++ -O3 -std=c++17 calculation/new_structures/agent-X29/independent_gmp.cpp -lgmpxx -lgmp -o /tmp/x29_gmp
4. python3 calculation/new_structures/agent-X29/construct.py --out /tmp/x29_seeds
5. /tmp/x29_gmp /tmp/x29_seeds/base.seed 20000 0542b847044b048d
6. python3 calculation/new_structures/agent-X29/packets.py
7. python3 calculation/new_structures/agent-X29/lemma.py
8. python3 calculation/new_structures/agent-X29/reset_search.py

Local git clone cannot resolve github.com and Lean is absent, so the full repository tools/verify.py --changed was unavailable. This atomic result adds only non-Lean code/data/note/report, and the standalone computations above were completed. It is not presented as whole-repository verification.
