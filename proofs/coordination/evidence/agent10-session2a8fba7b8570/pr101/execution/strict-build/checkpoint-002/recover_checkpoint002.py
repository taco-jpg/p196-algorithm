#!/usr/bin/env python3
"""Verify PR101 execution checkpoint 002; optionally extract to a new directory.

This additive recovery helper was created after the historical archive was
sealed. It is not a member of that archive. It executes no recovered code.
Only the Python standard library is used; verification is the default action.
"""
from pathlib import Path, PurePosixPath
import argparse
import base64
import hashlib
import io
import json
import os
import re
import stat
import sys
import tarfile

RECEIPT_NAME = 'PACKAGING_RECEIPT.json'
RECEIPT_SHA256 = '805e7fc04886ac8b4531c529747b67ca6e071545a21e442492c521d96220f1e0'
MANIFEST_NAME = 'MEMBERS.json'
MANIFEST_SHA256 = '6ced7e8ba17509fdac798c328c08c515016e4eb3d2ca2cfa1e3c7555d0e382d0'
ARCHIVE_NAME = 'pr101-execution-checkpoint-002.tar.xz'
ARCHIVE_SHA256 = '047b431acab1f452fd67e07cf705acb7c07221002ec496d1d2852cf414a64956'
ARCHIVE_BYTES = 702340
MEMBER_COUNT = 342
PAYLOAD_BYTES = 16138045
PART_NAMES = ['part-000.b64', 'part-001.b64', 'part-002.b64']


class RecoveryError(Exception):
    """A failed identity or safe-extraction condition."""


def require(condition, message):
    if not condition:
        raise RecoveryError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def no_symlink_components(path):
    """Reject existing symlinks in a path, including its ancestors."""
    absolute = Path(os.path.abspath(os.fspath(path)))
    cursor = Path(absolute.anchor)
    for component in absolute.parts[1:]:
        cursor = cursor / component
        try:
            metadata = cursor.lstat()
        except FileNotFoundError:
            continue
        require(not stat.S_ISLNK(metadata.st_mode), f'Symlink path component rejected: {cursor}')
    return absolute


def read_regular(path, expected_sha=None, expected_bytes=None):
    path = no_symlink_components(path)
    require(stat.S_ISREG(path.lstat().st_mode), f'Not a regular file: {path}')
    data = path.read_bytes()
    if expected_bytes is not None:
        require(len(data) == expected_bytes, f'Byte count mismatch: {path.name}')
    if expected_sha is not None:
        require(sha256(data) == expected_sha, f'SHA256 mismatch: {path.name}')
    return data


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f'Duplicate JSON key: {key}')
        result[key] = value
    return result


def parse_json(data):
    return json.loads(data, object_pairs_hook=unique_object)


def validate_member_name(name):
    require(isinstance(name, str), 'Archive member name must be a string')
    require('\x00' not in name and '\\' not in name, f'Invalid archive member name: {name!r}')
    path = PurePosixPath(name)
    require(not path.is_absolute(), f'Absolute archive member rejected: {name}')
    require('..' not in path.parts, f'Parent traversal rejected: {name}')
    require(path.as_posix() == name, f'Noncanonical archive member rejected: {name}')
    require(len(path.parts) >= 2 and path.parts[0] == 'strict-build', f'Unexpected archive member root: {name}')
    return path


def stream_identity(stream):
    digest = hashlib.sha256()
    size = 0
    for block in iter(lambda: stream.read(1024 * 1024), b''):
        digest.update(block)
        size += len(block)
    return {'bytes': size, 'sha256': digest.hexdigest()}


