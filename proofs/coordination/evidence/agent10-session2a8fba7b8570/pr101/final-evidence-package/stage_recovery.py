#!/usr/bin/env python3
"""Retain completed checkpoint-002 recovery helpers and substantive test logs."""
from pathlib import Path
import datetime
import hashlib
import json
import stat

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
PREFIX = Path('execution/strict-build/checkpoint-002')
SOURCE = BASE / PREFIX
names = ['recover_checkpoint002.py', 'RECOVERY.md', 'RECOVERY_TEST_RECEIPT.json',
         'test_recovery_checkpoint002.py', 'MEMBERS.json', 'PACKAGING_RECEIPT.json']
names += ['recovery-test-001/' + p.name for p in sorted((SOURCE / 'recovery-test-001').iterdir())]
assert len(names) == 12
receipt = json.loads((SOURCE / 'RECOVERY_TEST_RECEIPT.json').read_text())
assert receipt['status'] == 'PASSED'
rows = []
for name in names:
    path = SOURCE / name
    assert path.is_file() and not path.is_symlink()
    data = path.read_bytes()
    out = HERE / 'payload' / PREFIX / name
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('xb') as stream:
        stream.write(data)
    mode = stat.S_IMODE(path.stat().st_mode)
    assert mode in (0o444, 0o555, 0o644, 0o755)
    out.chmod(mode)
    assert path.read_bytes() == data
    rows.append({'path': (PREFIX / name).as_posix(), 'bytes': len(data),
                 'sha256': hashlib.sha256(data).hexdigest(), 'mode': mode})
rows.sort(key=lambda row: row['path'])
exclusions = [
    {'path': (PREFIX / directory).as_posix(),
     'reason': 'Regenerable duplicate extraction of the already published checkpoint-002 archive; all 342 original member identities are retained in the included original MEMBERS.json and the completed recovery test receipt.',
     'identity_manifest': (PREFIX / 'MEMBERS.json').as_posix(),
     'member_count': 342,
     'original_archive_sha256': '047b431acab1f452fd67e07cf705acb7c07221002ec496d1d2852cf414a64956'}
    for directory in ['helper-verified-extraction-001/', 'verified-extraction/']]
exclusions.append({'path': (PREFIX / 'pr101-execution-checkpoint-002.tar.xz').as_posix(),
                   'reason': 'Already published immutable 342-member execution archive; not duplicated in this additive evidence archive.',
                   'bytes': 702340, 'sha256': '047b431acab1f452fd67e07cf705acb7c07221002ec496d1d2852cf414a64956'})
exclusions.append({'path': (PREFIX / 'part-*.b64').as_posix(),
                   'reason': 'Already published transport copies of the same immutable execution archive.'})
record = {'group': 'checkpoint-002-recovery-additions',
          'staged_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'file_count': len(rows), 'bytes': sum(row['bytes'] for row in rows),
          'files': rows, 'excluded': exclusions, 'original_bytes_compared_after_copy': True}
out = HERE / 'stage-records/checkpoint-002-recovery-additions.json'
assert not out.exists()
out.write_text(json.dumps(record, indent=2, sort_keys=True) + '\n')
print(json.dumps({k: record[k] for k in ['group', 'file_count', 'bytes']}))
