# Constant-eighteen return registry preflight

This directory records source metadata for Agent #1's accepted task
`fcb20cb967483a96aa46261642d748fd32d4f5d6`, against the published foundation
`7f23ce839fcc88acb235b1816c2c57dc12e16a33`. The registry specialist does not
edit mathematical sources, execute Lean, write Git, or publish messages.

The frozen scoped registry is `proofs/Agent1PeriodicEighteenReturn.registry.json`,
project `agent1-periodic-eighteen-return`, with sole root
`Agent1PeriodicEighteenReturn`. It includes the actual import closure and
public declarations of `Agent1PeriodicEighteenBand`, `Agent1PeriodicEighteenTrack`,
`Agent1PeriodicEighteenClock`, and `Agent1PeriodicEighteenReturn` after those
sources and their author receipts were frozen. No source pins or endpoints are
invented in advance. The repository's global accepted registry is unchanged.

## Inherited source check

`run-000` completed with `INHERITED_SOURCE_PREFLIGHT_PASS`. Its exact command,
source pins, helper hash, source-map entry, and prior-registry provenance are
retained in `run-000/report.json` and `run-000/modules.json`.

The actual import closure of `Agent1PeriodicCycleGuard` and `RunAncestry` has
27 modules. Every source matches the published foundation byte for byte;
43 duplicate entries from the three prior registries have identical path,
SHA256, Git blob, and import pins. The executable-source token scan found no
prohibited tokens. This is source metadata validation, not proof execution.

The original logical alias is `RunAncestry`, mapped through `SOURCE_MAP.json`
to `proofs/RunAncestry__5f2702512ad8719e.lean`, SHA256
`6c8041050576a142949376818a2e37997031ce40b99a7908a763396ee702a9eb`,
Git blob `cdabce887a7f2ca952447f01bd99a2fe30855b81`. Its only direct import is
`LychrelDigitSums`. The registry does not introduce a second hashed logical
alias or use the separate extinction development.

## Freeze boundary

`run-001` completed with `SOURCE_PREFLIGHT_PASS_PROVISIONAL` after all four
actual source files appeared. Their import closure contains exactly 31
modules, and their public declarations comprise seven theorems and the
`quotientEighteenTrack` definition. The run retains all four source snapshots
and the provisional registry; its source token scan passed. These snapshots
do not assert that mutable author drafts have compiled.

`run-002 --author-checked` completed with `SOURCE_PREFLIGHT_PASS_AUTHOR_FROZEN`.
The exact registry SHA256 is
`a425319d71d007104942a2a7010d985ef6fd3f82bb645d75cc8913fb73fe1718`.
It records 31 actual modules, seven public theorems, and one public definition.
All 43 duplicate prior pins agree; all 27 inherited sources still match the
published foundation. No forbidden source tokens were found.

`confirm-authors.py` checks the four explicitly confirmed source hashes,
immutable successful snapshots, actual strict compile/audit command exits,
compiler identity, and sealed receipts. The authors' full new-module audits
cover 73 theorem constants, four safe definitions, and eight separately
inventoried generated runtime implementations. Their theorem axiom union is
`propext`, `Classical.choice`, and `Quot.sound`. These are author execution
receipts; neither preflight script executes Lean.

The registry status is `FROZEN_AUTHOR_CHECKED_FRESH_REVIEW_PENDING`. Author
compilation with pinned reused dependency objects remains distinct from the
parent's and reviewer's combined verification. The fresh combined build and
independent interpretation remain pending in this frozen metadata. The
source-only `run-000`, provisional `run-001`, and final `run-002` are retained
separately.

## Replay command

From the worktree root, the existing flattened verifier can use this strict
compiler launcher and a new output directory:

```sh
python3 proofs/verify_project__214bf7673efe116b.py \
  --lean "$PWD/proofs/contributions/agent-1/periodic-eighteen-return-20261017/registry-preflight/lean-trust0.sh" \
  --registry "$PWD/proofs/Agent1PeriodicEighteenReturn.registry.json" \
  --project agent1-periodic-eighteen-return \
  --output /workspace/p196-agent1-session-20261016/periodic-eighteen-return-parent-clean-001
```

This command is documented, not executed by the registry specialist. The
launcher forces `--trust=0 -j1 -DElab.async=false` on the pinned official
compiler. The existing verifier performs its module-origin theorem audit;
the independent reviewer separately checks safe definitions, generated
implementations, and literal public `#print axioms` output.
