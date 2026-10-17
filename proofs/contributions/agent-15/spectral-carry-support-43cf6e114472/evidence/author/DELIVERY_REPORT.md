# Author evidence delivery

The complete author/checker evidence snapshot is packaged as `author-evidence.tar.gz`. Every member is listed with its exact source-relative path, archive path, byte count, SHA256, and file mode in `author-evidence.manifest.json`.

- Archive bytes: 394386.
- Archive SHA256: `d98b44f9c8a8c8faa5d9401fb6767e1587e51a22ea23d795f1a12364803e8dcd`.
- Archive members: 152 regular files.
- Total uncompressed member bytes: 1452352.
- Manifest SHA256: `53cf8b942233fe4df3da79d1f99c5d70cec29f6b2f7eb433ee8dbcbaa5d9fc86`.
- Regenerable Lean objects omitted: 16 files, totaling 33634720 bytes.

Each omitted .olean/.ilean is individually enumerated with its complete relative path, byte count, SHA256, and reason. The entire delivery subtree is excluded to prevent recursive packaging. No other evidence files are omitted. All source attempts, failed and successful compile/audit logs, exact commands, reports, canonical checker provenance, runtime inventories, and canonical run sources and output streams are included.

The archive was reopened and every extracted member stream was rehashed against the exact manifest. All included and omitted originals remain present locally with identical bytes. The frozen mathematical source, checker, and build configuration were not changed. No archive member is an absolute path, parent traversal, symlink, or device.

`author-evidence.sha256` records both the archive and manifest hashes. This packaging step is evidence delivery, not a new independent proof review or acceptance claim.
