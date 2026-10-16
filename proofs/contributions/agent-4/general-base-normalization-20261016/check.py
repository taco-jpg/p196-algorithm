#!/usr/bin/env python3
"""Fresh source builds and complete exported-theorem audits; Lean 4.19.0."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

MODULES = json.loads((Path(__file__).resolve().parent / 'modules.json').read_text())
PREFIX = 'P196.Agent4.GeneralBase.'
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit('usage: python3 check.py /absolute/path/to/lean /new/audit/directory')
    if (not isinstance(MODULES, list) or not MODULES or len(MODULES) != len(set(MODULES))
            or any(not isinstance(x, str) or not re.fullmatch(r'[A-Za-z0-9_]+', x) for x in MODULES)):
        raise RuntimeError('Invalid explicit module manifest')
    lean = str(Path(sys.argv[1]).resolve())
    out = Path(sys.argv[2]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).resolve().parent
    version = subprocess.run([lean, '--version'], check=True, text=True,
                             stdout=subprocess.PIPE).stdout.strip()
    if 'version 4.19.0,' not in version:
        raise RuntimeError(f'Wrong compiler: {version}')
    print(version, flush=True)
    records = []
    hashes = {}
    try:
        for module in MODULES:
            path = source / f'{module}.lean'
            text = path.read_text()
            hashes[module] = hashlib.sha256(path.read_bytes()).hexdigest()
            if re.search(r'\b(sorry|admit|sorryAx|native_decide)\b', text):
                raise RuntimeError(f'Forbidden proof token in {module}')
            if re.search(r'^\s*(axiom|constant)\s', text, re.M):
                raise RuntimeError(f'Unverified declaration in {module}')
        print(json.dumps({'source_sha256': hashes}, sort_keys=True), flush=True)
        for run in [1, 2]:
            with tempfile.TemporaryDirectory(prefix=f'clean-{run}-', dir=out) as td:
                build = Path(td)
                for module in MODULES:
                    shutil.copyfile(source / f'{module}.lean', build / f'{module}.lean')
                env = dict(os.environ, LEAN_PATH=str(build))
                for module in MODULES:
                    command = [lean, '-o', f'{module}.olean', f'{module}.lean']
                    proc = subprocess.run(command, cwd=build, env=env, text=True,
                                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    logfile = out / f'pass-{run}-{module}.log'
                    logfile.write_text(proc.stdout)
                    print(f'BUILD {run}, MODULE {module}, EXIT {proc.returncode}', flush=True)
                    print(proc.stdout, end='', flush=True)
                    record = {'pass': run, 'module': module, 'command': command,
                              'exit_status': proc.returncode, 'log': logfile.name}
                    records.append(record)
                    if proc.returncode or re.search(r'sorryAx|Lean.ofReduceBool|Lean.trustCompiler|error:|declaration uses', proc.stdout):
                        raise RuntimeError(f'Compilation or trust check failed: {module}')
                    expected = {PREFIX + x for x in re.findall(
                        r'^theorem\s+([A-Za-z0-9_]+)', (source / f'{module}.lean').read_text(), re.M)}
                    audited = {}
                    for theorem, axioms in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", proc.stdout):
                        names = {x.strip() for x in axioms.split(',') if x.strip()}
                        if not names <= ALLOWED:
                            raise RuntimeError(f'Excluded axioms: {theorem}: {names}')
                        audited[theorem] = sorted(names)
                    for theorem in re.findall(r"'([^']+)' does not depend on any axioms", proc.stdout):
                        audited[theorem] = []
                    if set(audited) != expected or not expected:
                        raise RuntimeError(f'Audit coverage mismatch: {module}: {set(audited) ^ expected}')
                    record['axioms'] = audited
        status = {'status': 'LEAN_CHECKED', 'compiler': version, 'source_sha256': hashes,
                  'allowed_foundations': sorted(ALLOWED), 'builds': records,
                  'independent_semantic_review': False, 'integrated': False,
                  'decimal_lychrel_existence_proved': False,
                  'full_four_step_theorem_proved': False}
        (out / 'verification.json').write_text(json.dumps(status, indent=2) + '\n')
        print('All declared module targets and every exported theorem passed both fresh builds.', flush=True)
        return 0
    except Exception as exc:
        (out / 'verification-failed.json').write_text(json.dumps(
            {'status': 'FAILED', 'error': str(exc), 'compiler': version,
             'source_sha256': hashes, 'builds': records}, indent=2) + '\n')
        raise


if __name__ == '__main__':
    raise SystemExit(main())
