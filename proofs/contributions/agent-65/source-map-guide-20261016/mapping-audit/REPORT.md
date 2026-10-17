# A65-DOC-002: complete pinned source-map metadata audit

## Verdict and scope

**PASS.** The audit executed once and returned exit code **0**, with **0 issues** and empty stderr. All **9,161** source-map keys exactly equal the complete original baseline path set. For every entry, the recorded mode and Git object ID match the original baseline, and the effective selected path exists in the pinned migrated snapshot with that same mode and Git object ID.

This is a complete **Git metadata audit of the pinned map**, not a full SHA-256 audit of mapped file contents, full original-layout reconstruction, wrapper run, mathematical verification, or Lean compilation. No `LEAN_CHECKED` status is asserted. Git object identity establishes identity within the Git representation; the audit did not expand or independently hash all mapped source blobs.

The checked sources are immutable pins:

- Repository: `taco-jpg/p196-algorithm`.
- Migrated snapshot: [`ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3`](https://github.com/taco-jpg/p196-algorithm/commit/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3).
- Original baseline: [`2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`](https://github.com/taco-jpg/p196-algorithm/commit/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5).
- Map: [`proofs/SOURCE_MAP.json`](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/SOURCE_MAP.json), read from its pinned Git blob, not from an uncommitted working file.

The audit uses these explicit commit IDs; a change to local `HEAD` does not change the checked source scope.

## Complete results

| Check | Result |
|---|---:|
| Complete baseline tree entries | 9,161 |
| Complete migrated snapshot tree entries | 19,225 |
| Source-map entries | 9,161 |
| Baseline paths missing from the map | 0 |
| Map paths absent from the baseline | 0 |
| Recorded mode/OID equal baseline mode/OID | 9,161 / 9,161 |
| Effective selected mode/OID equal map mode/OID | 9,161 / 9,161 |
| Effective selected complete metadata equal baseline metadata | 9,161 / 9,161 |
| Unique effective selected paths | 9,161 |
| Selected-path collision groups | 0 |
| Valid per-entry SHA-256 field syntax | 9,161 / 9,161 |
| Total issues, including input/type/duplicate/path/identity checks | 0 |

The complete structured outcome is [run-001/result.json](run-001/result.json). Its `issues` array is empty; there are no hidden, truncated, or omitted mismatch records.

### Selection and exceptional cases

The selection rule matches the wrapper's effective rule: select `current` when truthy, otherwise select `preserved`.

| Selection source | Entries |
|---|---:|
| `current` | 2,565 |
| `preserved` | 6,596 |
| `current` is null | 6,596 |
| Empty-string `current` fallback | 0 |
| `current` equals `preserved` | 0 |
| Repeated effective selected paths | 0 |

Every effective selection was checked. A separate `preserved` path that is not selected was checked for field type and canonical relative-path syntax; its existence, metadata, and contents were not independently audited. This does not assert that both selection alternatives were verified for each entry.

| Git mode | Baseline and map entries | Migrated snapshot entries |
|---|---:|---:|
| `100644` regular non-executable file | 9,152 | 19,210 |
| `100755` executable file | 9 | 15 |
| `120000` symbolic link | 0 | 0 |
| `160000` gitlink | 0 | 0 |

No symlink or gitlink entry occurs in either complete tree. The script handles those Git modes explicitly and would retain every such original/selected identity as an exceptional-case record. There was no symlink instance to exercise in this pinned audit; no synthetic fixture run is claimed. The script does not follow or read symlink targets.

The JSON decoder retains object pairs until duplicate-key detection finishes, so duplicate object members cannot disappear silently through ordinary dictionary decoding. No duplicate JSON keys, duplicate tree paths, malformed entry types, unsafe/noncanonical paths, invalid modes/OIDs, or malformed digest fields were reported. Repeated effective selected paths would be retained and would not be treated as a defect merely for sharing: the per-original identity comparisons determine consistency. There were none here.

Five entries have paired `english_current` and `english_sha256` fields, together with `english_note`. Their types, path syntax, field pairing, and digest syntax were checked. These presentation fields do not participate in replay selection. Their target existence and bytes were not checked. No unknown top-level or entry fields occur in this map.

## Reproduction and execution evidence

The exact executed script is [audit_mapping_metadata.py](audit_mapping_metadata.py), using only the Python standard library and Git. It never invokes a wrapper, package checker, build, solver, or download. Its only source-blob read is the pinned source-map JSON; mapped source files are compared through tree metadata.

From the repository root, reproduce into a **new** evidence directory:

```sh
GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 \
python3 -B proofs/contributions/agent-65/source-map-guide-20261016/mapping-audit/audit_mapping_metadata.py \
  --repo . \
  --output /absolute/new/audit-output-directory
```

This reproduction example was not executed as a separate test. The actual captured argv used the new repository-relative output directory `proofs/contributions/agent-65/source-map-guide-20261016/mapping-audit/run-001`; its exact argv, working directory, timestamps, stream hashes, and exit code are in [execution-receipt.json](execution-receipt.json).

The script independently sets `GIT_NO_LAZY_FETCH=1` and `GIT_OPTIONAL_LOCKS=0` on every Git subprocess, plus `LC_ALL=C` and `LANG=C` for reproducible diagnostic locale. It verifies the repository's Git object format is `sha1`, resolves both explicit commit and tree IDs, reads complete NUL-delimited recursive tree metadata, then reads the pinned map blob. It does not use `HEAD` as the source revision and does not modify repository configuration, the index, or refs.

Recorded execution:

| Field | Value |
|---|---|
| Started UTC | `2026-10-17T00:19:30.068164+00:00` |
| Finished UTC | `2026-10-17T00:19:30.331237+00:00` |
| Exit code | `0` |
| Git version | `git version 2.51.1` |
| Python version | `3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]` |
| Script size | 19,472 bytes |
| Script SHA-256 | `0e9f02c19160435fe9b4f449349b785cf5f9f2c835634a021456711abd41ff00` |
| Original stdout size | 1,638 bytes |
| Original stdout SHA-256 | `cc73e9666f4892930ea812b6e5298ddaecc5c5df29e97a0560a9987c9468da2f` |
| Original stderr size | 0 bytes |
| Original stderr SHA-256 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

[The complete original stdout](audit.stdout.txt) and [complete original stderr](audit.stderr.txt) were written directly from captured subprocess bytes. Neither stream was truncated or reconstructed. [run-001/run-metadata.json](run-001/run-metadata.json) records every Git input command, exact argv, status, stderr, stdout length/hash, source identity, Python/platform information, and script hash. Absolute workspace paths in those raw records are execution provenance, not editorial navigation links.

A preparatory inline schema-inspection expression initially failed to parse because of a missing closing brace; no map read occurred in that failed parse. The corrected read-only schema probe succeeded. [preparation.json](preparation.json) retains that failure's cause and explicitly labeled error excerpt plus the successful schema observation. It does not claim to preserve a complete original stream for the preparatory error. The actual audit script executed successfully once; there was no failed audit result replaced by this PASS.

## Immutable input pins

The metadata input streams are fully determined by the retained Git objects and exact commands. They are identified here and in run metadata by source IDs, exact byte lengths, and SHA-256. Large per-entry success logs and duplicate tree dumps are not produced. The full structured result retains every exceptional case and every issue without truncation.

| Input | Immutable identity | Bytes | SHA-256 |
|---|---|---:|---|
| Source-map blob | `e5f8d27bf09f50f8b9756bf91dff02e992aa4a32` | 4,396,780 | `f6354e0411bc63c014c1ca0db07352a22f76ec6890417c097639a77c9539f8ba` |
| Complete migrated tree input | `6a0fdb7c7165f904e50b5ecec785b89196c622eb` | 3,451,946 | `34d7d7503fcf110bfb79ee702f6e8b83548893d0f9dbf2c07114dfac1af16741` |
| Complete original tree input | `9b7ce2e46a2f89c1cd3baf2cb4afc2d7032546ba` | 1,284,526 | `4adf1b7055ba528cde1a382930a47f2d48bb5a740f7d360df58763f3d262e4dc` |

The map blob SHA-256 was independently recomputed and matched the previously recorded pinned value. Its Git blob OID was also independently recomputed from the Git blob header and JSON bytes. For the tree inputs, SHA-256 hashes identify the exact `git ls-tree -r -z --full-tree <commit>` NUL-delimited byte streams; they are not substitutes for per-file SHA-256 validation.

## Change and evidence boundary

This task created only new files under `proofs/contributions/agent-65/source-map-guide-20261016/mapping-audit/`. Existing guide/source-map/wrapper/source files, prior evidence, generated repository indexes, Git configuration, Git refs, and the PR were not edited by this audit author. The parent independently owns `FIRST_PUBLICATION_RECEIPT.json`; this worker did not write or audit that file and excludes it from the worker's evidence inventory.

The first guide's three read-only command tests were not rerun. No complete replay, mapped-source download, dependency installation, mathematical check, Lean compilation, or GPU operation was attempted. Metadata PASS does not establish local sparse-checkout completeness or new proof validity. Independent non-author review of this new script and its evidence remains a separate step.
