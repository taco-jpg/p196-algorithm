#!/usr/bin/env python3
"""Recover and hash-check this evidence package; never execute archived code."""
from pathlib import Path, PurePosixPath
import argparse
import base64
import hashlib
import io
import json
import lzma
import os
import re
import tarfile

LIMIT = 256 * 1024 * 1024


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(ok, message):
    if not ok:
        raise ValueError(message)


def safe_name(name):
    require(isinstance(name, str) and name, 'Empty/non-string member path')
    path = PurePosixPath(name)
    require(not path.is_absolute() and '\\' not in name and '\0' not in name,
            'Absolute or nonportable member path')
    require(all(part not in ('', '.', '..') for part in name.split('/')),
            'Unsafe member path component')
    require(str(path) == name and not re.match(r'^[A-Za-z]:', name),
            'Noncanonical member path')
    return path


def regular_bytes(path):
    require(not path.is_symlink() and path.is_file(), 'Input must be a regular file: ' + str(path))
    return path.read_bytes()


def check_record(data, record, label):
    require(type(record.get('bytes')) is int and 0 <= record['bytes'] <= LIMIT,
            'Invalid byte count: ' + label)
    require(re.fullmatch('[0-9a-f]{64}', record.get('sha256', '')) is not None,
            'Invalid SHA256: ' + label)
    require(len(data) == record['bytes'], 'Byte count mismatch: ' + label)
    require(sha(data) == record['sha256'], 'SHA256 mismatch: ' + label)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package_directory', type=Path)
    parser.add_argument('new_output_directory', type=Path)
    parser.add_argument('--expected-archive-sha256')
    args = parser.parse_args()
    package = args.package_directory.absolute()
    require(not package.is_symlink() and package.is_dir(), 'Invalid package directory')
    manifest = json.loads(regular_bytes(package / 'package-manifest.json'))
    require(manifest.get('schema_version') == 1, 'Unsupported manifest version')
    if args.expected_archive_sha256:
        require(manifest['archive']['sha256'] == args.expected_archive_sha256,
                'Archive hash differs from independently supplied hash')
    parts = manifest['parts']
    require(isinstance(parts, list) and 0 < len(parts) <= 10000, 'Invalid part count')
    require(len({part['path'] for part in parts}) == len(parts), 'Duplicate part paths')
    decoded = []
    for i, part in enumerate(parts, 1):
        name = part['path']
        require(name == f'parts/part-{i:04d}.b64', 'Unexpected part path or order')
        require(not (package / 'parts').is_symlink(), 'Part directory is a symlink')
        encoded = regular_bytes(package / name)
        require(len(encoded) <= 20000 and len(encoded) % 4 == 0, 'Invalid part size')
        check_record(encoded, part, name)
        block = base64.b64decode(encoded, validate=True)
        check_record(block, part['decoded'], name + ' decoded')
        decoded.append(block)
    require(sum(map(len, decoded)) <= 64 * 1024 * 1024, 'Archive exceeds size limit')
    archive = b''.join(decoded)
    check_record(archive, manifest['archive'], 'archive')
    require(manifest['archive']['path'] == 'pr177-evidence.tar.xz', 'Unexpected archive name')
    members = manifest['members']
    require(isinstance(members, list) and 0 < len(members) <= 10000, 'Invalid member count')
    records = {}
    for record in members:
        name = record['path']
        safe_name(name)
        require(name not in records, 'Duplicate manifest member')
        require(type(record['bytes']) is int and 0 <= record['bytes'] <= 64 * 1024 * 1024,
                'Invalid member size')
        records[name] = record
    require(sum(r['bytes'] for r in records.values()) <= LIMIT, 'Members exceed size limit')
    decoder = lzma.LZMADecompressor(memlimit=128 * 1024 * 1024)
    tarbytes = decoder.decompress(archive, max_length=LIMIT + 1)
    require(len(tarbytes) <= LIMIT and decoder.eof and not decoder.unused_data,
            'Oversized, truncated, or trailing compressed data')
    recovered = {}
    with tarfile.open(fileobj=io.BytesIO(tarbytes), mode='r:') as bundle:
        for member in bundle:
            name = member.name
            safe_name(name)
            require(member.isreg(), 'Nonregular member (links/devices forbidden): ' + name)
            require(name not in recovered and name in records, 'Duplicate/unexpected member: ' + name)
            require(member.size == records[name]['bytes'], 'Tar size mismatch: ' + name)
            stream = bundle.extractfile(member)
            require(stream is not None, 'Unreadable member: ' + name)
            data = stream.read()
            check_record(data, records[name], name)
            recovered[name] = data
    require(set(recovered) == set(records), 'Missing archive members')
    output = args.new_output_directory.absolute()
    require(not output.exists() and not output.is_symlink(), 'Output must not already exist')
    require(output.parent.is_dir(), 'Output parent must already exist')
    require(all(not p.is_symlink() for p in [output.parent, *output.parent.parents]),
            'Output ancestors must not be symlinks')
    output.mkdir(mode=0o700)
    for name, data in sorted(recovered.items()):
        dest = output.joinpath(*PurePosixPath(name).parts)
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open('xb') as stream:
            stream.write(data)
        os.chmod(dest, 0o600)
    print(json.dumps({'status': 'RECOVERED_BYTE_EXACT', 'members': len(recovered),
                      'bytes': sum(map(len, recovered.values())),
                      'archive_sha256': sha(archive), 'output': str(output)}, indent=2))


if __name__ == '__main__':
    main()
