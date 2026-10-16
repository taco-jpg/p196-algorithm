#!/usr/bin/env python3
"""Replay only corrected postchecks of the already completed fresh Lean run."""
from pathlib import Path
import ast
import hashlib
import json
import re
import subprocess

root = Path('/workspace/p196-agent1-width-20261016')
review = root / 'proofs/contributions/agent-1/periodic-width-projection-20261016/review'
evidence = review / 'clean-001'
build = Path('/workspace/p196-agent1-session-20261016/periodic-width-review-clean-001')
recovery = evidence / 'postcheck-recovery-001'
recovery.mkdir(exist_ok=False)
sha = lambda b: hashlib.sha256(b).hexdigest()
(recovery / 'recover-postcheck.py').write_bytes(Path(__file__).read_bytes())
(recovery / 'replay.py').write_bytes((review / 'replay.py').read_bytes())
script = (recovery / 'replay.py').read_text()
ast.parse(script)
assert not (evidence / 'verification.json').exists()
identity = json.loads((evidence / 'final-source-identity.json').read_text())
manifest = identity['sources']
results = json.loads((evidence / 'results.json').read_text())
assert len(manifest) == 30 and len(results) == 31
assert [r['module'] for r in results] == [s['module'] for s in manifest] + ['ReviewAudit']
for result in results:
    assert result['exit_code'] == 0 and not result['timed_out']
    assert '--trust=0' in result['command']
    assert sha((evidence / (result['module'] + '.log')).read_bytes()) == result['log_sha256']
for entry in manifest:
    data = (root / entry['path']).read_bytes()
    assert sha(data) == entry['sha256']
    assert data == (build / (entry['module'] + '.lean')).read_bytes()
    assert data == (evidence / 'compiled-sources' / (entry['module'] + '.lean')).read_bytes()
    assert data == subprocess.check_output(
        ['git', 'show', identity['source_commit'] + ':' + entry['path']], cwd=root)
compiler = json.loads((evidence / 'compiler.json').read_text())
assert sha(Path(compiler['path']).read_bytes()) == compiler['sha256']
assert (build / 'ReviewAudit.lean').read_bytes() == (evidence / 'ReviewAudit.lean').read_bytes()
original_driver = (evidence / 'replay.py').read_bytes()
assert sha(original_driver) == '7c149b487737e775b9402244e115af62fdf751f476e3740e16e84ddab5a6cb33'

failure = {
    'status': 'REJECTED_WRAPPER_POSTCHECK',
    'stage': 'After all30 source compilations and ReviewAudit exited zero',
    'exception': "AssertionError: ('Agent1PeriodicWidthLift', ['admit'])",
    'cause': 'Raw source regex matched admit inside a documentation comment',
    'source_line': 'together. No abstract edge is asserted to admit a finite-word realization. -/',
    'source_sha256': 'a3897a4d7dc58b2f33efb519be75ea5f7ef61b8e6c4602749c0249de52b49978',
    'original_executed_driver_sha256': sha(original_driver),
    'full_lean_results_preserved': True,
    'prior_verification_claim': False,
}
(recovery / 'original-wrapper-failure.json').write_text(json.dumps(failure, indent=2) + '\n')
post = script.split('# BEGIN POSTCHECK\n', 1)[1]
helper = post.split('\nexports = []\n', 1)[0]
scope = globals().copy()
exec(compile(helper, str(recovery / 'replay.py') + ':token-helper', 'exec'), scope)
scan = scope['lean_code_tokens']
pattern = r'\b(?:sorry|admit|native_decide|sorryAx|axiom)\b|Lean\.ofReduceBool'
controls = [
    ('/- admit /- axiom -/ sorry -/\n-- native_decide\ntheorem ok : True := by trivial', []),
    ('def text := "admit /- sorry -/"', []),
    ('theorem bad : False := by admit', ['admit']),
    ('axiom bad : False', ['axiom']),
    ('theorem bad : True := by native_decide', ['native_decide']),
    ('theorem bad : False := by sorry', ['sorry']),
]
checks = []
for source, expected in controls:
    found = re.findall(pattern, scan(source))
    assert found == expected
    checks.append({'input_sha256': sha(source.encode()), 'expected': expected, 'actual': found})
for bad in ['/- unterminated', 'def x := "unterminated']:
    try:
        scan(bad)
    except AssertionError:
        checks.append({'input_sha256': sha(bad.encode()), 'unterminated_input_rejected': True})
    else:
        raise AssertionError('Malformed token-scan control unexpectedly accepted')
(recovery / 'tokenizer-controls.json').write_text(json.dumps(checks, indent=2) + '\n')
before = {p.name: sha(p.read_bytes()) for p in evidence.glob('*.log')}
exec(compile(post, str(recovery / 'replay.py') + ':postcheck', 'exec'), scope)
assert before == {p.name: sha(p.read_bytes()) for p in evidence.glob('*.log')}
receipt = {
    'status': 'PASS',
    'stage': 'Corrected source-token scan and complete original postcheck/inventory',
    'source_commit': identity['source_commit'],
    'no_lean_process_executed_in_recovery': True,
    'all31_existing_strict_lean_commands_verified_zero': True,
    'all_source_inputs_and_lean_logs_unchanged': True,
    'original_driver_sha256': sha(original_driver),
    'corrected_portable_driver_sha256': sha(script.encode()),
    'executed_recovery_driver_sha256': sha(Path(__file__).read_bytes()),
    'verification_sha256': sha((evidence / 'verification.json').read_bytes()),
    'implementation_inventory_sha256': sha((evidence / 'implementation-inventory.json').read_bytes()),
}
(recovery / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
