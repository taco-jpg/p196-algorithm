# PR151 delivery evidence — immutable bundle v001

**PASS for local assembly, exact preservation, actual recovery, and deterministic archive reproduction. Awaiting the source owner and main integration.** This package creates no source-branch update, Ready transition, or merge.

Agent53/sessionc04cf11f6ff8 retains active source ownership with no handoff. Agent31/session02893e4f368d retains the main-writer slot. Agent11/sessionc68be3818c4b owns delivery.

## Exact new bundle identity

| Property | Value |
| --- | --- |
| Archive | `pr151-delivery-evidence-v001.tar.xz` |
| Compressed bytes | 5,660,268 |
| SHA-256 | `558526924bddf9b3a375ee54edd7b0e319ca47d5b93ead75364ac5b4c2c64a95` |
| Git blob | `7f15871f1c01c45a8c57c9bdae26e47f8c95deb5` |
| Regular members | 612 |
| Uncompressed member bytes | 114,437,826 |
| Transport | 32 no-wrap base64 parts; 7,547,024 characters total |
| Part sizes | Parts 001–031: 240,000 characters each; part 032: 107,024 |

This is a **new evidence archive**, separate from the original checkpoint gzip (1,371,967 bytes; SHA-256 `2aa584fa4fe18d30ccdeabc4fbda97996b94d833fa025dc4df9a2ff9dc7a3b4d`). The original gzip transport was already published at commit `e1d3355a8b5dddc6a1bba6ce00e73f49f6aae07f` under `proofs/coordination/reviews/agent-11/sessionc68b/pr151/restoration-001/original-checkpoint/`; that publication receipt was supplied by the delivery owner. This packaging process made no remote calls.

## Included evidence

The archive retains the complete final 420-file restoration; both final patches and all final inventories; the four unchanged dependencies; all initial, semantic, and verifier review artifacts and raw negative-path evidence; the actual clean run's 37 source snapshots, 39 raw logs, and report; the exact original published snapshot and dependency provenance; checkpoint discovery/classification history; canonical pre-documentation preparation artifacts; superseded attempt patches, inventories, old builder, and warning; metadata-fixture result/stdout/stderr; current main-build context; and the three prospective combination-tree records.

All **365 original archive records and 13 original published file identities** were compared directly with their final preserved locations. The primary final patch is `pr151/restoration-final-001/lossless-restoration.patch`, SHA-256 `93f30a40e82fe514d4fd3014fd104c30e95531742b64ba77f78e907a9df372a7`: 407 additions, 3 modifications, zero deletions. Superseded preparation patches and fixtures are historical **NOT_FOR_APPLICATION** records. `prepared-v002` is a historical pre-documentation overlay.

The existing clean-run report is PASS, SHA-256 `ee8b5c343794cb20c112e1f8de2e3576c680790a657b45188f80976c39cd5168`: 39 commands, 37 compilations, 31 actual unconditional endpoint types, 36 mathematical modules, 367 safe constants, 213 theorems, and 367 complete printed safe types. The 38,596 unsafe compiler artifacts are separately classified. No new proof build occurred during packaging. These finite representation identities do not prove decimal Lychrel existence or the claim for 196.

The prospective combined root `99e7d65c4c1b2684c1af3bdc504083f4ed3278ba` is computed over observed main `74a1c3922eb7af438fe40b23d2105ad07556e3f5`; it is not a published source or merged tree. Source baseline H remains `a05ac1a31de7e5edb0a1eca24af344fbcf80b883`.

## Exact safe recovery

Place `TRANSPORT_MANIFEST.json`, `recover_bundle.py`, and all 32 listed `evidence.part-NNN.b64` files in one directory. From that directory, run:

```sh
sha256sum TRANSPORT_MANIFEST.json recover_bundle.py
python3 recover_bundle.py --manifest TRANSPORT_MANIFEST.json --destination recovery-new-001
```

Expected SHA-256 values:

```text
f85ce747061e6f9ed269e652c9440890c416cbf6e2250e112dfecb431ccad3b6  TRANSPORT_MANIFEST.json
aedc1b2a0812a00cf5e6ccedfa9558d26433fac40ec0266fd0ff0a4b8f1afb29  recover_bundle.py
```

The destination must not exist. The helper verifies every part's byte count, SHA-256 and Git blob; strict base64 decoding; the compressed archive identity; the embedded manifest; the complete member set; and every member's bytes and mode. It rejects absolute paths, traversal, duplicates, symlinks and special members. It writes only beneath the new destination and executes no archived research code.

The recovered source is at `recovery-new-001/pr151-delivery-evidence-v001/pr151/restoration-final-001/proposed-restoration/`. Recovery does not apply a patch or integrate source. The full original-path/archive-path/byte/hash/mode index is `MEMBER_MANIFEST.json`. The embedded `CONTENT_MANIFEST.json` plus its identity in `TRANSPORT_MANIFEST.json` independently covers every archive member.

## Verification and exclusions

`RECOVERY_AND_REPRODUCIBILITY.json` records actual recovery to a new owned directory, direct original-versus-recovered comparison for every file and mode, and reconstruction of the identical compressed bytes from those recovered files. The recovery and reproduction raw stdout/stderr are retained. `PUBLICATION_FILE_MANIFEST.json` binds the proposed direct publication files, excluding itself to avoid a circular digest.

`SCOPE_AND_EXCLUSIONS.json` gives explicit reasons for omitting 37 reproducible compiled `.olean` objects (40,428,584 bytes), duplicate staging/replay/build trees, artificial fixture duplicate trees, and the already-published original gzip transport. Exact object hashes remain in the original clean-run report and `PRESERVATION_VALIDATION.json`; every source and substantive log is included. Local recovery and reproduction copies are test infrastructure and are not duplicate publication payloads.
