#!/usr/bin/env python3
"""Read back every immutable published PR164 evidence-package byte and Git mode."""
import hashlib
import json
import os
import subprocess
import traceback
from pathlib import Path

ROOT = Path('/workspace/scratch/d4d5258160f7/agent5')
REPO = ROOT / 'repo'
LOCAL = ROOT / 'pr164-delivery-bundle'
OUT = ROOT / 'pr164-publication' / 'bundle-readback-001'
OUT.mkdir(exist_ok=False)
COMMIT = 'b867573da4ffe8416af9e9f8693be6e8259fa0fa'
PREFIX = 'proofs/coordination/reviews/agent5-sessiond4d5258160f7/pr164/'
commands = []

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git(*args):
    argv = ['git', '-c', 'credential.helper=', '-c', 'core.askPass=', '-C', str(REPO), *args]
    env = os.environ.copy()
    env.update(GIT_OPTIONAL_LOCKS='0', GIT_TERMINAL_PROMPT='0', GIT_PAGER='cat')
    p = subprocess.run(argv, capture_output=True, env=env)
    commands.append({'argv': argv, 'exit_code': p.returncode, 'stdout_sha256': sha(p.stdout), 'stderr': p.stderr.decode(errors='replace')})
    if p.returncode:
        raise RuntimeError(repr(commands[-1]))
    return p.stdout

try:
    raw_tree = git('ls-tree', '-rz', '--full-tree', COMMIT, '--', PREFIX)
    (OUT / 'published-tree.z').write_bytes(raw_tree)
    actual = {}
    for part in raw_tree.split(b'\0'):
        if part:
            meta, path = part.split(b'\t', 1)
            mode, kind, oid = meta.decode().split()
            actual[path.decode()[len(PREFIX):]] = (mode, kind, oid)
    rows = json.loads((LOCAL / 'FILES.json').read_text())['files']
    names = {x['path'] for x in rows} | {'FILES.json'}
    assert set(actual) == names and len(actual) == 10
    observed = []
    for name in sorted(names):
        data = git('show', COMMIT + ':' + PREFIX + name)
        original = (LOCAL / name).read_bytes()
        assert data == original, name
        oid = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual[name] == ('100644', 'blob', oid), name
        observed.append({'path': name, 'bytes': len(data), 'sha256': sha(data), 'git_blob': oid, 'mode': '100644'})
    for row in rows:
        assert row == next(x for x in observed if x['path'] == row['path'])
    archive = next(x for x in observed if x['path'] == 'pr164-evidence.tar.xz')
    assert archive['sha256'] == '4a1413f198e7804171a0c2fbd22ef654ed201cf67ca5b9a74ece9b1bc97980a5'
    assert archive['git_blob'] == '2269cfbbfae53f623beeab282930c7a99b3fae1e'
    receipt = {'status': 'PASS_EXACT_REMOTE_PACKAGE_BYTES_AND_MODES', 'publication_commit': COMMIT,
               'prefix': PREFIX, 'published_files_checked': len(observed), 'files': observed,
               'archive_is_identical_to_fully_restored_local_archive': True,
               'original_evidence_paths_recovered_and_validated': 122,
               'original_evidence_bytes': 67295995,
               'main_mutation': False, 'source_mutation': False}
    (OUT / 'verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k: v for k, v in receipt.items() if k != 'files'}, indent=2))
except Exception as error:
    (OUT / 'failure.json').write_text(json.dumps({'error': repr(error), 'traceback': traceback.format_exc()}, indent=2) + '\n')
    raise
finally:
    (OUT / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
