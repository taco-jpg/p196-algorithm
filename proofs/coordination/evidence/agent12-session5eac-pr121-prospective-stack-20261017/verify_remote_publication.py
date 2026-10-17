#!/usr/bin/env python3
"""Verify the published own-path delta and exact remote archive byte identities."""
import base64
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile

OUT = Path(__file__).resolve().parent
REPO = OUT.parent.parent / 'agent12-integration'
COMMIT = 'e0fcabbd8e7963d3aec2091fa1ce6e1da83f5587'
PARENT = '025eb1f6193356371b9466720d176909ab232958'
PREFIX = 'proofs/coordination/evidence/agent12-session5eac-pr121-prospective-stack-20261017/'
TASK = 'proofs/coordination/tasks/agent12-session5eac-pr121-prospective-stack-20261017.json'
payload = json.loads((OUT / 'publication_transport.json').read_text())
commands = []
def run(args, binary=False):
    r = subprocess.run(['git', '-C', str(REPO), *args], capture_output=True, env={**os.environ, 'GIT_NO_LAZY_FETCH': '1'})
    row = {'argv': ['git', '-C', str(REPO), *args], 'exit_code': r.returncode, 'stderr': r.stderr.decode()}
    if binary:
        row.update(stdout_bytes=len(r.stdout), stdout_sha256=hashlib.sha256(r.stdout).hexdigest(), stdout_retention='Exact public archive blob already published in this commit; full body equals the named local/public archive. Recover with the recorded git command.')
    else:
        row['stdout'] = r.stdout.decode()
    commands.append(row)
    assert r.returncode == 0, row
    return r.stdout

delta = [line.split('\t') for line in run(['diff-tree', '--no-commit-id', '--name-status', '-r', PARENT, COMMIT]).decode().splitlines()]
expected_paths = {PREFIX + name for name in payload['text_files']} | {PREFIX + name for name in payload['binary_files']}
assert set((status, path) for status, path in delta) == {('A', p) for p in expected_paths} | {('M', TASK)}
assert run(['show', '-s', '--format=%P', COMMIT]).decode().strip() == PARENT
entries = {}
for line in run(['ls-tree', '-r', COMMIT, '--', PREFIX, TASK]).decode().splitlines():
    meta, path = line.split('\t', 1)
    mode, kind, oid = meta.split()
    entries[path] = {'mode': mode, 'type': kind, 'oid': oid}
text_rows = []
for name, text in payload['text_files'].items():
    data = text.encode()
    oid = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert entries[PREFIX + name] == {'mode': '100644', 'type': 'blob', 'oid': oid}
    text_rows.append({'path': PREFIX + name, 'git_blob': oid, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'api_exact_text_readback': 'PASS in separately retained parent tool receipt'})
binary_rows = []
for name, encoded in payload['binary_files'].items():
    expected = base64.b64decode(encoded)
    actual = run(['cat-file', 'blob', entries[PREFIX + name]['oid']], binary=True)
    assert actual == expected == (OUT / name).read_bytes()
    mf = json.loads((OUT / name.replace('.tar.xz', '.files.json')).read_text())
    rows = mf['files']
    with tarfile.open(fileobj=io.BytesIO(actual), mode='r:xz') as tf:
        expected_members = {(r.get('archive_member') or mf['archive_root'] + '/' + r['path']): r for r in rows}
        assert set(m.name for m in tf.getmembers()) == set(expected_members)
        for m in tf.getmembers():
            assert m.isfile()
            data = tf.extractfile(m).read()
            row = expected_members[m.name]
            assert len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256']
    binary_rows.append({'path': PREFIX + name, 'git_blob': entries[PREFIX + name]['oid'], 'bytes': len(actual), 'sha256': hashlib.sha256(actual).hexdigest(), 'exact_remote_local_byte_equality': True, 'verified_members': len(rows)})
result = {'status': 'PASS', 'commit': COMMIT, 'parent': PARENT, 'delta': delta, 'files_added': 10, 'own_task_modified': 1, 'other_paths_changed': 0,
          'text_files': text_rows, 'binary_files': binary_rows, 'commands': commands, 'lean_execution': 'NOT_RUN',
          'method': 'Immutable public commit fetched with blob:none; two exact archive blobs fetched separately with no refs changed. Text/API readback already matched all eight text files and own task. This script verifies native path/OID identities and both archive bodies plus every recovered member.'}
(OUT / 'REMOTE_PUBLICATION_RECEIPT.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'commit': COMMIT, 'delta_entries': len(delta), 'binary_archives': binary_rows, 'git_command_count': len(commands)}))
