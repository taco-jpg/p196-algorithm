#!/usr/bin/env python3
"""Explicit trust-zero audit of the modules produced by a completed fresh build."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
LEAN_SHA256 = '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--canonical-run', type=Path, required=True)
    parser.add_argument('--registry', type=Path, required=True)
    parser.add_argument('--comparison-ledger', type=Path, required=True)
    parser.add_argument('--lean', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--executor', required=True)
    args = parser.parse_args()
    run, out, lean = args.canonical_run.resolve(), args.output.resolve(), args.lean.resolve()
    out.mkdir(parents=True, exist_ok=False)
    original_bytes = (run / 'verification.json').read_bytes()
    original = json.loads(original_bytes)
    registry_bytes = args.registry.read_bytes()
    registry = json.loads(registry_bytes)
    old_ledger_bytes = args.comparison_ledger.read_bytes()
    old_ledger = json.loads(old_ledger_bytes)
    project = 'groupii-overflow'
    source = run / project / 'source'
    audit = source / 'ProjectAudit.lean'
    assert original['status'] == 'PASS'
    assert sha(registry_bytes) == original['registry_sha256']
    assert sha(original_bytes) == old_ledger['verification_sha256']
    assert sha(lean.read_bytes()) == LEAN_SHA256
    records = registry['projects'][project]['modules']
    snapshots = {}
    for module, rec in records.items():
        path = source / (module.replace('.', '/') + '.lean')
        olean = path.with_suffix('.olean')
        raw = path.read_bytes()
        assert sha(raw) == rec['sha256']
        assert hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest() == rec['git_blob']
        snapshots[str(path)] = sha(raw)
        snapshots[str(olean)] = sha(olean.read_bytes())
    manifest = json.loads((run / 'FILES.json').read_text())
    assert sha(audit.read_bytes()) == manifest[str(audit.relative_to(run))]['sha256']
    snapshots[str(audit)] = sha(audit.read_bytes())
    command = [str(lean), '--trust=0', '-j1', '-DElab.async=false', 'ProjectAudit.lean']
    env = os.environ.copy()
    env['LEAN_PATH'] = str(source)
    result = {
        'status': 'RUNNING', 'executor': args.executor,
        'purpose': 'Explicit trust0 type-check of all imported modules from the one prior fresh18 build, followed by the original full module-origin audit.',
        'not_a_second_fresh18_source_build': True,
        'canonical_run': str(run), 'canonical_verification_sha256': sha(original_bytes),
        'run_source_head': original['source_commit'],
        'registry_sha256': sha(registry_bytes), 'comparison_ledger_sha256': sha(old_ledger_bytes),
        'official_lean_sha256': LEAN_SHA256, 'launcher_sha256': sha(Path(__file__).read_bytes()),
        'argv': command, 'cwd': str(source), 'LEAN_PATH': str(source),
        'explicit_trust_level': 0, 'prior_fresh_local_modules': len(records),
        'snapshots_before': snapshots, 'started_at_epoch': time.time(),
        'source_math_modified': False, 'canonical_verifier_modified': False,
    }
    (out / 'strict-import-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    log = out / 'ProjectAudit-trust0.log'
    with log.open('wb') as stream:
        try:
            rc = subprocess.run(command, cwd=source, env=env, stdout=stream,
                                stderr=subprocess.STDOUT, timeout=1800).returncode
        except subprocess.TimeoutExpired:
            rc = 124
    result['exit_code'] = rc
    result['finished_at_epoch'] = time.time()
    result['log_sha256'] = sha(log.read_bytes())
    result['status'] = 'FAIL' if rc else 'VALIDATING_AUDIT_AND_POSTHASH'
    try:
        if rc:
            raise RuntimeError('Explicit trust0 audit exited ' + str(rc))
        spec = importlib.util.spec_from_file_location('complete_axiom_parser', HERE / 'extract_axiom_ledger.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        text = log.read_text()
        ledger = {}
        for match in module.AUDITED.finditer(text):
            origin, name = match.group(1), match.group(2)
            assert name not in ledger
            ledger[name] = {'module': origin, 'axioms': module.bracket_list(text, match.end() - 1)}
        expected = old_ledger['full_module_origin_ledger']
        assert ledger.keys() == expected.keys()
        for name, rec in ledger.items():
            assert rec['module'] == expected[name]['module']
            assert set(rec['axioms']) == set(expected[name]['axioms'])
        declared_count = re.findall(r'^FULL_MODULE_AUDIT theorems=(\d+) union=', text, re.M)
        assert declared_count == [str(len(ledger))]
        unsafe = re.findall(r'^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$', text, re.M)
        assert set(unsafe) == {tuple(row) for row in original['projects'][project]['unsafe_implementation_axioms']}
        assert all(sha(Path(path).read_bytes()) == h for path, h in snapshots.items())
        assert sha(lean.read_bytes()) == LEAN_SHA256
        result.update({
            'status': 'PASS_EXPLICIT_TRUST0_FULL_IMPORT_TYPECHECK_AND_FULL_MODULE_AUDIT',
            'theorem_constants_audited': len(ledger),
            'all_module_origin_names_and_complete_axiom_sets_match_prior_fresh_audit': True,
            'explicit_new_endpoints_checked': len(old_ledger['new_explicit_exports']),
            'actual_axiom_union': sorted({a for rec in ledger.values() for a in rec['axioms']}),
            'unsafe_implementation_axioms_separately_reported': unsafe,
            'all_source_and_fresh_olean_posthashes_unchanged': True,
            'full_module_origin_ledger': ledger,
        })
    except Exception as error:
        result['status'] = 'FAIL'
        result['validation_error'] = repr(error)
        rc = rc or 1
    (out / 'strict-import-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result.get(k) for k in ['status', 'exit_code',
        'theorem_constants_audited', 'explicit_new_endpoints_checked', 'actual_axiom_union']}))
    return rc


if __name__ == '__main__':
    raise SystemExit(main())
