#!/usr/bin/env python3
"""Pin actual frozen author receipts without executing Lean."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
CONTRIBUTION = HERE.parent
COMPILER_SHA = '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
SPECS = [
    ('Agent1PeriodicNinesPath', 'path-author', 'attempt-002',
     '72518762371d6174e300104d817b0e4cbe7a72d2f0f548ce6b6a9e1c79717866',
     16, 0, 0, ['manifest.json', 'README.md']),
    ('Agent1PeriodicNinesCycle', 'numeric-author', 'attempt-003',
     '2bcd823a039a8fd1e9a4f54c01ae367cb2e46f97b96b9d31e29336342953dafd',
     7, 0, 0, ['frozen-receipt.json', 'origin-summary.json']),
]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


modules = {}
for suffix, directory, attempt, source_sha, theorems, safe, runtime, receipts in SPECS:
    name = suffix
    source = ROOT / 'proofs' / (name + '.lean')
    author = CONTRIBUTION / directory
    run = author / attempt
    raw = source.read_bytes()
    assert sha(raw) == source_sha
    assert (run / source.name).read_bytes() == raw
    result = json.loads((run / 'result.json').read_bytes())
    assert result['exit_code'] == 0 and result['source_sha256'] == source_sha
    commands = json.loads((run / 'commands.json').read_bytes())
    assert [c['name'] for c in commands] == ['compile', 'audit']
    for command in commands:
        assert command['exit_code'] == 0
        assert command['compiler_sha256'] == COMPILER_SHA
        assert '--trust=0' in command['command'] and '-j1' in command['command']
        assert '-DElab.async=false' in command['command']
    audit = (run / 'audit.log').read_text()
    assert 'MODULE_AUDIT' in audit
    # Counts below are the authors' full origin audits, not preflight execution.
    paths = [author / r for r in receipts] + [run / r for r in
        ['result.json', 'commands.json', 'compile.log', 'audit.log']]
    modules[name] = {
        'source_sha256': source_sha,
        'source_git_blob': hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest(),
        'compile_status': 'PASS', 'new_module_audit_status': 'PASS',
        'strict_trust_zero': True, 'author_attempt': attempt,
        'origin_theorem_constants': theorems, 'safe_definitions': safe,
        'generated_runtime_implementations': runtime,
        'axiom_union': ['propext', 'Classical.choice', 'Quot.sound'],
        'fresh_full_closure': False,
        'receipts': [{'path': str(p.relative_to(ROOT)), 'sha256': sha(p.read_bytes())}
                     for p in paths],
    }

out = {
    'author_confirmation_received': True,
    'confirmation_basis': 'Explicit frozen-source messages from both authors, '
                          'checked against their immutable source snapshots, '
                          'actual successful compile/audit command records and sealed receipts.',
    'compiler_sha256': COMPILER_SHA,
    'modules': modules,
    'total_origin_theorems': 23, 'total_safe_definitions': 0,
    'total_generated_runtime_implementations': 0,
    'lean_execution_performed_by_this_script': False,
    'fresh_combined_verification': 'PENDING',
    'script_sha256': sha(Path(__file__).read_bytes()),
}
target = HERE / 'author-confirmation.json'
assert not target.exists(), 'Do not overwrite an existing confirmation'
target.write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({'status': 'AUTHOR_RECEIPTS_PINNED', 'modules': len(modules),
                  'sha256': sha(target.read_bytes())}))
