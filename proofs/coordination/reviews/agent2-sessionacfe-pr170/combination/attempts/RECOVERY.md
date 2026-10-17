# Historical operational helper source recovery

## Finding

Before this sealing addendum, complete separate source files for attempts001–004 had **not** been saved. The directory contained the final `check_combination.py`, historical failure reports/logs, and the successful attempt003 log. The helper was edited in place between some executions.

All four historical source versions can now be recovered exactly from the visible original tool record: the complete initial `apply_patch` creation and every subsequent successful update are available in this specialist's conversation. No code is inferred from a failure message or guessed from intended behavior. The unchanged final file is anchored to the SHA256 already recorded in the original `SHA256SUMS.json`.

The recovered complete files, exact before/after patch blocks, hashes, byte counts, execution references, and surviving result/log bindings are now preserved under `attempts/`. These are retrospective reconstructions from recorded edits, not falsely labeled contemporaneous source snapshots.

## Complete recovered versions

| Actual execution | Complete recovered file | Bytes | SHA256 |
| --- | --- | ---: | --- |
| attempt001 | `attempt001-check_combination.py` | 14735 | `a43533a54e3ced9a520528ea17627c315dddeeefee73d4c31fc4b74d5cb56664` |
| attempt002 | `attempt002-check_combination.py` | 14735 | `a43533a54e3ced9a520528ea17627c315dddeeefee73d4c31fc4b74d5cb56664` |
| attempt003 | `attempt003-check_combination.py` | 14946 | `1e64a73c6aadcbf927cce2ff6933e4443b657b489e8ad3ffa9dffab6be58f313` |
| attempt004 | `attempt004-check_combination.py` | 15675 | `2d763c83c458062e500c019304626d83c2ec4c3c6b01f4fc9423bc83726f06c1` |
| Final successful execution | `final-check_combination.py` | 16589 | `30c59bd5dcff0ec14e462affb62e73ff92d3275b72bf781e41a533ddb9b62fb4` |

Attempts001 and002 used identical code. Between those runs, only the accidentally appended newline in the downloaded package input was removed after matching the authoritative Git blob. The helper itself was not changed.

Three exact source transitions occurred afterward:

1. **T1, before attempt003:** replace the incorrect all-mode100644 assertion with preservation of ordinary `100644` and `100755` file modes, and record the actual executable-path inventory. Attempt003 then passed 210 checks.
2. **T2, before attempt004:** add explicit accumulated-parent graph checks and the actual canonical verifier identity check. The resulting execution failed because the new single-best-common-ancestor assumption did not hold for PR168. This run originally wrote `check-final.log`; its output and result were subsequently preserved as attempt004 artifacts.
3. **T3, after attempt004:** explicitly handle PR168's two best common ancestors and record the effective ancestor tree. The final execution passed 226 checks.

The precise original edit blocks are retained in `MANIFEST.json` and as literal strings in `reconstruct_versions.py`. Recovery reverses T3, T2, and T1 from the sealed final bytes, then forward-applies those same literal replacements as data. Every replacement requires exactly one matching occurrence. The forward result equals the previously sealed final file byte for byte. This checks the reconstruction chain; it does not rerun the operational checker.

## Source provenance and actual execution references

The source basis is the original successful `tools.apply_patch` call that created the full helper and the three original successful update calls transcribed above. The execution associations are separately supported by the visible original command invocations and their actual completion results:

| Execution | Original tool evidence | Actual exit | Surviving output |
| --- | --- | ---: | --- |
| attempt001 | `exec_command` completion chunk `3efc76` | 1 | `check-attempt001.log`, `COMBINATION_CHECK-attempt001.json` |
| attempt002 | session `77846`, completion chunk `971ac8` | 1 | `check-attempt002.log`, `COMBINATION_CHECK-attempt002.json` |
| attempt003 | session `83282`, completion chunk `19c0e2` | 0 | `check-attempt003.log` |
| attempt004 | session `44776`, completion chunk `3e958a` | 1 | `check-attempt004.log`, `COMBINATION_CHECK-attempt004.json` |
| Final | session `1094`, completion chunk `6257fd` | 0 | `check-final.log`, `COMBINATION_CHECK.json` |

These are tool execution references, not Git commit IDs, GitHub review IDs, or additional executions. The manifest also records each surviving log/result's SHA256 and each recovered script's Git blob hash as a content digest; calculating that digest does not create a Git object.

## Explicit unknowns and scope

**Contemporaneous independent run-to-script hash attestation: UNKNOWN.** The original executions did not separately hash their running source or preserve per-run source files. Exact historical code is recoverable from the complete recorded edit sequence, but no newly computed hash is misrepresented as one recorded at original execution time.

**Original full attempt003 result JSON: UNKNOWN / not separately retained.** Its successful original log remains, but the shared `COMBINATION_CHECK.json` was overwritten by the later run before a separate attempt003 copy was saved. No full historical JSON, timestamps, or command-output record has been invented. Attempts001,002,004 are the failed runs with separately retained JSON; attempt003 was successful.

The recovered versions are solely an **operational data-validation helper** for immutable Git trees, source identities, archive input identities, and prospective combination applicability. They contain no mathematical proof source and did not run Lean. Their initial diagnostic failures were helper assumptions/input materialization issues, not failed Lean proofs.

This addendum executed only the new reconstruction utility, which reads and writes ordinary files and calculates hashes. It did not import or execute any recovered helper, rerun any previous check, invoke Git, access the network, mutate source/history, or alter any original file or log. The utility recorded hashes of original top-level files before recovery and confirmed they remained unchanged. The original `REPORT.md`, final checker, final check report, original manifests, and all original logs remain intact.
