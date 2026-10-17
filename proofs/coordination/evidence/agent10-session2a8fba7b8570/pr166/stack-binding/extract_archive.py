#!/usr/bin/env python3
"""Verify and extract this evidence archive into a new directory, without execution."""
import base64
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import sys
import tarfile

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    if len(sys.argv) != 4:
        raise SystemExit('Usage: python extract_archive.py ARCHIVE_OR_BASE64 ARCHIVE_RECEIPT.json NEW_DIRECTORY')
    source, receipt_path, destination = map(Path, sys.argv[1:])
    receipt = json.loads(receipt_path.read_text())
    transport = source.read_bytes()
    if source.name.endswith('.base64'):
        assert digest(transport) == receipt['base64_sha256'], 'base64 transport hash mismatch'
        archive = base64.b64decode(b''.join(transport.split()), validate=True)
    else:
        archive = transport
    assert digest(archive) == receipt['archive_sha256'], 'archive hash mismatch'
    assert len(archive) == receipt['archive_bytes'], 'archive length mismatch'
    assert not destination.exists(), 'destination already exists; choose a new directory'
    payload = {}
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:*') as tf:
        for member in tf.getmembers():
            path = PurePosixPath(member.name)
            assert member.isfile(), 'archive contains a nonregular member'
            assert not path.is_absolute() and '..' not in path.parts and str(path) == member.name and member.name not in ('', '.'), 'unsafe archive path'
            assert member.name not in payload, 'duplicate archive member'
            data = tf.extractfile(member).read()
            assert len(data) == member.size, 'member size mismatch'
            payload[member.name] = data
    assert len(payload) == receipt['archive_member_count'], 'member count mismatch'
    assert sum(map(len, payload.values())) == receipt['archive_uncompressed_bytes'], 'uncompressed length mismatch'
    manifest_bytes = payload['ARCHIVE_MANIFEST.json']
    assert digest(manifest_bytes) == receipt['manifest_sha256'], 'manifest hash mismatch'
    manifest = json.loads(manifest_bytes)
    assert set(payload) == set(manifest['files']) | {'ARCHIVE_MANIFEST.json'}, 'unexpected or absent archive member'
    for name, pin in manifest['files'].items():
        assert len(payload[name]) == pin['bytes'] and digest(payload[name]) == pin['sha256'], 'payload hash or size mismatch: ' + name
    destination.mkdir()
    for name, data in payload.items():
        target = destination.joinpath(*PurePosixPath(name).parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as handle:
            handle.write(data)
    print(json.dumps({'status': 'VERIFIED_AND_EXTRACTED', 'destination': str(destination), 'members': len(payload), 'executed_archive_scripts': False}, indent=2))

if __name__ == '__main__':
    main()
