# Remaining support evidence: packaging and recovery receipt

**Result: PASS.** A deterministic lossless archive was created and every member was checked through one decompression pass against its original byte count, SHA256 and normalized metadata.

## Package identity

- Archive: remaining-support-evidence.tar.xz
- Compressed bytes: 271236
- Archive SHA256: ca4cec2b37b1a152b72cf49810cb9473babfd3481f8bdb020e46a26e27b6c642
- Regular-file members: 17
- Original payload bytes: 1792733
- Complete manifest: remaining-support-manifest.json
- Manifest SHA256: f8261a00002be4ec17efcd6c0080e87876e1d1b6add79a7f2b5188fde5e4fa1d
- Verification record: remaining-support-verification.json
- Retained packager: package_remaining_support.py
- Packager SHA256: beba4ae401a598fbd4413d3c316e36d44b12a39be6612510915d78e99d6e975a

## Exact inclusion and preservation

Included the single open-queue snapshot; every file in periodic-ownership and successor; and all regular files in agent12-runtime except the named official download. This includes RuntimeSmoke.lean and its compiled .olean, the full runtime-member-checks.json, original commands/receipts/logs, official release metadata, and the original verification script. Command history, initial failures and approved remedies are retained inside runtime-receipt.json.

All original input bytes and permission bits are preserved. Inputs were read only. The archive excludes the installed runtime, any repository clone/cache, the Agent26 archive, other session files and the separately published PR97, PR157 and PR121 directories. Companion manifest/verification/receipt/packager files are external to the archive, preserving exactly the requested member scope.

Members use USTAR, lexical relative-path order, uid/gid zero, empty uname/gname, mtime zero and original mode bits. XZ uses preset9 and CRC64 without wall-clock metadata. Determinism follows from these explicit settings; no optional second build or second decompression was run.

## Historical runtime evidence and limits

The original runtime receipt is dated 2026-10-17T05:04:54.467220+00:00. It records the earlier official Lean4.19.0 comparison of 5,066 members, including 4,605 regular files, version/prefix observations and strict trust0 RuntimeSmoke compilation with an empty axiom list. It explicitly says P196 verification was NOT_RUN. These are preserved historical results, not new execution by this task.

This packaging task invoked no Lean, Lake, original runtime-verifier, P196 proof, PR check, download, workflow or remote mutation. RuntimeSmoke.olean is historical runtime smoke output, not an accepted P196 dependency object.

An initial orchestration call failed JavaScript parsing with SyntaxError: Unexpected token '{' before any file or packager execution. The orchestration was corrected; there was only one executed archive build and one full member-by-member decompression/hash check.

## Excluded official download: exact recovery identity

- Official pinned URL: https://github.com/leanprover/lean4/releases/download/v4.19.0/lean-4.19.0-linux.tar.zst
- Official release page: https://github.com/leanprover/lean4/releases/tag/v4.19.0
- GitHub release ID: 215958880
- GitHub asset ID: 250981932
- Filename: lean-4.19.0-linux.tar.zst
- Recorded bytes: 343842845
- Recorded SHA256: 6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe
- Digest qualification: Locally computed digest of a fresh download from the official pinned HTTPS release. The upstream release API digest is null; this is not a separately published upstream checksum.

The upstream release API digest is null. The recorded SHA256 is the original session's local digest of the fresh fixed-version official HTTPS download; it is not a separately published upstream checksum. The exact recovery provenance is retained in runtime-receipt.json, runtime-archive-check.json and official-release-metadata.json. This excluded download was not read, copied, rehashed, deleted or downloaded again during packaging.

## Recovery instructions (not executed here)

1. Verify this evidence archive's SHA256, inspect member paths and extract only safe relative regular-file members into a new empty recovery directory. Compare every recovered file's bytes, SHA256 and mode against the complete manifest.
2. Recover the excluded official archive from the exact pinned HTTPS URL above through the normally authorized download mechanism. Require exactly 343842845 bytes and the recorded SHA256 before extraction. If either differs, retain the discrepancy and do not treat the result as the original artifact.
3. Inspect official archive paths and links before extracting into a new isolated directory. The preserved verify_runtime_archive.py documents the original complete comparison and historical fixed paths. Inspect/adapt a separate copy if recovery paths differ; never overwrite the original evidence.
4. Retain normal execution restrictions. This package confers no permission changes and no new runtime execution authority. Recovery and smoke commands were not rerun here.

## Complete member inventory

| Path | Bytes | SHA256 |
|---|---:|---|
| agent12-evidence/open-queue-snapshot.json | 13179 | f5ba03cfd7d2a14c81d482a8efd5091256a0bbb259b3ca1d8c8ede9367ff75c6 |
| agent12-evidence/periodic-ownership/FRESHNESS_UPDATE.json | 65567 | d5e923a6e2a0ba9786fe4ee6a99afc515fde3f6e070f017ee0042371712c7179 |
| agent12-evidence/periodic-ownership/FRESHNESS_UPDATE.md | 9860 | 4bce00a0c1f60c7454bd7cb362991652d468ad78f32837b7dadd50770b1e0583 |
| agent12-evidence/periodic-ownership/OWNERSHIP_EVIDENCE.json | 113092 | 0e98430144aa2adad428cd5b8eea8b14d35c3250639faef3f9dea553b6c5ded6 |
| agent12-evidence/periodic-ownership/OWNERSHIP_REPORT.md | 9809 | 2ba45a521ce892e5902a5848a2b974803115877b8444ca82fc5b728f9dfd60bc |
| agent12-evidence/successor/SUCCESSOR_SCOUT_REPORT.md | 11112 | 8cabec80a8d0549e9748f2fb60fa374c1bc0538abdf0c36cab184a974dabf67e |
| agent12-runtime/RuntimeSmoke.lean | 119 | 365b520b668593fad06469809ba8102031109262b72e5c8b4246873a9aded48f |
| agent12-runtime/RuntimeSmoke.olean | 19624 | 820aa0b0d35209dde090f7ae1f2fc81656732fc7d6c31ceb059370692f854599 |
| agent12-runtime/lake-version.log | 49 | dc1f8f58960933047871f7df82c5de73ea0f705617e101b7dd9413a418a2195d |
| agent12-runtime/lean-prefix.log | 40 | abcef5baa4d798f26d4217102091c996045d67ab7168c6c4c40a94132aa33fa4 |
| agent12-runtime/lean-version.log | 78 | 5362a246ce2545424db10a77de8fd4694f4cf8b0170dfd43fa727acf7f7f259b |
| agent12-runtime/official-release-metadata.json | 382 | 19ee914568a229d0db77964beab9401846a225901bb9f88a202c03ec7f6c0a76 |
| agent12-runtime/runtime-archive-check.json | 624 | e584eb7c4796f097983b6a9dfa691ec458e5e2225225ee90f2608055f5530583 |
| agent12-runtime/runtime-member-checks.json | 1540925 | 4c2e1a00d4d00317b8cbe7fbb2d39555de7da091f8b6e8384098560218cc83a4 |
| agent12-runtime/runtime-receipt.json | 5242 | 0be270c93ed2595297318806c6e71b403798ebc156678cc72a41aa2e79451c7e |
| agent12-runtime/smoke.log | 54 | fa51ca4c37906b84ca651bd2b0c34e2d1c9755b632fa8ed4405bc77ee724d2c4 |
| agent12-runtime/verify_runtime_archive.py | 2977 | 3549e97adb8117ab6ff310dd139a9be8f37bdb6ceac7846f6360bd847d2a8dfb |

Paths are relative to the original Agent12 workspace.
