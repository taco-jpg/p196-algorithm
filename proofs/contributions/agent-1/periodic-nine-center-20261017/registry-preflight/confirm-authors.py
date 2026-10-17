#!/usr/bin/env python3
"""Check frozen author evidence without invoking Lean or changing source."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
CONTRIBUTION = HERE.parent
COMPILER = '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}
SPECS = [
    ('Agent1PeriodicCenterWrap', 'wrap-author', 'attempt-002',
     'dd0cba7b9f1fd97eb733d8815e1059440040a464508a3a3a265bf11084383523',
     '6e33969cde94f82d6b4b6067cf2ae921d3ec36204a6c3170f65588a525c3482f', 6, 11),
    ('Agent1PeriodicNinesCenter', 'center-author', 'attempt-004',
     '7d6d27081c480345e796c6b8e950c08a5ce0d7207e4030d24e504db4abde695e',
     'ee014d316c85bbda93f60ba0b4d57cbb4ffebf411925ebcc338c58b12d48aa98', 12, 16),
]

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def load(path):
    return json.loads(path.read_bytes())

modules = {}
for name, author, attempt, expected, receipt_sha, count, deps in SPECS:
    base = CONTRIBUTION / author
    run = base / attempt
    source = ROOT / 'proofs' / (name + '.lean')
    assert sha(source.read_bytes()) == expected
    assert source.read_bytes() == (run / source.name).read_bytes()
    receipt_path = base / 'frozen-receipt.json'
    assert sha(receipt_path.read_bytes()) == receipt_sha
    receipt = load(receipt_path)
    assert receipt['source_sha256'] == expected
    result = load(run / 'result.json')
    assert result['exit_code'] == 0 and result['source_sha256'] == expected
    assert result['dependency_count'] == deps
    assert result['dependency_objects_reused'] and not result['fresh_full_closure']
    commands = load(run / 'commands.json')
    assert [c['name'] for c in commands] == ['compile', 'audit']
    for command in commands:
        assert command['exit_code'] == 0
        assert command['compiler_sha256'] == COMPILER
        assert {'--trust=0', '-j1', '-DElab.async=false'} <= set(command['command'])
        assert command['cwd'] == str(run)
        assert command['LEAN_PATH']
    audit = (run / 'audit.log').read_text()
    rows = re.findall(r'^AUDIT_THEOREM (\S+)\s*:\s*\[([^\]]*)\]', audit, re.M)
    assert len(rows) == count and len({n for n, _ in rows}) == count
    union = set()
    for _, axioms in rows:
        names = {a.strip() for a in axioms.split(',') if a.strip()}
        assert names <= ALLOWED
        union |= names
    assert f'MODULE_AUDIT theorems={count}' in audit
    public = receipt.get('public_declarations', receipt.get('public_endpoints'))
    assert set(public) <= {n for n, _ in rows}
    compile_log = (run / 'compile.log').read_text()
    for endpoint in public:
        assert f"'{endpoint}' depends on axioms:" in compile_log or \
               f"'{endpoint}' depends on axioms:" in audit
    checked_files = []
    if author == 'wrap-author':
        for relative, digest in receipt['files_sha256'].items():
            assert sha((base / relative).read_bytes()) == digest
            checked_files.append(relative)
    else:
        manifest = load(base / 'manifest.json')
        assert sha((base / 'manifest.json').read_bytes()) == receipt['manifest_sha256']
        for entry in manifest['files']:
            data = (base / entry['path']).read_bytes()
            assert len(data) == entry['bytes'] and sha(data) == entry['sha256']
            checked_files.append(entry['path'])
    evidence = [receipt_path, run / 'result.json', run / 'commands.json',
                run / 'audit.log', run / 'compile.log', run / 'dependencies.json']
    if author == 'center-author':
        evidence.append(base / 'manifest.json')
    modules[name] = {
        'source_sha256': expected,
        'compile_status': 'PASS', 'new_module_audit_status': 'PASS',
        'strict_attempt': attempt, 'theorem_constants': count,
        'safe_definitions': 0, 'runtime_entries': 0,
        'actual_axiom_union': sorted(union), 'public_endpoints': public,
        'dependency_objects_reused': deps, 'fresh_full_closure': False,
        'author_manifest_entries_checked': checked_files,
        'receipts': [{'path': str(p.relative_to(ROOT)), 'sha256': sha(p.read_bytes())}
                     for p in evidence],
    }
target = HERE / 'author-confirmation.json'
assert not target.exists()
target.write_text(json.dumps({
    'author_confirmation_received': True,
    'qualification': 'Actual frozen sources, author command/log receipts and sealed evidence checked. '
                     'No Lean execution by this preflight; fresh combined verification remains pending.',
    'script_sha256': sha(Path(__file__).read_bytes()),
    'modules': modules,
}, indent=2) + '\n')
print(json.dumps({'status': 'PASS', 'module_count': len(modules),
                  'author_confirmation_sha256': sha(target.read_bytes())}, indent=2))
