# Agent #1 whole-period center stripping: author evidence

Author: Agent #1 specialist `cap4_existing_theorems`. Root Agent #1 is the sole
Git writer. Claim `9f5d29396d3f1c379c504572c2f7189a6a96b729`; proposal:
<https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6225218046>.
Base guard publication: `95a17ceeaba51b7d2c14645401df5159a3d483d1`.

Final source: `proofs/Agent1PeriodicCenterStrip.lean`.

- SHA-256: `566c7c5eac1fa54b98a9150a21f7ac61c403d8b0391b7aa92c1dbdea51c300c3`
- Git blob: `bfcfd913cfd7b4063c9b632f2b0461aafd9ca437`

## Executable operation and exact contract

All source exports are in `Agent1.Periodic`. For arbitrary natural-number
words, `stripPeriodCenter w H` returns `(remaining, count)`. Each successful
iteration removes a complete prefix `w` and complete suffix `w.reverse`, then
increments `count` once. Empty `w` explicitly returns `(H, 0)`.

The executable equality test reconstructs the input from `w`, the extracted
middle, and `w.reverse`. `stripPeriodCenter_test_iff` proves that it is exactly
equivalent to the original loop's three simultaneous tests:

1. `2 * w.length <= H.length`;
2. `H.take w.length = w`;
3. `H.drop (H.length - w.length) = w.reverse`.

Thus overlapping matching ends that are too short to remove are rejected.
The test does not reverse the remaining center or alter coefficient order.

`stripPeriodCenterAux` uses structural recursion on fuel. A successful
removal strictly decreases input length for nonempty `w`, proved by
`stripPeriodMiddle_length_lt`. `stripPeriodCenterAux_maximal` proves stopping
maximality for **every fuel at least the input length**. The zero-fuel case is
covered because its length premise forces an empty input. The public function
uses exactly the original input length, so its maximality does not assume an
unproved finite cutoff.

The main public specifications are:

```lean
stripPeriodCenter_decomposition (w H : Word) :
  H = pow w (stripPeriodCenter w H).2 ++ (stripPeriodCenter w H).1 ++
    pow w.reverse (stripPeriodCenter w H).2

stripPeriodCenter_maximal (w H : Word) (hw : w ≠ []) :
  ¬ ∃ K, (stripPeriodCenter w H).1 = w ++ K ++ w.reverse

stripPeriodCenter_length (w H : Word) :
  H.length = 2 * ((stripPeriodCenter w H).2 * w.length) +
    (stripPeriodCenter w H).1.length
```

Additional exports prove remaining length cannot increase, preserve any supplied
coefficient bound, and preserve center reversal symmetry. Those three results
also cover the explicit empty-period convention. Maximality alone requires
`w ≠ []`; actual period-four applications supply this from their length.

The module imports the existing `Agent1PeriodicGuard` only for the unchanged
word/power infrastructure, including `pow_succ_right` and `pow_reverse`. It
does not duplicate the power definitions. These are finite list statements;
they assert no full output validity, canonical ordinary integer, safety,
return cycle, or infinite orbit.

## Verification and retained failures

All development attempts used Lean 4.19.0 / commit `6caaee842e94`, `--trust=0`,
`-j1`, and `-DElab.async=false`. Source snapshots, complete compiler logs, and
receipts are retained for each attempt:

- `attempt-001`: failed because unrestricted simplification reassociated the
  append expression inside a negative branch test. The exact source/log are
  preserved. The repaired proof uses an explicit `if_neg` rewrite.
- `attempt-002`: the executable function, reconstruction, termination measure,
  sufficient-fuel maximality, and length specifications compiled successfully.
- `attempt-003`: the added exact original-test equivalence left one
  definitionally equal extracted-middle goal open; symmetry and boundedness
  already compiled. This exact failed source/log are preserved.
- `attempt-004`: an explicit `rfl` closes that goal; the complete final source
  compiles. All 15 explicit public declarations have literal axiom prints.

Failed compiler logs may contain Lean diagnostic `sorryAx` for unfinished
proofs. There is no explicit `sorry`/`admit` in those sources, and no `sorryAx`
occurs in the successful final audit. Initial development attempts explicitly
reused prior parent objects after checking byte-identical dependency sources;
that reuse is recorded in `attempt-001/receipt.json`.

`clean-001` is the subsequent **fresh author replay**: eleven project modules
were copied from their pinned sources and compiled in an initially absent
build directory, with no project object reuse. All eleven compiler commands
and the separate control-module command exited zero. The complete 15-export
inventory comprises three definitions and twelve theorems; all were audited.
The final source's axiom union is only `propext` and `Quot.sound`. Source hashes
were checked before and after compilation, with no drift.

`CenterControls.lean` adds six separate kernel-checked, axiom-free controls:
empty period, empty center, two removals of a non-symmetric period, overlapping
short ends, an unreversed suffix, and complete removal leaving an empty center.
These check the executable corner cases; the quantified specifications supply
the general proof.

This is author evidence, not an independent review or repository-wide audit.
Compiled objects remain only in the temporary build directory. Root's final
combined clean audit/review is separate.

## Reproduction

Choose nonexistent build and evidence output directories, then run from the
repository root:

```sh
python3 proofs/contributions/agent-1/periodic-block-strip-20261016/center-author/replay.py \
  --source-root "$PWD" \
  --build-dir /tmp/agent1-center-strip-replay \
  --evidence-dir /tmp/agent1-center-strip-replay-evidence \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean
```

The replay pins the existing guard dependency registry, every selected source,
the final center-strip source, and the official compiler hash. It builds in a
fresh isolated `LEAN_PATH`, checks every new explicit export's axiom output,
checks the six semantic controls, and rejects source drift. `clean-001` retains
the actual compiler version, commands, source pins, complete logs, and final
verification result.
