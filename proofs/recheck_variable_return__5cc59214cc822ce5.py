"""Replay the frozen variable-return certificates in a disposable copy."""
from pathlib import Path
import hashlib, json, os, shutil, subprocess, sys, time

HERE = Path(__file__).resolve().parent
PASS = HERE.parent
PROJECT = PASS.parents[1]
SOURCE = PASS / 'variable_return'
REPLAY = HERE / 'variable_return_replay'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
manifest_path = SOURCE / 'FROZEN_MANIFEST.json'
manifest_hash = sha(manifest_path)
manifest = json.loads(manifest_path.read_text())

def check_frozen():
    assert sha(manifest_path) == manifest_hash
    for row in manifest['files']:
        p = SOURCE / row['path']
        assert p.stat().st_size == row['bytes'] and sha(p) == row['sha256'], str(p)
    for row in manifest['dependency_sources']:
        assert sha(PROJECT / row['path']) == row['sha256'], row['path']

check_frozen()
REPLAY.mkdir(exist_ok=True)
for row in manifest['files']:
    target = REPLAY / row['path']
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE / row['path'], target)
checks = [
    ('check_affine_catalogue.py', ['affine_catalogue_audit.json']),
    ('check_regeneration_graph.py', ['regeneration_interface_audit.json', 'regeneration_interface_ranks.json.gz']),
    ('check_regeneration_gate.py', ['regeneration_gate_audit.json']),
]
rows = []
logs = []
for script, outputs in checks:
    start = time.monotonic()
    result = subprocess.run([sys.executable, '-B', script], cwd=REPLAY,
                            text=True, capture_output=True,
                            env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    row = {'script': script, 'exit_code': result.returncode,
           'seconds': time.monotonic() - start}
    logs.extend([json.dumps(row), result.stdout, result.stderr])
    (HERE / 'variable_return_recheck.log').write_text('\n'.join(logs))
    assert result.returncode == 0, result.stdout + result.stderr
    row['reproduced_outputs'] = {}
    for name in outputs:
        assert sha(REPLAY / name) == sha(SOURCE / name), name
        row['reproduced_outputs'][name] = sha(REPLAY / name)
    rows.append(row)
    print(json.dumps(row), flush=True)
check_frozen()
receipt = {
    'status': 'PASS', 'frozen_manifest_sha256': manifest_hash,
    'source_files': manifest['files'], 'dependency_sources': manifest['dependency_sources'],
    'copied_replays': rows,
    'written_proofs_reviewed': [
        'VARIABLE_RETURN_THEOREMS.md', 'POSITIVE_REGENERATION_GATE.md',
        'affine target equality and the all-time width-potential bound',
        'arbitrary-gap mixed-carry graph identities and descending ranks',
        'actual no-overflow gate including gap zero; failed nine-step return',
    ],
    'verification_scope': 'All-parameter written proofs and independent exact certificates; finite multiplicative and prefix probes retain their finite scope.',
    'no_source_files_mutated': True,
    'excluded_duplicate_infrastructure': ['variable_return_replay/'],
    'decimal_lychrel_existence_proved': False,
}
(HERE / 'variable_return_review.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({'status': 'PASS', 'source_files': len(manifest['files']),
                  'manifest_sha256': manifest_hash}), flush=True)
