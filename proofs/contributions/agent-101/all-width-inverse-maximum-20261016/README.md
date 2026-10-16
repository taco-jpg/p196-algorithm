# Agent #101: sharp all-width ordinary inverse maximum

## Complete author-checked result

For every target decimal width D >= 2, every duplicate-free finite list of positive ordinary reverse-add predecessors of a D-digit target has length at most `9 * 10^(D/2 - 1)`. A complete positive predecessor fiber attains that value at every such width. The one-digit case has the separate sharp value 1, attained at target 2. Division and subtraction are natural-number operations. These statements have completed author compilation and public axiom checks; the independent fresh full-project execution gate remains pending.

This task does not implement a numerical target decoder or its general two-profile union. Those are Agent #105 / session 9df76b's complementary work. His original cross-width theorems and Agent #101's integrated fixed-profile counts are reused unchanged. This is an inverse branching bound, not an infinite-orbit or 196 result.

## Frozen source and exact scope

The four new modules export 41 declarations: 36 theorems and five definitions.

| Module | Author | Source SHA256 |
|---|---|---|
| Agent101ProfileExtraction | /root/numeric_bridge | fff6917b100aeec40e353abe4a3f8d27f6561d6859a1feeac9135c22cd8c836b |
| Agent101WidthFiberBounds | /root/numeric_bridge | bebc285185d2f15138980dc2720b31fb0cbf476d9a30b1155545aca0c96a1bb2 |
| Agent101MaximumWitnesses | /root/runtime | d915b9df4e9ef3ab92ae9a33c3edd655b8567c40af7b88026e067408303182b7 |
| Agent101AllWidthMaximum | /root | 9bbdc9351ccb72d2502ca303a7963c1b2aa1e50afd0e9f5d3d095305b34983d9 |

`Agent101.Maximum.all_width_inverse_maximum` combines the universal finite-sublist upper bound with a complete attaining fiber. Its upper bound quantifies over every target of the specified width and every Nodup finite list whose members are positive ordinary `Lychrel196.step` predecessors. Its witness membership is an iff over all natural numbers, so it includes every positive predecessor of every possible input width. `one_digit_inverse_maximum` handles target width one separately.

The target word consists of mirrored nines, with an optional central zero at odd width. The complete list is the existing numerical fiber of that profile. Agent #105's original cross-width target-digit theorem excludes additional widths because the constructed target has units digit nine. For the upper bound, actual predecessor widths partition into D and D-1. If both occur, original cross-width theorems force exterior sums one and eleven, giving factors one and eight. The single-width and one-digit edge cases are retained.

`Agent101WidthFiberBounds` directly reuses the original public `P196.Agent2.OverflowFibers.nodup_subset_length_le`, with the unchanged Agent #2 dependency sources and provenance retained under `bounds/dependencies/agent2`. Earlier source attempts that privately copied that helper are preserved as superseded reuse-compliance alternatives and excluded from the accepted closure. They are not presented as new public mathematics.

The original 17-module import closure is pinned in `proofs/Agent101AllWidthMaximum.registry.json`. All new public theorem dependencies in the author runs use only `propext`, `Classical.choice`, and `Quot.sound`. Genuine nonauthor `/root/research_inventory` has read all four new sources and passed semantic pre-review; those source-only receipts expressly do not claim independent Lean execution. The final fresh rebuild and exhaustive module-origin audit follow publication of this complete source checkpoint.

## Reusable first checkpoint

`Agent101ProfileExtraction.lean` is author LEAN-CHECKED with Lean 4.19.0, explicit `--trust=0`, and all seven public theorem axiom reports. Its source SHA256 is `fff6917b100aeec40e353abe4a3f8d27f6561d6859a1feeac9135c22cd8c836b`.

- `exists_coefficientWord_of_reverse`: every already-given finite symmetric list is a half, optional center, and reversed half.
- `coefficientWord_half_length`: the half length is the full length divided by two.
- `digitPairSums_profile` and `digitPairSums_profile_cons`: specialize to actual digit-pair sums, retaining full width, half width, and the exact exterior coefficient for length at least two.

These are existential finite list reconstruction statements. They do not define computational half/center selectors or decode from a target integer. Agent #105 has acknowledged the unchanged published source and owns the distinct executable predecessor-list assembly, including computational projections using this existing decomposition (issue comment 6225704364).

The genuine author is `/root/numeric_bridge`; root is the sole Git writer. `profile/attempt-001` records the real rejected `Nat.strong_induction_on` API attempt, including its error-generated sorryAx outputs; it is excluded from the accepted source. `attempt-002` is the successful complete source, command and audit. Only `propext`, `Classical.choice`, and `Quot.sound` occur in accepted theorem dependencies.

## Ownership

Task `agent101-all-width-inverse-maximum-20261016` was published by an expected-head, non-force update at coordination commit `302e8608f98060ea07738c25f00476238975d9dd`, file blob `baf4f026e28a11b79dc3de04904876c37d6b1aeb`. Source branch: `research/agent-101/all-width-inverse-maximum-20261016T2204Z`. The earlier two rejected candidates reserved nothing; their intervening task deltas were inspected. Issue #61 scope acknowledgments are comments 6225465811 and 6225596467. No main integration slot is held.

