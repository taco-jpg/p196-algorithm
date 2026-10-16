# Agent111 digit-layer author's independent source review of the main theorem and position pools

Date:2026-10-15. Conclusion: **no blocking defect found in the pinned source versions below.**

Independent targets are other authors' `Saturation.lean` and `DigitPools.lean`, with relevant composition contracts in `ArithmeticCRT.lean`, `ModularSpan.lean`, `PairWeights.lean`, `OuterBlock.lean`, `ModulusSplit.lean`, `PeriodExistence.lean`, and `ResidueOrbit.lean` traced. This reviewer authored `PalindromeDigits.lean`, so **does not count that file as independently reviewed**; only its interface instantiation by position pools is checked. Ordinary reversal and exact-digit semantics come from existing `Lychrel196Research.lean`.

This is independent source/mathematical-semantic review. Author compilation records are not treated as an independent fresh full-chain build; another specialist performs the final empty-directory rebuild and axiom checks. No Lean source was changed.

## Pinned source SHA-256 hashes

| File | SHA-256 |
|---|---|
| `Saturation.lean` | `a638ff9844afa378dfe168feeaa8be372d2f2b5f6f3c1ff62ca5c2fe9f0685e0` |
| `DigitPools.lean` | `40981b1b8f2874c9ed179e113f5dae95776c0cfe9e1e49fa521fe4cee61aa7ec` |
| `ArithmeticCRT.lean` | `c5709b1de255e43d84a4d323257b13f9a314872d77cae955ac9c0c088ced59a5` |
| `ModularSpan.lean` | `1cad197771ad6a4a9577ac08d3e1a4afe143e354a96a261b8ebaa2c687c09754` |
| `PairWeights.lean` | `8b4d5b4b85a9c1957705ca13cc848483418593a7268818ba2f0e791b8d19c7ae` |
| `OuterBlock.lean` | `bccb6914ec1070c5d291881af8c806bb6735f9369b45b79029dc19662a163705` |
| `ModulusSplit.lean` | `b5d01b31bb37c24c60b8af544329f86341637af7d442ca29aaca7ac60a49bf7f` |
| `PeriodExistence.lean` | `e670385bb0e423fdb9db8f487bd53d5ab4bc4d745cad37f2de20f1f832f6e6dd` |
| `ResidueOrbit.lean` | `989e42134e6ae6c05775f569cc1b4cd916d0d45d5d87b6e471cbf3fe3e2cdfc6` |
| `PalindromeDigits.lean`, pinned interface dependency only, not independently reviewed here | `323bee6eee1e85ec6f8e75226e2f037ee8f5bf2cfa07b25d0ea7b7fd9211789f` |
| `proofs/research/Lychrel196Research.lean`, existing core semantic dependency | `f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c` |

## Quantifiers and coverage

`exists_saturation_bound` in `Saturation.lean` constructs B for every positive `M : Nat`. B comes from a decomposition k,u,q depending only on M and a positive period r modulo q. `SaturationAbove M B` then quantifies over **every** L≥B and **every** natural a; the threshold is not silently placed after L or a, and a<M is not required.

`exact_length_palindrome_residues` preserves the correct order `∃ B, ∀ L, B ≤ L → ∀ a, ... ↔ ...`. Its right side is exactly the units-digit restriction and even-length11 restriction. `decimal_modulus_decomposition_coprime` and `exists_positive_ten_period` are instantiated inside the main theorem, not left as external decomposition/period assumptions. M=0 is explicitly excluded; positive u,q in `saturation_of_split` also ensure M=u*q>0.

The explicit bound `2*k+4*q*r` applies to any interface-compatible k,u,q,r. Code claims neither minimal k, minimal positive period, nor minimal threshold; automatic decomposition may return a larger k than the sharpest paper choice. That is the correct scope, not an existence-theorem gap.

## Position-pool and exact-length instantiation

`alignIndex` in `DigitPools.lean` satisfies `k ≤ start < k+r` and `start % r = a % r`. Natural subtraction loses no required information: k%r<r makes a+r−k%r the intended nonnegative difference.

`positions` recursively constructs a finite list of exactly the specified length. `positions_endpoint` gives the strong last-position bound `i+r ≤ start+r*n`; together with start<k+r this yields strict i<k+q*r when n≤q. Alignment does not consume an extra period of space.

