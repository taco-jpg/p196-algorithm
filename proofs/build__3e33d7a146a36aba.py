#!/usr/bin/env python3
"""Build original Agent4 saturation dependencies as a development cache only."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import subprocess
import time

WORK = Path('/workspace/scratch/63e10b24caf2')
REPO = WORK / 'p196-algorithm'
HERE = Path(__file__).resolve().parent
BUILD = WORK / 'saturation-deps'
LEAN = WORK / 'runtime-audit/lean'
SOURCE = REPO / 'proofs/agent4/prefix_growth'
ORDER = ['PrefixModel', 'SaturationCertificate', 'SaturationTheorem']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    BUILD.mkdir(exist_ok=False)
    logs = HERE / 'logs'
    logs.mkdir(exist_ok=False)
    scanner_path = REPO / 'proofs/contributions/agent-105/actual-high-return/check.py'
    scanner = runpy.run_path(str(scanner_path))
    env = os.environ.copy()
    for key in ['LEAN_PATH', 'LEAN_SRC_PATH', 'LEAN_SYSROOT', 'LD_PRELOAD', 'LD_LIBRARY_PATH']:
        env.pop(key, None)
    env['LEAN_PATH'] = str(BUILD)
    report = {'status': 'RUNNING', 'operator': '/root/runtime_audit',
              'scope': 'Dependency compilation support only; not a new independent mathematical review',
              'started_utc': datetime.now(timezone.utc).isoformat(), 'build_dir': str(BUILD),
              'build_dir_initially_absent': True, 'project_object_reuse': False,
              'LEAN_PATH': str(BUILD), 'runtime_launcher': str(LEAN),
              'runtime_launcher_sha256': sha(LEAN),
              'official_lean_sha256': sha(WORK / 'runtime-audit/lean-4.19.0-linux/bin/lean'),
              'compatibility_adapter_source_sha256': sha(WORK / 'runtime-audit/app-path-compat.c'),
              'compatibility_adapter_sha256': sha(WORK / 'runtime-audit/app-path-compat.so'),
              'driver_sha256': sha(Path(__file__)),
              'scanner': {'path': str(scanner_path.relative_to(REPO)), 'sha256': sha(scanner_path),
                          'provenance': 'Explicitly reused Agent105 public_theorems/code_only'},
              'sources': {}, 'commands': []}
    assert report['official_lean_sha256'] == '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'

    def save():
        (HERE / 'verification.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')

    def run(label, args):
        argv = [str(LEAN), *args]
        log = logs / (label + '.log')
        started = time.monotonic()
        print('START', label, flush=True)
        with log.open('w') as handle:
            result = subprocess.run(argv, cwd=BUILD, env=env, stdout=handle, stderr=subprocess.STDOUT, text=True)
        elapsed = round(time.monotonic() - started, 3)
        report['commands'].append({'label': label, 'argv': argv, 'cwd': str(BUILD),
                                   'exit_code': result.returncode, 'seconds': elapsed,
                                   'log': str(log.relative_to(HERE)), 'log_sha256': sha(log)})
        save()
        print('END', label, result.returncode, elapsed, flush=True)
        assert result.returncode == 0, label
        return log.read_text()

    try:
        version = run('version', ['--version']).strip()
        assert 'version 4.19.0' in version and 'commit 6caaee842e94' in version
        report['version'] = version
        names, available = [], {'Lean.Elab.Tactic.Omega'}
        for name in ORDER:
            path = SOURCE / (name + '.lean')
            source = path.read_text()
            code = scanner['code_only'](source)
            assert not re.search(r'\b(?:sorry|admit|axiom|native_decide|sorryAx|ofReduceBool|unsafe|implemented_by)\b', code)
            imports = [word for line in re.findall(r'^import\s+([^\n]+)', code, re.M) for word in line.split()]
            assert set(imports) <= available
            try:
                theorems = scanner['public_theorems'](source)
            except ValueError as exc:
                if str(exc) != 'No public theorems found':
                    raise
                theorems = []
            names.extend(item['name'] for item in theorems)
            report['sources'][name] = {'path': str(path.relative_to(REPO)), 'sha256': sha(path),
                                       'imports': imports, 'theorems': theorems, 'forbidden_scan': 'PASS'}
            (BUILD / path.name).write_bytes(path.read_bytes())
            run(name, ['-j1', '-DElab.async=false', '-o', name + '.olean', name + '.lean'])
            assert sha(path) == report['sources'][name]['sha256'] == sha(BUILD / path.name)
            report['sources'][name]['olean_sha256'] = sha(BUILD / (name + '.olean'))
            available.add(name)
            save()
        assert len(names) == len(set(names)) == 28
        audit = 'import SaturationTheorem\n' + ''.join('#print axioms ' + name + '\n' for name in names)
        (BUILD / 'SaturationDependencyAudit.lean').write_text(audit)
        (HERE / 'SaturationDependencyAudit.lean').write_text(audit)
        stdout = run('SaturationDependencyAudit', ['-j1', '-DElab.async=false', 'SaturationDependencyAudit.lean'])
        rows = re.findall(r"^'([^\n]+)' depends on axioms:\s*\[([^\]]*)\]", stdout, re.M)
        rows = [(name, sorted(x.strip() for x in value.split(',') if x.strip())) for name, value in rows]
        rows += [(name, []) for name in re.findall(r"^'([^\n]+)' does not depend on any axioms", stdout, re.M)]
        counts = Counter(name for name, _ in rows)
        assert set(counts) == set(names) and set(counts.values()) == {1}
        assert all(set(axioms) <= {'propext', 'Classical.choice', 'Quot.sound'} for _, axioms in rows)
        for name, rec in report['sources'].items():
            assert sha(REPO / rec['path']) == rec['sha256'] == sha(BUILD / (name + '.lean'))
            assert sha(BUILD / (name + '.olean')) == rec['olean_sha256']
        report.update(status='PASS', completed_utc=datetime.now(timezone.utc).isoformat(),
                      theorem_count=28, axiom_audit=dict(sorted(rows)), source_hashes_unchanged=True)
        save()
        (BUILD / 'BUILD_MANIFEST.json').write_bytes((HERE / 'verification.json').read_bytes())
        for path in BUILD.iterdir():
            if path.is_file():
                path.chmod(0o444)
        BUILD.chmod(0o555)
        print('PASS: three source modules; 28 theorem axiom queries; read-only cache', flush=True)
    except Exception as exc:
        report.update(status='FAILED', error=repr(exc))
        save()
        raise


if __name__ == '__main__':
    main()
