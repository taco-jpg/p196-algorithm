# Rational growth envelopes for the Fibonacci fiber recurrence

**Status: mathematical derivation only; not a Lean proof.** This note narrows the Std-only follow-up to explicit natural-number inequalities. It does not claim the conventional real limit.

Let F₀=0, F₁=1, and Fₙ₊₂=Fₙ₊₁+Fₙ. For positive naturals p,q, compare the rational rate p/q to the algebraic threshold x²=x+1 using the integer sign of p²−pq−q².

## Upper envelope

Claim to formalize: if 1 ≤ q ≤ p and p² ≥ pq+q², then for every n ≥ 0, qⁿ Fₙ ≤ pⁿ.

The base cases are n=0, where the left side is zero, and n=1, where q ≤ p. For the induction step, multiply the Fibonacci recurrence by qⁿ⁺²:

qⁿ⁺² Fₙ₊₂ = q(qⁿ⁺¹Fₙ₊₁) + q²(qⁿFₙ).

Applying the two induction hypotheses bounds this by q pⁿ⁺¹ + q²pⁿ = pⁿ(pq+q²) ≤ pⁿ⁺².

This is an exact all-index integer inequality. It uses no floating point, square roots, or compiler-trusted evaluation.

## Lower envelope

Claim to formalize: if p,q ≥ 1 and p² ≤ pq+q², then for every n ≥ 1, p² qⁿ Fₙ ≥ pⁿ.

For n=1, this reduces to p²q ≥ p; for n=2, it reduces to p²q² ≥ p². Both follow from p,q ≥ 1. The same recurrence identity and induction hypotheses yield

p²qⁿ⁺²Fₙ₊₂ ≥ q pⁿ⁺¹ + q²pⁿ = pⁿ(pq+q²) ≥ pⁿ⁺².

The factor p² is a fixed multiplicative constant, not an index-dependent one. This lower envelope is therefore a meaningful discrete comparison for rates below the algebraic threshold, though it is not itself a proof of a real n-th-root limit.

## What remains to make this an accepted theorem

1. Encode these exact statements using the repository's existing Fibonacci definition, without duplicating the definition under a new name.
2. Prove both induction lemmas in the pinned Lean 4.19.0 environment with the existing Std-only dependency contract.
3. Audit the new declarations and dependencies.
4. If claiming the conventional limit Fₙ^(1/n) → (1+√5)/2, additionally formalize the bridge from these rational envelopes to the real limit in an available real-analysis environment. The repository's current source closure does not supply that bridge merely by stating the recurrence bounds.

The upper/lower envelopes express the threshold through p² ≥ or ≤ pq+q², but this note deliberately does not claim that a real-limit theorem has been established. No conclusion about correlated multi-step inverse fibers or the orbit of 196 follows.
