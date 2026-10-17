#!/usr/bin/env python3
"""Package only new extension evidence; preserve all upstream originals in place."""
import hashlib
import json
import lzma
from pathlib import Path
import tarfile

ROOT = Path(__file__).resolve().parent
PREFIX = 'pr172-ordered-extension/'
ARCHIVE = ROOT / 'pr172-ordered-extension.tar.xz'
MANIFEST = ROOT / 'ARCHIVE_MEMBERS.json'
RESULT = ROOT / 'ARCHIVE_RESULT.json'
CHUNK = 1024 * 1024

def identity(path):
    size = path.stat().st_size
    sha = hashlib.sha256()
    blob = hashlib.sha1(b'blob ' + str(size).encode() + b'\0')
    with path.open('rb') as stream:
        while data := stream.read(CHUNK):
            sha.update(data)
            blob.update(data)
    return {'bytes': size, 'sha256': sha.hexdigest(), 'git_blob': blob.hexdigest()}

files = sorted(p for p in ROOT.iterdir() if p.is_file() and p not in (ARCHIVE, MANIFEST, RESULT))
members = [{'member': PREFIX + p.name, **identity(p)} for p in files]
manifest = {
 'schema_version': 1, 'scope': 'New ordered-extension evidence only; this manifest is hashed in external ARCHIVE_RESULT.json.',
 'excluded': ['objects.git/', 'upstream/', ARCHIVE.name, RESULT.name],
 'upstream_reference': {'commit': '159c5360dcb8e0698ba42b7cdf9dcfab29946c17',
                        'path': 'proofs/coordination/reviews/agent16-session02ac12/pr168/EVIDENCE_PACKAGE.json',
                        'git_blob': 'be60aef62b0836311251cf0c53aefa1033929a11'},
 'members': members}
MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
files.append(MANIFEST)
files.sort()
with lzma.LZMAFile(ARCHIVE, 'wb', format=lzma.FORMAT_XZ, check=lzma.CHECK_CRC64, preset=1) as output:
    with tarfile.open(fileobj=output, mode='w|', format=tarfile.USTAR_FORMAT) as archive:
        for path in files:
            info = tarfile.TarInfo(PREFIX + path.name)
            info.size = path.stat().st_size
            info.mode = 0o644
            info.uid = info.gid = info.mtime = 0
            info.uname = info.gname = ''
            with path.open('rb') as stream:
                archive.addfile(info, stream)
expected = {r['member']: r for r in members}
expected[PREFIX + MANIFEST.name] = identity(MANIFEST)
seen = []
with tarfile.open(ARCHIVE, mode='r|xz') as archive:
    for member in archive:
        assert member.isfile() and member.name in expected and member.name not in seen
        assert member.uid == member.gid == member.mtime == 0 and member.mode == 0o644
        sha = hashlib.sha256()
        count = 0
        stream = archive.extractfile(member)
        while data := stream.read(CHUNK):
            count += len(data)
            sha.update(data)
        assert count == member.size == expected[member.name]['bytes']
        assert sha.hexdigest() == expected[member.name]['sha256']
        seen.append(member.name)
assert seen == sorted(expected)
result = {
 'status': 'PASS_STREAM_VERIFIED_ORDERED_EXTENSION_ARCHIVE', 'archive': ARCHIVE.name,
 **identity(ARCHIVE), 'member_count': len(seen),
 'uncompressed_member_bytes': sum(v['bytes'] for v in expected.values()),
 'manifest': {'member': PREFIX + MANIFEST.name, **identity(MANIFEST)},
 'encoding': 'XZ preset 1, CRC64; USTAR sorted members, uid/gid/mtime=0, mode=0644, empty owner names',
 'stream_chunk_bytes': CHUNK, 'original_files_removed': False,
 'unchanged_upstream_package_republished': False, 'git_object_store_included': False,
 'remote_mutations': False}
RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
print(json.dumps(result, indent=2))
