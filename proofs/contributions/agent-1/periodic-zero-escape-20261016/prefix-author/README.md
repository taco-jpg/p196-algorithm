# Finite-prefix zero-period guard: author evidence

Claim accepted at `0db777cb118e3c395cb495a1a8e8dc7b13cf9893`; scope proposal [6225969071](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6225969071). Genuine Agent #1 specialist `/root/symbolic_scope` authored only `Agent1PeriodicZeroPrefix.lean` and this evidence directory. Parent is sole Git writer and owns the final arithmetic composition.

Frozen source SHA256 `c922e0268511b93865a2a047d8c59599ebaf3463d713f6ff90351230f4eda5cb`, Git blob `4eb692897249bd632d6db69c0cc5bbfa9982c2c0`.

The two exact exports in namespace `Agent1.Periodic` are:

* `zeroExponent_guarded_prefix s hv M N hbound t ht`, with `ht : t ≤ N`, supplies the guard `3 ≤ zeroExponent s (M+3) t` and unchanged width invariant `M+24 ≤ interfaceWidth(t)+8*zeroExponent s (M+3) t`.
* `zeroLiftWord_step_prefix s hv M N hbound t ht`, with `ht : t < N`, supplies the literal equality `Agent8.stepWord (zeroLiftWord s (M+3) t) = zeroLiftWord s (M+3) (t+1)`.

Here `hbound` quantifies only times `t ≤ N`. No all-time interface bound is introduced. The file imports the frozen `Agent1PeriodicZeroExponent` and reuses the original `zero_width_step`, validity propagation, exact quotient theorem, and actual zero-period invariance. There are no new word, orbit, exponent, carry, or validity definitions. No safety premise or positive M/N premise is added. The final cap-escape theorem is outside this module.

## Execution and audit

The only source attempt is `attempt-001`, which passed on its first actual execution. Exact source, full log, timing, hash and command are preserved. Official Lean 4.19.0 compiler identity/hash is in `compiler.json`; strict options were `--trust=0 -j1 -DElab.async=false`.

The author build reused source-pinned objects from the prior separate fresh review at `/workspace/p196-agent1-session-20261016/periodic-zero-cycle-review-clean-001`, source baseline `fc17722becfd671e349aeae21501d0fd5867dfb0`. All 24 existing registry source/object pairs were copied and hashed. The actual transitive import closure of this module's sole import contains 20 of those modules. `reused-dependencies.json` explicitly records both sets. No fresh dependency compilation or independent new-module review is claimed by this incremental author receipt.

`audit-001` passed with the same strict compiler options. All seven safe constants originating in the new module are theorems, including five generated proof helpers; there are zero unsafe implementation constants. Complete transitive axiom union is exactly `propext`, `Classical.choice`, `Quot.sound`. The audit rejects new axiom declarations and every disallowed transitive axiom. Full multiline output is retained; public theorem prints follow it. All accepted source is free of sorry/admit, new axioms, native_decide and Lean.ofReduceBool.

## Reproduction

The preserved source-snapshot runner refuses to overwrite any existing attempt directory. With the explicitly recorded pinned author object directory present:

```sh
python3 proofs/contributions/agent-1/periodic-zero-escape-20261016/prefix-author/run-attempt.py attempt-002
```

Actual isolated build directory: `/workspace/p196-agent1-session-20261016/periodic-zero-prefix-author-build`. Full fresh verification should build the source closure in import order, then this module and the preserved `audit-001/ZeroPrefixAudit.lean`. Parent and genuine nonauthor reviewer own the later complete combined build.
