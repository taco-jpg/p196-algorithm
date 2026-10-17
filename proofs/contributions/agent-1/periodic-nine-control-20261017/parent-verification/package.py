#!/usr/bin/env python3
"""Copy and validate existing canonical text evidence; never execute Lean."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
ORIGINAL = Path('/workspace/p196-agent1-session-20261016/nine-control-parent-clean-001')
CONSOLE = ORIGINAL.with_name(ORIGINAL.name + '.console.log')
COMMIT = 'bfa0247b78845558d087eec08e113e91decaaddb'
PROJECT = 'agent1-periodic-nine-control'
REGISTRY = 'proofs/Agent1PeriodicNinesExtraStrip.registry.json'
CHECKER = 'proofs/verify_project__214bf7673efe116b.py'
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda p, x: p.write_text(json.dumps(x, indent=2) + '\n')
published = lambda path: subprocess.check_output(['git', 'show', COMMIT + ':' + path], cwd=ROOT)

manifest_bytes = (ORIGINAL / 'FILES.json').read_bytes()
manifest = json.loads(manifest_bytes)
report_bytes = (ORIGINAL / 'verification.json').read_bytes()
report = json.loads(report_bytes)
project = report['projects'][PROJECT]
assert report['status'] == project['status'] == 'PASS'
assert report['source_commit'] == COMMIT and report['source_tree_clean'] is True
assert len(manifest) == 33
for path, rec in manifest.items():
    assert not Path(path).is_absolute() and '..' not in Path(path).parts
    assert Path(path).suffix in ['.lean', '.log', '.json']
    data = (ORIGINAL / path).read_bytes()
    assert len(data) == rec['bytes'] and sha(data) == rec['sha256'], path
assert len(project['sources']) == len(project['build_order']) == 15
assert len(project['commands']) == 16
assert all(c['exit_code'] == 0 for c in project['commands'])
assert project['theorem_count'] == 1348
assert project['axiom_union'] == '[Classical.choice, Quot.sound, propext]'
assert len(project['unsafe_implementation_axioms']) == 13
for command in project['commands']:
    assert not any(x.startswith('--trust') for x in command['argv'])
    assert '-j1' in command['argv'] and '-DElab.async=false' in command['argv']
    assert sha((ORIGINAL / command['log']).read_bytes()) == command['log_sha256']
log = (ORIGINAL / PROJECT / 'logs/ProjectAudit.log').read_text()
assert len(re.findall(r'^AUDIT_THEOREM ', log, re.M)) == 1348
assert 'FULL_MODULE_AUDIT theorems=1348 union=[Classical.choice, Quot.sound, propext]' in log
assert len(CONSOLE.read_text().splitlines()) == 16
assert all(line.endswith(' exit=0') for line in CONSOLE.read_text().splitlines())

registry = (ROOT / REGISTRY).read_bytes()
checker = (ROOT / CHECKER).read_bytes()
assert registry == published(REGISTRY)
assert checker == published(CHECKER)
assert sha(registry) == report['registry_sha256']
assert sha(checker) == 'c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a'
pins = []
registry_modules = json.loads(registry)['projects'][PROJECT]['modules']
assert set(project['sources']) == set(project['build_order']) == set(registry_modules)
for name, rec in project['sources'].items():
    source = (ROOT / rec['path']).read_bytes()
    built = (ORIGINAL / PROJECT / 'source' / (name + '.lean')).read_bytes()
    committed = published(rec['path'])
    registered = registry_modules[name]
    assert source == built == committed
    assert sha(source) == rec['sha256'] == rec['build_sha256'] == registered['sha256']
    assert rec['path'] == registered['path'] and rec['imports'] == registered['imports']
    blob = hashlib.sha1(b'blob ' + str(len(source)).encode() + b'\0' + source).hexdigest()
    assert blob == registered['git_blob']
    pins.append({'module': name, 'path': rec['path'], 'sha256': sha(source),
        'git_blob': blob, 'published_bytes_equal': True, 'compiled_bytes_equal': True,
        'current_bytes_equal': True, 'registry_pin_equal': True})

dest = HERE / 'parent-clean-001'
dest.mkdir(exist_ok=False)
for path in manifest:
    target = dest / path
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ORIGINAL / path, target)
    assert target.read_bytes() == (ORIGINAL / path).read_bytes()
(dest / 'FILES.json').write_bytes(manifest_bytes)
(HERE / 'parent-console.log').write_bytes(CONSOLE.read_bytes())
(HERE / 'registry.json').write_bytes(registry)
(HERE / 'canonical-verifier.py').write_bytes(checker)
dump(HERE / 'publication-source-receipt.json', {'status': 'PASS_SOURCE_IDENTITY',
    'published_source_commit': COMMIT, 'module_count': 15,
    'registry_path': REGISTRY, 'registry_sha256': sha(registry),
    'checker_path': CHECKER, 'checker_sha256': sha(checker), 'sources': pins,
    'lean_executed_by_packager': False})
dump(HERE / 'parent-launch.json', {'evidence_kind': 'Parent executor transcript confirmation',
    'argv': ['python3', CHECKER, '--lean', '/workspace/p196-tools/lean-4.19.0-linux/bin/lean',
        '--output', str(ORIGINAL), '--project', PROJECT, '--registry', REGISTRY],
    'cwd': str(ROOT), 'tool_session_id': 10353, 'actual_exit_code': 0,
    'per_lean_argv_source': 'parent-clean-001/verification.json',
    'confirmation': 'Original parent executor explicitly supplied this launch argv and exit readback; the packager did not rerun it.'})
dump(HERE / 'parent-result-addendum.json', {'status': 'PASS_PRESERVED_PARENT_RUN',
    'original_source_commit': report['source_commit'],
    'original_source_tree_clean': report['source_tree_clean'],
    'clean_field_limit': 'Canonical verifier uses tracked-file git status; untracked files are excluded. Original value unchanged.',
    'all_source_and_registry_bytes_match_published_commit': True,
    'modules': 15, 'commands': 16, 'theorem_constants': 1348,
    'theorem_axiom_union': ['propext', 'Classical.choice', 'Quot.sound'],
    'separate_unsafe_implementation_axioms': 13,
    'safe_definition_audit_claimed_here': False,
    'explicit_trust_zero': False,
    'flags_limit': 'Actual Lean argv contains no --trust=0. Canonical execution is not relabeled as the separate strict review.',
    'original_started_at_epoch': report['started_at_epoch'],
    'original_finished_at_epoch': report['finished_at_epoch'],
    'original_started_at_utc': datetime.datetime.fromtimestamp(report['started_at_epoch'], datetime.timezone.utc).isoformat(),
    'original_finished_at_utc': datetime.datetime.fromtimestamp(report['finished_at_epoch'], datetime.timezone.utc).isoformat(),
    'elapsed_seconds': report['finished_at_epoch'] - report['started_at_epoch'],
    'original_manifest_entries': len(manifest), 'original_manifest_sha256': sha(manifest_bytes),
    'original_report_sha256': sha(report_bytes), 'original_console_sha256': sha(CONSOLE.read_bytes()),
    'packaging_driver_sha256': sha(Path(__file__).read_bytes()),
    'original_files_changed': False, 'lean_rerun_by_packager': False,
    'packager_affiliation': 'Agent #1 specialist center_parent_receipt is a new resumer packaging the existing root execution. This packager authored no mathematical source and did not execute Lean; packaging is not independent mathematical review.'})
for path, rec in manifest.items():
    data = (dest / path).read_bytes()
    assert len(data) == rec['bytes'] and sha(data) == rec['sha256']
assert (dest / 'FILES.json').read_bytes() == manifest_bytes
package = {}
for f in sorted(HERE.rglob('*')):
    if f.is_file() and f.name not in ['PACKAGE-FILES.json', 'frozen-receipt.json']:
        assert f.suffix not in ['.olean', '.ilean', '.pyc']
        package[str(f.relative_to(HERE))] = {'bytes': f.stat().st_size, 'sha256': sha(f.read_bytes())}
dump(HERE / 'PACKAGE-FILES.json', package)
for path, rec in package.items():
    data = (HERE / path).read_bytes()
    assert len(data) == rec['bytes'] and sha(data) == rec['sha256']
dump(HERE / 'frozen-receipt.json', {
    'status': 'SEALED',
    'agent': 'Agent #1 specialist center_parent_receipt',
    'published_source_commit': COMMIT,
    'lean_rerun_by_packager': False,
    'payload_file_count': len(package),
    'total_file_count': len(package) + 2,
    'manifest_file': 'PACKAGE-FILES.json',
    'manifest_sha256': sha((HERE / 'PACKAGE-FILES.json').read_bytes()),
    'result_receipt_sha256': sha((HERE / 'parent-result-addendum.json').read_bytes()),
    'source_receipt_sha256': sha((HERE / 'publication-source-receipt.json').read_bytes()),
    'manifest_scope': 'Every package file except PACKAGE-FILES.json and this frozen-receipt.json. The seal binds the complete manifest and receipt hashes; its own SHA256 is reported separately.',
    'compiled_objects_packaged': False,
    'original_manifest_entries': len(manifest),
    'original_manifest_sha256': sha(manifest_bytes),
    'original_report_sha256': sha(report_bytes),
    'coordination_continuation_record': 'routing-continuation.json'
})
print(json.dumps({'status': 'SEALED', 'original_manifest_entries': len(manifest),
    'package_entries': len(package), 'package_manifest_sha256': sha((HERE / 'PACKAGE-FILES.json').read_bytes()),
    'receipt_sha256': sha((HERE / 'parent-result-addendum.json').read_bytes()),
    'source_identity_sha256': sha((HERE / 'publication-source-receipt.json').read_bytes()),
    'seal_sha256': sha((HERE / 'frozen-receipt.json').read_bytes()),
    'total_file_count': len(package) + 2}, indent=2))
