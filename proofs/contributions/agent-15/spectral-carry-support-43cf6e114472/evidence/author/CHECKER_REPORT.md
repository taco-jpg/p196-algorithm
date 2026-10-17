# Canonical checker completion record

Recorded: 2026-10-16T23:45:35.984248+00:00

## Result and role boundary

The delegated canonical checker completed its first actual run with `PASS`, process exit 0, in a newly created output directory. All eight selected mathematical modules were copied from their pinned repository sources and freshly compiled. The initially available project object count was zero. The final audit printed complete declarations and transitive axioms for 22 new exports and 15 critical prerequisites; all 37 axiom reports satisfy the accepted foundational policy.

This is author execution of the canonical driver. It closes the real driver gate and does not replace separate independent source review, independent execution, or the all-origin audit of safe mathematical declarations and generated implementations. The previously frozen mathematical source was not changed during this delegated checker task.

The coordinator explicitly extended this author's owned write scope to `check.py`, `BUILD.json`, `lean-toolchain`, and checker evidence under `development/author/`. The earlier `AUTHOR_REPORT.md` records the preceding mathematical authoring phase. No Git mutation, remote message, README change, CONTRACT change, shared-registry change, or source dependency change was made here.

## Final identities

| File | SHA256 | Git blob |
| --- | --- | --- |
| `check.py` | `b9466cdfd0bf667fe82d9acbf68a15670be294370af5f0366f998615fc78d814` | `ff326ec8517dc270759b53d3e39ba0ecfc23af13` |
| `BUILD.json` | `2b7e1e9527ea69d093ac5dcef32ea10c5c1933f88311f1a4be386867f7de2c3e` | `2d1fb81576f5c21f2acc4f03b9ca71b9be1a6d18` |
| `lean-toolchain` | `55e97be96000b5e9e290c9e74482e5e317861499a5540353ce845471bded8cea` | `7aca1d8a939cc24c413eddd793671cdce7070b74` |
| `ActualCarrySupport.lean` | `4c06522efae7aa254b6281003d042e49f6b60162d01d00881d50052c7a73c646` | `c0e5562e1661570546bced3dca82dd4fb459fa5f` |

The checker, build configuration, and toolchain file are byte-identical to their preserved first attempt. There was no failed checker run or checker-source revision. Mathematical source identity still matches `development/author/attempt-0003/ActualCarrySupport.lean` exactly.

## Original checker provenance

The original checker was read from commit `e8d706dc8a67248e1531b0b828fbe05ff50052ed`, path `proofs/contributions/agent-15/spectral-carry-charge-43cf6e114472/check.py`:

- Git blob: `ea730bac77298967a8be4e103b0de5b40cd2a5a8`.
- SHA256: `f0da79f56ca4c2e24ff90700f3491d4999247f9b88db6cc306074ac84c646ab3`.
- Preserved exact bytes: `provenance/original-check.py`.

The corresponding original BUILD.json and lean-toolchain are also preserved. `provenance/original-records.json` records the exact read-only Git queries, exit codes, hashes, and matches against the existing working copies. Standard error for each provenance query is retained separately.

## What the adaptation verifies

The driver uses an explicit source map with repository-relative paths, SHA256, Git blob, byte count, and expected import list for each of the eight modules. Legacy hashed filenames are copied to the correct Lean module names in the new source directory. The four spectral dependency sources remain fixed at their existing PR145 commit. The actual support source remains fixed at the reviewed final hash above.

The import graph is checked for topological compilation order, exact target reachability, and the sole external import `Std`. The complete selected local closure is `LychrelDigitSums`, `IncomingCarrySensitivity`, `RawSymmetryObstruction`, `SpectralWeights`, `BinaryCode`, `ChargeSymmetry`, `SourceFormula`, and `ActualCarrySupport`. `ChargeControls` is not part of this import closure.

