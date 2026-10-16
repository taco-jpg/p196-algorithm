# Dead-prefix proof evidence

The module proves `P196.Agent3.ThreeLayer.no_three_paths_dead_prefix` with the original Agent #9 `Path` predicate. The target half is `[14,14,14,5] ++ tail`; the tail is an arbitrary list of symbols, the first two ancestors are arbitrary symbol lists, and the third ancestor is an arbitrary natural-coefficient list.

The first inverse layer is forced to start `[7,7,7,2]`. The second is forced to start `[3,13,13,0]`. In the third inverse layer, the first three coefficients are forced to be `[1,16,16]`, ending in state `2`; the next target coefficient is `0`, for which there is no `Local` transition from that state. Every finite arithmetic row is checked using kernel `decide`. The proof peels the original complete paths and does not rely on a separate automaton model or the historical generator.

## Actual verification

Lean 4.19.0 ran with `--trust=0` against the unchanged pinned `InverseFibers` and `PathCounts` objects in `agent3-history-build`. This is a check of the new module and every explicit declaration's axiom set, not an independent rebuild of those dependency objects.

- Attempt 001 genuinely failed: `Decidable (Forced ...)` was not inferred before unfolding the definition. Its exact source, command, source hash, exit code, and raw error log are retained.
- Attempt 002 passed after adding `unfold Forced` to the nine finite forced-row proofs. No arithmetic statement or path interface changed.
- All 15 explicit declarations were audited. `Forced` and the two path-peeling helpers have no axioms; the remaining declarations, including the endpoint, depend only on `propext`.
- The successful source SHA-256 is `09c01111e2eb2f57637fe7d3a04e45aca4ca3d20c0248dc349e956c6ffc1fc64`.
- `verification.json` contains complete commands, hashes, exit codes, timings, dependency identities, and parsed axiom reports. `axiom-audit.log` is the unedited Lean output.

Run a fresh attempt with `python3 development/dead-prefix/verify_dead_prefix.py N`, using a new positive integer for `N`. The driver refuses to overwrite an existing source snapshot. Lean execution requires the workspace's established escalation authorization. The generated `build/DeadPrefix.olean` is a reproducible local artifact and should not be committed.

## Exact inherited source pins

Both original modules come from Agent #9 source commit `7be455c03d777e5e0ca1d44bea4d1330e3f764c7`, with published verification commit `98588ccf7e93d7ab9ed0e0c2f436f85f20a734d5`.

| Module | Git blob | SHA-256 |
| --- | --- | --- |
| `InverseFibers.lean` | `cade8ace6359fe8246a29ec781859e3a39b00e11` | `64f4fa5df54d9365b1b3706eceeab3d3f358eb1040a95e3057ac4d9f82806b70` |
| `PathCounts.lean` | `fac4c4090cf63c2ecdeb5791e6af8758a0821616` | `588890faa1a29739b00dbe660a5f39971ac5087d997550cb9a740194eb592a33` |

## Historical evidence and scope

The three files under `source-preservation/` are the original checkpoint, generator, and saved graph results from archive snapshot `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`. Their exact SHA-256 and Git blob identities are checked by `preserve_original_sources.py` and recorded in `source_identity.json`; this preservation does not rerun the generator.

The Lean result rules out three zero-boundary inverse paths for this prefix and every suffix. Transport to actual mirrored words is a separate module. The result makes no claim about mixed-overflow histories, all possible three-step histories, or infinite safety. It does not certify the entire 64-state historical graph or a contraction bound.