def verify_bundle(bundle):
    """Verify all transport and member bytes without creating any output file."""
    bundle = no_symlink_components(bundle)
    require(bundle.is_dir(), 'Bundle directory does not exist')
    receipt = parse_json(read_regular(bundle / RECEIPT_NAME, RECEIPT_SHA256, 1442))
    members = parse_json(read_regular(bundle / MANIFEST_NAME, MANIFEST_SHA256, 58685))
    require(receipt['status'] == 'PASSED', 'Original packaging receipt is not PASSED')
    require(receipt['archive'] == {'name': ARCHIVE_NAME, 'bytes': ARCHIVE_BYTES, 'sha256': ARCHIVE_SHA256}, 'Unexpected archive pin')
    require(receipt['member_manifest'] == {'name': MANIFEST_NAME, 'bytes': 58685, 'sha256': MANIFEST_SHA256}, 'Unexpected member-manifest pin')
    require(receipt['member_count'] == MEMBER_COUNT and len(members) == MEMBER_COUNT, 'Unexpected member count')
    require(receipt['payload_bytes'] == PAYLOAD_BYTES, 'Unexpected payload byte count')
    require([row['name'] for row in receipt['base64_parts']] == PART_NAMES, 'Unexpected base64 part order')
    encoded_parts = []
    for row in receipt['base64_parts']:
        require(0 < row['characters'] <= 450000 and row['bytes'] == row['characters'], 'Invalid base64 chunk size')
        data = read_regular(bundle / row['name'], row['sha256'], row['bytes'])
        require(len(data.decode('ascii')) == row['characters'], 'Non-ASCII base64 data')
        encoded_parts.append(data)
    archive = base64.b64decode(b''.join(encoded_parts), validate=True)
    require(len(archive) == ARCHIVE_BYTES and sha256(archive) == ARCHIVE_SHA256, 'Reassembled archive identity mismatch')
    if (bundle / ARCHIVE_NAME).exists() or (bundle / ARCHIVE_NAME).is_symlink():
        require(read_regular(bundle / ARCHIVE_NAME, ARCHIVE_SHA256, ARCHIVE_BYTES) == archive, 'Local archive differs from decoded parts')
    for name, row in members.items():
        validate_member_name(name)
        require(set(row) == {'bytes', 'sha256'}, f'Unexpected manifest fields: {name}')
        require(type(row['bytes']) is int and 0 <= row['bytes'] <= PAYLOAD_BYTES, f'Invalid member size: {name}')
        require(re.fullmatch(r'[0-9a-f]{64}', row['sha256']) is not None, f'Invalid member hash: {name}')
        for parent in PurePosixPath(name).parents:
            require(parent.as_posix() not in members, f'File/directory member collision: {name}')
    require(sum(row['bytes'] for row in members.values()) == PAYLOAD_BYTES, 'Manifest payload-size mismatch')
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:xz') as tar:
        entries = tar.getmembers()
        require(len(entries) == MEMBER_COUNT, 'Archive member count mismatch')
        names = [entry.name for entry in entries]
        require(len(set(names)) == len(names), 'Duplicate archive members')
        require(set(names) == set(members), 'Archive members differ from manifest')
        for entry in entries:
            validate_member_name(entry.name)
            require(entry.type in {tarfile.REGTYPE, tarfile.AREGTYPE}, f'Non-regular archive member: {entry.name}')
            require(not entry.issym() and not entry.islnk(), f'Archive link rejected: {entry.name}')
            require(entry.size == members[entry.name]['bytes'], f'Archive size mismatch: {entry.name}')
            stream = tar.extractfile(entry)
            require(stream is not None, f'Member data unavailable: {entry.name}')
            with stream:
                require(stream_identity(stream) == members[entry.name], f'Archive member hash mismatch: {entry.name}')
    return archive, members


def extract_verified(archive, members, destination):
    """Copy already verified regular members into a new, non-symlink directory."""
    destination = no_symlink_components(destination)
    require(not os.path.lexists(destination), 'Extraction destination already exists')
    require(destination.parent.is_dir(), 'Extraction destination parent must already exist')
    destination.mkdir(mode=0o700)
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:xz') as tar:
        for entry in tar.getmembers():
            relative = validate_member_name(entry.name)
            target = destination.joinpath(*relative.parts)
            require(target.resolve().is_relative_to(destination), 'Extraction path escaped destination')
            no_symlink_components(target.parent)
            target.parent.mkdir(parents=True, exist_ok=True)
            no_symlink_components(target.parent)
            stream = tar.extractfile(entry)
            require(stream is not None, 'Verified member stream unavailable')
            # Exclusive creation refuses an existing file or symlink. No archived
            # ownership, executable mode, permission bits, or timestamps are applied.
            with stream, target.open('xb') as output:
                for block in iter(lambda: stream.read(1024 * 1024), b''):
                    output.write(block)
            require(sha256(read_regular(target, expected_bytes=members[entry.name]['bytes'])) == members[entry.name]['sha256'], f'Extracted member mismatch: {entry.name}')
    actual = sorted(p.relative_to(destination).as_posix() for p in destination.rglob('*') if p.is_file())
    require(actual == sorted(members), 'Extracted file inventory mismatch')
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle-dir', type=Path, default=Path(__file__).absolute().parent,
                        help='Directory holding receipt, MEMBERS.json, and the three base64 parts')
    parser.add_argument('--extract-to', type=Path,
                        help='Optional new destination; its parent must exist and no path component may be a symlink')
    args = parser.parse_args()
    archive, members = verify_bundle(args.bundle_dir)
    result = {'status': 'VERIFIED', 'receipt_sha256': RECEIPT_SHA256,
              'member_manifest_sha256': MANIFEST_SHA256, 'archive_sha256': ARCHIVE_SHA256,
              'archive_bytes': ARCHIVE_BYTES, 'verified_member_count': len(members),
              'verified_payload_bytes': PAYLOAD_BYTES, 'all_members_verified_before_any_extraction': True,
              'recovered_code_executed': False}
    if args.extract_to is not None:
        destination = extract_verified(archive, members, args.extract_to)
        result.update({'status': 'VERIFIED_AND_EXTRACTED', 'destination': str(destination),
                       'extracted_member_count': len(members), 'all_extracted_bytes_verified': True})
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (RecoveryError, OSError, ValueError, KeyError, TypeError, tarfile.TarError) as exc:
        print(json.dumps({'status': 'REJECTED', 'reason': str(exc)}), file=sys.stderr)
        sys.exit(1)
