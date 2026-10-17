#!/usr/bin/env python3
"""Copy only explicitly completed PR101 evidence groups into a new freeze."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import shutil
import stat
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
STAGED = HERE / 'payload'
RECORDS = HERE / 'stage-records'
RECORDS.mkdir(exist_ok=True)
ALLOWED = {'adoption-001', 'root-inputs', 'target-binding-001', 'independent-review'}


def identity(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


for group in sys.argv[1:]:
    assert group in ALLOWED, 'Unexpected evidence group'
    record_path = RECORDS / (group + '.json')
    assert not record_path.exists(), 'Evidence group already staged; do not overwrite a freeze'
    origin = BASE / group
    rows, excluded = [], []
    for current, dirs, files in os.walk(origin, followlinks=False):
        current = Path(current)
        for name in list(dirs):
            path = current / name
            assert not path.is_symlink(), 'Symlink directory is not allowed'
            if name == '.git':
                dirs.remove(name)
                excluded.append({'path': path.relative_to(BASE).as_posix(),
                                 'reason': 'Operational Git object/index/ref metadata; original evidence and reconstructed-tree receipts are retained.'})
        for name in sorted(files):
            path = current / name
            rel = path.relative_to(BASE).as_posix()
            assert not path.is_symlink() and stat.S_ISREG(path.lstat().st_mode), 'Only regular files are supported'
            if name == '.git':
                excluded.append({'path': rel, 'reason': 'Operational Git worktree pointer file'})
                continue
            data = path.read_bytes()
            out = STAGED / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            with out.open('xb') as stream:
                stream.write(data)
            mode = stat.S_IMODE(path.stat().st_mode)
            assert mode in (0o444, 0o555, 0o644, 0o755), (rel, mode)
            out.chmod(mode)
            assert path.read_bytes() == data
            rows.append({'path': rel, **identity(data), 'mode': mode})
    rows.sort(key=lambda row: row['path'])
    record = {'group': group,
              'staged_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'file_count': len(rows), 'bytes': sum(row['bytes'] for row in rows),
              'files': rows, 'excluded': excluded,
              'original_bytes_compared_after_copy': True}
    record_path.write_text(json.dumps(record, indent=2, sort_keys=True) + '\n')
    print(json.dumps({k: record[k] for k in ['group', 'file_count', 'bytes', 'excluded']}))