The new public export list is explicit and is checked against the source namespace structure. It retains the question mark in `outgoing_getElem?` and the `Controls` subnamespace. Each of the 22 public declarations is printed with `#print` and `#print axioms`. The same audit covers 15 critical prerequisites: the canonical digit predicate, paired coefficient and carry definitions, coefficient bounds, coefficient symmetry, carry bounds, the existing nonnine division theorem, Binary, carryCharge, charge faithfulness, both exact source-sum bridges, both weight dominance theorems, and binary weighted-code injectivity.

The driver verifies the exact BUILD.json configuration and lean-toolchain contents. It sets LEAN_PATH solely to the new source directory and removes any LEAN_SYSROOT override. Every Lean command, including the version query, uses `--trust=0 -j1 -DElab.async=false`. It requires the official 4.19.0 version string and compiler commit `6caaee842e94`.

Existing output directories are refused. The driver never clears, deletes, or reuses an output directory. It preserves each original source copy and raw stdout/stderr stream, records command arrays and exit codes, and writes a FAIL receipt with a traceback for a failed verification gate. Successful runs also check that original sources, copied sources, the checker configuration, and the installed runtime remained unchanged.

## Runtime identity

The installed official runtime is a pinned external dependency and is not copied or modified.

- Executable SHA256: `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
- Shared library SHA256: `2ab605c74c78f9ba4431a7b5305a4b28a9071d8a826f223eb14fe5530f78e14d`.
- Std.olean SHA256: `7d3771da25b893da62564bf8198487ff28f01af5cbd410be88d493a4921b2bb1`.
- Complete installed object inventory: 1,471 .olean files.
- Inventory SHA256: `3006ed0315f417028aac57869ba6a033fa9fb23c75e5795aa3087d9f5e039b32`.

The inventory stores relative POSIX paths, byte counts, and individual SHA256 hashes in canonical JSON. Its complete encoding is documented in BUILD.json. The initial baseline, the canonical run's before inventory, and its after inventory are preserved. Before and after identities match the configured pins exactly.

## Actual execution evidence

Output directory: `development/author/checker/canonical-run-0001`.

Invocation and full driver stdout/stderr: `development/author/checker/attempt-0001/canonical-driver.*`.

The actual driver process ran for 100.798 seconds. Its ten Lean commands all returned exit 0:

| Command | Exit code | Seconds |
| --- | --- | --- |
| `lean-version` | 0 | 0.042 |
| `LychrelDigitSums` | 0 | 89.034 |
| `IncomingCarrySensitivity` | 0 | 1.648 |
| `RawSymmetryObstruction` | 0 | 3.036 |
| `SpectralWeights` | 0 | 0.471 |
| `BinaryCode` | 0 | 0.376 |
| `ChargeSymmetry` | 0 | 0.413 |
| `SourceFormula` | 0 | 0.978 |
| `ActualCarrySupport` | 0 | 0.847 |
| `PublicAudit` | 0 | 0.946 |

The audit found only `propext`, `Classical.choice`, and `Quot.sound`. `public-and-critical-axioms.json` records all 37 declarations with their exact axiom lists and audit groups. `logs/PublicAudit.stdout` retains the complete printed declarations and axiom output (36,872 bytes); stderr is retained separately.

The final receipt reports `source_unchanged = true`, `runtime_unchanged = true`, and `configuration_unchanged = true`. Its SHA256 is `4361dce65b796f228c4cd8cf8fac8a87df70aec6c9533183749260e4252ef31e`. Source pins, object pins, the full import closure, exports, critical prerequisites, runtime inventories, commands, and individual command output streams are all retained alongside the receipt.

`BUILD.json` is immutable configuration with status `CONFIGURATION_PINNED`. Actual run status lives in each output directory's `verification.json`, so no post-run manifest edit is needed to claim a PASS against the exact checked configuration. The concrete canonical command remains:

```text
python3 check.py --lean /absolute/path/to/lean-4.19.0/bin/lean --output /absolute/new/directory
```

Publication and independent acceptance state remain with the coordinator.
