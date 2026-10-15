#!/usr/bin/env python3
"""Retain the fail-closed apostrophe-parser attempt; recheck hashes and audit."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

ROOT = Path('/workspace/scratch/63e10b24caf2')
REPO = ROOT / 'p196-algorithm'
HERE = REPO / 'proofs/contributions/agent-110/runtime'
EVIDENCE = HERE / 'dev-cache-rebuild'
BUILD = ROOT / 'dev-deps'
LEAN = ROOT / 'runtime-audit/lean'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    record = json.loads((EVIDENCE / 'manifest.failed-parser.json').read_text())
    assert record['status'] == 'FAILED'
    assert record['commands'][-1]['name'] == 'Agent110DevAudit'
    assert all(command['returncode'] == 0 for command in record['commands'])
    assert len(record['sources']) == 18
    names = [theorem['name'] for source in record['sources'].values() for theorem in source['public_theorems']]
    assert len(names) == len(set(names)) == 515
    for name, source in record['sources'].items():
        assert sha(REPO / source['path']) == source['sha256']
        assert sha(BUILD / (name + '.lean')) == source['sha256']
        assert sha(BUILD / (name + '.olean')) == source['olean_sha256']
    assert sha(LEAN) == record['compiler_launcher_sha256']
    assert (BUILD / 'Agent110DevAudit.lean').read_bytes() == (EVIDENCE / 'Agent110DevAudit.lean').read_bytes()
    env = os.environ.copy()
    for key in ['LEAN_PATH', 'LEAN_SRC_PATH', 'LEAN_SYSROOT', 'LD_PRELOAD', 'LD_LIBRARY_PATH']:
        env.pop(key, None)
    env['LEAN_PATH'] = str(BUILD)
    argv = [str(LEAN), '-j1', '-DElab.async=false', str(BUILD / 'Agent110DevAudit.lean')]
    log = EVIDENCE / 'Agent110DevAudit.parser-recovery.log'
    start = time.monotonic()
    with log.open('w') as handle:
        proc = subprocess.run(argv, cwd=BUILD, env=env, stdout=handle, stderr=subprocess.STDOUT, text=True)
    assert proc.returncode == 0
    stdout = log.read_text()
    rows = re.findall(r"^'([^\n]+)' depends on axioms:\s*\[([^\]]*)\]", stdout, re.M)
    rows = [(name, sorted(a.strip() for a in value.split(',') if a.strip())) for name, value in rows]
    rows += [(name, []) for name in re.findall(r"^'([^\n]+)' does not depend on any axioms", stdout, re.M)]
    counts = Counter(name for name, _ in rows)
    assert set(counts) == set(names), ('Name mismatch', set(names) - set(counts), set(counts) - set(names))
    assert set(counts.values()) == {1}
    assert all(set(axioms) <= {'propext', 'Classical.choice', 'Quot.sound'} for _, axioms in rows)
    for name, source in record['sources'].items():
        assert sha(REPO / source['path']) == source['sha256']
        assert sha(BUILD / (name + '.lean')) == source['sha256']
        assert sha(BUILD / (name + '.olean')) == source['olean_sha256']
    record['parser_recovery'] = {
        'reason': 'Initial fail-closed regex missed the trailing apostrophe in Agent109.Cert.append_inj_left\'. All 18 builds and initial Lean audit had exit 0.',
        'prior_manifest': 'manifest.failed-parser.json', 'initial_driver_sha256': sha(EVIDENCE / 'initial_driver.py.txt'),
        'corrected_driver_sha256': sha(HERE / 'build_dev_cache.py'), 'recovery_driver_sha256': sha(Path(__file__)),
        'recompiled_modules': False, 'all_sources_and_objects_rehashed_before_after': True,
    }
    record['commands'].append({'name': 'Agent110DevAudit.parser-recovery', 'argv': argv,
                               'cwd': str(BUILD), 'returncode': 0,
                               'seconds': round(time.monotonic() - start, 3),
                               'log': log.name, 'log_sha256': sha(log)})
    record['axiom_audit'] = dict(sorted(rows))
    record['all_source_hashes_unchanged'] = True
    record['status'] = 'PASS'
    record['completed_utc'] = datetime.now(timezone.utc).isoformat()
    record.pop('error', None)
    (EVIDENCE / 'manifest.json').write_text(json.dumps(record, indent=2, sort_keys=True) + '\n')
    (BUILD / 'BUILD_MANIFEST.json').write_bytes((EVIDENCE / 'manifest.json').read_bytes())
    for path in BUILD.iterdir():
        if path.is_file():
            path.chmod(0o444)
    BUILD.chmod(0o555)
    print('PASS: 18 freshly compiled modules; 515 complete axiom queries; read-only development cache')


if __name__ == '__main__':
    main()
