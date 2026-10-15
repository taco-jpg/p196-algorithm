# Prefix bridge build record

Source: `../../HighReturnPrefix.lean`.

Lean 4.19.0, Std only. All dependencies were rebuilt independently into
`/workspace/scratch/b14cfbb70606/agent105-build-prefix`:

1. `LychrelDigitSums.lean`: `base-01.log`, exit 0.
2. `HighReturnRank.lean`: `rank-01.log`, exit 0.
3. `HighCarryReduction.lean`: `reduction-01.log`, exit 0.
4. `HighReturnPrefix.lean`: `prefix-02.log`, exit 0.

The invocation environment was:

```sh
LD_PRELOAD=/workspace/scratch/b14cfbb70606/agent105-runtime/app-path-compat.so
LEAN_PATH=/workspace/scratch/b14cfbb70606/agent105-build-prefix
```

Executable:
`/workspace/scratch/b14cfbb70606/agent105-runtime/lean-4.19.0-linux/bin/lean`.
The preload repairs executable-location discovery in the restricted runtime;
it does not alter Lean source, binary, elaborator, or kernel.

The first source snapshot and its failure log are retained as
`HighReturnPrefix-01.lean` and `prefix-01.log`. The failure was an unavailable
`conv_lhs` tactic in Std; replacing it with `congrArg` produced the successful
second snapshot and build. There are no admitted proofs in the successful
source. Failure output contains Lean's automatically generated `sorryAx`
diagnostics and is not a certified result.

The successful axiom audit reports only `propext`, `Quot.sound`, and (for the
finite-edge result) `Classical.choice`.

## Integration interface

Namespace: `Agent105.HighReturnPrefix`.

- `successor q L = nextColumns (nextColumns q L) (L + 1)`.
- `successor_actual` identifies this with the actual first updated width.
- `first_admissible` proves admissibility of the first image at width `L + 1`.
- `actual_control_lt_two` bounds the actual `carry (nextColumns q L) (L - 2)`.
- `actual_prefix_formulas` establishes the three formulas from Section 3.
- `code_properties` establishes the range below 900 and all three decodings.
- `actual_prefix_edge` assumes the two high words and a zero second final
  carry; it proves the finite `HighReturnRank.next` edge.
- `actual_prefix_rank_decreases` composes that edge with the checked rank.

The no-second-overflow hypothesis is intentionally explicit here; the
neutral-exterior module discharges it from actual return assumptions.
