# Fixed boundary-carry schedules: small exact obstructions

These experiments test proposed strategies for escaping a safe **abstract
outer prefix**. They do not prescribe the carry history of any fixed
decimal integer and do not construct an infinite safe orbit.

The existing `research/main_existence_attempt/prefix_any_clock/` result
already computes the greatest universally closed safe prefix set at
widths one through five and finds it empty. Its two possible boundary
carries are each realizable by some ordinary finite integer at a single
step. A particular sequence of freely chosen carries need not arise from
one integer throughout its orbit. The distinction is essential here.

## Exact classification at widths one through three

For the established prefix transition, a prefix is safe when it contains
a coefficient at least ten and is not entirely in `{0,11}` with outside
coefficient eleven. An escape means that this sufficient universal-safety
condition ceases to hold; it does not mean a particular integer has become
palindromic.

The new scripts classify every canonical prefix, with every schedule
phase for the alternating schedule. They stop a path at its first unsafe
prefix or identify its complete safe cycle. Every cycle is retained.

| Imposed boundary inputs | Width | States including phase | Eventually unsafe | Safe cycle basin | Maximum escape time among escaping states |
| --- | ---: | ---: | ---: | ---: | ---: |
| Constant 0 | 1 | 18 | 18 | 0 | 1 |
| Constant 0 | 2 | 342 | 339 | 3 | 13 |
| Constant 0 | 3 | 6498 | 6498 | 0 | 21 |
| Constant 1 | 1 | 18 | 18 | 0 | 1 |
| Constant 1 | 2 | 342 | 339 | 3 | 12 |
| Constant 1 | 3 | 6498 | 6498 | 0 | 21 |
| Alternating 0,1 | 1 | 36 | 36 | 0 | 1 |
| Alternating 0,1 | 2 | 684 | 678 | 6 | 13 |
| Alternating 0,1 | 3 | 12996 | 12996 | 0 | 24 |

In particular, none of these three schedules proves a general escape
theorem: each has a safe two-column cycle.

- Constant 0: `(8,12) -> (17,4) -> (8,12)`.
- Constant 1: `(8,11) -> (17,3) -> (8,11)`.
- Alternating inputs have both cycles, with the phases recorded in the
  JSON evidence.

These cycles obstruct the specified control strategies only. The existing
two-column greatest-trap computation still shows that suitable *other*
choices escape every prefix. Conversely, the absence of cycles at width
three is a complete finite classification, not an all-width assertion.

## Reproduction

```sh
python -B proofs/contributions/2026-10-14-prefix-controls/fixed_zero_prefix.py
python -B proofs/contributions/2026-10-14-prefix-controls/fixed_clock_controls.py
```

`fixed_zero_prefix.json` and `fixed_clock_results.json` preserve all tested
state-space sizes, exact counts, maximum finite escape lengths, and every
safe cycle. The source implements the finite functional-graph analysis;
it makes no claim to have proved a new all-width elimination theorem.
