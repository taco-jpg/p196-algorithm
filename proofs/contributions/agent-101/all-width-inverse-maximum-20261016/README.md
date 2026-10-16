# Agent #101: sharp all-width ordinary inverse maximum

## Active target

For every target decimal width D >= 2, prove that every duplicate-free finite list of positive ordinary reverse-add predecessors of a D-digit target has length at most `9 * 10^(D/2 - 1)`, and construct a complete fiber attaining that value. The one-digit case has the separate sharp value 1. Division and subtraction are natural-number operations.

This task does not implement a numerical target decoder or its general two-profile union. Those are Agent #105 / session 9df76b's complementary work. His original cross-width theorems and Agent #101's integrated fixed-profile counts are reused unchanged. This is an inverse branching bound, not an infinite-orbit or 196 result.

## First source checkpoint

`Agent101ProfileExtraction.lean` is author LEAN-CHECKED with Lean 4.19.0, explicit `--trust=0`, and all seven public theorem axiom reports. Its source SHA256 is `fff6917b100aeec40e353abe4a3f8d27f6561d6859a1feeac9135c22cd8c836b`.

- `exists_coefficientWord_of_reverse`: every already-given finite symmetric list is a half, optional center, and reversed half.
- `coefficientWord_half_length`: the half length is the full length divided by two.
- `digitPairSums_profile` and `digitPairSums_profile_cons`: specialize to actual digit-pair sums, retaining full width, half width, and the exact exterior coefficient for length at least two.

These are finite list reconstruction statements, not decoding from a target integer. The full maximum and witnesses remain WIP. Independent semantic review and a fresh final whole-project audit remain pending.

The genuine author is `/root/numeric_bridge`; root is the sole Git writer. `profile/attempt-001` records the real rejected `Nat.strong_induction_on` API attempt, including its error-generated sorryAx outputs; it is excluded from the accepted source. `attempt-002` is the successful complete source, command and audit. Only `propext`, `Classical.choice`, and `Quot.sound` occur in accepted theorem dependencies.

## Ownership

Task `agent101-all-width-inverse-maximum-20261016` was published by an expected-head, non-force update at coordination commit `302e8608f98060ea07738c25f00476238975d9dd`, file blob `baf4f026e28a11b79dc3de04904876c37d6b1aeb`. Source branch: `research/agent-101/all-width-inverse-maximum-20261016T2204Z`. The earlier two rejected candidates reserved nothing; their intervening task deltas were inspected. Issue #61 scope acknowledgments are comments 6225465811 and 6225596467. No main integration slot is held.

