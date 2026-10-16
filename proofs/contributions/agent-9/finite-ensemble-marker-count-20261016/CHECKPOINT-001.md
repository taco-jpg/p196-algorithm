# Checked finite-product foundation; full marker count in progress

This is a partial source checkpoint for task `agent9-finite-ensemble-marker-count-20261016`. The complete all-width ordinary-integer marker-complement equation (3) remains in progress. No independent whole-task acceptance or exact early-hit probability is claimed here.

`Agent9FiniteProducts.lean` has compiled with official Lean 4.19.0 using `--trust=0`. Its companion audit printed transitive axiom reports for every explicitly named export: twelve theorem declarations and three definitions. The reported dependencies stay within the ordinary `propext`, `Classical.choice`, and `Quot.sound` set. The full task will additionally require an exhaustive module-origin audit and an independent complete source-closure rebuild after all mathematical layers are complete.

## Completed reusable results

- `wordChoices` enumerates every fixed-length word over a given finite alphabet. Membership, exact length, and duplicate freedom are proved.
- Generic mapped Cartesian products have exact length and are duplicate-free under the stated injectivity assumptions.
- `appendProduct` concatenates fixed-length blocks without losing the decomposition needed for injectivity.
- `blockChoices` concatenates exactly `J` allowed blocks followed by an allowed suffix. Its length is `blocks.length^J * suffixes.length`, with duplicate freedom under the explicit block-length assumptions.
- `mem_blockChoices` proves complete positional membership: total length, suffix after `J*r`, and every block `(xs.drop (j*r)).take r`. It includes `J=0`.

These results do not yet identify the decimal mirrored-marker predicate or enumerate all canonical integers. Those bridges are the next active proof work.

## Frozen sources and retained attempts

| File | SHA256 |
| --- | --- |
| `Agent9FiniteProducts.lean` | `b4d3b1f4b910438533186b60c0a88e946887aaa47978d730b7eedc5352a10ccf` |
| `Agent9FiniteProductsAudit.lean` | `3c15edb98b24db362ed6dae369911ab423c67dcfb1d10fef7ddd1e7b44a5f919` |

The first two rejected generic attempts, the successful third attempt, and the successful literal audit retain their exact source snapshots, command/status records, and stdout/stderr under `development/Agent9FiniteProducts/` and `development/Agent9FiniteProductsAudit/`. Failed attempts keep their original status. `compile_attempt.py` is the recorded author driver.

`checkpoint-001/MANIFEST.json` records the exact published checkpoint files and their hashes. Later mathematical modules are deliberately outside this frozen checkpoint; they will be preserved in their own subsequent checkpoints. The parent performs publication; the delegated proof author continues implementation without Git writes.

## Intended ordinary-integer endpoint

For `L >= 1`, `r >= 1`, and `J=(L/2-1)/r`, the manuscript requires the exact count

```text
9 * 10^(L-1-2*r*J) * (10^(2*r)-1)^J
```

of all positive canonical width-`L` integers with none of the selected disjoint mirrored all-nine blocks. Each entire `r`-pair block excludes one filling, giving `10^(2*r)-1` possibilities. The count must retain the nonzero leading digit, trailing zeros, odd center, and zero-block boundary. The finite positive-time early-hit upper bound will reuse the existing `FiniteHorizonBlocks.mirroredNines_safe_prefix` theorem.

The written source is `proofs/contributions/2026-10-14-finite-horizon-density/README.md`, equation (3), original commit `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`, blob `6d6d188df78e26eb6ffdde6ebc3bdb6fc749eb9c`; its exact bytes are preserved under `checkpoint-001/source/`. This is formalization of an existing written proof. Real probabilities, analytic limits, time-zero/intersection refinements, and infinite-survivor conclusions remain outside this claim.

The coordination claim is `5d54351a6cf3375351f2cf985e9ef40854a0dd8c`, task blob `3c888868a9fb2312f79a77db665533fdb11e520d`. The isolated source branch starts at main `f44c06c4851b26523bcec920d93a52b93fd2a0a6`. No main integration slot is claimed.
