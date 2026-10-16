# Agent 124: five- and six-column prefix-ancestry kernel

Task `agent124-prefix-five-six-column-kernel` on `p196/coordination`
(claim commit `405aa651f4e56cb8d168aa33eeb90f89d853a551`).
Branch `research/agent-124/s20261015T1600`, source base main
`eec3d5f3646cab50abad6e610ea19626cd249070`.

**Decimal Lychrel existence and the claim for 196 remain unproved.** This
task targets 33 restricted palindrome families only.

## Target

For each of the 33 remaining baseline three-digit prefixes (24 that close at
five certificate columns: 119, 213, 216, 257, 348, 384, 426, 429, 474, 674,
737, 755, 778, 783, 784, 787, 788, 789, 858, 859, 905, 906, 923, 935; and 9
that close at six: 276, 277, 278, 377, 385, 785, 786, 856, 857), prove in Lean:
every positive ordinary decimal integer that reaches a palindrome beginning
with that prefix does so within an explicit number of steps, and hence the
ordinary orbit of 196 never contains such a palindrome.

## Status

| Component | Status |
|---|---|
| `Agent124PrefixK.lean`: width-generic endpoint | **LEAN-CHECKED (conditional), dev build** |
| Concrete k = 5 / k = 6 certificates | WIP, nothing checked |
| Leading-digit-1 bridge for 119 | WIP |
| Independent review | not requested yet |

`Agent124PrefixK.lean` (SHA256 `e05b7758d18da8b40a3048595cfdab7d563a90342e069b05e305e36fe1ae9396`)
compiles with official Lean 4.19.0 (release commit `6caaee842e94`) against
Agent #104's accepted, unchanged modules `LychrelDigitSums`, `PrefixInverse`,
`FastInverse`, `ActualPrefix`, `PrefixCertificate`, `LongRowsBase`,
`FastRowsBase`, `PalindromeBridge`, `ShortBoundary`. Its exported theorems
depend only on `propext`, `Classical.choice`, `Quot.sound`
(`logs/Agent124PrefixK-dev01.log`). This was a development build in one
directory, not yet a clean pinned rebuild.

Main declarations (namespace `Agent124.PrefixK`):

- `wordOf_mem_symWords`: every admissible pair word of any width `n` lies in
  the executable list `symWords n` (generated from halves).
- `actual_iterPairs_rank_k`: for any certificate width `k > 0`, all checked
  long rows plus short-transition rank descent bound the time of any actual
  pair trajectory ending in the rank tree by the endpoint rank.
- `target_project_mem_initialWordsK`: the width-`k` projection of every
  admissible digit word beginning `a, b, c` lies in the finite list
  `initialWordsK k a b c`, for every width at least three.
- `canonical_last_step_initialK`: the last predecessor of a palindrome
  beginning `a, b, c` with `a ≥ 2` projects into that list (via Agent #104's
  `canonical_last_step`).
- `ancestry_bound_of_checks` / `no_196_of_checks`: conditional endpoints.
  Given a rank tree with all long rows checked, short descent, and every
  initial word of rank at most `bound`, every positive integer reaches a
  target palindrome within `bound + 1` steps; if `bound + 1 ≤ 100`, the 196
  orbit never contains one (using the existing kernel-checked first 100 steps).

These are conditional theorems; no concrete certificate instance is supplied
yet, so no prefix family is excluded by this checkpoint.

## Exploration (untrusted)

`exploration/` holds the Python scoping scripts and their raw output:
minimal-width backward closures for all 397 three-digit classes
(`scope_all.log`), the claimable set (`claim_set.json`), and combined-closure
sizes (`union.py`: 25,936 nodes at k = 5 for the 24 five-column classes;
360,916 at k = 6 for the 9 six-column classes). These are discovery tools,
not proofs.
