#!/usr/bin/env python3
"""Focused recovery checks; preserves the sealed evidence and all test outputs."""
from pathlib import Path
import datetime
import hashlib
import json
import runpy
import subprocess
import sys
import time
import traceback

BUNDLE = Path(__file__).resolve().parent
STRICT = BUNDLE.parent
HELPER = BUNDLE / 'recover_checkpoint002.py'
LOGS = BUNDLE / 'recovery-test-001'
DESTINATION = BUNDLE / 'helper-verified-extraction-001'
LOGS.mkdir(exist_ok=False)
assert not DESTINATION.exists()
ENV = {'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8',
       'PYTHONDONTWRITEBYTECODE': '1'}
receipt = {'status': 'RUNNING', 'tests': [], 'started_at': datetime.datetime.now(datetime.timezone.utc).isoformat()}
START = time.monotonic()

def ident(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''): h.update(block)
    return {'bytes': path.stat().st_size, 'sha256': h.hexdigest()}

def run(label, extra, expected_status, expected_exit):
    argv = [sys.executable, '-B', str(HELPER)] + extra
    t = time.monotonic()
    result = subprocess.run(argv, cwd=BUNDLE, env=ENV, stdin=subprocess.DEVNULL,
                            capture_output=True, timeout=30)
    (LOGS / (label + '.stdout.log')).write_bytes(result.stdout)
    (LOGS / (label + '.stderr.log')).write_bytes(result.stderr)
    parsed = json.loads(result.stdout if expected_exit == 0 else result.stderr)
    record = {'label': label, 'argv': argv, 'cwd': str(BUNDLE), 'exit_code': result.returncode,
              'elapsed_seconds': time.monotonic() - t, 'result': parsed,
              'stdout': ident(LOGS / (label + '.stdout.log')),
              'stderr': ident(LOGS / (label + '.stderr.log'))}
    receipt['tests'].append(record)
    assert result.returncode == expected_exit and parsed['status'] == expected_status

frozen = {}
try:
    members = json.loads((BUNDLE / 'MEMBERS.json').read_text())
    for name, expected in members.items():
        path = (BUNDLE / 'CHECKPOINT002_CONTENTS.json' if name == 'strict-build/CHECKPOINT002_CONTENTS.json'
                else STRICT / name.removeprefix('strict-build/'))
        assert ident(path) == expected
        frozen[str(path)] = expected
    transport = ['PACKAGING_RECEIPT.json', 'MEMBERS.json', 'pr101-execution-checkpoint-002.tar.xz',
                 'part-000.b64', 'part-001.b64', 'part-002.b64']
    for name in transport:
        frozen[str(BUNDLE / name)] = ident(BUNDLE / name)
    receipt['frozen_original_payload_members'] = len(members)
    receipt['frozen_transport_files'] = len(transport)
    receipt['additive_helper'] = ident(HELPER)
    receipt['additive_document'] = ident(BUNDLE / 'RECOVERY.md')
    receipt['test_script'] = ident(Path(__file__))
    run('001-default-verify', [], 'VERIFIED', 0)
    run('002-fresh-extraction', ['--extract-to', str(DESTINATION)], 'VERIFIED_AND_EXTRACTED', 0)
    for name, expected in members.items():
        assert ident(DESTINATION / name) == expected
    receipt['independent_extraction_comparison'] = {'member_count': len(members), 'all_hashes_equal': True}
    run('003-existing-destination-rejection', ['--extract-to', str(DESTINATION)], 'REJECTED', 1)
    assert receipt['tests'][-1]['result']['reason'] == 'Extraction destination already exists'
    namespace = runpy.run_path(str(HELPER), run_name='recovery_path_validation_test')
    try:
        namespace['validate_member_name']('strict-build/../../escape')
    except namespace['RecoveryError'] as exc:
        assert str(exc) == 'Parent traversal rejected: strict-build/../../escape'
        receipt['tests'].append({'label': '004-parent-traversal-rejection',
                                 'scope': 'Direct focused invocation of the same member-name validator used before extraction',
                                 'input': 'strict-build/../../escape', 'status': 'REJECTED_AS_REQUIRED', 'reason': str(exc)})
    else:
        raise AssertionError('Traversal fixture was accepted')
    inputs = json.loads((STRICT / 'supplement-002/input-after.json').read_text())
    for name, expected in inputs.items(): assert ident(Path(name)) == expected
    runtime = json.loads((STRICT / 'attempt-002/runtime-after.json').read_text())
    build = json.loads((STRICT / 'attempt-002/receipt.json').read_text())
    final = json.loads((STRICT / 'supplement-002/receipt.json').read_text())
    assert build['source_unchanged'] and build['runtime_unchanged'] and final['all_inputs_unchanged']
    assert build['compiled_count'] == 97 and build['reused_count'] == 6 and build['covered_count'] == 103
    assert final['coverage']['modules'] == 104 and final['coverage']['audited_declarations'] == 2660
    receipt['final_source_runtime_recheck'] = {'current_input_files_checked': len(inputs),
                                             'runtime_files_bound_in_these_inputs': len(runtime),
                                             'all_current_hashes_match_final_manifest': True,
                                             'source_unchanged': True, 'runtime_unchanged': True,
                                             'successful_build_new_modules': 97, 'reused_modules': 6,
                                             'repaired_wip_modules': 1, 'audited_modules': 104,
                                             'audited_safe_declarations': 2660}
    assert all(ident(Path(name)) == expected for name, expected in frozen.items())
    receipt['all_frozen_payload_transport_reports_and_manifests_unchanged'] = True
    receipt['status'] = 'PASSED'
except BaseException as exc:
    receipt['status'] = 'FAILED'; receipt['exception'] = repr(exc)
    (LOGS / 'exception.log').write_text(traceback.format_exc())
finally:
    receipt['finished_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    receipt['elapsed_seconds'] = time.monotonic() - START
    (BUNDLE / 'RECOVERY_TEST_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))
sys.exit(0 if receipt['status'] == 'PASSED' else 1)
