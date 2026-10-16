# Runtime development evidence archive

`runtime-development.tar.gz` preserves all 102 regular files under the contribution's `normalization/`, `safety/`, and `dependencies/safe-high/` directories. Member names are relative to the repository root. The original file contents total 1,040,000 bytes; the compressed archive is 140,683 bytes. Original local files remain present and unchanged.

Archive SHA-256:

```text
6c1ec4e2aa0084369ad16f8133a24d8148b006dfbdaabab48ce0eb3a8e45a130
```

`manifest.json` records each member's repository-relative path, byte count, and SHA-256, plus the complete archive checksum. It excludes `.olean`, `.ilean`, Python bytecode, and cache directories by policy; none of the 102 source evidence files required exclusion. It also records the unchanged accepted normalization and safety source pins and identifies their matching source snapshots inside the archive.

## Verify or restore

Run with any working directory:

```bash
python3 /path/to/archives/verify-runtime-development.py
```

The default operation only verifies. To restore into a repository root or a new directory:

```bash
python3 /path/to/archives/verify-runtime-development.py --extract-to /path/to/restore-root
```

The helper verifies the whole archive SHA-256 and every member's path, size, and SHA-256 before writing. It rejects unexpected members, links, non-regular files, duplicate paths, path traversal, and symlink ancestors. It checks every destination before creating files, skips identical existing files, and refuses different existing files. Missing files use exclusive creation, so existing files cannot be overwritten. It never invokes Lean or Git.

`pack-runtime-development.py` is the exact packaging recipe. It refuses to overwrite an existing archive or manifest. The manifest records both helper hashes. `archive-verification.json` and `archive-verification.log` retain the actual verification commands and results: nine cases passed, including expected rejection cases, a fresh extraction, and an idempotent second extraction. Every restored member was also independently compared with its manifest hash, and every original source was checked unchanged after packaging.

## Evidence classifications

The preserved `normalization/attempt-001` is a failed Lean development attempt. The corrected SafeHigh implementation, the complete former 20-module build, and the time-zero helper compiled against that chain are retained as **alternative evidence**. The final accepted normalization imports the unchanged published Agent 3 bridge; it does not use the SafeHigh alternative.

The final 21-module author records are an **exact-hash local author snapshot**. Their original verifier recorded HEAD `e3802562ce44ce2c5211b6396e5f4d1693c39fc5`; the newly written normalization, safety, vendored IntegerInterfaces path, and registry were not published at that recorded HEAD. Its `source_tree_clean` field checks tracked changes only and ignores untracked files. The manifest and archived receipt preserve this caveat explicitly. Later published exact-commit verification is a separate record.

This archive contains the complete development evidence under the named prefixes, including source snapshots, actual commands, raw logs, failure records, and the original SafeHigh dependency sources. The recorded registries refer to additional unchanged repository dependencies; this evidence archive is not a standalone Lean installation or a replacement for the published dependency registry.

Accepted source pins remain:

| Source | SHA-256 |
|---|---|
| `proofs/Agent101NormalizationValue.lean` | `50d2d40d5d8db605b8b6d363bf1d0ec762d8c06983c4bb3384f3e1f3094adac9` |
| `proofs/Agent101ProtectedSafety.lean` | `7b3f060d84e7b955f47425dc69277ea8d8f2fa94a62db173a47f3a614d2a2eb2` |
