# W04: exponential one-step carry-gauge funnel into a two-dimensional decimal 20k rectangle

**PAPER PROOF** for all-length one-step pairword collision and its combination with the previously proved 20k rectangle; **COMPUTED** for exhaustive and independent whole-integer controls. **UNDECIDED** for any infinite decimal orbit. This result combines, rather than claims to rediscover, the `x+(b-1)z` carry-gauge from `AgentN28CarryGaugeFunnel` and the independent two-counter finite-horizon construction from the preceding `AgentW04IndependentCounterRectangle`. The new consequence is a **uniform 2^m-dimensional family of ordinary decimal seeds over every independent (m,n) in the 20k rectangle**, with **common literal step-2 integer**, not a single diagonal k or a mere arbitrary digit split of one fixed pairword.

## Explicit decimal seeds and image

Fix independently m,n>=1, and let z=(z_0,...,z_(m-1)) be ANY binary word. Define its least-significant-first folded pair-coefficient half

    H_z(m,n) = [10] ++ [8+9*z_0,...,8+9*z_(m-1)] ++ [5,11] ++ [16]^n ++ [8].

The full even palindromic pairword P_z is `H_z ++ reverse(H_z)`; all coefficients are 0..18 and its outer coefficient is 10. Physically realize it as a canonical positive decimal seed `N_z` by placing high-side digit `min(p,9)` and low-side digit `p-min(p,9)` at each reflected pair of positions. The most significant digit is 9, every `N_z` is a genuine 2(m+n+4)-digit integer, and the odd coefficients 5,11 prove every starting number nonpalindromic.

**Exact universal identity (PAPER PROOF).** Define `F(P)=pairs(normalize_10(P))`, with the pairword of the normalized decimal integer folded outside-to-centre. Then for all m,n>=1 and ALL binary masks z,

    fold(F(P_z)) = [1,9] ++ [16]^(m-1) ++ [13,7,9] ++ [14]^(n-1) ++ [15,16],

with final odd-length symmetric completion and **one leading overflow digit**. This is precisely the old N19 phase-1 word, now obtained without requiring the initial 8-run to be uniform. For two masks z,z', their distinct ordinary first successors have the same pairword, so applying ordinary reverse-and-add a second time gives **exactly the same integer**. The folded phase-1 word begins `[1,9]`, so none of these first successors is palindromic.

**Carry derivation.** The coefficient at source low index 0 is 10, so its outgoing carry is 1 and normalized low digit is 0. In the masked segment at low positions `i=j+1` (0<=j<m), the coefficient is `8+9z_j`; since the entering carry is 0 or 1, its outgoing carry is exactly `z_j`. Write `z_-1=1`. Its normalized low digit is `8+z_(j-1)-z_j`. On the reflected high masked segment, the outgoing carry is similarly determined by the reflected mask, and its normalized upper digit at the shifted overflow partner of low site `j+1` is `8+z_j-z_(j-1)` for j>=1. The two digits sum to **16**, independent of mask. At j=0 the upper partner is the old most-significant input coefficient 10 with incoming carry `z_0`; its normalized digit is `z_0`, while the low digit is `9-z_0`, giving the fixed output coefficient **9**. The extra leading digit 1 gives output outer coefficient 1. At the right mask boundary, the low normalized digit of coefficient 5 is `5+z_(m-1)`; its high shifted partner, the final mirrored masked coefficient, is `8-z_(m-1)`, giving output coefficient **13**. The unmasked `11,16^n,8` centre-and-tail transitions are ordinary fixed carry arithmetic: they produce `[7,9] ++ 14^(n-1) ++ [15,16]` with a single even central coefficient 16. The source's outermost coefficient 10 always produces overflow 1, since its entering upper carry is 0 or 1. This checks every column and every centre terminal, establishing the full identity. The algebra is an instance of N28's existing overflow carry-gauge cancellation, here with fixed non-gauge `10,5,11,16^n,8` boundaries.

The 2^m canonical seed integers are distinct because the low/high digit split directly records each bit z_i at the corresponding position. Their first successor integers are likewise distinct: the source symmetric pairwords have identical even width but distinct coefficients, and the fixed-width uniqueness theorem for symmetric pairword weighted values from `AgentW07ReverseFibre20k` applies. Equivalently, the first changed coefficient is a nonzero ±9 in a symmetric position, which cannot be cancelled by the remaining ±9 digits in the fixed-width palindromic weighted sum. Thus `t=2` is their **first common ordinary integer**, not merely a common pairword.

