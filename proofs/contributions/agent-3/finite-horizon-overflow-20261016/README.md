# Agent #3: finite-horizon overflow fibers

This contribution formalizes the final finite-horizon section of the preserved
`persist_inverse_fibers_proof.txt`. It does not claim a new discovery or an
infinite palindrome-avoiding seed.

## Checked source checkpoint

Pinned base: `4b4edf976b2c7a9ba1dad80636c0e21c66350325`.
Claim: `55c0133a597cd3577fbbb864414fe4527729e554` on `p196/coordination`.
Toolchain: Lean 4.19.0, release commit `6caaee842e94`.

`FamilyDefinitions.lean`, `FamilyCardinality.lean`,
`FiniteHorizonOverflow.lean`, `SafetyBridge.lean`, `NormalizedSafety.lean`, and
`FiniteHorizonTheorem.lean` compile. The transition module proves the exact formula
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

`finite_horizon_overflow_family` joins this exact enumeration and transition
to ordinary decimal arithmetic. For every counted input `w`, the unchanged
normalization `Agent8.normalize w 0` represents a positive integer. Its
ordinary `Lychrel196.orbit` contains no palindrome at any time `t <= k`,
including time zero. All these normalized integers have the same next
ordinary reverse-add value, namely the decimal coefficient value of the
common target. The counted objects remain coefficient words; this does not
assert that there are exactly `2 ^ m` distinct normalized integers or count
all decimal digit splits of each word.

The target's central run contains `2 * k - 1` eighteens. The safety proof
applies the existing `DecimalSafeRuns.iter_not_palindrome_of_run` for positive
times and uses the target's odd outer coefficient `5` for time zero.
`NormalizedSafety` proves canonicality and identifies the existing list-pair
operation with the original decimal column sums. It does not change the
decimal reverse-add definitions.

The current checkpoint is `LEAN-CHECKED`. The portable verifier completed a
fresh ten-module build and audited all 67 explicit public source declarations
plus 62 generated logical helpers. Every audited proof dependency is confined
to `propext`, `Classical.choice`, and `Quot.sound`. All source exports are safe
and nonpartial. The 33 compiler implementation symbols are recorded separately
using Lean's own safety flags; they are not accepted logical proof declarations.
A separate reviewer completed the fresh cardinality rebuild and interpretation
review, and the independent whole-chain review is in progress.

No shared accepted registry has been modified. Failed development source and
logs remain in `development/`, outside the completed module set. The original
written source and finite diagnostic specification checks are retained with
their provenance under `development/specification/`; those diagnostics do
not replace the all-parameter Lean proofs.

## Dependencies and reproduction

Use unchanged current-main sources, renamed only in a fresh build directory:

| Lean module | Repository source | Git blob |
|---|---|---|
| PeriodObstructions | `proofs/PeriodObstructions__70ce034b31b5b218.lean` | `a89dda20e9a9b3452f7d0272b4fbd28f7d6ce119` |
| ActualWordBridge | `proofs/ActualWordBridge__7f032d27940694a8.lean` | `d3f49353f9970c610d818d8f5da78ad5c739e7df` |
| LychrelDigitSums | `proofs/LychrelDigitSums__0810ace083af80c5.lean` | pinned in the verification manifest |
| DecimalSafeRuns | `proofs/DecimalSafeRuns__aaaac5a66315c5e2.lean` | pinned in the verification manifest |

Compile in the order `PeriodObstructions`, `ActualWordBridge`,
`LychrelDigitSums`, `DecimalSafeRuns`, `FamilyDefinitions`, `FamilyCardinality`,
`FiniteHorizonOverflow`, `SafetyBridge`, `NormalizedSafety`,
`FiniteHorizonTheorem`, with `LEAN_PATH` set to a fresh build directory.
Independent evidence is retained under `review/`. The source-pinned verifier
and manifest under `verification/` reproduce the complete accepted
contribution module set and its axiom audit:

```bash
python3 proofs/contributions/agent-3/finite-horizon-overflow-20261016/verification/verify.py \
  --lean /absolute/path/to/lean-4.19.0/bin/lean \
  --repo /absolute/path/to/p196-algorithm \
  --build-dir /absolute/path/to/a-new-clean-build
```

`verification/evidence/verification.json` records the successful commands,
source identities, compiler environment, exit statuses, and full logical
axiom inventory. `verification/evidence/artifact-index.json` authenticates the
retained logs and generated audit source.

The generic central-run propagation theorem already exists in
`DecimalSafeRuns`; it is an attributed dependency, not a new theorem here.
Agent #2 owns the separate sharp all-width overflow upper bound. Agent #9 owns
the separate no-overflow Fibonacci count. This contribution counts coefficient
words, rather than individual decimal digit splits. The finite words vary with
the requested horizon.

Compiled Lean objects, runtime installations, copied build dependencies, and
operational transfer helpers are reproducible infrastructure and are excluded.
Original new sources and substantive successful/failed proof logs are retained.
