# PR #153 evidence publication package

This package preserves the frozen substantive contents of `pr153-evidence/`,
`pr153-verifier/`, and `runtime-publication/` for exact source head
`6641b1ea166fcef0e6f9d1fa23afed7b1f6b8a82`, observed base
`74a1c3922eb7af438fe40b23d2105ad07556e3f5`, and combined tree
`6cfa3582ce49216a0fc055f42dba84532a608407`.

## Contents and preservation

`evidence.tar.xz` contains only regular files, under those three directory names.
It includes original incoming sources, the original author development archive,
semantic and evidence reviews, every retained infrastructure history, failed and
successful run records and raw logs, the completed verification report, the
literal-audit continuation, the complete portable reproducer, and runtime
recovery/provenance records.

Only generated `.olean`, `.pyc`, and `__pycache__` infrastructure is excluded.
`PAYLOAD_MANIFEST.json` lists every included file and every excluded file by exact
path, byte count, SHA256, Git blob SHA1, and reason where excluded. Original input
files are not deleted or changed. Excluded compiled outputs can be regenerated;
their existing recorded identities remain part of the retained build evidence.

`ARCHIVE_MANIFEST.json` records archive and Base64 identities, all packaging
artifacts, compression settings, and the frozen-package boundary.
`PACKING_VERIFICATION.json` records complete member verification and Base64
round-trip verification. The archive manifest is explicitly excluded from its
own hash list to avoid a self-reference.

## Verify and recover

Python 3 with its standard library is sufficient to verify this delivered
package. No Lean installation, repository access, or network is needed:

```sh
python pack_evidence.py --verify-only --output .
```

This checks the identities of the packaging artifacts, every archive member's
path, length, SHA256, and Git blob SHA1, deterministic metadata, and the complete
Base64 decoding. It then independently verifies all members of the decoded
archive. A failed check raises an error; no proof result is inferred from
packaging success.

If recovering from the wrapped Base64 representation:

```sh
base64 --decode evidence.tar.xz.b64 > recovered-evidence.tar.xz
```

The decoded archive must match the archive SHA256 and Git blob SHA1 in
`ARCHIVE_MANIFEST.json`. After successful verification, extract into an empty
directory:

```sh
mkdir restored-evidence
tar -xJf evidence.tar.xz -C restored-evidence
```

If only the decoded archive was available, substitute
`recovered-evidence.tar.xz` in that extraction command. No symlinks or special
members are present in the verified archive.

Read `pr153-verifier/VERIFICATION_REPORT.md` for the actual compilation and audit
outcome and its limitations. The portable fresh reproducer is in
`pr153-verifier/audit-continuation/portable/`; its README explains the runtime,
repository, source pins, and invocation. Failed original attempts remain intact
alongside the corrected continuation. The combined-tree report is
`pr153-evidence/combined-tree/COMBINED_TREE_REVIEW.md`.

## Determinism and freeze

The packing script uses lexicographically ordered USTAR regular members, fixed
mode `0644`, uid/gid zero, empty owner names, and modification time zero. XZ uses
LZMA2 preset 6, an 8 MiB dictionary, and CRC64. The packing process has a 256 MiB
address-space limit. Base64 is wrapped at 76 columns with LF endings.

To pack a separate fresh destination from the original frozen inputs:

```sh
python pack_evidence.py --workspace /path/to/containing-workspace --output /path/to/new-package
```

The script refuses to overwrite an existing package and rechecks the complete
source inventory after packing. Identical payload bytes produce identical
archive bytes. On success, the seven packaging artifacts are made read-only.
The directory remains available for the coordinator's separately authored
`INTEGRATION_PACKET.md` and delivery context; those files are outside this
packing script's scope. Packaging performs no Lean execution, remote write,
Ready transition, or merge.
