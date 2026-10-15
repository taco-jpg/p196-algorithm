#!/usr/bin/env python3
"""Independent empty-object-directory Lean rebuild and environment axiom audit.

This driver does not import the development-cache driver or its declaration
scanner. The audit enumerates ALL compiled constants by their owning module
inside Lean's Environment. Kernel-safe declarations (including every theorem)
are transitively axiom-audited; compiler-generated unsafe artifacts are recorded
separately, since Lean deliberately erases their proofs to lcProof.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

BASE = [
    'proofs/research/continuation/LychrelDigitSums.lean',
    'proofs/contributions/agent-109/template-step-bridge/TemplateStep.lean',
    'proofs/contributions/agent-109/template-step-bridge/Compat.lean',
    'proofs/contributions/agent-109/template-step-bridge/IntegerEndpoints.lean',
    'proofs/contributions/agent-109/template-return-certificate/ReturnCertificate.lean',
    'proofs/contributions/agent-109/template-return-certificate/CertCompat.lean',
    'proofs/contributions/agent-109/outer-projection-bridge/OuterBridge.lean',
    'proofs/contributions/agent-109/outer-projection-bridge/OuterCompat.lean',
    'proofs/contributions/agent-109/outer-projection-bridge/agent7-deps/OuterFinite.lean',
    'proofs/contributions/agent-109/outer-projection-bridge/agent7-deps/OuterBounds.lean',
    'proofs/contributions/2026-10-15-agent8-complementary-bulk/PeriodObstructions.lean',
    'proofs/contributions/2026-10-15-agent8-complementary-bulk/ActualWordBridge.lean',
    'proofs/contributions/2026-10-15-agent2-complementary-search/ExteriorCharge.lean',
    'proofs/agent5/ExteriorClock.lean',
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def code_only(s):
    """Erase nested Lean comments and strings, preserving line positions."""
    out, i, depth, quoted = [], 0, 0, False
    while i < len(s):
        if depth:
            if s.startswith('/-', i):
                depth += 1; out.extend('  '); i += 2
            elif s.startswith('-/', i):
                depth -= 1; out.extend('  '); i += 2
            else:
                out.append('\n' if s[i] == '\n' else ' '); i += 1
        elif quoted:
            if s[i] == '\\' and i + 1 < len(s):
                out.extend('  '); i += 2
            elif s[i] == '"':
                quoted = False; out.append(' '); i += 1
            else:
                out.append('\n' if s[i] == '\n' else ' '); i += 1
        elif s.startswith('/-', i):
            depth = 1; out.extend('  '); i += 2
        elif s.startswith('--', i):
            end = s.find('\n', i)
            if end < 0: end = len(s)
            out.extend(' ' * (end - i)); i = end
        elif s[i] == '"':
            quoted = True; out.append(' '); i += 1
        else:
            out.append(s[i]); i += 1
    assert not depth and not quoted, 'Unterminated comment/string'
    return ''.join(out)


def audit_source(order):
    imports = '\n'.join('import ' + x for x in order)
    selected = ', '.join('`' + x for x in order)
    return imports + '\nimport Lean\n\nopen Lean Elab Command\n\nrun_cmd do\n' + f'  let modules : Array Name := #[{selected}]\n' + '''  let allowed : Array Name := #[`propext, `Classical.choice, `Quot.sound]
  let env ← getEnv
  let mut declarations : Array Name := #[]
  let mut theoremCount := 0
  let mut safeCount := 0
  let mut unsafeCount := 0
  for (n, _) in env.constants do
    if let some idx := env.getModuleIdxFor? n then
      if modules.contains env.header.moduleNames[idx]! then
        declarations := declarations.push n
  for n in declarations.qsort Name.lt do
    let ci := (env.find? n).get!
    let deps ← collectAxioms n
    if ci.isUnsafe then
      unsafeCount := unsafeCount + 1
      logInfo m!"AUDIT_UNSAFE_COMPILER_ARTIFACT|{n}|{deps.qsort Name.lt |>.toList}"
    else
      for ax in deps do
        unless allowed.contains ax do
          throwError m!"DISALLOWED_AXIOM|{n}|{ax}"
      let kind := if ci.isTheorem then "THEOREM" else "CONSTANT"
      if ci.isTheorem then theoremCount := theoremCount + 1
      safeCount := safeCount + 1
      logInfo m!"AUDIT|{kind}|{n}|{deps.qsort Name.lt |>.toList}"
  logInfo m!"AUDIT_TOTAL|{safeCount}|{theoremCount}|{unsafeCount}"
'''


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo', required=True, type=Path)
    ap.add_argument('--lean', required=True, type=Path)
    ap.add_argument('--build', required=True, type=Path)
    ap.add_argument('--evidence', required=True, type=Path)
    ap.add_argument('--source', action='append', required=True)
    ap.add_argument('--pin', help='Require this exact repository HEAD before snapshotting')
    args = ap.parse_args()
    repo, build, evidence, lean = args.repo.resolve(), args.build.resolve(), args.evidence.resolve(), args.lean.resolve()
    build.mkdir(parents=True, exist_ok=False)
    evidence.mkdir(parents=True, exist_ok=False)
    head = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip()
    if args.pin: assert head == args.pin, (head, args.pin)
    env = os.environ.copy()
    for k in ('LEAN_PATH', 'LEAN_SRC_PATH', 'LEAN_SYSROOT', 'LD_PRELOAD', 'LD_LIBRARY_PATH'):
        env.pop(k, None)
    env['LEAN_PATH'] = str(build)
    manifest = {'status': 'RUNNING', 'repo_head_at_snapshot': head, 'requested_pin': args.pin,
                'started_utc': datetime.now(timezone.utc).isoformat(),
                'driver_path': str(Path(__file__).resolve().relative_to(repo)),
                'driver_sha256': sha(Path(__file__).read_bytes()),
                'empty_build_directory_created': True, 'objects_reused': False,
                'compiler_launcher': str(lean), 'compiler_launcher_sha256': sha(lean.read_bytes()),
                'LEAN_PATH': str(build), 'sources': {}, 'commands': [],
                'audit_method': 'Lean Environment owning-module enumeration of ALL constants; collectAxioms transitively for every kernel-safe declaration including every theorem; generated unsafe compiler artifacts separately inventoried; no source declaration parser'}

    def save():
        (evidence / 'manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')

    def execute(label, argv):
        start = time.monotonic()
        logfile = evidence / (label + '.log')
        print('START', label, flush=True)
        with logfile.open('w') as out:
            process = subprocess.run(argv, cwd=build, env=env, stdout=out, stderr=subprocess.STDOUT)
        manifest['commands'].append({'label': label, 'argv': argv, 'cwd': str(build),
                                     'exit_code': process.returncode, 'seconds': round(time.monotonic() - start, 3),
                                     'log_sha256': sha(logfile.read_bytes()), 'log': logfile.name})
        save()
        print('END', label, process.returncode, flush=True)
        assert process.returncode == 0, f'{label} failed: {logfile}'
        return logfile.read_text()

    try:
        version = execute('version', [str(lean), '--version'])
        assert 'version 4.19.0' in version and '6caaee842e94' in version, version
        manifest['version'] = version.strip()
        mapping = {Path(p).stem: repo / p for p in BASE}
        for p in args.source:
            src = repo / p
            mapping[src.stem] = src
        order, visiting, snapshots = [], set(), {}

        def visit(name):
            if name in order: return
            assert name not in visiting, ('Import cycle', name)
            visiting.add(name)
            src = mapping[name]
            data = src.read_bytes()
            code = code_only(data.decode())
            forbidden = re.findall(r'\b(?:sorry|admit|axiom|native_decide|ofReduceBool|sorryAx|unsafe|partial)\b|debug\.skipKernelTC', code)
            assert not forbidden, (src, forbidden)
            dependencies = [x for row in re.findall(r'^import\s+([^\n]+)', code, re.M) for x in row.split()]
            for d in dependencies:
                if d not in {'Init', 'Std', 'Lean'}:
                    assert d in mapping, ('Unmapped dependency', name, d)
                    visit(d)
            snapshots[name] = data
            relative = str(src.relative_to(repo))
            blob = hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()
            pinned = subprocess.run(['git', '-C', str(repo), 'rev-parse', f'{head}:{relative}'], capture_output=True, text=True)
            manifest['sources'][name] = {'path': relative, 'sha256': sha(data), 'bytes': len(data),
                                         'git_blob_sha1': blob, 'matches_snapshot_commit': pinned.returncode == 0 and pinned.stdout.strip() == blob,
                                         'imports': dependencies, 'forbidden_tokens': []}
            if args.pin: assert manifest['sources'][name]['matches_snapshot_commit'], ('Not pinned source', relative)
            (build / (name + '.lean')).write_bytes(data)
            order.append(name)

        for src in args.source: visit(Path(src).stem)
        manifest['build_order'] = order
        save()
        for name in order:
            execute(name, [str(lean), '-j1', '-DElab.async=false', '-o', str(build / (name + '.olean')), str(build / (name + '.lean'))])
            manifest['sources'][name]['olean_sha256'] = sha((build / (name + '.olean')).read_bytes())
            save()
        audit = audit_source(order)
        (build / 'IndependentEnvironmentAudit.lean').write_text(audit)
        (evidence / 'IndependentEnvironmentAudit.lean').write_text(audit)
        result = execute('IndependentEnvironmentAudit', [str(lean), '-j1', '-DElab.async=false', str(build / 'IndependentEnvironmentAudit.lean')])
        rows = re.findall(r'AUDIT\|(THEOREM|CONSTANT)\|([^|\n]+)\|\[([^\]]*)\]', result)
        unsafe = re.findall(r'AUDIT_UNSAFE_COMPILER_ARTIFACT\|([^|\n]+)\|\[([^\]]*)\]', result)
        total = re.findall(r'AUDIT_TOTAL\|(\d+)\|(\d+)\|(\d+)', result)
        assert len(total) == 1
        assert len(rows) == int(total[0][0])
        assert len({row[1] for row in rows}) == len(rows)
        assert sum(row[0] == 'THEOREM' for row in rows) == int(total[0][1])
        assert len(unsafe) == int(total[0][2])
        assert len({row[0] for row in unsafe}) == len(unsafe)
        assert not ({row[0] for row in unsafe} & {row[1] for row in rows})
        allowed = {'propext', 'Classical.choice', 'Quot.sound'}
        assert all(set(x.strip() for x in row[2].split(',') if x.strip()) <= allowed for row in rows)
        manifest['axiom_audit'] = {name: {'kind': kind, 'axioms': [x.strip() for x in deps.split(',') if x.strip()]} for kind, name, deps in rows}
        manifest['compiled_constants_audited'] = len(rows)
        manifest['compiled_theorems_audited'] = int(total[0][1])
        manifest['compiled_constants_enumerated'] = len(rows) + len(unsafe)
        manifest['unsafe_compiler_artifacts'] = {name: [x.strip() for x in deps.split(',') if x.strip()] for name, deps in unsafe}
        manifest['unsafe_compiler_artifact_scope'] = 'Every source is scanned to exclude unsafe/partial definitions. Compiler-generated unsafe constants cannot occur in kernel-safe proof terms; their erased lcProof dependencies are NOT added to the mathematical axiom whitelist.'
        manifest['all_source_hashes_unchanged'] = all(mapping[n].read_bytes() == snapshots[n] for n in order)
        assert manifest['all_source_hashes_unchanged'], 'Source changed during independent build'
        manifest.update(status='PASS', completed_utc=datetime.now(timezone.utc).isoformat())
        save()
        print('PASS:', len(order), 'freshly compiled modules;', len(rows), 'compiled constants audited', flush=True)
    except Exception as exc:
        manifest.update(status='FAILED', failure=repr(exc), completed_utc=datetime.now(timezone.utc).isoformat())
        save()
        raise


if __name__ == '__main__':
    main()
