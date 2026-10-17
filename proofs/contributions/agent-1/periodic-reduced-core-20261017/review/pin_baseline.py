#!/usr/bin/env python3
"""Seal objects from this review's successful fresh dependency build."""
from pathlib import Path
import hashlib
import json

review = Path(__file__).resolve().parent
evidence = review / 'baseline-001'
build = Path('/workspace/p196-agent1-session-20261016/reduced-core-review-build-001')
identity = json.loads((evidence / 'baseline-source-identity.json').read_text())
verification = review / 'baseline-inventory-review-001/verification.json'
result = json.loads(verification.read_text())
commands = json.loads((evidence / 'results.json').read_text())
assert result['status'] == 'PASS' and result['source_modules'] == 46
assert result['trust'] == 0 and not result['final_package_pass_claimed']
assert len(commands) == 47 and all(c['exit_code'] == 0 for c in commands)
sha = lambda b: hashlib.sha256(b).hexdigest()
objects = {}
for entry in identity['sources']:
    module = entry['module']
    assert sha((build / (module + '.lean')).read_bytes()) == entry['sha256']
    raw = (build / (module + '.olean')).read_bytes()
    objects[module] = {'bytes': len(raw), 'sha256': sha(raw),
                       'source_sha256': entry['sha256']}
out = {
    'status': 'BASELINE_FRESH_BUILD_AND_AUDIT_PASS',
    'source_commit': identity['source_commit'], 'module_count': 46, 'trust': 0,
    'external_objects_reused': False, 'build_directory': str(build),
    'evidence_directory': str(evidence), 'final_package_pass_claimed': False,
    'new_package_modules_compiled': [],
    'theorem_constants_audited': result['theorems_audited'],
    'safe_definitions_audited': result['safe_definitions_audited'],
    'theorem_axiom_union': result['axiom_union'],
    'safe_definition_axiom_union': result['safe_definition_axiom_union'],
    'compiler': result['compiler'], 'objects': objects,
    'baseline_replay_sha256': sha((evidence / 'replay.py').read_bytes()),
    'verification_sha256': sha(verification.read_bytes()),
    'commands_sha256': sha((evidence / 'results.json').read_bytes()),
    'reviewer_role': result['reviewer'],
    'verification_path': str(verification),
    'retained_driver_postcheck_failure': True,
    'inventory_classification_only_recovery': True,
    'pin_script_sha256': sha(Path(__file__).read_bytes()),
}
target = review / 'baseline-objects.json'
assert not target.exists(), 'Preserve earlier object receipts'
target.write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({'status': out['status'], 'module_count': len(objects),
                  'sha256': sha(target.read_bytes())}))
