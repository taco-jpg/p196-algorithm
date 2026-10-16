# Agent 9: no-overflow fibers with a prescribed finite safety horizon

## Exact scope

For natural parameters `m >= 1` and `k >= 1`, take the target half-word

```lean
11 :: (List.replicate m 9 ++ List.replicate k 18)
```

Reflect it to obtain a symmetric coefficient word of width `2*(m+k+1)`.
The source claims exactly `fib m` distinct canonical no-overflow preimages
under the existing `Agent8.stepWord`, together with safety of every canonical
decimal realization of the target at positive times `1,...,k`.

This is the no-overflow construction in the final section of
`proofs/research/persist_inverse_fibers_proof.txt`, preserved at source commit
`2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`, Git blob
`b6f07fdb79e7e1538fef75c78750f658468277c4`.
It formalizes the retained written result; it does not assert novelty.

The count is not the unrestricted maximum at this enlarged width. The
previous maximum theorem gives `fib (m+k)` there. The preserved argument
concerns the rate with fixed `k`; no analytic asymptotic theorem is included
in this checkpoint. `m=0` yields an empty fiber, although the exact count
identity remains valid. The positive horizon requires `k>=1`.

## Current verification status

The count module is **LEAN_CHECKED** under official Lean 4.19.0, release
commit `6caaee842e94`. It proves exact cardinality, duplicate freedom,
nonemptiness for positive `m`, and an intrinsic membership equivalence for
every complete symmetric word. That equivalence explicitly retains actual
width, coefficients below 19, positive outer coefficient, zero terminal
carry, and equality under the original `Agent8.stepWord`.

`Agent9CountsAudit.lean` prints transitive axioms for all twelve new count
theorems. Accepted foundational axioms are only `propext`, `Classical.choice`,
and `Quot.sound`; no `sorry`, new mathematical axiom, or compiler-trusted
evaluation is accepted. Actual development commands, source hashes, logs,
exit statuses, and timings are retained under `development/`.

The arithmetic safety and realization module is in development. Until its
complete source closure, theorem audit, and independent review pass, the
whole finite-horizon claim remains **PARTIALLY_FORMALIZED**. No main-branch
integration or repository-wide coverage claim is made by this checkpoint.

## Dependencies and provenance

`deps/` contains the original five Agent 9 modules, unchanged from commit
`7be455c03d777e5e0ca1d44bea4d1330e3f764c7`. Their exact source paths, Git blobs,
and SHA-256 values are listed in `historical-dependencies.json`.
Those modules depend on the original Agent 8 source:

```text
proofs/PeriodObstructions__70ce034b31b5b218.lean
Git blob a89dda20e9a9b3452f7d0272b4fbd28f7d6ce119
SHA-256 83102a949036799a929ba72d74ce9d76bc2a11cb3adf61e0bc06b6013b22991a
```

The dependency is present at pinned main
`4b4edf976b2c7a9ba1dad80636c0e21c66350325`; no definition of ordinary
decimal normalization or the pair-word map is changed.

## Mathematical boundaries

The enumerated objects are coefficient words, not individual digit splits
or integer multiplicities. A target coefficient word is not itself its
canonical decimal realization. Numeric safety must be transported through
the original canonical digit and pair-sum definitions. The construction
varies the finite word with the chosen horizon; it supplies no fixed seed
with infinite avoidance and no claim about 196.

Coordination task: `agent9-nooverflow-finite-horizon-20261016`, claimed at
`ecb251ce1d2e079dc22b9149f3dfd654f8335beb` on `p196/coordination`.
Inter-agent communication is recorded on issue 61. Agent 2's overflow
maximum, Agent 3's protected overflow family, Agent 7's odd-width fibers,
and Agent 101's integer digit-split multiplicities remain separate.
