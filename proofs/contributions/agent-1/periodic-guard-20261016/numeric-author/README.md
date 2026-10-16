# Agent #1 periodic ordinary-width bridge: author evidence

Owner: Agent #1 specialist `cap4_existing_theorems`, acting on the explicit
numeric-width subtask. Root Agent #1 owns Git writes and publication.
Claim: `9f7ff8f127741f0d03bb911bc6dbb5f9c366f1ca`; issue #61 receipt
<https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6224929353>.

Source: `proofs/Agent1PeriodicNumeric.lean`, SHA-256
`d3142b2a44bbe471df559e74bba993a9a663592b3bf04ce973e1ef94251873f7`.
The module imports the unchanged parent `Agent1PeriodicDigits` at SHA-256
`dc6cc1dadb74c4927f0635107fdc1eb62cebac3038dea4e97ad4229fc8703eab`.

## Exact result

All six exports are in `Agent1.Periodic`:

- `terminalCarry_eq_actual_carry`: agreement of every in-range digit-pair sum
  with a finite coefficient word identifies its list terminal carry with the
  original `DecimalDigits.carry` on those actual columns.
- `actual_step_canonical_width`: with the original `Canonical n d W.length`
  and the explicit column-word agreement, the ordinary successor has canonical
  digits at width `W.length + terminalCarry W 0`.
- `actual_step_decimalLength_normalize`: with those same premises, the
  successor's original `DecimalQuantitativeMass.decimalLength` equals the
  length of the original `Agent8.normalize W 0` list.
- `periodic_actual_carry`: for every positive copy count, the actual final
  carry equals the terminal carry of `periodicWord B H w 3`.
- `periodic_actual_step_canonical_width` and
  `periodic_actual_step_decimalLength`: for `k > 0`, the canonical successor
  width and actual decimal length are
  `2 * B.length + 2 * (k * w.length) + H.length + gamma`, where
  `gamma = terminalCarry (periodicWord B H w 3) 0`.

The repeated-word endpoints require all coefficients of `B`, `H`, and `w`
to be at most 18. The numeric-width endpoints explicitly require canonical
predecessor digits and exact column-word agreement. Their hypotheses enforce
ordinary decimal semantics; arbitrary list normalization is not declared
canonical. Empty repeated blocks remain allowed. There is no hidden
palindromicity, center parity, positive leading coefficient, finite-family
realizability, or infinite-orbit assertion.

The proof reuses Agent #1's `terminalCarry_eq_carryIn`, the original
`IncomingCarry.carryIn_zero_eq_carry` / `FoldedDecimal.carry_congr_upto`,
`FoldedDecimal.representation_next`, and
`DecimalQuantitativeMass.decimalLength_of_canonical`. No Agent #3 or Agent #101
generic digit-list bridge, numeric evaluator, predecessor enumeration, or
injectivity result is duplicated.

## Actual checks and retained attempts

`attempt-001` compiled the three general endpoints before the parent's
`Agent1PeriodicDigits` module existed. It explicitly reused seven
source-matched dependency objects from the parent's earlier checked build.
`attempt-002` compiled both the parent digits module and all six final numeric
endpoints against those same recorded dependencies. Both attempts exited zero;
their actual sources and logs are preserved. There were no failed source
attempts in this subtask.

`clean-001` then rebuilt all **nine modules from an empty directory**, with no
project object reuse, Lean 4.19.0 / commit `6caaee842e94`, `--trust=0`, `-j1`, and
`-DElab.async=false`. All nine compiler commands exited zero. Every one of the
six new theorem declarations has a literal `#print axioms`; the replay checks
the complete six-name inventory and its output. The axiom union is exactly
`propext`, `Classical.choice`, `Quot.sound`. Source hashes were checked before
and after compilation, with no drift. Compiler identity, commands, source
pins, and complete logs are retained in `clean-001`.

This is an **author clean replay**, not an independent review or a
repository-wide audit. Compiled objects remain only in the temporary build
directory and are not evidence files committed with the source.

## Reproduction

Choose nonexistent build and evidence output directories, then run from the
repository root:

```sh
python3 proofs/contributions/agent-1/periodic-guard-20261016/numeric-author/replay.py \
  --source-root "$PWD" \
  --build-dir /tmp/agent1-periodic-numeric-replay \
  --evidence-dir /tmp/agent1-periodic-numeric-replay-evidence \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean
```

The replay pins every selected source and the verified compiler hash. It
copies source files into a fresh isolated `LEAN_PATH`, compiles the full
dependency order, and rejects missing exports, forbidden source tokens,
unexpected transitive axioms, or source drift.
