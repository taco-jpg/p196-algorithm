# Frozen follow-up evidence publication package

## Result

**PASS — the complete retained payload was recovered and verified, and every frozen original input remained unchanged.** This is a local publication-ready package. No remote publication, Lean execution, mathematical review, source modification, Git ref update, or main integration was performed by this packaging task.

The package retains three distinct evidence roots, with their original root names in every archive member path:

| Root | Retained files | Original payload bytes |
|---|---:|---:|
| `pr148-replay-evidence/` | 109 | 1,720,070 |
| `pr155-delivery/` | 33 | 573,520 |
| `pr167-evidence/` | 20 | 100,878 |
| **Total** | **162** | **2,394,468** |

All 42 directories are also retained with their permission modes. Every substantive source, receipt, log, failure, report, historical or preliminary PR167 output, and helper inside the frozen roots is included unless it is one of the nine exact exclusions authorized below. No compiler installation or full repository was copied.

## Exact archive and manifest identities

| Artifact | Identity |
|---|---|
| Archive | `followup-evidence.tar.xz` |
| Compressed bytes | **246,792** |
| Archive SHA-256 | `aa7961ee6c937166f55a466849c3612193ba0caf24bea2b0d921a0638ce244de` |
| Archive Git blob | `48935209b0f628e92c16adece8e6c1e9da79839f` |
| Uncompressed tar bytes | 2,590,720 |
| Uncompressed tar SHA-256 | `2e43fdc49332180103d0a31392f4405a6c6e5f09c2533360780a39386127b39c` |
| Manifest | `publication-manifest.json` |
| Manifest SHA-256 | `5a4734702fa9b36c20956d7c2369909df82b373c34647120d0e8dec75790e8c3` |
| Successful verification receipt | `packaging-success.json` |

Git blob identities are computed as SHA-1 of the standard Git blob header (`blob <byte-count>` followed by NUL) and the complete file bytes. No Git object or ref write is needed for this calculation.

The manifest identifies every retained and excluded original file by original absolute path, archive-relative path, byte count, original permission mode, SHA-256, and Git blob. It also records the archive's stored path and compressed identity, original directory layout, exact compression parameters, recovery commands, and transport part identity. Its creation-stage status remains `PACKAGED_PENDING_RECOVERY_RECEIPT`; the subsequently generated `packaging-success.json` supplies the successful full recovery and unchanged-input result without rewriting the earlier manifest.

## The nine authorized exclusions

The original inventory contains 171 regular files totaling 26,040,987 bytes. Exactly nine files totaling 23,646,519 bytes are excluded from this new archive. Every exclusion has its own full identity and explanation in `publication-manifest.json`; there is no suffix-based catch-all exclusion. The original local files remain in place.

1. Five regenerable `.olean` files under `pr148-replay-evidence/canonical-strict-001/agent51-overflow-saturation/source/`: `LychrelDigitSums`, `OverflowDigits`, `OverflowWitness`, `ResidueSums`, and `Saturation`. All corresponding sources, compiler identities, invocation code, substantive execution logs, proof-audit output, and result receipts are included.
2. Three regenerable private Git tree objects under `pr148-replay-evidence/combined-tree/objects/`: `1bf192ed215d829a1726cab8a61dcfdf89a965b1`, `5db569370a28249328208eb7fd1540f31128e7f3`, and `d6a9dcb8406615e10091e4a8b34e6c0196e7858f`. The complete diff, tree identities, preservation manifests, immutable map references, and commands are included.
3. The byte-identical readback copy `pr155-delivery/remote-readback/pr155-evidence.tar.xz`, already published at commit `286545e5717d2cf9de5c94a8066d28b0e55c24ff`, path `proofs/coordination/reviews/agent4-session87258c67b0f5/pr155/evidence/pr155-evidence.tar.xz`. Its local bytes were rehashed and match 8,696,788 bytes, SHA-256 `7074071e389c6f9d70f1ab72cdcb5ca598af48c3e4ffccc58c1484e8e35fb1d7`, Git blob `18b5269920b575977b263eb227cddcdb0c69aadd`. Its existing full remote readback receipt is included unchanged. No new remote request was made.

This follow-up archive therefore complements the previously published PR155 archive; it does not contain another copy of that transport. Its manifest retains the immutable remote locator. Existing references to other evidence retain their original meaning and are not represented as newly recovered corpora.

## Deterministic format and bounded resources

The archive is PAX tar compressed as one XZ/LZMA2 stream with **CRC64** and a **16,777,216-byte dictionary (16 MiB)**. The read-only `xz --robot --list --verbose --verbose` output confirms one stream, one block, CRC64, and `--lzma2=dict=16MiB`; its command and full output are retained.

