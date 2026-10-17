#!/usr/bin/env python3
"""Preserve the two bounded queue inspections without executing their contents."""
import base64
import hashlib
import json
from pathlib import Path, PurePosixPath
import tarfile

ROOT = Path(__file__).resolve().parent
DEST = ROOT / 'evidence/campaign-boundary'
ITEMS = [
    ('pr167_ownership_stop', ROOT.parent / 'agent10-pr167/evidence/retained',
     'pr167-ownership-boundary.tar.xz', 'b7a7f1dff053d7ade7fa806f728f826c70f4f61ca63ca1bad49345fef1d4bf72'),
    ('queue_continuation', ROOT / 'evidence/queue-boundary-final',
     'queue-boundary-final.tar.xz', 'ff540ca5bd8afd8e7e0cc41735707470bc94e4fffcacf12c548fc203383138e2'),
]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    assert not DEST.exists(), 'Preserve existing publication preparation'
    DEST.mkdir()
    packet = {'schema_version': 1, 'purpose': 'Retain exact read-only campaign selection and ownership-stop evidence',
              'archive_encoding': 'tar.xz base64', 'archives': [],
              'later_disposition': 'PR167 remains Agent15; no Agent10 claim or proof qualification. Agent7 retains161 after Agent14 withdrawal. PR101 was subsequently accepted by Agent10 at3ca64c214401fbd4e20626e0e90bfa05196a3141 after PR166 external disposition; Agent117 source ownership remains ACTIVE. Agent11 subsequently accepted151. The enclosed reports retain their original earlier observation boundaries.'}
    for label, directory, filename, expected in ITEMS:
        binary = (directory / filename).read_bytes()
        assert sha(binary) == expected
        manifest = json.loads((directory / 'ARCHIVE_MANIFEST.json').read_text())
        entries = manifest.get('members', manifest.get('files'))
        pins = {item['path']: item for item in entries}
        with tarfile.open(directory / filename, 'r:xz') as archive:
            members = archive.getmembers()
            names = [m.name for m in members]
            assert len(names) == len(set(names))
            extra = set() if label == 'pr167_ownership_stop' else {'ARCHIVE_MANIFEST.json'}
            assert set(names) == set(pins) | extra
            for member in members:
                path = PurePosixPath(member.name)
                assert member.isfile() and not path.is_absolute() and '..' not in path.parts
                data = archive.extractfile(member).read()
                local = Path(*path.parts[1:]) if label == 'pr167_ownership_stop' else Path(*path.parts)
                assert data == (directory / local).read_bytes()
                if member.name in pins:
                    pin = pins[member.name]
                    assert len(data) == pin['bytes'] and sha(data) == pin['sha256']
        packet['archives'].append({'label': label, 'file': filename, 'bytes': len(binary),
                                   'sha256': expected, 'members': len(members), 'manifest': manifest,
                                   'all_member_bytes_matched': True, 'base64': base64.b64encode(binary).decode()})
    (DEST / 'CAMPAIGN_BOUNDARY_EVIDENCE.json').write_text(json.dumps(packet, indent=2) + '\n')
    (DEST / 'PR167_OWNERSHIP_BOUNDARY.md').write_bytes((ITEMS[0][1] / 'OWNERSHIP_BOUNDARY.md').read_bytes())
    (DEST / 'QUEUE_CONTINUATION.md').write_bytes((ITEMS[1][1] / 'QUEUE_CONTINUATION.md').read_bytes())
    print(json.dumps({'status': 'ALL_ARCHIVE_MEMBERS_EXACT', 'files': [str(p) for p in sorted(DEST.iterdir())],
                      'archives': [{k: a[k] for k in ['label', 'bytes', 'sha256', 'members']} for a in packet['archives']]}))

if __name__ == '__main__':
    main()
