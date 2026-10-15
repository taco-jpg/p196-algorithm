#!/usr/bin/env python3
"""Independent source snapshot, clean Lean rebuild, and exported-theorem audit.

This script is maintained by the reviewer and is run only after source freeze.
The build directory is freshly created and never consumes author .olean files.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import time

ROOT = Path('/workspace/scratch/64704429df15')
REPO = ROOT / 'p196-agent-107'
CONTRIB = REPO / 'proofs/contributions/agent-107/partition-seam-response'
REVIEW = CONTRIB / 'review'
LEAN = ROOT / 'env107/lean'
BASE_MODULES = [
    ('LychrelDigitSums', REPO / 'proofs/research/continuation/LychrelDigitSums.lean'),
    ('IncomingCarrySensitivity', REPO / 'proofs/research/main_existence_attempt/renewal_pass/lean/incoming_carry/IncomingCarrySensitivity.lean'),
    ('RawSymmetryObstruction', REPO / 'proofs/research/main_existence_attempt/renewal_pass/lean/raw_symmetry/RawSymmetryObstruction.lean'),
    ('IncomingCarry', REPO / 'proofs/contributions/2026-10-14-collision-formal/IncomingCarry.lean'),
    ('CarryResponseMass', REPO / 'proofs/contributions/2026-10-14-collision-mass/CarryResponseMass.lean'),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def uncomments(source):
    """Erase Lean comments while retaining newlines for declaration extraction."""
    result = []
    i = 0
    level = 0
    in_string = False
    while i < len(source):
        if level:
            if source.startswith('/-', i):
                level += 1
                result.extend('  ')
                i += 2
            elif source.startswith('-/', i):
                level -= 1
                result.extend('  ')
                i += 2
            else:
                result.append('\n' if source[i] == '\n' else ' ')
                i += 1
        elif not in_string and source.startswith('/-', i):
            level = 1
            result.extend('  ')
            i += 2
        elif not in_string and source.startswith('--', i):
            end = source.find('\n', i)
            if end < 0:
                result.extend(' ' * (len(source) - i))
                break
            result.extend(' ' * (end - i))
            i = end
        else:
            ch = source[i]
            result.append(ch)
            if ch == '"' and (i == 0 or source[i - 1] != '\\'):
                in_string = not in_string
            i += 1
    return ''.join(result)


def theorem_names(source):
    clean = uncomments(source)
    namespace = None
    names = []
    for line in clean.splitlines():
        ns = re.match(r'^namespace\s+(\S+)\s*$', line)
        if ns:
            if namespace is not None:
                raise RuntimeError('Nested namespace requires explicit audit parser update')
            namespace = ns.group(1)
        declaration = re.match(r'^(?:noncomputable\s+)?theorem\s+([^\s(:]+)', line)
        if declaration:
            if namespace is None:
                raise RuntimeError('Exported theorem outside expected namespace')
            names.append(namespace + '.' + declaration.group(1))
        if line.startswith('end '):
            namespace = None
    return names


def resolve_modules():
    """Discover all delivered top-level modules, then sort their import DAG."""
    paths = dict(BASE_MODULES)
    new = {p.stem for p in CONTRIB.glob('*.lean')}
    paths.update((p.stem, p) for p in CONTRIB.glob('*.lean'))
    remaining = dict(paths)
    ordered = []
    complete = {'Std'}
    while remaining:
        progressed = False
        for name, path in list(remaining.items()):
            imports = []
            for line in uncomments(path.read_text()).splitlines():
                if line.startswith('import '):
                    imports.extend(line.split()[1:])
            if all(dep in complete for dep in imports):
                ordered.append((name, path))
                complete.add(name)
                del remaining[name]
                progressed = True
        if not progressed:
            raise RuntimeError('Unresolved or cyclic imports: ' + repr(list(remaining)))
    return ordered, new


def main():
    modules, new = resolve_modules()
    build = Path(tempfile.mkdtemp(prefix='review107-clean-', dir=ROOT))
    logs = REVIEW / build.name
    logs.mkdir()
    manifest = {
        'status': 'RUNNING',
        'independent_reviewer_execution': True,
        'author_olean_files_used': False,
        'build_directory': str(build),
        'lean_path': str(LEAN),
        'lean_version': subprocess.check_output([str(LEAN), '--version'], text=True).strip(),
        'lean_native_sha256': sha(ROOT / 'toolchain/lean-4.19.0-linux/bin/lean'),
        'shim_sha256': sha(ROOT / 'env107/readlink_self.so'),
        'sources': [],
        'compile_records': [],
        'exported_theorems': [],
    }
    manifest_path = logs / 'manifest.json'

    def save():
        manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')

    for module, original in modules:
        copy = build / (module + '.lean')
        shutil.copyfile(original, copy)
        source_hash = sha(original)
        if sha(copy) != source_hash:
            raise RuntimeError('Snapshot mismatch: ' + module)
        record = {'module': module, 'source': str(original.relative_to(REPO)),
                  'source_sha256': source_hash, 'new_module': module in new}
        if module in new:
            clean = uncomments(copy.read_text())
            forbidden = sorted(set(re.findall(r'\b(?:sorry|admit|native_decide|axiom)\b', clean)))
            record['forbidden_tokens_outside_comments'] = forbidden
            if forbidden:
                raise RuntimeError('Forbidden proof token: ' + module + ': ' + repr(forbidden))
            names = theorem_names(copy.read_text())
            record['exported_theorems'] = names
            manifest['exported_theorems'].extend(names)
        manifest['sources'].append(record)
    save()
    env = dict(os.environ, LEAN_PATH=str(build))

    def execute(module, audit=False):
        command = [str(LEAN), '-j1', '-DElab.async=false']
        if not audit:
            command += ['-o', module + '.olean']
        command += [module + '.lean']
        print('START', module, flush=True)
        start = time.monotonic()
        result = subprocess.run(command, cwd=build, env=env, text=True, capture_output=True)
        log = logs / (module + '.log')
        log.write_text(result.stdout + result.stderr)
        record = {'module': module, 'command': command, 'cwd': str(build),
                  'LEAN_PATH': str(build), 'exit_code': result.returncode,
                  'seconds': round(time.monotonic() - start, 3),
                  'log': str(log.relative_to(REPO)), 'log_sha256': sha(log)}
        if not audit and (build / (module + '.olean')).exists():
            record['olean_sha256'] = sha(build / (module + '.olean'))
        manifest['compile_records'].append(record)
        save()
        if result.returncode:
            manifest['status'] = 'FAIL_COMPILE'
            save()
            print(result.stdout + result.stderr, flush=True)
            raise SystemExit(1)
        print('PASS', module, record['seconds'], flush=True)
        return result.stdout + result.stderr

    for module, original in modules:
        execute(module)
    audit_source = '\n'.join('import ' + module for module, _ in modules if module in new) + '\n\n'
    audit_source += '\n'.join('#print axioms ' + name for name in manifest['exported_theorems']) + '\n'
    audit_path = build / 'IndependentAxiomAudit.lean'
    audit_path.write_text(audit_source)
    shutil.copyfile(audit_path, logs / audit_path.name)
    audit_output = execute('IndependentAxiomAudit', audit=True)
    axioms = set()
    reports = {}
    for name in manifest['exported_theorems']:
        empty = "'" + name + "' does not depend on any axioms"
        if empty in audit_output:
            reports[name] = []
            continue
        match = re.search(re.escape("'" + name + "' depends on axioms: [") + r'([^\]]*)\]', audit_output)
        if match is None:
            raise RuntimeError('Missing axiom report: ' + name)
        deps = sorted(item.strip() for item in match.group(1).split(',') if item.strip())
        reports[name] = deps
        axioms.update(deps)
    manifest['axiom_reports'] = reports
    manifest['axiom_union'] = sorted(axioms)
    manifest['unexpected_axioms'] = sorted(axioms - {'propext', 'Quot.sound', 'Classical.choice'})
    for source in manifest['sources']:
        original = REPO / source['source']
        snapshot = build / (source['module'] + '.lean')
        source['unchanged_after_execution'] = sha(original) == source['source_sha256'] == sha(snapshot)
    manifest['status'] = ('PASS' if not manifest['unexpected_axioms']
                          and all(s['unchanged_after_execution'] for s in manifest['sources'])
                          else 'FAIL_AUDIT_OR_SOURCE_CHANGED')
    save()
    print(manifest['status'], manifest_path, flush=True)
    if manifest['status'] != 'PASS':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
