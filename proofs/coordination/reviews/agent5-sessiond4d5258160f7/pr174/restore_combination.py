#!/usr/bin/env python3
"""Verify and restore the original full PR174 combination archive into a new directory."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import resource
import tarfile


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--archive', type=Path, required=True)
p.add_argument('--manifest', type=Path, required=True)
p.add_argument('--receipt', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args()
resource.setrlimit(resource.RLIMIT_AS, (384 * 1024**2, 384 * 1024**2))
receipt = json.loads(a.receipt.read_text())
archive = a.archive.read_bytes()
require(len(archive) == receipt['bytes'] and sha(archive) == receipt['sha256'], 'Archive identity mismatch')
manifest_bytes = a.manifest.read_bytes()
require(sha(manifest_bytes) == receipt['manifest_sha256'], 'Manifest identity mismatch')
rows = json.loads(manifest_bytes)['files']
expected = {row['path']: row for row in rows}
require(len(expected) == len(rows), 'Duplicate manifest path')
out = a.output.resolve()
out.mkdir(parents=True, exist_ok=False)
with tarfile.open(a.archive, 'r:xz') as tar:
    members = tar.getmembers()
    require(len(members) == receipt['members'] == len(rows) + 1, 'Member count mismatch')
    require(len({m.name for m in members}) == len(members), 'Duplicate tar member')
    require(all(m.isfile() for m in members), 'Non-regular archive member')
    require({m.name for m in members} == {'pr174-combination/' + x for x in expected} | {'pr174-combination/FILES.json'}, 'Member selection mismatch')
    for member in members:
        relative = PurePosixPath(member.name)
        require(not relative.is_absolute() and '..' not in relative.parts and str(relative) == member.name, 'Unsafe or noncanonical member path')
        raw = tar.extractfile(member).read()
        short = member.name.removeprefix('pr174-combination/')
        if short == 'FILES.json':
            require(raw == manifest_bytes, 'Embedded manifest differs')
        else:
            row = expected[short]
            require(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'Original member bytes mismatch')
        target = out.joinpath(*relative.parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        target.chmod(0o644)
        require(target.read_bytes() == raw, 'Written member mismatch')
print(json.dumps({'status': 'PASS_ALL_ORIGINAL_COMBINATION_MEMBERS_RESTORED',
                  'members': len(members), 'payload_files': len(rows),
                  'payload_bytes': sum(x['bytes'] for x in rows),
                  'archive_sha256': receipt['sha256'], 'output': str(out)}, indent=2))