## 20,000-step rectangular consequence and proof

The maskless member z=0 has the exact initial pairword of our previous result `AgentW04IndependentCounterRectangle`, with **independent** run lengths m,n. For **every m,n>=15000** that result's 20,000 fully checked carry-transfer edges prove that its orbit has no palindrome through and including t=20000 (two disjoint independently pumpable scalar bulk runs, at least two odd pair coefficients in every reference state). The universal identity above proves for every mask z that the complete pairword at t=1 is identical to that of the maskless member. Therefore their complete integers at t=2 are identical, and all later ordinary integers are identical by deterministic reverse-and-add. Original t=0 and t=1 were separately shown nonpalindromic. Induction yields for **all masks** at every `(m,n)` in the rectangle:

    forall 0 <= t <= 20000, N_z(t) is not a palindrome.

This is **finite horizon** only. Mask information is destroyed at the first image and does not replenish either shrinking bulk counter. No new indefinite invariant, Lean theorem or statement about t>20000 is claimed. N28 previously proved a general gauge cancellation and various long-lived fibres, W07 proved exponential ordinary-digit-split fibres, and N19 proved a diagonal 20k family. The added nonredundant content here is a *mask family of distinct pairwords* (not digit splits) grafted onto the **off-diagonal independently pumpable** W04 rectangle with exact first ordinary-integer coalescence t=2.

## Independent controls and reproduction

`mask_funnel.py` independently normalizes complete symmetric coefficient words and independently computes ordinary Python arbitrary-size integer `N+reverse(N)` on **3,060 exhaustive small decimal seeds** (m=1..8, n=1..6, every 2^m mask) and **90 longer controls** (m up to 1000, assorted random masks); all confirm the exact phase-1 folded image, literal equality at t=2, distinct t=0/t=1 seeds and no palindrome in these steps. This program is not an induction proof; the column carry derivation above supplies the unbounded parameter soundness.

A separate C++17 oracle `mask_funnel_20k.cpp` uses only **ordinary decimal digit-vector reverse/add**, without the pairword updater as its transition kernel. It constructs four physical masked seeds for `(m,n)=(15000,16000)`: all-zero, all-one, alternating, and seeded pseudorandom (xorshift32 seed 47404). The four original integers are pairwise distinct and nonpalindromic. It verifies that all four *full* first-successor pairwords are identical (not necessarily their first-successor integers) and that all four **complete integer values at t=2** agree digit for digit. It then evolves the irregular-mask descendant from t=2 to t=20000, checking nonpalindromicity at every full state and full decimal fingerprint checkpoints:

| t | decimal digits | full-number FNV64 |
|---:|---:|---|
| 2 | 62,009 | `e55585a7067342b2` |
| 5,000 | 64,083 | `74c3a64cfc9ee20` |
| 10,000 | 66,171 | `e0b95978a86c23cd` |
| 15,000 | 68,210 | `4be963ab548b47d4` |
| 20,000 | 70,241 | `67dc3790ddabed81` |

The final checkpoint exactly matches the **independently GMP-checked off-diagonal seed** from W04's first commit `ef8721802c8dc2b86c39eb2d6269d552549371f3`, giving a cross-engine control with the same true full-number value. `mask_checkpoints.json` stores the expected small evidence. The runner verifies every checkpoint and deliberately rejects an altered expected final fingerprint.

Run at repository root:

    bash calculation/new_structures/agent-W04/run_mask_funnel.sh

Requires Python3 and C++17 g++, no external Python packages or Lean. The runner terminates `AGENT_W04_MASK_FUNNEL_ALL_CHECKS_PASSED`. This is a compact proof-plus-code result with no unverified infinite claim. Repository-wide `verify.py --changed` and Lean were not available in this environment, so neither is claimed.

## Search implication (constructive, not exclusion)

The central IC3/PDR learning target is **not** arbitrary hidden 8/17 mask bits: the first overflow destroys those bits completely. A quotient state should canonicalize their whole mask cylinder to the phase-1 fold, retain *only* the two independent bulk lengths and the actual shrinking exterior/centre interface, and search for a regenerating transition whose counter drift offsets the known six-step `(-5,-2)`. Keeping arbitrary masks as reachability-state bits would blow up the search without adding an infinite-lived degree of freedom.