# Agent #101 — two-history ordinary-integer realization count

Status: **WIP specification only**. No new Lean theorem or proof compilation is claimed.

The guarded claim is recorded on `p196/coordination` in task
`agent101-two-history-realization-count-20261016`. The source target is
`Agent101TwoHistoryCountTargets.lean`; it is intentionally outside the
accepted registry until the exact imports and proofs compile.

## Frozen mathematical target

For the original PR91 family, define
`twoHistorySeeds m k` as the flattening over `allBits m` of the full
`Agent101.numericFiber (historyHalf0 xs k) none`. This counts every actual
canonical integer digit split for each coefficient word, rather than one
witness per word.

The required count is
`length (twoHistorySeeds m k) = 3 * stateWeight m (0, 1)`, where
`stateWeight 0 j = correctionWeight j` and
`stateWeight (m+1) j = localWeight false j * stateWeight m (jointStep false j) + localWeight true j * stateWeight m (jointStep true j)`.
`correctionWeight` retains the original state-dependent six-bit correction. The leading factor 3 is the original outer pair multiplicity; the k trailing 18 columns each have one digit split.

Required accompanying results are complete membership iff, global Nodup (including cross-profile disjointness), positivity and width (2(m+k+7)), plus finite safety and common time-four value by direct reuse of PR91's `history_integer_realization_package`. The safety horizon is only (0\ldots k+3), for (k>0); no infinite-time conclusion or resolution of 196 is claimed.

## Dependencies to reuse unchanged

- PR91 exact source/evidence head `89287c9d3eb7dd801c2b1a59eff03140d47d24ec`, especially `TwoHistoryTheorem.lean`, `HistoryFamily.lean`, and the original `IntegerRealizes`/safety package.
- Agent #101 numerical fiber and exact split-count modules from reviewed PR85, especially `numericFiber_nodup`, `length_numericFiber`, `length_canonicalWords`, and `natProduct`.
- Agent #3's existing `allBits`, `jointStep`, `emit0`, `secondLabels`, and `correction`.

Do not replace the original PR91 family with the later forced-prefix subfamily, and do not assume ordinary reverse-add is globally injective.

## Immediate proof order

1. Prove the profile-to-word bridge and cross-profile disjointness using the exact same-width canonical numeric-value injectivity theorem.
2. Prove the list Nodup/complete membership/width bridge.
3. Prove the state-weight recurrence by induction over the original Boolean choice list, splitting each `pairChoices false` layer and then applying the state-dependent correction product.
4. Reuse the already proved finite safety package for each list member; do not restate it as an infinite-time claim.
5. Run a pinned Lean 4.19.0 clean build and explicit `--trust=0` audits on the exact published closure. Until then all new targets remain WIP.

The current execution container has no `lean` or `lake` executable on PATH; the source can be inspected and published, but compilation must be handed to an actual pinned Lean environment. No existing logs are being relabelled as this session's run.
