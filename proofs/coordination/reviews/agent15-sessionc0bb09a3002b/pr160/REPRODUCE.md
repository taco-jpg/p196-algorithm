# Reproducing the scoped PR160 checks

The archive preserves the exact executed Python sources and their records. Python 3 and Git are the only dependencies used by the delivery tree/selection check; no Lean execution is involved.

Extract the archive without overwriting an existing working directory:

```sh
mkdir pr160-delivery-evidence
tar -xJf pr160-delivery-evidence.tar.xz -C pr160-delivery-evidence
```

Use `ARCHIVE.json` to verify each extracted relative path, byte count and SHA-256. It also identifies the compressed file bytes and Git blob. The archive deliberately excludes its own external manifest and compressed copy.

`verify_integration.py` records the original run with `REPO` fixed to `/workspace/scratch/c0bb09a3002b/agent15-repo`. That isolated checkout supplied immutable Git commit/tree objects P, B, H and M identified in `DELIVERY_PACKET.md`, and local files restored from H. The other map was fetched exactly from PR164 head `fa2683e489acc7c85e08764450550f7e463041da` into the sibling path `../pr164/source/head/proofs/SOURCE_MAP.json`. It was verified against the Git blob at that same pinned commit before use. The immutable sources remain retrievable from the public repository; they are not replaced by inferred content in this archive.

For another environment, prepare an isolated clone containing those pinned objects, restore H's `proofs/SOURCE_MAP.json` and `proofs/archive/documentation/agent-63/10a173cb635fa8d03e357f454232816fc3e77609/SOURCE_MAP.json`, and fetch PR164's exact map. Adjust only the local `REPO` and `other_map` filesystem locations in a working copy of the preserved script. Run that copy with Python 3. Keep the original executed script and prior outputs intact; new outputs are a separate reproduction.

The review-reuse check is independently reproducible from `review-reuse/check_review_reuse.py` and its retained `retrieved-inputs.json`. Its command records show the immutable sources and original local Git lookup. The failed shallow-parent attempt is retained separately from the successful corrected attempt.

The base, source and test-merge identities are historical pins. Reproduction of this packet does not authorize merging against a newer base without rebinding the combination. A GitHub test-merge commit must never be interpreted as an actual completed merge.
