# Recovering PR101 execution checkpoint 002

`recover_checkpoint002.py` is an additive recovery helper created after the historical archive was sealed. The helper and this document are deliberately outside that archive. They do not change its original bytes, member manifest, packaging receipt, reports, or historical verification results.

The helper uses only the Python standard library. Verification is its default action. It never invokes Lean, a shell, Git, a generator, or any recovered research script. Python 3.9 or newer is required.

## Files to retain together

Place these files in one directory, preserving their names:

- `recover_checkpoint002.py`
- `PACKAGING_RECEIPT.json`
- `MEMBERS.json`
- `part-000.b64`
- `part-001.b64`
- `part-002.b64`

The binary `pr101-execution-checkpoint-002.tar.xz` is optional: the helper reconstructs the archive in memory from the three base64 parts in the pinned receipt's order. If the binary archive is also present, it must match the reconstructed bytes exactly.

## Verify without extracting

From the directory holding the helper and transport files:

```sh
python3 -B recover_checkpoint002.py
```

The helper also accepts an explicit input directory:

```sh
python3 -B recover_checkpoint002.py --bundle-dir /absolute/path/to/checkpoint-002
```

Successful verification exits 0 and prints a JSON record containing `"status": "VERIFIED"`, `"verified_member_count": 342`, and `"verified_payload_bytes": 16138045`. This mode creates no output files or extraction directory.

Before any extraction is possible, the helper checks:

1. The packaging receipt and member-manifest byte counts and pinned SHA256 hashes.
2. Exactly three base64 parts in receipt order, each part's pinned byte count and SHA256, ASCII encoding, and strict base64 decoding.
3. The reconstructed archive's exact byte count and pinned SHA256.
4. Every archive member's name, regular-file type, uniqueness, size, and SHA256 against all 342 entries of `MEMBERS.json`.
5. The absence of absolute paths, parent traversal, noncanonical paths, symbolic links, hardlinks, special files, duplicate members, and file/directory path collisions.

## Extract into a new directory

Choose a destination that does not exist. Its parent directory must already exist, and neither the destination path nor its ancestors may be symbolic links:

```sh
python3 -B recover_checkpoint002.py --extract-to /absolute/path/to/new-pr101-checkpoint
```

All 342 member hashes are verified **before the destination directory is created**. The helper then copies the already verified regular files with exclusive creation, verifies the written bytes, and checks the complete extracted file inventory. It does not use `tarfile.extractall` or apply archived ownership, executable modes, permissions, or timestamps.

Successful extraction exits 0 and reports `"status": "VERIFIED_AND_EXTRACTED"`, `"all_members_verified_before_any_extraction": true`, and `"all_extracted_bytes_verified": true`. The files appear beneath the new destination's `strict-build/` directory.

An existing destination is rejected; it is never overwritten. Any verification failure exits 1 with `"status": "REJECTED"`. If an operating-system failure occurs during copying, a partially created new destination is retained for inspection; the helper performs no cleanup or deletion.

## Frozen transport pins

These pins are embedded in the recovery helper. They identify the original sealed checkpoint, rather than a newly generated replacement.

| File | Bytes | SHA256 |
| --- | ---: | --- |
| `PACKAGING_RECEIPT.json` | 1,442 | `805e7fc04886ac8b4531c529747b67ca6e071545a21e442492c521d96220f1e0` |
| `MEMBERS.json` | 58,685 | `6ced7e8ba17509fdac798c328c08c515016e4eb3d2ca2cfa1e3c7555d0e382d0` |
| Reconstructed archive | 702,340 | `047b431acab1f452fd67e07cf705acb7c07221002ec496d1d2852cf414a64956` |
| `part-000.b64` | 450,000 | `329ee0f04d03c3f27ee9fd159ab5c7738ddc804b416adeb7053e8be2bc54375f` |
| `part-001.b64` | 450,000 | `489dec9d0df74fa41c7438cdd1b8ce086d591b5973e2f439c4adf980a4b51361` |
| `part-002.b64` | 36,456 | `dbc2bff5c913ea8febea28840080d4d1f8a6fcbf0d4226ac86b66f85f33e1996` |

`RECOVERY_TEST_RECEIPT.json` records the exact helper/document identities and the actual verification, fresh extraction, and focused rejection checks performed after this helper was added. These are recovery checks, not additional mathematical verification.

The previous evidence checkpoint remains immutable at commit `a676d2c8ee41b1e76e9b7c9f98d83936fda18015`, under the delivery owner's `pr101/checkpoint-001/` prefix. After extraction, consult `strict-build/PORTABILITY.md` and `strict-build/EXECUTION_REPORT.md` for historical source/runtime paths, omitted regenerable object identities, and the precise verification scope.