The first pool lies in `[k,k+q*r)`, the second in `[k+q*r,k+2*q*r)`. `selectedPositions_nodup` uses these intervals for cross-pool distinctness and r>0 for strict growth within each pool. Only the first pool's length bound is needed for cross-pool distinctness; the second bound is separately used by `selectedPositions_bounds`, so nothing is omitted.

L≥2*k+4*q*r gives k≤i and **strict** i<L−1−i for every selected position. This excludes central self-pairing and low/mirrored-position collisions and ensures mirrored indices are at least k. Even at i=k+2*q*r−1 and L=2*k+4*q*r, L−1−i=k+2*q*r>i.

`residue_pools_realize` supplies concrete `Nodup`/`LowerPositions` proofs to `two_pool_realization`, and `positions_length` identifies list lengths with x,y. The two equal-weight identities come from actual index residues and the mirror-period theorem, not assuming the target residue in digit construction. The interface returns core `DecimalDigits.Canonical P d L` and `Lychrel196.Palindrome P`. Canonical includes digit bounds, nonzero highest digit, and value d L=P; Palindrome is ordinary reverse10 P=P. No shadowed/replaced definition was found. The main theorem derives P>0 from the same hc.

## Boundary and adversarial checks

| Check | Result and reason |
|---|---|
| M=1 | Decomposition allows u=q=1; a positive period exists and all residues modulo1 are0. Compatibility is true and a positive actual palindrome is still returned. |
| q=1 | x<q,y<q in shifted_modular_span force x=y=0; pools are empty and the base outer frame suffices. No modular inverse or q>1 is required. |
| r=1 | Both index labels are0, but spatial intervals remain disjoint. The second pool uses i%r=1%r, not an incorrect equality to natural1. |
| a=0, 10∣M | Incompatible and rejected by necessity; no positive palindrome ending in0 is promised. |
| a=0, 10∤M | Compatible zero residues are included. If a%u=0, outer-block construction may take A=u; 10∤u ensures a nonzero units digit and the appropriate proper-divisor bound gives A<10^k. |
| u=1 | The outer block can have a nonzero units digit, preservation modulo1 is trivial, and CRT still holds. |
| u=10^k | Compatibility ensures the residue's units digit is nonzero, selecting the branch without adding u and avoiding an oversized outer block. |
| Even L | The triple gcd is gcd(q,11). Since q∣M, it divides gcd(M,11), hence a. The even symmetric outer frame is divisible by11 and meets the same gcd condition. |
| Odd L | The weight gcd is1; both span assumptions follow from 1∣_, with no extra11 restriction. |
| Higher powers of11 | The weight gcd equals11 exactly, not merely a multiple of11, so no erroneous requirement such as121∣a is introduced. |
| L−1 and L−2 exponents | k≥1 and the length bound give L≥2 before invocation; mirrored-period transport separately obtains i<L, so natural truncation does not alter the differences used. |

## Combining moduli and the necessary direction

`shifted_modular_span` uses b=a+q−C%q, not a−C which could truncate a negative difference. Since C%q<q, C%q+b=a+q exactly. The triple gcd divides a,q,C, hence C%q and chosen b. The resulting equality has direction `(C+x*c0+y*c1)%q=a%q`.

In the main theorem, hPu:P%u=A%u and hAu:A%u=a%u compose forward; hPq and the span equality do likewise. `crt_mod_eq` concludes P%(u*q)=a%(u*q), and rewriting M=u*q matches the goal. CRT uses integer differences and Bézout, without P≥a, so natural ordering creates no gap.

Necessity in `ResidueOrbit.lean` derives compatibility from actual Canonical, actual Palindrome, and p%M=a%M: positive palindromes have nonzero units digits and even-length palindromes are divisible by11. These facts transfer through the residue equality using factors dividing M. Neither direction of the final iff is reversed or weakened.

## Subsequent corollaries and review boundary

`every_orbit_matches_palindrome` says only that an actual orbit state and constructed palindrome have equal width/residue, not that the numbers are equal or the orbit hits a palindrome. `fixed_modulus_closed_set_contains_palindrome` takes the maximum of the constructed saturation threshold and the set's eventual threshold; positivity permits each application of forward closure on positive integers. Membership transfers from the orbit state to the same-width, same-residue palindrome, as claimed.

No Lean statement needing repair was found. This report supports composition and boundary handling for the hashes above, not independent review of the reviewer's own digit-semantics file or the final fresh build/full-dependency axiom audit.
