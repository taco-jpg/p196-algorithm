# Agent #9 — Fibonacci inverse-fiber rate: formalization feasibility

**Status: WIP research note; no new Lean theorem or compiler run is claimed.**

## Exact existing result

The preserved source `proofs/coordination/patches/agent9-nooverflow-fibonacci-20261016/InverseFibers.lean` imports only `Std`. It defines the Fibonacci sequence by
`fib 0 = 0`, `fib 1 = 1`, and `fib (n+2) = fib (n+1) + fib n`. The existing declarations include `fib_le_succ`, `run_bound`, `inverseCount_bound`, and `nines_exact`. The accompanying original written argument gives the exact no-overflow maximum `max(1, F_(m-1))) and identifies its exponential rate informally as `phi = (1 + sqrt(5))/2`.

This is already an exact recurrence and finite-fiber theorem. The missing claim is the asymptotic rate, not the Fibonacci recurrence or the finite maximum.

## Formalization boundary

The repository's current reproduction guidance says the pinned Lean modules use `Std` and require no Mathlib download. This session's container has neither `lean` nor `lake` available, and no connected tool has executed Lean. Therefore the ordinary real-limit statement has **not** been formalized or verified here. No use of `Real`, `Filter.Tendsto`, or a golden-ratio limit API should be assumed available in the current source closure.

A correct proof route must first choose one of two explicit scopes:

1. **Real-analysis scope:** provide an authorized, pinned real-analysis dependency and prove the conventional limit of the (m)-th roots. That changes the dependency contract and needs separate approval and source-closure review.
2. **Std-only scope:** formulate a fully discrete growth characterization with rational comparison rates and explicit integer inequalities, prove it in Lean, and state precisely how that characterization corresponds to the usual golden-ratio rate. This requires real proofs of the upper and lower comparison bounds; merely citing the written asymptotic sentence or checking finitely many indices is insufficient.

The second route is the only one compatible with the currently documented dependency contract, but its exact theorem statements and constructive constants still need to be worked out before authoring accepted source. A simple recurrence lemma or finite table alone would not discharge the asymptotic obligation.

## Mathematical scope limit

The result concerns the worst-case size of a **single-step** no-overflow inverse fiber. Even a formally proved rate (phi) would not bound correlated fibers over repeated reverse-add steps, establish a uniform contraction of terminating basins, produce one seed that avoids palindromes forever, or resolve the orbit of 196.

## Next action

Inspect the exact current declarations and determine whether a discrete rational-rate squeeze can be stated with explicit constants using only `Nat` arithmetic. If the construction cannot be completed without importing unapproved real analysis, keep this as a documented blocker rather than adding axioms or presenting an uncompiled Lean draft as a theorem.
