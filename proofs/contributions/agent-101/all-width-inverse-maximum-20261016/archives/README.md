# Final independent all-width maximum evidence

The final archive was created only after the reviewer froze all evidence at
source/registry commit `0a746261de31531b3ed1dc3d754cd3093753ff56` and supplied
final receipt SHA256
`d0e7aabdbcd8e02c1c99743439bae09504bf82536d60cfff470463312ced1ef5`.
Before packing, all 54 files in the reviewer's frozen review index and all
38 indexed canonical non-object files were checked against that index.

**Packing and validation passed:** 124 regular members, 1,858,429 original
file bytes, in a 311,452-byte archive. One verify-only run and one fresh safe
extraction checked all 124 members against the manifest and their original
bytes. Original sources, logs, and review files remain unchanged.

| Artifact | SHA256 |
|---|---|
| `final-independent.tar.gz` | `9fa2ace5f285fdda99b405d6ce25fae768c88a658c208c86d41f4b44ac6f0f79` |
| `final-independent-manifest.json` | `30de149d3255fde08d431c27bb064ef6ea67015e82038f0c5a4f022f97500252` |
| Unchanged safe verification/extraction helper | `8022d9a0c75bce41048a0fee59a1878f431d52e5f80eeb1d6fce00ce09ba6e76` |

## Preserved scope

| Group | Files |
|---|---:|
| Exact registered original mathematical sources | 17 |
| Original checker, supplementary auditor source, registry, metadata, provenance | 11 |
| Actual canonical module sources and generated ProjectAudit | 18 |
| Complete canonical compiler and ProjectAudit logs | 18 |
| Original canonical verification and FILES reports | 2 |
| All independent-review records, raw audits, scripts, source snapshots, and frozen index | 55 |
| Archiving, verification, and validation script sources | 3 |
| **Total** | **124** |

The 17 canonical `.olean` files are excluded and listed separately in the
manifest; there are no compiler-object members. The original canonical
`FILES.json` is retained verbatim: it contains 37 entries, already excludes
`.olean`, and does not index itself. Later review artifacts have their own
frozen index and archive manifest entries.

Repository files retain their original repository-relative paths. The
external build at
`/workspace/scratch/2a8a87fd78df/agent101-all-width-canonical-review-01`
retains its complete relative hierarchy below this archive's
`final-independent-canonical/` prefix. The manifest records every member's
path, byte count, SHA256, group, and original location. Author attempt trees
remain separately published at `0fcbe9973659f178e9c834c68d45f660241d6fbd`;
they were not repackaged wholesale.

The unchanged final review receipt preserves the one fresh 17-module
canonical build and three subsequent explicit `--trust=0` audits: 1,305
transitive theorems, all 41 new public declarations, and 225 safe definitions
(zero safe opaque declarations). Its original audit sources and full logs
are included. The initial failed Git-object readback is retained; it was an
object-availability precheck failure before any Lean attempt. The receipt's
authorship disclosures and its explanation of two unrelated preserved
README modifications are unchanged. Packaging performs no additional
mathematical verification and does not change these classifications.

## Verify or restore

```bash
python3 /path/to/archives/final-independent-verify.py
python3 /path/to/archives/final-independent-verify.py --extract-to /path/to/restore-root
```

The first command writes nothing. The second validates the full archive
before writing, rejects unsafe paths and links, skips identical existing
files, and refuses to overwrite different files. The helper is an exact
byte-for-byte copy of the previously validated helper; its earlier fault
tests were not repeated. This run's exact commands and outputs are in
`final-independent-pack.log` and `final-independent-validation.log`, with
all 124 original-byte comparisons in `final-independent-validation.json`.
The actual fresh restore directory was
`/tmp/agent101-max-independent-restore-u_690c6q`.

`final-independent-pack.py` records the packaging recipe. Sorted member
names and normalized tar/gzip metadata preserve every payload byte while
removing host timestamps and ownership. Its `--repack-from-root`,
`--manifest`, and `--output-dir` options reproduce the fixed member set from
an extraction and compare the resulting archive hash; no additional repack
test was run. Matching compression behavior is required for identical
compressed bytes.

`PREPARATION.md` and `preparation-001-pack.py` retain the earlier preparation
stage. Before the first actual pack, the recipe was adapted to the final
receipt's observed `published_commit` field and to include the original
supplementary auditor source. There was no failed packing attempt. No Lean
or Git command was run during this archival work.
