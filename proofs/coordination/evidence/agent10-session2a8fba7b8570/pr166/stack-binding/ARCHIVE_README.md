# Evidence archive and safe extraction

`stack-binding-evidence.tar.xz` is the preferred lossless compressed archive. `stack-binding-evidence.tar.xz.base64` is its text transport representation for publication through a UTF-8 GitHub file endpoint. `ARCHIVE_RECEIPT.json` records both transport hashes and sizes, the inner manifest hash, member count, and uncompressed size. The archive has regular files only, with relative names and no symbolic links, hard links, device files, or absolute paths.

`ARCHIVE_MANIFEST.json` records the exact byte length and SHA256 of every payload file. The manifest itself is included in the archive and separately bound by `ARCHIVE_RECEIPT.json`. Raw responses, reused prerequisite records, the first constructor version, both successful numbered attempts, the portable input packet, and result reports are retained. The earlier gzip transport, its receipt and manifest, the original extraction helper, and its instructions are retained locally. The XZ archive preserves the same original evidence together with the earlier packaging records. No source or evidence was discarded.

Use the supplied `extract_archive.py` with either the binary archive or the base64 transport. Its third argument must be a new directory. It verifies the externally supplied archive receipt, the archive hash, the inner manifest hash, the exact member set, allowed relative paths, regular-file types, lengths, and every member SHA256 before creating the destination and writing files. It refuses an existing destination.

```sh
python extract_archive.py stack-binding-evidence.tar.xz.base64 ARCHIVE_RECEIPT.json stack-binding-reproduction
```

The extraction command does not run the retained scripts. To reproduce the candidate construction after inspection:

```sh
python stack-binding-reproduction/construct_candidates.py --attempt 3
```

Only standard Python is required. The constructor reads `PACKED_INPUTS.json`, creates a new numbered result receipt, and performs no Git, Lean, network, or repository-source execution. It does not mutate the live repository. Attempt003 should reproduce candidate150 `7b3e2b7b53d4fae2068be44dc01069ebce961cf8` and candidate166 `1a4c99d1d85755e38608e54195c2d72199375b75`. These remain prospective conditional trees.

The archive receipt and text transport are outside the compressed archive to avoid self-referential hashes. The manifest excludes itself for the same reason; its separate receipt hash binds it. Keep both the archive transport and receipt when publishing.
