# Complete PR121 prospective-stack evidence packaging receipt

## Result

PASS. The root agent elected **full lossless publication** instead of the compact suggested subset in the original PUBLISH_MANIFEST.json. This archive contains every meaningful file from the PR121 combination evidence directory, including complete commands.jsonl, complete tree_entries.json, all failed construction versions and diagnostics, the full source intake, the reports, inventories and scripts. No unique transcript was excluded because of its size.

- Archive: `prospective-stack-evidence.tar.xz`
- Archive bytes: **1,462,544**
- Archive SHA256: `4ff284b2f011322a163c90984b103178b6a8f62ea9a7e07b3cdd501354844742`
- Original regular-file count: **43**
- Original total file bytes: **73,360,407**
- Complete per-file manifest: `prospective-stack-evidence.files.json`
- Per-file manifest SHA256: `6eee252500f8c7434553a052a10138a94f0616d61f60c3c65c2a9ec1ee8542a7`
- Archive verification record: `prospective-stack-evidence.verification.json`
- Archive verification record SHA256: `7f32ad43d5f22c114d64e9b023183b87c43bf513ad453776a11602828ffb3696`

This is packaging only. No combination, Lean build, mathematical review, source repair, task update, Git ref change or remote mutation was performed. No blocked Agent26 archive was accessed or repackaged. The files packaged here are this subtask's already retained public-source intake and new evidence.

## Determinism and exclusions

The packager sorts all relative file paths, includes regular-file bodies losslessly, preserves each original permission mode, normalizes mtime/uid/gid to zero and owner/group names to empty strings, writes PAX-format tar entries, and compresses with XZ/LZMA preset 6 and CRC64. The full standalone implementation is `package_complete_evidence.py`.

The sole exclusion rule is a path component exactly `__pycache__`: reproducible Python bytecode cache only. The per-file manifest lists the exact excluded paths. No source, report, failure, retained evidence or intake file was excluded. No prospective.index exists; failed private-index construction did not create one.

The original files remain unchanged:

- REPORT.md SHA256: `d9121da672f5ddfe2af323a7595e2f28bb5621a6f3369f8db5b548c6dc2b866f`
- PUBLISH_MANIFEST.json SHA256: `201b1088a12a6e4b0a63c10c1972486944bdbc9d7a9734fa7c87739d13862253`

Their earlier suggested subset is retained as historical evidence; this receipt supersedes that selection for publication without rewriting either original.

## Archive inspection and recovery

After compression, the archive was opened once and every member was inspected. Exactly 43 unique regular-file members matched the manifest; every body was decompressed and SHA256-hashed once. Paths, member types, normalized metadata, original permission modes, byte counts and hashes all matched. There are no symlinks or hard links.

Run the following commands from a directory containing the published archive and manifest. The recovery directory should be new:

```sh
printf '%s  %s\n' '4ff284b2f011322a163c90984b103178b6a8f62ea9a7e07b3cdd501354844742' 'prospective-stack-evidence.tar.xz' | sha256sum -c -
mkdir pr121-prospective-recovered
tar -xJf prospective-stack-evidence.tar.xz -C pr121-prospective-recovered
```

Verify every recovered file against the complete publication manifest:

```sh
python3 - <<'PY'
import hashlib
import json
from pathlib import Path
manifest = json.loads(Path('prospective-stack-evidence.files.json').read_text())
root = Path('pr121-prospective-recovered') / manifest['archive_root']
expected = {row['path']: row for row in manifest['files']}
actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
assert actual == set(expected), 'Unexpected or missing recovered file'
for name, row in expected.items():
    data = (root / name).read_bytes()
    assert len(data) == row['bytes'], name
    assert hashlib.sha256(data).hexdigest() == row['sha256'], name
print('PASS', len(expected), 'files', sum(row['bytes'] for row in expected.values()), 'bytes')
PY
```

The archive contains the folder `pr121-combination/`; commands.jsonl and tree_entries.json recover under that folder in full. The manifest and this packaging receipt remain adjacent publication artifacts rather than altering the original evidence directory.
