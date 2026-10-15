#!/usr/bin/env python3
"""Fresh Lean 4.19.0 build and transitive axiom audit for Agent 106.

Build products are isolated; existing objects never enter the import path.
Research logs and source hashes are written to the requested evidence directory.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
BASE = REPO / 'proofs/research/continuation/LychrelDigitSums.lean'
BASE_SHA = 'ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57'
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}
FLAGS = ['-j1', '-DElab.async=false']


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def code_only(text):
    out, i, depth = [], 0, 0
    while i < len(text):
        if text.startswith('/-', i):
            depth += 1
            i += 2
        elif depth and text.startswith('-/', i):
            depth -= 1
            i += 2
        elif depth:
            i += 1
        elif text.startswith('--', i):
            end = text.find('\n', i)
            i = len(text) if end < 0 else end
        else:
            out.append(text[i])
            i += 1
    assert depth == 0, 'Unclosed comment'
    return ''.join(out)


def declarations(source):
    """Require a simple, explicit namespace layout for the audit inventory."""
    ns = re.findall(r'^namespace\s+(\S+)\s*$', source, re.M)
    assert len(ns) == 1, ('Expected one namespace', ns)
    names = re.findall(r'^(?:noncomputable\s+)?(?:theorem|def|abbrev)\s+([\w\u0080-\uffff]+)', source, re.M)
    return [ns[0] + '.' + n for n in names]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--lean', type=Path, required=True)
    ap.add_argument('--build-dir', type=Path, required=True)
    ap.add_argument('--evidence-dir', type=Path, required=True)
    ap.add_argument('--modules', nargs='+', required=True,
                    help='Explicit complete modules to include; dependencies are added automatically.')
    args = ap.parse_args()
    lean, build, evidence = args.lean.resolve(), args.build_dir.resolve(), args.evidence_dir.resolve()
    assert not build.exists() or not any(build.iterdir()), 'Use an empty build directory'
    build.mkdir(parents=True, exist_ok=True)
    evidence.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, LEAN_PATH=str(build))
    env.pop('LEAN_SRC_PATH', None)
    env.pop('LEAN_SYSROOT', None)
    version = subprocess.check_output([str(lean), '--version'], env=env, text=True).strip()
    assert 'version 4.19.0,' in version, version
    assert sha(BASE) == BASE_SHA, 'Baseline source changed'
    sources = {'LychrelDigitSums': BASE}
    sources.update({p.stem: p for p in HERE.glob('*.lean') if p.stem != 'AllAxioms'})
    order, active, audit_names = [], set(), []
    def visit(name):
        if name in order:
            return
        assert name in sources and name not in active, ('Unknown/cyclic import', name)
        active.add(name)
        code = code_only(sources[name].read_text())
        assert not re.search(r'\b(sorry|admit|native_decide|axiom|unsafe|sorryAx)\b', code), name
        for line in re.findall(r'^import\s+([^\n]+)', code, re.M):
            for dep in line.split():
                if dep not in {'Std', 'Init'}:
                    visit(dep)
        if name != 'LychrelDigitSums':
            audit_names.extend(declarations(code))
        active.remove(name)
        order.append(name)
    for name in args.modules:
        visit(name)
    assert len(audit_names) == len(set(audit_names)), 'Duplicate declaration'
    for name in order:
        shutil.copyfile(sources[name], build / (name + '.lean'))
    audit = '\n'.join('import ' + n for n in args.modules) + '\n'
    audit += '\n'.join('#print axioms ' + n for n in audit_names) + '\n'
    (build / 'AllAxioms.lean').write_text(audit)
    (evidence / 'AllAxioms.lean').write_text(audit)
    report = {'status': 'RUNNING', 'version': version, 'compiler_sha256': sha(lean),
              'flags': FLAGS, 'modules_requested': args.modules, 'modules': [],
              'base_sha256': BASE_SHA, 'checker_sha256': sha(__file__),
              'preloads': {p: sha(p) for p in re.split(r'[:\s]+', env.get('LD_PRELOAD', '')) if p},
              'audit_declarations': audit_names}
    def save():
        (evidence / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    save()
    for name in order + ['AllAxioms']:
        command = [str(lean), *FLAGS, '-o', name + '.olean', name + '.lean']
        start = time.monotonic()
        proc = subprocess.run(command, cwd=build, env=env, capture_output=True, text=True)
        output = proc.stdout + proc.stderr
        log = evidence / (name + '.log')
        log.write_text(output)
        ok = proc.returncode == 0 and not re.search(r"sorryAx|Lean\.ofReduceBool|Lean\.trustCompiler|error:|declaration uses 'sorry'", output)
        item = {'module': name, 'command': command, 'exit_code': proc.returncode,
                'seconds': time.monotonic() - start, 'source_sha256': sha(build / (name + '.lean')),
                'log_sha256': sha(log), 'status': 'PASS' if ok else 'FAIL'}
        if name in sources:
            item['source_path'] = str(sources[name].relative_to(REPO))
            assert sha(sources[name]) == item['source_sha256'], 'Source changed while compiling'
        report['modules'].append(item)
        save()
        print(name, item['status'], round(item['seconds'], 2), flush=True)
        if not ok:
            report['status'] = 'FAIL'
            save()
            raise SystemExit(1)
    output = (evidence / 'AllAxioms.log').read_text()
    found = {}
    for name, axioms in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", output):
        found[name] = [a.strip() for a in axioms.split(',') if a.strip()]
    for name in re.findall(r"'([^']+)' does not depend on any axioms", output):
        found[name] = []
    assert set(found) == set(audit_names), ('Audit inventory mismatch', set(audit_names) - set(found))
    assert all(set(aa) <= ALLOWED for aa in found.values()), found
    report['axioms'] = found
    report['status'] = 'PASS'
    save()


if __name__ == '__main__':
    main()
