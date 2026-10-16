from pathlib import Path
import hashlib
import json
import re

root = Path('/workspace/scratch/f8aedc6d7adf')
base = root / 'claims-agent6/cycle-dev'
folder = root / 'agent6-work/proofs/contributions/agent-6/exterior-coordinate-dynamics-20261016'
expected = {
    'CoordinateDynamics': '8f37d2991087c3c232e9e5a09c440e266672403fe895af59d770e2f90a72a05b',
    'CoordinateSign': '9142e73dff4b25fd43dee0f708e5681a47f42b0630329512934916f370f0da21',
    'CoordinateCycle': '0b135c2b14c04cf3d980fc7cc2bd6852e65406edb0a6cdaa377a0fa427163f21',
}

def record(path):
    data = path.read_bytes()
    return {
        'path': str(path), 'bytes': len(data),
        'sha256': hashlib.sha256(data).hexdigest(),
        'git_blob': hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest(),
    }

pins = {name: record(folder / (name + '.lean')) for name in expected}
for name, pin in pins.items():
    assert pin['sha256'] == expected[name], (name, pin)

module = (folder / 'CoordinateCycle.lean').read_text()
forbidden = re.findall(r'\b(?:sorry|admit|axiom|sorryAx|native_decide|ofReduceBool|skipKernelTC|unsafe|partial)\b', module)
assert forbidden == [], forbidden
exports = re.findall(r'^(?:@\[[^\]]*\]\s*)?(def|theorem)\s+([A-Za-z_][\w\']*)', module, re.M)
namespace = 'Agent6.ExteriorCoordinates.'
exports = {namespace + name: kind for kind, name in exports}

audit_dir = base / 'attempts/CoordinateCycleAudit-002'
audit_log = (audit_dir / 'compile.log').read_text()
entries = re.findall(r'^AUDIT_DECLARATION CoordinateCycle (\S+) : \[([^\]]*)\]', audit_log, re.M)
actual = {name: [ax.strip() for ax in axioms.split(',') if ax.strip()] for name, axioms in entries}
assert len(actual) == len(entries) == 74
assert set(exports) <= set(actual)
allowed = {'propext', 'Classical.choice', 'Quot.sound'}
assert all(set(axioms) <= allowed for axioms in actual.values())
summary = re.findall(r'^FULL_MODULE_AUDIT theorems=(\d+) safeDefinitions=(\d+) unsafeImplementations=(\d+) union=\[([^\]]*)\]', audit_log, re.M)
assert len(summary) == 1
theorems, definitions, unsafe, union = summary[0]
assert [int(theorems), int(definitions), int(unsafe)] == [58, 16, 23]
assert {ax.strip() for ax in union.split(',')} == allowed

commands = []
for stage in ['CoordinateSign-001', 'CoordinateCycle-005', 'CoordinateCycleAudit-002']:
    path = base / 'attempts' / stage / 'verification.json'
    receipt = json.loads(path.read_text())
    assert receipt['exit_code'] == 0
    assert '--trust=0' in receipt['argv']
    commands.append({'stage': stage, 'receipt': record(path), 'command': receipt['argv'],
                     'exit_code': 0, 'log': record(path.parent / 'compile.log')})

prior_review = {
    'REVIEW.md': '08d30d7803ecb55f426d7bd1669f0cc460a9156e724590d78934835f312381ee',
    'check_signed_beta.py': 'c07462f084925a2df948f2a1cb44f90b1cfd1ebf9b9499d0d791074a4d76c212',
    'signed-beta-controls.json': 'b290730335962462a97971ade4b7ea19af16d4b8befd2688f13b7e3babad9ecb',
}
for name, sha in prior_review.items():
    assert record(root / 'claims-agent6/coordinate-review' / name)['sha256'] == sha

report = {
    'status': 'KERNEL_PASS_SOURCE_FROZEN',
    'role': 'Agent #6 finite-cycle theorem author',
    'owned_source': pins['CoordinateCycle'],
    'source_pins': pins,
    'toolchain': {
        'version': 'Lean 4.19.0, commit 6caaee842e94',
        'binary': record(root / 'runtime-agent6/lean-4.19.0-linux/bin/lean'),
        'trust_level': 0,
    },
    'explicit_exports': exports,
    'explicit_theorem_count': sum(kind == 'theorem' for kind in exports.values()),
    'explicit_definition_count': sum(kind == 'def' for kind in exports.values()),
    'audit': {
        'source': record(base / 'CoordinateCycleAudit.lean'),
        'all_theorem_constants': 58,
        'safe_definition_constants': 16,
        'unsafe_compiler_implementations_recorded_separately': 23,
        'allowed_axiom_union': sorted(allowed),
        'audited_declarations': actual,
        'explicit_exports_all_audited': True,
        'first_failed_audit': 'attempts/CoordinateCycleAudit-001',
        'audit_correction': 'The first audit also applied the proof axiom allowlist to unsafe compiler-generated definitions. The corrected audit retains and logs those implementation artifacts separately, checks every theorem and safe definition, and rejects every safe custom axiom.',
    },
    'successful_commands': commands,
    'build_scope': 'Fresh Sign rebuild against final Dynamics, followed by Cycle compilation and complete Cycle theorem/safe-definition audit. Existing pinned upstream objects were reused; the runtime specialist performs the independent fresh combined closure.',
    'failed_sources_and_logs_preserved': ['CoordinateCycle-001', 'CoordinateCycle-003', 'CoordinateCycle-004', 'CoordinateCycleAudit-001'],
    'prior_numerical_algebra_review_unchanged': prior_review,
    'semantic_scope': {
        'map': 'The imported literal finite outerNext map on arbitrary natural phases and natural-coefficient lists.',
        'telescope': 'All finite lengths, including zero, with no phase or coefficient restrictions.',
        'closed_zero_sum': 'Literal state return suffices; equal beta endpoints and constant-band padding returns also suffice.',
        'both_signs': 'Positive period, literal state return, and positive initial phase; the nonneutral-phase corollary follows. Only the initial nonzero increment is used.',
        'weighted_balance': 'Overflow is counted by a zero/nonzero carry indicator. No assumption that the carry is at most one is needed.',
        'excluded_claims': ['cycle existence', 'global acyclicity', 'ordinary integer orbit correspondence', 'experiments as universal proof'],
    },
    'git_mutations': False,
}
(base / 'RESULT.json').write_text(json.dumps(report, indent=2) + '\n')
(base / 'exported-axioms.json').write_text(json.dumps({name: actual[name] for name in exports}, indent=2) + '\n')
print(json.dumps({'result': str(base / 'RESULT.json'), 'source': pins['CoordinateCycle'],
                  'theorems': report['explicit_theorem_count'], 'definitions': report['explicit_definition_count'],
                  'status': report['status']}, indent=2))
