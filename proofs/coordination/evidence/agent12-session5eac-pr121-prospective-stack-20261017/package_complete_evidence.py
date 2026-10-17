#!/usr/bin/env python3
"""Create and verify a deterministic, complete, lossless PR121 evidence archive."""
from pathlib import Path
import hashlib
import json
import lzma
import stat
import tarfile

SOURCE=Path('/workspace/scratch/5eac7b9c26af/agent12-evidence/pr121-combination')
OUTPUT=Path(__file__).resolve().parent
ARCHIVE=OUTPUT/'prospective-stack-evidence.tar.xz'
MANIFEST=OUTPUT/'prospective-stack-evidence.files.json'
RECEIPT=OUTPUT/'PACKAGING_RECEIPT.md'
VERIFY=OUTPUT/'prospective-stack-evidence.verification.json'
PREFIX='pr121-combination'

def digest_file(path):
    digest=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):
            digest.update(block)
    return digest.hexdigest()

def digest_stream(stream):
    digest=hashlib.sha256(); size=0
    for block in iter(lambda:stream.read(1024*1024),b''):
        size+=len(block); digest.update(block)
    return size,digest.hexdigest()

assert not any(path.exists() for path in [ARCHIVE,MANIFEST,RECEIPT,VERIFY]),'Preserve existing publication artifacts.'
all_entries=sorted(SOURCE.rglob('*'))
assert not any(path.is_symlink() for path in all_entries),'Review symlinks explicitly before packaging.'
excluded=[path.relative_to(SOURCE).as_posix() for path in all_entries if '__pycache__' in path.relative_to(SOURCE).parts]
files=[path for path in all_entries if path.is_file() and '__pycache__' not in path.relative_to(SOURCE).parts]
rows=[{'path':path.relative_to(SOURCE).as_posix(),'bytes':path.stat().st_size,'sha256':digest_file(path),'mode':format(stat.S_IMODE(path.stat().st_mode),'04o')} for path in files]
unchanged={name:digest_file(SOURCE/name) for name in ['REPORT.md','PUBLISH_MANIFEST.json']}
manifest={'schema_version':1,'archive_root':PREFIX,'file_count':len(rows),'original_file_bytes':sum(row['bytes'] for row in rows),
          'selection':'Every regular file in the evidence directory except explicitly named Python bytecode cache entries. No size-based exclusions.',
          'exclusions':{'rule':'Any path component exactly __pycache__; reproducible Python bytecode only.','actual_paths':excluded},
          'files':rows}
MANIFEST.write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
with lzma.open(ARCHIVE,'wb',format=lzma.FORMAT_XZ,check=lzma.CHECK_CRC64,preset=6) as compressed:
    with tarfile.open(fileobj=compressed,mode='w|',format=tarfile.PAX_FORMAT) as archive:
        for row in rows:
            info=tarfile.TarInfo(PREFIX+'/'+row['path'])
            info.size=row['bytes']; info.mode=int(row['mode'],8)
            info.mtime=0; info.uid=0; info.gid=0; info.uname=''; info.gname=''
            info.type=tarfile.REGTYPE
            with (SOURCE/row['path']).open('rb') as data:
                archive.addfile(info,data)

expected={PREFIX+'/'+row['path']:row for row in rows}
checked=[]
with tarfile.open(ARCHIVE,'r:xz') as archive:
    members=archive.getmembers()
    assert len(members)==len(expected)
    assert len({member.name for member in members})==len(members)
    assert {member.name for member in members}==set(expected)
    for member in members:
        assert member.isfile() and not member.issym() and not member.islnk()
        assert member.mtime==0 and member.uid==0 and member.gid==0
        assert member.uname=='' and member.gname==''
        row=expected[member.name]
        with archive.extractfile(member) as data:
            length,digest=digest_stream(data)
        assert length==row['bytes']==member.size
        assert digest==row['sha256']
        assert member.mode==int(row['mode'],8)
        checked.append({'member':member.name,'bytes':length,'sha256':digest,'verified':True})
assert {name:digest_file(SOURCE/name) for name in unchanged}==unchanged
archive_bytes=ARCHIVE.stat().st_size
archive_sha=digest_file(ARCHIVE)
verification={'status':'PASS','archive':ARCHIVE.name,'archive_bytes':archive_bytes,'archive_sha256':archive_sha,
              'manifest_sha256':digest_file(MANIFEST),'verified_file_count':len(checked),'verified_original_bytes':sum(row['bytes'] for row in checked),
              'inspection':'Exactly one complete decompression/member hashing pass; all names, types, normalized metadata, original modes, lengths and SHA256 values matched.',
              'protected_original_hashes_unchanged':unchanged,'members':checked}
