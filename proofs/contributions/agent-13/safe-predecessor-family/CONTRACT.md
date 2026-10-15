# Agent #13 — exact safe-predecessor family

Source: `proofs/research/main_existence_attempt/continuation_pass/finite_seed/FINITE_SEED_OBSTRUCTIONS.md`, section 3, at `c2b6977e43a79caa5ff3bb88801f3ba896986f38`. Ownership: `agent13-safe-predecessor-family`, published on coordination at `c84a73a1888b51971be6a62354dfa9034a4cd81f` through a non-force expected-head update. Contribution branch: `formalize/agent-13/s20261015`.

## Exact mathematical contract

For every natural `m >= 2`, put `y_m = 10^(2*m) + 99*10^(m-1) - 1`. For every canonical decimal word `A` of width `m-1`, form `n_A = A || 99 || complement(reverse(A))`, retaining the full width of the complemented block. Prove the actual natural-number equality `Lychrel196.step n_A = y_m`. Prove `0 < n_A < 10^(2*m) < y_m`, `not Palindrome n_A`, `not Palindrome y_m`, and `not Palindrome (step y_m)`.

Prove that distinct words `A` give distinct natural inputs, and instantiate an injection from `Fin (9*10^(m-2))` into this family. This proves a lower bound on the complete safe fiber; it does not assert that the complete fiber has exactly that cardinality. The quoted exact cardinality belongs to this constructed family.

Implementation parameter `k=m-1` is positive. Digits are indexed least-significant first using existing `DecimalDigits.value`, `reflected`, `columnSum`, and `Canonical`. The two central input digits have indices `k,k+1`; all other reflected pairs sum to 9. The intended `Agent13SafeFamily` endpoints include `family_step`, `target_safe`, `family_safe`, `family_injective`, and `safe_predecessor_family`.

No abstract transition hypothesis will replace `step`. Leading-zero conventions, zero exclusion, width, input injectivity, and both source and target safety are obligations, not assumptions added to the source claim. Iteration continues after a palindrome in the existing definitions; this result only concerns two consecutive safe states.

## Dependencies and acceptance

Reuse unchanged `proofs/research/continuation/LychrelDigitSums.lean`, which imports only `Std`. Lean version: 4.19.0, compiler commit `6caaee842e94`. The full unchanged dependency compiled locally to a fresh `.olean`, exit 0; runtime reported 50.73 seconds. An earlier container-limited attempt terminated at 200 seconds without a completed object; its partial log is preserved separately and is not a theorem failure or a successful build. A smaller baseline `SignedDigitUniqueness.lean` also compiled, exit 0. Both sources match the pinned main snapshot byte for byte.

Every exported result requires exact statement review, actual compilation, `#print axioms`, and a separate empty-directory rebuild. Permitted foundational axioms are only `propext`, `Classical.choice`, and `Quot.sound`; results requiring none are recorded as such. No `native_decide`, compiler-trusted evaluation, new mathematical axioms, incomplete proofs, or external oracle conclusions are accepted. Self-review and a separate local rebuild are not independent-agent review.

## Remaining distinct claims

The real-valued positive nonincreasing-weight amplification, absence of a finite uniform multiplier, and square-root quantitative bound remain separate unformalized obligations. Completing this family does not close those stronger inventory entries. Section 4 fixed-target ancestry is owned by Agent #12 and is excluded here. No novelty, external peer review, default-branch integration, exhaustive corpus coverage, decimal Lychrel existence, or 196 proof is asserted.
