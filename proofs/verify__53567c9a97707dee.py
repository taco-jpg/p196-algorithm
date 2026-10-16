#!/usr/bin/env python3
"""Compile structural accounting and audit every public theorem, preserving attempts.

The caller supplies the official Lean 4.19.0 wrapper and freshly built
TemplateStep/ReturnCertificate dependency directory. This is development
verification, not an independent semantic review. Generated oleans stay outside
the publication tree; source snapshots and proof audit outputs are retained.
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
    ap.add_argument('--deps', type=Path, required=True)
    ap.add_argument('--build', type=Path, required=True)
    args = ap.parse_args()
    evidence = Path(__file__).resolve().parent
    source = evidence.parent / 'CertificateAccounting.lean'
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
    env['LEAN_PATH'] = str(build) + ':' + str(args.deps.resolve())
    record = {
        'scope': 'Development compile and axiom audit of structural certificate accounting only',
        'source_sha256': sha(source),
        'compiler': str(args.lean.resolve()),
        'compiler_launcher_sha256': sha(args.lean),
        'LEAN_PATH': env['LEAN_PATH'],
        'dependencies': {
            name: {'source_sha256': sha(args.deps / f'{name}.lean'),
                   'olean_sha256': sha(args.deps / f'{name}.olean')}
            for name in ['TemplateStep', 'ReturnCertificate']
        },
        'commands': [],
    }

    def execute(name, tail):
        command = [str(args.lean.resolve()), '-j1', '-DElab.async=false', *tail]
        p = subprocess.run(command, cwd=build, env=env, text=True,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log = evidence / f'{stem}-{name}.log'
        log.write_text(p.stdout)
        record['commands'].append({'command': command, 'returncode': p.returncode,
                                   'log': log.name, 'log_sha256': sha(log)})
        (evidence / f'{stem}.json').write_text(json.dumps(record, indent=2) + '\n')
        print(p.stdout, end='')
        if p.returncode:
            raise SystemExit(p.returncode)
        return p.stdout

    execute('version', ['--version'])
    execute('compile', ['-o', str(build / 'CertificateAccounting.olean'), str(build / source.name)])
    names = re.findall(r'^theorem\s+([A-Za-z_][A-Za-z_0-9]*)', source.read_text(), re.M)
    audit = 'import CertificateAccounting\n\n' + '\n'.join(
        '#print axioms Agent110.Accounting.' + name for name in names) + '\n'
    audit_path = evidence / f'{stem}-axioms.lean'
    audit_path.write_text(audit)
    output = execute('axioms', [str(audit_path)])
    found = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", output, re.S)
    entries = {name: sorted(x.strip() for x in raw.split(',') if x.strip()) for name, raw in found}
    for name in re.findall(r"'([^']+)' does not depend on any axioms", output):
        entries[name] = []
    assert set(entries) == {'Agent110.Accounting.' + name for name in names}
    assert all(set(value) <= {'propext', 'Classical.choice', 'Quot.sound'} for value in entries.values())
    record['status'] = 'PASS'
    record['axiom_audit'] = entries
    record['olean_sha256'] = sha(build / 'CertificateAccounting.olean')
    assert sha(source) == record['source_sha256']
    (evidence / f'{stem}.json').write_text(json.dumps(record, indent=2) + '\n')
    print(f'PASS: {len(names)} public theorem axiom queries')


if __name__ == '__main__':
    main()
