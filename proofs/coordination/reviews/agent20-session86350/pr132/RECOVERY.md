# PR132 Evidence Recovery

This package retains every regular file and directory in the original completed evidence tree, including the original inventory, retrieval metadata, failed history, validation scripts, and raw validation outputs. The readable REPORT.md is an exact copy of the archived original report.

- Original root: /dev/shm/p196-agent20-86350e418736/pr132-evidence
- Files: 289
- Directories: 51
- Original file payload: 4653910 bytes
- Archive: pr132-verification-evidence.tar.gz
- Archive size: 1151309 bytes
- Archive SHA-256: 236b1fb05d910109964fa4316f1f970d166568764ea9a4270ee95411db0c0409
- Archive Git blob SHA-1: 77e9f43a5370608f2a0bdaac9fb07175b1b7a24e
- Report SHA-256: a3a9eb4dde09d6151bca966cd5d6a74576cd60a60ead99039df1de39c8ba9463
- Pinned PR132 head: 43219b02c191325d0263b4ad2fa1f4ebb1470a5c

## Restore and verify

Place PACKAGE_MANIFEST.json, restore_and_verify.py, and the archive in one directory. Use Python 3 and an unused output directory:

    python3 restore_and_verify.py PACKAGE_MANIFEST.json pr132-verification-evidence.tar.gz restored-evidence

The script first checks the compressed archive's exact size and SHA-256, rejects absolute or traversing paths, rejects duplicate entries and special objects, restores every expected file and directory, and verifies the complete path sets plus every restored file's size and SHA-256. A successful run prints RESTORATION PASS.

PACKAGE_MANIFEST.json lists each original absolute path, relative path, byte size, SHA-256, Git blob identity, original mode, and original modification time. The archive normalizes ownership, permissions, and timestamps. Recovery guarantees file content and path equality; it does not reinstate original ownership or timestamps.

The packaging run additionally compared every restored file directly with its original bytes and rechecked that the original tree did not change. Its exact output is retained in package.stdout.log, package.stderr.log, restore.stdout.log, and restore.stderr.log; PACKAGE_VALIDATION.json records the result and command.

## Evidence scope

Fresh Lean execution in this session remains **NOT_RUN**. This operation validates packaging and byte restoration only. The archived existing-evidence report retains its attributed historical compiler logs, theorem-axiom outputs, independent review, failures, and stated limitations. Immutable blob creation does not attach a branch, update a pull request, or merge code. The delivery owner performs any subsequent guarded coordination attachment.

## Independent source index check

After restoration, restored-evidence/EVIDENCE_FILES.json remains the original 288-file index, excluding only itself. The outer package manifest indexes all 289 files, including that original inventory.
