# Agent #111: bounded variable-modulus obstruction

Task: `agent111-bounded-variable-modulus-20261016`, claimed in `p196/coordination`. Coordinate via issue #61.

## Mathematical scope

Let `mu(L)` be a positive modulus at each sufficiently large ordinary decimal width `L`, with uniform bound `mu(L) ≤ K`. If set membership is constant on positive canonical same-width decimal integers congruent modulo `mu(L)`, then it is constant on same-width classes modulo the common product `U(K) = 1·2·...·K`. The statement is a direct, attributed consequence of Agent111's merged PR #40 theorem `ExactLengthResidues.fixed_modulus_closed_set_contains_palindrome`.

Under nonempty positive membership and forward closure under actual decimal reverse-and-add, the resulting set must contain an ordinary positive palindrome.

This rules out bounded *width-dependent* congruence-only safe invariants; it says nothing about moduli increasing without a uniform bound, richer digit languages, direct orbital palindrome hits, or whether 196 is Lychrel.

## Lean and evidence

`BoundedModulus.lean` imports the original `Saturation` module without editing its theorem declarations. The local `universalModulus` recursively defines the common product without requiring Mathlib. Its divisibility lemma and `Nat.mod_mod_of_dvd` form the bridge to `SetSaturatedAbove`.

**Current status: LEAN-CHECKED; independent mathematical review pending.** Official GitHub Actions [run #38970352264](https://github.com/taco-jpg/p196-algorithm/actions/runs/38970352264) succeeded with Lean 4.19.0 (commit `6caaee842e94`). It rebuilt **12 actual modules** in a clean runner directory, including the unchanged canonical decimal source and the new module, and audited **1,008 compiled theorem constants**. All transitive mathematical theorem axioms were among `propext`, `Classical.choice`, `Quot.sound`; no new unsafe implementation axioms were introduced. The 13 existing compiler-generated implementation symbols in the unchanged decimal module were recorded separately, and do not enter any theorem axiom audit. Actual evidence: [`verification/CI.json`](verification/CI.json), [`verification/BoundedModulus.log`](verification/BoundedModulus.log) and the full [CI artifact archive](https://github.com/taco-jpg/p196-algorithm/actions/runs/38970352264/artifacts/12075449870) (GitHub artifact expires after 30 days). The full source/snapshot checker and workflow allow reproduction after expiry.

The pinned original is retained at `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/contributions/agent-111/exact-length-residues/`. Original source commit: `c3192d5bf2962298bcb2bb209a0947f657e8a7e5`. The canonical decimal semantics come from the same archived original tree.

No shared accepted registry, default branch, or integration slot is modified.
