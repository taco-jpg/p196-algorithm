# Agent 6: exact exterior coordinate dynamics

Base source: `4b4edf976b2c7a9ba1dad80636c0e21c66350325`.
Task claim: coordination commit `1b3935d7f0ad6aaff290a9c8baa883f60d572434`.

## Scope and current verification

This package proves exact finite-coordinate identities and necessary conditions
for returns of the unchanged `P196.Agent7.Finite.outerNext`. All four new
modules compile with pinned Lean 4.19.0 and `--trust=0`; every authored theorem
has an axiom report. The threshold and the completed Dynamics/Sign closure have
also passed separate clean builds and semantic review by `/root/runtime`.
The final nine-module independent Cycle review passed as well. The unchanged
repository verifier also passed on published source commit
`a075b2719c4ff1cb972b68b1d9240d8eaa8d463f` with a clean tracked source tree:
nine modules, ten commands, all 58 authored root theorem endpoints, and all
235 theorem constants found by module origin. Its receipt is retained in
`verification/canonical-source-a075b27/`; it remains a scoped result.

The new statements provide neither a closed exterior orbit nor global
acyclicity. They do not supply an infinite ordinary integer orbit or resolve
the status of 196. Formal identities on arbitrary natural states describe the
literal finite map; interpreting an arbitrary state as a decimal construction
still requires the original arithmetic realization hypotheses.

## Exact carry threshold

Write `n = B.length`, `D = 10^n`, `H = highValue B`,
`k = if 10 <= c then 1 else 0`, and `t = c - 9*k`.
The actual reversed normalization carry is `gamma = (H+k)/D`.
`CoordinateThreshold.lean` proves

```text
gamma = rhoNum c B / (9*D)
```

whenever `c <= 17` and `c != 9`, for arbitrary natural coefficients.
`quotient_identity_forall_iff` proves these phase restrictions are also
necessary for equality to hold for every finite word. That converse concerns
uniform equality, not equality at each individually selected word.

Under the same phase restrictions, `gamma = 0` is equivalent to
`rhoNum c B < 9*D`. If every coefficient is at most 18, `gamma = 1` is
equivalent to `9*D <= rhoNum c B`, and the numerator is less than `18*D`.
Empty words are included. Kernel-checked controls preserve the failures at
phases 9 and 18 and the possibility of carry 2 without coefficient control.
The latter refutes removing coefficient control altogether; it does not
assert that the pointwise bound is necessary for each particular word.

## Signed update and nonvanishing

`CoordinateDynamics.lean` uses the ordinary integer coordinate

```text
betaNum c B = zValue c B - c = 9*lowValue B - c*D.
```

Let `R = revN n (H+k)`, the reversal of the fixed-width normalized digits.
Every subtraction in the following contribution is an integer subtraction:

```text
highContribution c B = 9*R - t*D                 if gamma = 0
                       9 + 90*R - 10*t*D         otherwise.
```

`betaNum_outerNext` proves that the successor coordinate equals the input
coordinate plus this contribution, for every natural `c` and finite natural
word `B`. The proof reuses the original Agent115 `rawSucc_values` and
`successor_observation`, including the actual suffix stripping. The natural
subtractions defining the phase and the old raw successor are justified
explicitly; no phase or coefficient bound is needed for this algebraic identity.

`CoordinateSign.lean` proves `highContribution_ne_zero_of_pos` for every
`c > 0` and arbitrary word. The zero-overflow branch uses the strict
fixed-width reversal bound; the nonzero-overflow branch is 9 modulo 10.
The empty phase-zero control has contribution zero. Four canonical states
show that the overflow bit alone does not determine the sign:

| Phase | Word | Overflow | Contribution |
|---:|---|---:|---:|
| 2 | `[1]` | 0 | -11 |
| 2 | `[3]` | 0 | 7 |
| 2 | `[10]` | 1 | -191 |
| 2 | `[13]` | 1 | 79 |

## Finite trajectories and conditional returns

`CoordinateCycle.lean` defines `outerIter` by repeated use of the original
map and proves the exact telescope

```text
contributionSum s n = betaNum (outerIter n s) - betaNum s.
```

The notation above suppresses the explicit `.c` and `.B` projections. The
formal theorem `contributionSum_eq_betaNum_sub` includes them. The path of
length zero is included. A supplied finite chain has the same identity.
Equal endpoint beta coordinates, an exact state return, or a return with a
constant phase suffix appended all force the total contribution to be zero.
Only the sign-witness statements require a positive path length.

For a closed trajectory starting with a positive phase,
`closed_orbit_both_signs_of_pos` requires both a positive and a negative
increment. It assumes the return rather than establishing one.
`closed_orbit_weighted_balance` also gives the exact equality

```text
sum weightedPhase = 9*sum weightedReverse + 9*overflowCount.
```

Here `overflowCount` counts steps with nonzero high carry, and the weight is
1 at zero carry and 10 otherwise. This is an indicator even when an
unbounded input produces carry greater than one; no coefficient hypothesis
is silently needed by the weighted identity.

## Original dependencies and evidence

The unchanged definitions and earlier normalization/factorization/update
semantics retain the names and attribution of Agents 7 and 115.
`proofs/ExteriorUpdateLaw.lean` restores the exact Agent115 source from
commit `fba03a902e0f6b198cbf8f42efa8d11f8f2ba7a6`, original path
`proofs/contributions/agent-115/exterior-factorization/ExteriorUpdateLaw.lean`,
blob `db2f3c5ea38b8d49ef7da82631b2ed7a95a29bea`. Its original independent
Agent113 review is at `7f7afcd799b9a6363be7a4ecb317b1557df3ab4b`.
This restoration is dependency adoption, not a new result attributed to Agent6.

All reported theorem dependencies are within `propext`, `Classical.choice`,
and `Quot.sound`. Compiler-generated unsafe implementation artifacts are
inventoried separately from logical theorem dependencies; they are not used
as proof oracles. Failed development sources, diagnostics, author receipts,
and finite exploratory controls are preserved with their original status.
Python controls are corroborating experiments, not accepted proof evidence.

The first threshold source was published at
`000730e8b6a65bb76f10e06e34195eb1fd203f51`, with exact source blob
`34ddc74962d8bbef954f1626a80593de60906215` independently read back.
Local checkpoint `d0aefc4d854dfd661dd26df1ead220412499cbb9` has the same
tree but different commit metadata; that local hash is not a remote publication.

## Reproduce the scoped build

From a repository checkout, with the official Lean 4.19.0 executable (commit `6caaee842e94`):

```sh
python3 proofs/verify_project__214bf7673efe116b.py --lean /absolute/path/to/lean --registry proofs/contributions/agent-6/exterior-coordinate-dynamics-20261016/threshold.registry.json --project agent6-coordinate-threshold --output /absolute/new/output/directory
```

The threshold registry covers the complete four-module closure. The complete
`coordinates.registry.json` covers all nine modules with project key
`agent6-coordinate-dynamics`; use it in the same command for the full package.
These scoped registries do not modify the global accepted catalogue.
The unchanged verifier retains its original Agent1 field; the actual actor
and precise command belong in the accompanying run receipt.

PR: https://github.com/taco-jpg/p196-algorithm/pull/90 .
Independent-review evidence and publication bindings are appended separately
from the frozen theorem source. Only the serialized integration owner can
place this contribution into the shared accepted build.
