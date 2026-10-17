#!/usr/bin/env python3
"""Inspect the existing fresh-002 artifacts. This script never invokes Lean."""
import base64
import datetime
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
ROOT = BASE.parents[4]
FRESH = BASE / 'fresh-002'
AUTHOR = '9ab3c2d21160ccbf6e7186e29500d75f64f78058'
REVIEW = 'a04744ae9065335b73924ae633990d8a1e47bd12'
PREVIOUS = 'b590d2e7ab700be5d28f102e8b27da61da0db2b3'
FIRST = '8906a445566cb533ab56aaf0f2ce1cf1c164c081'
BUILD = Path('/workspace/p196-agent1-session-20261016/ceilhalf-review-build-002')
CONSOLE = BUILD.with_name(BUILD.name + '.console.log')
sha = lambda data: hashlib.sha256(data).hexdigest()

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def record(data):
    return {'bytes': len(data), 'sha256': sha(data)}

def new_json(name, value):
    with (HERE / name).open('x') as out:
        out.write(json.dumps(value, indent=2) + '\n')

assert git('rev-parse', 'HEAD').decode().strip() == REVIEW
assert not git('status', '--porcelain', '--untracked-files=no')
old_path = BASE.parent / 'FILES.json'
old_bytes = old_path.read_bytes()
assert old_bytes == git('show', FIRST + ':' + str(old_path.relative_to(ROOT)))
old_manifest = json.loads(old_bytes)
assert len(old_manifest) == 55
for rel, expected in old_manifest.items():
    assert record((BASE.parent / rel).read_bytes()) == expected, rel

# Hash all 49 pre-existing corrected-run artifacts before adding any seal files.
originals = {
    str(p.relative_to(BASE)): record(p.read_bytes())
    for p in sorted(BASE.rglob('*'))
    if p.is_file() and HERE not in p.parents
}
assert len(originals) == 49
for name in ['replay.py', 'source_scanner.py', 'AuditTemplate.lean.txt',
             'source-pins.json', 'closure.json']:
    assert (BASE / name).read_bytes() == (FRESH / name).read_bytes(), name
assert (BASE / 'original-source-mapping.json').read_bytes() == (
    BASE.parent / 'original-source-mapping.json').read_bytes()

pins = json.loads((BASE / 'source-pins.json').read_text())
mapping = {r['module']: r for r in json.loads(
    (BASE / 'original-source-mapping.json').read_text())['modules']}
closure = json.loads((BASE / 'closure.json').read_text())
commands = json.loads((FRESH / 'commands.json').read_text())
verification = json.loads((FRESH / 'verification.json').read_text())
assert len(pins) == len(commands) == 14
assert [r['module'] for r in commands] == closure['requested_build_order']
assert closure['claimed_scope_commit'] == '90af7ccf5b9ce9b92da13351c71b9d1c88905bf8'
checks = []
for pin in pins:
    name, path = pin['module'], pin['source_path']
    data = git('show', AUTHOR + ':' + path)
    blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert sha(data) == pin['sha256'] and blob == pin['git_blob']
    assert len(data) == pin['bytes']
    assert data == git('show', REVIEW + ':' + path)
    assert data == git('show', pin['source_commit'] + ':' + path)
    assert data == (FRESH / 'compiled-sources' / (name + '.lean')).read_bytes()
    assert data == (BUILD / (name + '.lean')).read_bytes()
    disk = ROOT / path
    if disk.is_file():
        assert disk.read_bytes() == data
    item = {'module': name, 'source_path': path, 'bytes': len(data),
            'sha256': sha(data), 'git_blob': blob,
            'author_commit_matches': True, 'review_commit_matches': True,
            'original_pin_commit_matches': True, 'compiled_snapshot_matches': True,
            'external_build_source_matches': True,
            'worktree_file_present': disk.is_file(),
            'worktree_file_matches_if_present': True}
    if name != 'Agent105CeilHalfSuffix':
        assert data == git('show', PREVIOUS + ':' + path)
        assert data == (BASE.parent / 'fresh-001/compiled-sources' / (name + '.lean')).read_bytes()
        assert mapping[name]['sha256'] == sha(data)
        assert mapping[name]['git_blob'] == blob
        item.update(inherited_source_unchanged=True, original_mapping_matches=True,
                    previous_compiled_snapshot_matches=True)
        if path.startswith('proofs/archive/source-trees/'):
            archive_commit, original_path = path[len('proofs/archive/source-trees/'):].split('/', 1)
            assert data == git('show', archive_commit + ':' + original_path)
            item.update(historical_archive_commit=archive_commit,
                        historical_original_path=original_path, historical_original_matches=True)
    checks.append(item)

