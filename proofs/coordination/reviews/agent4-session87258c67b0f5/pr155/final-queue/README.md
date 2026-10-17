# Campaign final revisit — lossless publication package

## Scope and exact archive identity

This package preserves **every one of the 70 regular files** under the closed source root:

`/workspace/scratch/87258c67b0f5/campaign-final-revisit/`

Their total size is **1,002,741 bytes**. No source file, original evidence, report, manifest, task record, comment body or inspection result was excluded. The source tree's bytes and original modes were unchanged by packaging. Freeze means a closed writer scope bound to the exact inventory in SOURCE_MANIFEST.json, with full before/after comparisons; source filesystem permissions were deliberately preserved.

| Item | Exact value |
|---|---|
| Archive | `campaign-final-revisit.tar.xz` |
| Compressed bytes | 158,468 |
| SHA256 | `a6340dba576b153f09c0e9e5dfa90526dfec3f9b825b08688a33d087dc638adb` |
| Git blob SHA1 | `22802173facfb8b433af05cee7413bfee6df4d68` |
| Source manifest SHA256 | `0b532919e03aadd51d1490af1a51163b98679799d9d867caa6d1e570a8f2ada0` |
| Archive members | 71: embedded source manifest plus all 70 source files |
| Uncompressed tar bytes | 1,095,680 |
| Compression | One LZMA2 compressor, one thread, preset 6, 16 MiB dictionary, CRC64 |
| Virtual-address-space limit | 1,073,741,824 bytes (1 GiB), enforced with RLIMIT_AS |
| Base64 pieces | One |
| Base64 payload characters | 211,292 |
| PAYLOAD.b64 file bytes | 211,293, including one terminal newline |
| Requested transport bound | Strictly below 524,288 characters/bytes |

SOURCE_MANIFEST.json records each original absolute path, relative archive path, original mode, byte count and SHA256. The same exact manifest is the first archive member, named PACKAGE_SOURCE_MANIFEST.json. The other 70 members retain the root prefix `campaign-final-revisit/`.

The compressed stream inspection actually reports one stream, one block, CRC64, and `--lzma2=dict=16MiB`. Full output and command/exit status are preserved in XZ_INSPECTION.*. The deterministic representation uses sorted relative paths, fixed JSON encoding/key order, zero tar timestamps/UIDs/GIDs, empty owner names, original modes and fixed compression parameters. No second compression run was performed.

## Safe recovery from the publication transport

Place these files in a new local directory:

- PAYLOAD.b64
- ARCHIVE_METADATA.json
- SOURCE_MANIFEST.json
- decode_payload.py
- recover_archive.py

First verify the published package metadata against the exact archive hash above through the trusted publication reference. Never substitute an unknown archive or treat a matching filename as identity.

Use a destination archive filename and recovery directory that **do not already exist**:

```sh
python decode_payload.py PAYLOAD.b64 ARCHIVE_METADATA.json recovered-campaign-final-revisit.tar.xz
python recover_archive.py recovered-campaign-final-revisit.tar.xz ARCHIVE_METADATA.json recovered-campaign-final-revisit > recovery-receipt.json
```

The decoder validates strict base64 plus the exact decoded size, SHA256 and Git blob before writing a new file with exclusive creation. The recovery program verifies that identity again, checks the embedded source-manifest identity, rejects nonregular entries, links, duplicate/unexpected paths and path escapes, refuses an existing destination, restores each original mode and checks every member's bytes and SHA256. It consumes the complete XZ stream for its integrity check. Both programs apply the 1 GiB address-space limit. Neither program invokes Git, network requests, Lean or repository scripts.

On success, original evidence is recovered under:

`recovered-campaign-final-revisit/campaign-final-revisit/`

The checked manifest is also recovered at:

`recovered-campaign-final-revisit/PACKAGE_SOURCE_MANIFEST.json`

Do not use unguarded tar extraction into an existing working tree. If a run fails, retain its output, partial destination and logs; correct the cause and choose a different new destination rather than deleting evidence or overwriting files.

## Recovery actually performed

The package builder completed at 2026-10-17T06:29:37.364765+00:00 with exit code 0. Its exact command, elapsed time, stdout and stderr are retained. Stderr was empty; no packaging or recovery failure occurred. Earlier evidence and historical failure records remain inside the source archive without reinterpretation.

The complete recovery to the local `recovered/` directory passed:

- Exact compressed size, SHA256 and Git blob.
- Exact manifest identity and the full set of 71 members.
- Original size, mode and SHA256 for all 70 source files.
- Direct byte-for-byte comparison of every recovered source file against its original.
- Complete base64 decode round trip.
- Source inventory unchanged after compression and recovery.
- Complete XZ decompression and CRC64 integrity validation.

RECOVERY_VERIFICATION.json retains all 70 per-file recovery results. The recovered tree is an exact local verification copy of the archived bytes, not additional distinct evidence requiring a second archive.

## Publication inventory and preservation

Publish the single PAYLOAD.b64 transport plus every small top-level technical file listed for publication in PUBLICATION_INVENTORY.json, including the manifests, recovery tools, builder, complete logs, receipts and this README. PUBLICATION_INVENTORY.json itself is included in that publication set; its own identity is supplied separately with the handoff because a manifest cannot contain its own final hash.

The local binary XZ is the authoritative compressed representation. The one base64 payload decodes to its exact bytes; publishing both is optional transport duplication, not additional evidence. No content is omitted when the complete base64 piece is published. The local `recovered/` copy is retained and may be checked again without being separately uploaded.

build_package.py is the preserved exact executed producer, tied to the source root and this output root. It refuses overwriting its outputs. Reproduction should use a new explicitly chosen output location, preserve its logs and keep the already published original intact. Reproducing identical compression was not a verification gate and was not performed.

This preservation task claims no PR or main ownership and performed no remote mutations, mathematical review or Lean execution.
