#!/usr/bin/env python3
"""Retain incremental Lean compilation and complete public-theorem axiom audits.

Dependencies must be freshly compiled from the recorded project sources. No
dependency is copied into the publication source directory. Generated oleans
are reproducible build products kept outside it.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--lean', type=Path, required=True)
    ap.add_argument('--deps', type=Path, nargs='+', required=True)
    ap.add_argument('--build', type=Path, required=True)
    args = ap.parse_args()
    evidence = Path(__file__).resolve().parent
    source = evidence.parent / 'CertificateSaturation.lean'
    build = args.build.resolve()
    build.mkdir(parents=True, exist_ok=True)
    n = 1
    while (evidence / f'attempt-{n:03d}.lean').exists():
        n += 1
    stem = f'attempt-{n:03d}'
    (evidence / f'{stem}.lean').write_bytes(source.read_bytes())
    (build / source.name).write_bytes(source.read_bytes())
    env = os.environ.copy()
    for key in ['LEAN_PATH', 'LEAN_SRC_PATH', 'LEAN_SYSROOT', 'LD_PRELOAD', 'LD_LIBRARY_PATH']:
        env.pop(key, None)
    env['LEAN_PATH'] = ':'.join(str(p.resolve()) for p in [build, *args.deps])
    record = {
        'scope': 'Development composition verification; final direct endpoints require exact CertificatePrefix projection',
        'source_sha256': sha(source),
        'compiler': str(args.lean.resolve()),
        'compiler_launcher_sha256': sha(args.lean),
        'LEAN_PATH': env['LEAN_PATH'],
        'dependencies': {}, 'commands': [],
    }
    for name in re.findall(r'^import\s+(\w+)', source.read_text(), re.M):
        matches = [p for p in args.deps if (p / f'{name}.olean').exists()]
        if not matches:
            raise SystemExit(f'Missing compiled dependency: {name}')
        p = matches[0]
        record['dependencies'][name] = {
            'path': str((p / f'{name}.lean').resolve()),
            'source_sha256': sha(p / f'{name}.lean'),
            'olean_sha256': sha(p / f'{name}.olean'),
        }

    def execute(name, tail):
        command = [str(args.lean.resolve()), '-j1', '-DElab.async=false', *tail]
        proc = subprocess.run(command, cwd=build, env=env, text=True,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log = evidence / f'{stem}-{name}.log'
        log.write_text(proc.stdout)
        record['commands'].append({'command': command, 'returncode': proc.returncode,
                                   'log': log.name, 'log_sha256': sha(log)})
        (evidence / f'{stem}.json').write_text(json.dumps(record, indent=2) + '\n')
        print(proc.stdout, end='')
        if proc.returncode:
            raise SystemExit(proc.returncode)
        return proc.stdout

    execute('version', ['--version'])
    execute('compile', ['-o', str(build / 'CertificateSaturation.olean'), str(build / source.name)])
    names = re.findall(r'^theorem\s+([A-Za-z_][A-Za-z_0-9]*)', source.read_text(), re.M)
    audit = 'import CertificateSaturation\n\n' + '\n'.join(
        '#print axioms Agent110.CertificateSaturation.' + name for name in names) + '\n'
    audit_path = evidence / f'{stem}-axioms.lean'
    audit_path.write_text(audit)
    output = execute('axioms', [str(audit_path)])
    found = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", output, re.S)
    entries = {name: sorted(x.strip() for x in raw.split(',') if x.strip()) for name, raw in found}
    for name in re.findall(r"'([^']+)' does not depend on any axioms", output):
        entries[name] = []
    assert set(entries) == {'Agent110.CertificateSaturation.' + name for name in names}
    assert all(set(value) <= {'propext', 'Classical.choice', 'Quot.sound'} for value in entries.values())
    record['status'] = 'PASS'
    record['axiom_audit'] = entries
    record['olean_sha256'] = sha(build / 'CertificateSaturation.olean')
    assert sha(source) == record['source_sha256']
    (evidence / f'{stem}.json').write_text(json.dumps(record, indent=2) + '\n')
    print(f'PASS: {len(names)} public theorem axiom queries')


if __name__ == '__main__':
    main()