Members are sorted by path. Original permission modes are preserved; tar uid, gid, and mtime are zero, and owner names are empty. Original timestamps and inode observations are retained in the external manifest and freeze snapshots. Those normalized ownership/time fields are not restored as original filesystem metadata. This normalization does not change file contents, names, directory layout, or permission modes.

Exactly **one compression invocation** was performed with one compressor. The packager and recovery process use a hard **1,073,741,824-byte address-space limit (1 GiB)**. Reported process peak resident set was **70,788 KiB (69.13 MiB)**. The decoder additionally limits liblzma memory to 64 MiB and bounds the complete decompressed tar size against the manifest. The successful packaging-and-recovery invocation took approximately 0.664 seconds. Raw resource observations are retained in the success receipt.

Determinism is specified by the retained code and fixed serialization/compression settings. No second compression or repeat-build comparison was performed, and no alternative compression variant was generated.

## Safe recovery

Requirements: Python 3 on a POSIX system with its standard-library `lzma`, `tarfile`, and `resource` modules. Place the archive, `publication-manifest.json`, and the exact `recover_evidence.py` together. The recovery script SHA-256 is `9cbccd0cdbe28f98fb32e40351b1657dcc2a296e5daf56b84eec2a36e4da90e3`.

From that directory, use a new absolute destination whose parent already exists:

```bash
python3 -B recover_evidence.py --manifest publication-manifest.json --destination /absolute/new/followup-restored
```

For the prepared base64 transport, keep the `parts/` directory beside the manifest:

```bash
python3 -B recover_evidence.py --manifest publication-manifest.json --from-parts --destination /absolute/new/followup-restored
```

The destination must not exist. Recovery creates the three original root names inside it. It also retains a verified intermediate tar and, in parts mode, the reconstructed compressed transport for inspection. It does not run any recovered code.

Before writing payloads, recovery verifies the complete compressed identity, Git blob, XZ CRC64 stream, and complete uncompressed tar digest. It accepts only the exact manifest allowlist, rejects noncanonical or traversing paths, duplicates, links, devices, sparse members and unexpected metadata, and creates files exclusively in the new destination. Every recovered file is rehashed from disk and its permission mode is checked. Directory inventory and modes are also checked. Partial results and traceback records are retained on failure; nothing is deleted.

## Executed verification and transport

The actual successful recovery used the base64 transport and the destination `recovered-from-parts/` in this publication directory. It recovered and verified **all 162 files, all 2,394,468 payload bytes, and all 42 directories**. This also establishes that the reconstructed transport exactly matches the original binary archive.

There is one ASCII base64 part, with no whitespace or JSON wrapper:

| Part | Characters / bytes | SHA-256 |
|---|---:|---|
| `parts/followup-evidence.tar.xz.b64.part-000001.txt` | **329,056** | `16a80cc3e1bb7ca1baed2141c363be8c23af523ae45a7e4077c5f62e960e1c6a` |

Its size is below the 524,288-character limit. It decodes to the complete 246,792-byte archive. The part index, decoded offset, decoded bytes, and encoded/decoded digests are in the manifest.

After recovery, every frozen input was scanned again, including all nine excluded originals. Before and after snapshots match exactly in paths, file contents, byte counts, modes, mtime/ctime observations, inode identities, and directory metadata. Both snapshot files have SHA-256 `cd79a7c6f8a291b44f2ffc844814f7e68370ff7209b215d66c35285b87324653`. Read access time is outside the freeze comparison.

## Retained operational evidence and limits

`PROCEDURE_INSPECTION.json` records inspection and syntax checking before execution. `package_evidence.py`, `recover_evidence.py`, and `run_packaging.py` preserve the exact procedures. `packaging-command.json`, `recovery-command.json`, full stdout/stderr files, snapshots, the successful receipt, and XZ inspection outputs preserve the actual operations. No packaging or recovery attempt failed. Original failed, stopped, preliminary, and superseded research evidence remains unchanged within the payload.

`PUBLICATION_FILES.json` inventories the new publication artifacts with identities. Recovered duplicate transports and payload copies remain locally available under `recovered-from-parts/`; they are operational verification copies of the manifest-listed bytes. Publishing the archive and its evidence files is the coordinator's next operation, not an action performed here.

This package changes no mathematical status. It does not claim a new Lean PASS, a new semantic review, recovery of the missing original PR148 corpus, PR167 delivery ownership, or any main merge. Agent #28 retains delivery responsibility, Agent #51 source responsibility, and Agent #31 main responsibility. All existing evidence labels and attribution are preserved.