VERIFY.write_text(json.dumps(verification,indent=2,sort_keys=True)+'\n')
RECEIPT.write_text(f'''# Complete PR121 prospective-stack evidence packaging receipt

## Result

PASS. The root agent elected **full lossless publication** instead of the compact suggested subset in the original PUBLISH_MANIFEST.json. This archive contains every meaningful file from the PR121 combination evidence directory, including complete commands.jsonl, complete tree_entries.json, all failed construction versions and diagnostics, the full source intake, the reports, inventories and scripts. No unique transcript was excluded because of its size.

- Archive: `{ARCHIVE.name}`
- Archive bytes: **{archive_bytes:,}**
- Archive SHA256: `{archive_sha}`
- Original regular-file count: **{len(rows)}**
- Original total file bytes: **{manifest['original_file_bytes']:,}**
- Complete per-file manifest: `{MANIFEST.name}`
- Per-file manifest SHA256: `{digest_file(MANIFEST)}`
- Archive verification record: `{VERIFY.name}`
- Archive verification record SHA256: `{digest_file(VERIFY)}`

This is packaging only. No combination, Lean build, mathematical review, source repair, task update, Git ref change or remote mutation was performed. No blocked Agent26 archive was accessed or repackaged. The files packaged here are this subtask's already retained public-source intake and new evidence.

## Determinism and exclusions

The packager sorts all relative file paths, includes regular-file bodies losslessly, preserves each original permission mode, normalizes mtime/uid/gid to zero and owner/group names to empty strings, writes PAX-format tar entries, and compresses with XZ/LZMA preset 6 and CRC64. The full standalone implementation is `package_complete_evidence.py`.

The sole exclusion rule is a path component exactly `__pycache__`: reproducible Python bytecode cache only. The per-file manifest lists the exact excluded paths. No source, report, failure, retained evidence or intake file was excluded. No prospective.index exists; failed private-index construction did not create one.

The original files remain unchanged:

- REPORT.md SHA256: `{unchanged['REPORT.md']}`
- PUBLISH_MANIFEST.json SHA256: `{unchanged['PUBLISH_MANIFEST.json']}`

Their earlier suggested subset is retained as historical evidence; this receipt supersedes that selection for publication without rewriting either original.

## Archive inspection and recovery

After compression, the archive was opened once and every member was inspected. Exactly {len(rows)} unique regular-file members matched the manifest; every body was decompressed and SHA256-hashed once. Paths, member types, normalized metadata, original permission modes, byte counts and hashes all matched. There are no symlinks or hard links.

Run the following commands from a directory containing the published archive and manifest. The recovery directory should be new:

```sh
printf '%s  %s\\n' '{archive_sha}' '{ARCHIVE.name}' | sha256sum -c -
mkdir pr121-prospective-recovered
tar -xJf {ARCHIVE.name} -C pr121-prospective-recovered
```

Verify every recovered file against the complete publication manifest:

```sh
python3 - <<'PY'
import hashlib
import json
from pathlib import Path
manifest = json.loads(Path('{MANIFEST.name}').read_text())
root = Path('pr121-prospective-recovered') / manifest['archive_root']
expected = {{row['path']: row for row in manifest['files']}}
actual = {{p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}}
assert actual == set(expected), 'Unexpected or missing recovered file'
for name, row in expected.items():
    data = (root / name).read_bytes()
    assert len(data) == row['bytes'], name
    assert hashlib.sha256(data).hexdigest() == row['sha256'], name
print('PASS', len(expected), 'files', sum(row['bytes'] for row in expected.values()), 'bytes')
PY
```

The archive contains the folder `{PREFIX}/`; commands.jsonl and tree_entries.json recover under that folder in full. The manifest and this packaging receipt remain adjacent publication artifacts rather than altering the original evidence directory.
''')
for path in [ARCHIVE,MANIFEST,VERIFY,RECEIPT,Path(__file__)]:
    print(json.dumps({'path':str(path),'bytes':path.stat().st_size,'sha256':digest_file(path)}))
