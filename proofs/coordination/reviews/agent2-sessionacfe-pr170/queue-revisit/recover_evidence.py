#!/usr/bin/env python3
"""Recover and validate the complete PR170 delivery evidence as data only."""
import argparse
import base64
import hashlib
import io
import json
import lzma
from pathlib import Path, PurePosixPath
import tarfile


def digest(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package-dir', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    package = args.package_dir.resolve()
    output = args.output.resolve()
    require(not output.exists() or not any(output.iterdir()), 'Output must be absent or empty')
    transport = json.loads((package / 'TRANSPORT.json').read_text())
    chunks = []
    for row in transport['parts']:
        relative = PurePosixPath(row['path'])
        require(not relative.is_absolute() and '..' not in relative.parts, 'Unsafe part path')
        content = (package / str(relative)).read_bytes()
        require(len(content) == row['bytes'] and digest(content) == row['sha256'], 'Part mismatch: ' + str(relative))
        chunks.append(content)
    compressed = base64.b64decode(b''.join(chunks), validate=True)
    archive = transport['archive']
    require(len(compressed) == archive['bytes'] and digest(compressed) == archive['sha256'], 'Archive mismatch')
    decoded = lzma.decompress(compressed)
    with tarfile.open(fileobj=io.BytesIO(decoded), mode='r:') as bundle:
        members = bundle.getmembers()
        names = [m.name for m in members]
        require(len(names) == len(set(names)), 'Duplicate archive path')
        require(all(m.isfile() for m in members), 'Nonregular archive entry')
        manifest_data = bundle.extractfile('ARCHIVE_MANIFEST.json').read()
        require(digest(manifest_data) == transport['archive_manifest']['sha256'], 'Manifest identity mismatch')
        manifest = json.loads(manifest_data)
        rows = {row['archive_member']: row for row in manifest['members']}
        require(set(names) == set(rows) | {'ARCHIVE_MANIFEST.json'}, 'Archive coverage mismatch')
        require(len(members) == archive['members'], 'Archive count mismatch')
        verified = []
        for member in members:
            relative = PurePosixPath(member.name)
            require(not relative.is_absolute() and '..' not in relative.parts, 'Unsafe archive path')
            content = bundle.extractfile(member).read()
            row = rows.get(member.name)
            if row:
                require(len(content) == row['bytes'] and digest(content) == row['sha256'], 'Member mismatch: ' + member.name)
                require(member.mode == int(row['mode'], 8), 'Mode mismatch: ' + member.name)
            target = output.joinpath(*relative.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            require(not target.exists(), 'Refusing existing file: ' + str(target))
            target.write_bytes(content)
            target.chmod(member.mode)
            verified.append({'path': member.name, 'bytes': len(content), 'sha256': digest(content), 'mode': format(member.mode, '04o')})
    receipt = {'schema_version': 1, 'result': 'PASS_COMPLETE_EVIDENCE_RECOVERY', 'archive_sha256': archive['sha256'], 'files': len(verified), 'bytes': sum(r['bytes'] for r in verified), 'members': verified, 'executed_recovered_code': False}
    (output / 'RECOVERY_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({key: receipt[key] for key in ['result', 'archive_sha256', 'files', 'bytes', 'executed_recovered_code']}))


if __name__ == '__main__':
    main()
