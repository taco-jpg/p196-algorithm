#!/usr/bin/env python3
"""Verify both lossless evidence archives and rebuild the original pinned Lean review."""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
import lzma
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tarfile
import tempfile


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_archive(root: Path, name: str, spec: dict, inventory: dict) -> dict[str, bytes]:
    pieces = []
    for part in spec['parts']:
        data = (root / part['path']).read_bytes()
        if len(data) != part['bytes'] or digest(data) != part['sha256']:
            raise ValueError(f"corrupt archive part: {part['path']}")
        pieces.append(data)
    compressed = b''.join(pieces)
    if len(compressed) != spec['compressed_bytes'] or digest(compressed) != spec['compressed_sha256']:
        raise ValueError(f'compressed identity mismatch: {name}')
    raw = lzma.decompress(compressed)
    if len(raw) != spec['decoded_bytes'] or digest(raw) != spec['decoded_sha256']:
        raise ValueError(f'decoded identity mismatch: {name}')
    result = {}
    with tarfile.open(fileobj=io.BytesIO(raw), mode='r:') as archive:
        for member in archive:
            path = PurePosixPath(member.name)
            if not member.isfile() or path.is_absolute() or '..' in path.parts or member.name in result:
                raise ValueError(f'unsafe or duplicate archive member: {member.name}')
            stream = archive.extractfile(member)
            if stream is None:
                raise ValueError(f'unreadable archive member: {member.name}')
            data = stream.read()
            expected = inventory.get((name, member.name))
            if expected != (len(data), digest(data)):
                raise ValueError(f'member identity mismatch: {name}/{member.name}')
            result[member.name] = data
    expected_paths = {path for kind, path in inventory if kind == name}
    if set(result) != expected_paths or len(result) != spec['member_count']:
        raise ValueError(f'incomplete archive: {name}')
    return result


def write_members(dest: Path, members: dict[str, bytes]) -> None:
    for name, data in members.items():
        path = dest / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-only', action='store_true')
    parser.add_argument('--restore-to', type=Path, help='New directory for all historical and publication-replay evidence')
    parser.add_argument('--repo-root', type=Path, help='Checkout containing the nine unchanged pinned dependencies')
    parser.add_argument('--lean', default='lean')
    parser.add_argument('--out', type=Path, help='New or empty output directory for a fresh Lean run')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    inventory = {}
    with (root / 'INVENTORY.tsv').open(newline='') as stream:
        for row in csv.DictReader(stream, delimiter='\t'):
            key = (row['archive'], row['original_relative_path'])
            if key in inventory:
                raise ValueError(f'duplicate inventory entry: {key}')
            inventory[key] = (int(row['original_bytes']), row['original_sha256'])
    specs = json.loads((root / 'ARCHIVES.json').read_text())
    if {kind for kind, _ in inventory} != set(specs):
        raise ValueError('archive inventory mismatch')
    archives = {name: load_archive(root, name, spec, inventory) for name, spec in specs.items()}
    history = archives['history']
    for name in ['All.lean', 'AuditAll.lean', 'ScopeRegression.lean']:
        if (root / name).read_bytes() != history[name]:
            raise ValueError(f'visible source differs from archived checked source: {name}')
    # Verify the original author-generated manifest as well as the publication inventory.
    for line in history['SHA256SUMS'].decode().splitlines():
        sha, name = line.split(None, 1)
        if digest(history[name.strip()]) != sha:
            raise ValueError(f'historical SHA256SUMS mismatch: {name}')
    if args.repo_root:
        for pin in json.loads(history['source_pins.json']):
            data = (args.repo_root.resolve() / pin['path']).read_bytes()
            blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            if digest(data) != pin['sha256'] or blob != pin['git_blob_sha1']:
                raise ValueError(f"upstream source pin changed: {pin['path']}")
    print('PASS: 65 original files and 15 publication-replay files; exact source and archive identities.', flush=True)
    if args.restore_to:
        dest = args.restore_to.resolve()
        dest.mkdir(parents=True, exist_ok=False)
        for name, members in archives.items():
            write_members(dest / name, members)
        print(f'Restored evidence to {dest}', flush=True)
    if args.verify_only or (args.restore_to and args.out is None):
        return 0
    if args.repo_root is None or args.out is None:
        parser.error('a Lean rebuild requires --repo-root and --out; use --verify-only to check stored bytes')
    with tempfile.TemporaryDirectory(prefix='agent114-restored-review-') as temp:
        dest = Path(temp)
        write_members(dest, history)
        return subprocess.run([sys.executable, str(dest / 'reproduce.py'),
            '--repo-root', str(args.repo_root.resolve()), '--lean', args.lean,
            '--out', str(args.out.resolve())], check=False).returncode


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, lzma.LZMAError, tarfile.TarError) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        raise SystemExit(1)