target = pins[-1]
assert target['module'] == 'Agent105CeilHalfSuffix'
assert git('diff', '--name-only', PREVIOUS, AUTHOR).decode().splitlines() == [target['source_path']]
published = json.loads((HERE / 'published-target-response.json').read_text())
assert published['sha'] == target['git_blob']
assert sha(base64.b64decode(published['content'])) == target['sha256']

compiler = json.loads((FRESH / 'compiler.json').read_text())
assert sha(Path(compiler['path']).read_bytes()) == compiler['sha256']
for cmd in commands:
    name = cmd['module']
    expected = 1 if name == 'Agent105CeilHalfSuffix' else 0
    assert cmd['argv'] == [compiler['path'], '--trust=0', '-j1', '-DElab.async=false',
                           '-o', name + '.olean', name + '.lean']
    assert cmd['cwd'] == cmd['LEAN_PATH'] == str(BUILD)
    assert cmd['exit_code'] == expected and not cmd['timed_out']
    assert cmd['address_space_mib'] == 8192 and cmd['timeout_seconds'] == 600
    assert cmd['seconds'] > 0 and cmd['finished_at_utc'] >= cmd['started_at_utc']
    log = (FRESH / (name + '.log')).read_bytes()
    assert sha(log) == cmd['log_sha256']
    assert bool(cmd['object_exists']) == (expected == 0)
    assert (BUILD / (name + '.olean')).exists() == bool(cmd['object_exists'])
    if expected == 0:
        assert b'error:' not in log
assert verification['status'] == 'FAIL'
assert verification['source_commit'] == AUTHOR
assert verification['completed_commands'] == 14
assert verification['successful_module_compilations'] == 13
assert verification['failed_module'] == 'Agent105CeilHalfSuffix'
assert verification['source_changes'] is False
assert verification['full_origin_audit_completed'] is False

diagnostics = (FRESH / 'Agent105CeilHalfSuffix.log').read_text()
error_lines = [line for line in diagnostics.splitlines() if ': error:' in line]
assert error_lines == [
    'Agent105CeilHalfSuffix.lean:67:4: error: unsolved goals',
    'Agent105CeilHalfSuffix.lean:70:4: error: no goals to be solved']
assert '\u22a2 0 < d 0' in diagnostics
console = CONSOLE.read_bytes()
expected_console = ''.join(f"{c['module']}: exit {c['exit_code']}\n" for c in commands)
assert console == (expected_console + diagnostics + '\n').encode()
assert not (FRESH / 'ReplicationAudit.lean').exists()
assert not (FRESH / 'ReplicationAudit.log').exists()
assert not (BUILD / 'ReplicationAudit.lean').exists()
assert not (BASE / 'fresh-003').exists()
assert not any(p.suffix in {'.olean', '.ilean', '.o'} for p in BASE.rglob('*'))
with (HERE / 'original-console.log').open('xb') as out:
    out.write(console)
new_json('preserved-inputs.json', originals)
report = {
    'status': 'PASS_STORED_ARTIFACT_INTEGRITY',
    'inspected_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'validator': '/root/suffix_receipt_resume',
    'lean_invocations_by_validator': 0,
    'source_commit': AUTHOR, 'review_head': REVIEW,
    'compiler_binary_hash_matches_stored_record': True,
    'existing_corrected_artifacts_preserved': len(originals),
    'first_failure_manifest': {'commit': FIRST, 'sha256': sha(old_bytes),
        'manifest_byte_identical': True, 'all_55_file_sizes_and_hashes_match': True},
    'all_13_inherited_sources_unchanged': True,
    'all_11_historical_archive_originals_match': True,
    'published_target_api_matches': True,
    'all_14_command_logs_match_recorded_hashes': True,
    'all_recorded_commands_have_start_finish_elapsed_exit_metadata': True,
    'all_recorded_argv_use_strict_flags_and_isolated_lean_path': True,
    'console_matches_14_exit_lines_and_complete_failure_log': True,
    'console_source_path': str(CONSOLE), 'console_sha256': sha(console),
    'recorded_elapsed_seconds': verification['seconds'],
    'recorded_first_command_start_utc': commands[0]['started_at_utc'],
    'recorded_last_command_finish_utc': commands[-1]['finished_at_utc'],
    'outer_tool_session_exit_status': None,
    'outer_tool_session_exit_note': 'Not available in the inspected stored artifacts after reattachment; no inference from child exit or driver code.',
    'no_target_object_present': True, 'no_origin_audit_output_present': True,
    'no_second_corrected_source_build_present': True,
    'diagnostic_lines': error_lines, 'modules': checks,
}
new_json('integrity.json', report)
print(json.dumps({k: report[k] for k in ['status', 'existing_corrected_artifacts_preserved',
    'first_failure_manifest', 'all_13_inherited_sources_unchanged',
    'published_target_api_matches', 'recorded_elapsed_seconds', 'diagnostic_lines']}, indent=2))
