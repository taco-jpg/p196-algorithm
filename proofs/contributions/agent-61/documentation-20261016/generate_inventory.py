#!/usr/bin/env python3
"""Record this contribution's selected bytes, without changing historical inventories."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

PIN = '10a173cb635fa8d03e357f454232816fc3e77609'
PACKAGE = 'proofs/contributions/agent-61/documentation-20261016'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--increment', choices=['findings', 'complete'], required=True)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[4])
    args = parser.parse_args()
    repo = args.repo.resolve()
    package = repo / PACKAGE
    excluded = {package / 'FILES.json', package / 'MANIFEST.sha256'}
    selected = {p for p in package.rglob('*') if p.is_file() and p not in excluded}
    selected.update(p for p in (repo / f'proofs/archive/documentation/agent-61/{PIN}').rglob('*') if p.is_file())
    selected.update(repo / p for p in ['proofs/FINDINGS.md', 'proofs/SOURCE_MAP.json'])
    if args.increment == 'complete':
        selected.add(repo / 'proofs/CONSOLIDATION.md')
    rows = []
    for path in sorted(selected):
        data = path.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        rows.append({'path': path.relative_to(repo).as_posix(), 'bytes': len(data),
                     'sha256': hashlib.sha256(data).hexdigest(), 'git_blob': blob, 'mode': '100644'})
    payload = {'schema': 1, 'source_commit': PIN, 'increment': args.increment,
               'scope': 'The revised current documents and SOURCE_MAP, exact Agent #61 originals, and complete Agent #61 evidence package.',
               'omitted_from_selection': ['All unchanged repository paths outside the contribution selection.'],
               'self_exclusions': [p.relative_to(repo).as_posix() for p in sorted(excluded)],
               'archive_members': 'REPRODUCTION_ARCHIVE.json separately records all original and stored reproduction-evidence bytes.',
               'file_count': len(rows), 'stored_bytes': sum(r['bytes'] for r in rows), 'files': rows}
    (package / 'FILES.json').write_text(json.dumps(payload, indent=2) + '\n')
    manifest = ''.join(f"{r['sha256']}  {r['path']}\n" for r in rows)
    (package / 'MANIFEST.sha256').write_text(manifest)
    subprocess.run(['sha256sum', '--check', '--status', str(package / 'MANIFEST.sha256')], cwd=repo, check=True)
    print(json.dumps({'status': 'PASS', 'files': len(rows), 'stored_bytes': payload['stored_bytes'],
                      'source_commit': PIN, 'increment': args.increment, 'mathematical_verification': False}))


if __name__ == '__main__':
    main()
