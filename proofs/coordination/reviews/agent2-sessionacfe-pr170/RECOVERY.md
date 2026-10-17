# Exact evidence recovery

This package retains the complete640-member PR170 delivery archive, including the original569-file source/evidence snapshot and all new qualification records. The xz-compressed tar is930,912 bytes with SHA256 `56a1ea7926f00a4eaba5ed20153ba19e534d2e12b5d6df73d970424594bccf98`. Its uncompressed member payload is14,683,987 bytes. `TRANSPORT.json` binds the seven ordered ASCII base64 parts and the manifest. `ARCHIVE_MANIFEST.json` inventories each original relative path, member path, byte count, SHA256, Git content hash and mode.

Keep `TRANSPORT.json`, `recover_evidence.py`, and every `pr170-delivery-evidence.tar.xz.b64.part001` through `part007` together. After obtaining those exact files from this same immutable publication commit, run:

```sh
python3 recover_evidence.py --package-dir . --output ./recovered-pr170
```

The output must be absent or empty. This standard-library recovery program verifies every encoded part, the complete compressed archive, the original manifest, every regular member's full bytes and mode, and complete coverage. It rejects duplicate paths, nonregular entries, unsafe paths and existing output files. It only recovers data; it does not execute archived research, Git, Lean, a compiler, or a dependency installer. A complete `RECOVERY_RECEIPT.json` is written after successful validation.

The reconstructed `snapshot/` contains all569 original added files, including the100755 strict-launcher mode. A separate portable source-recovery route, already actually executed in this session, reconstructs that same snapshot from the complete original GitHub patches and seven missing raw blobs:

```sh
python3 recovered-pr170/replay_snapshot.py --inputs ./recovered-pr170 --output ./recovered-source
```

That route also validates the exact Git-mode map and source manifest; it runs no recovered code. `metadata/replay-execution.json` and `replay-001/RECOVERED-MANIFEST.json` retain the actual earlier recovery receipt. The complete original source remains independently published at PR170 head `5e67f08231c1973cb4908c167dbd8e08b3ee50fa`.

To inspect the archive manually after verifying the ordered part hashes, concatenate the seven parts in numeric order, base64-decode the concatenation once, and read the resulting xz-compressed tar. No per-part decoding or lossy text conversion is appropriate. Preserve the executable member's mode when extracting. The portable verifier above provides the exact tested path without executing archived code.

The duplicate original and recovered source directories are reproducible. Only the original full snapshot and the distinct recovery manifest are archived. Runtime installations, `.olean` caches, external Git infrastructure and the operational packaging helper are excluded with explicit reasons. New publication and recovery receipts are additional files beside the immutable archive; they are not retroactively inserted into an already hashed archive.
