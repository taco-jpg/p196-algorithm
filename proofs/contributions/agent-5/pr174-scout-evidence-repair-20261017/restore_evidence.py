#!/usr/bin/env python3
"""Restore and verify every original evidence path into a new output directory."""
import argparse
import hashlib
import json
import tarfile
import resource
from pathlib import Path, PurePosixPath

def digest(data):
    return hashlib.sha256(data).hexdigest()

def require(condition, message):
    if not condition:
        raise ValueError(message)

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--archive', type=Path, required=True)
parser.add_argument('--receipt', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
resource.setrlimit(resource.RLIMIT_AS, (384 * 1024**2, 384 * 1024**2))
receipt = json.loads(args.receipt.read_text())
archive_bytes = args.archive.read_bytes()
require(len(archive_bytes) == receipt['archive']['bytes'], 'Archive size mismatch')
require(digest(archive_bytes) == receipt['archive']['sha256'], 'Archive hash mismatch')
output = args.output.resolve()
output.mkdir(parents=True, exist_ok=False)
with tarfile.open(args.archive, mode='r:xz') as tar:
    members = tar.getmembers()
    require(len({m.name for m in members}) == len(members), 'Duplicate tar members')
    require(all(m.isfile() for m in members), 'Only regular members are supported')
    manifest_bytes = tar.extractfile('MANIFEST.json').read()
    require(digest(manifest_bytes) == receipt['manifest']['sha256'], 'Manifest hash mismatch')
    manifest = json.loads(manifest_bytes)
    rows = manifest['files']
    require(len({x['path'] for x in rows}) == len(rows) == manifest['original_files'], 'Path inventory mismatch')
    require({m.name for m in members} == {'MANIFEST.json'} | {x['archive_member'] for x in rows}, 'Unexpected archive member selection')
    payloads = {m.name: tar.extractfile(m).read() for m in members if m.name != 'MANIFEST.json'}
    for row in rows:
        relative = PurePosixPath(row['path'])
        require(not relative.is_absolute() and '..' not in relative.parts and str(relative) == row['path'], 'Unsafe or noncanonical relative path')
        require(row['archive_member'] == 'objects/' + row['sha256'], 'Content object binding mismatch')
        data = payloads[row['archive_member']]
        require(len(data) == row['bytes'] and digest(data) == row['sha256'], 'Original content mismatch: ' + row['path'])
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        require(blob == row['git_blob'], 'Git blob mismatch: ' + row['path'])
        path = output.joinpath(*relative.parts)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        path.chmod(int(row['original_mode'], 8) & 0o777)
        require(path.read_bytes() == data, 'Restored byte mismatch')
        require(oct(path.stat().st_mode & 0o777) == row['original_mode'], 'Restored mode mismatch')
print(json.dumps({'status': 'PASS_RESTORED_ALL_ORIGINAL_BYTES', 'files': len(rows),
                  'bytes': sum(x['bytes'] for x in rows), 'output': str(output)}, indent=2))
