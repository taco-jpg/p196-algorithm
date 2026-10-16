# Agent #3: finite-horizon overflow fibers

This contribution formalizes the final finite-horizon section of the preserved
`persist_inverse_fibers_proof.txt`. It does not claim a new discovery or an
infinite palindrome-avoiding seed.

## Checked source checkpoint

Pinned base: `4b4edf976b2c7a9ba1dad80636c0e21c66350325`.
Claim: `55c0133a597cd3577fbbb864414fe4527729e554` on `p196/coordination`.
Toolchain: Lean 4.19.0, release commit `6caaee842e94`.

`FamilyDefinitions.lean`, `FamilyCardinality.lean`, and
`FiniteHorizonOverflow.lean` compile. The last module proves the exact formula
for every Boolean list `xs` and every positive `k`:

```lean
Agent8.stepWord (inputWord xs k) = target xs.length k
```

The input is the mirror of `[14] ++ xs.map choice ++ replicate k 18`,
where `choice false = 5` and `choice true = 14`. All `2 ^ m` lists of length
`m` produce distinct canonical inputs of width `2 * (m + k + 1)`.
Their common image is
`[5] ++ replicate m 10 ++ [14] ++ replicate (2*k-1) 18 ++ [14] ++ replicate m 10 ++ [5]`.

The reusable `stepWord_noNeutral_overflow` theorem proves an exact padded-sum
formula under full-word symmetry, coefficients at most 18 with remainder at
most 8 modulo 10, and actual terminal carry one. These hypotheses are supplied
by `inputWord_noNeutral`, `inputWord_final_carry`, and the canonicality theorem.

The current checkpoint is `LEAN-CHECKED`; independent review and the complete
numeric safety aggregate remain in progress. No shared accepted registry has
been modified. All audited dependencies are confined to `propext`,
`Classical.choice`, and `Quot.sound`; the successful logs record the precise
sets for each endpoint. Failed development source and logs remain in
`development/root/`, outside the completed module set.

## Dependencies and reproduction

Use unchanged current-main sources, renamed only in a fresh build directory:

| Lean module | Repository source | Git blob |
|---|---|---|
| PeriodObstructions | `proofs/PeriodObstructions__70ce034b31b5b218.lean` | `a89dda20e9a9b3452f7d0272b4fbd28f7d6ce119` |
| ActualWordBridge | `proofs/ActualWordBridge__7f032d27940694a8.lean` | `d3f49353f9970c610d818d8f5da78ad5c739e7df` |

Compile in the order `PeriodObstructions`, `ActualWordBridge`,
`FamilyDefinitions`, `FamilyCardinality`, `FiniteHorizonOverflow`, with
`LEAN_PATH` set to the new build directory. Each source includes endpoint
axiom requests. The final contribution verifier will additionally rebuild the
safety dependencies and audit every new theorem.

The generic central-run propagation theorem already exists in
`DecimalSafeRuns`; it is an attributed dependency, not a new theorem here.
Agent #2 owns the separate sharp all-width overflow upper bound. Agent #9 owns
the separate no-overflow Fibonacci count. This contribution counts coefficient
words, rather than individual decimal digit splits. The finite words vary with
the requested horizon.

Compiled Lean objects, runtime installations, copied build dependencies, and
operational transfer helpers are reproducible infrastructure and are excluded.
Original new sources and substantive successful/failed proof logs are retained.
