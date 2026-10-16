#!/usr/bin/env python3
"""Fresh, pinned Lean 4.19.0 rebuild. Never converts missing tooling into PASS.

Usage:
  python verify_lean.py --lean /path/to/lean --repo /path/to/p196-algorithm --output /new/path
  python verify_lean.py --lean /path/to/lean --download-pinned --output /new/path
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.request import urlopen

PIN = '1c6c56b25de0c7348d82cb304e761f227326b6c9'
REPO = 'taco-jpg/p196-algorithm'
DEPENDENCIES = [
    ('ExteriorClock', 'proofs/ExteriorClock__b2b9d37012d53747.lean', 'fc873f14a30ab4ef01c9a78a25a64dfddac1d560'),
    ('GeneralCarryMass', 'proofs/GeneralCarryMass__ad1a2561147adc83.lean', 'c39b06abecab551006fad351b941dbbf1ccb56ea'),
    ('GeneralMomentAbsorption', 'proofs/GeneralMomentAbsorption__d6c541c17a8aa76f.lean', '8e6aac5d5450b68b98535fa90d5b828019068b69'),
]
NEW = ['InitialValidity', 'FiniteOverflow']
NS = 'P196.Agent5.General.InitialValidity.'
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}
HERE = Path(__file__).resolve().parent


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def lean_code_only(source: str) -> str:
    """Remove nested block comments, line comments, and quoted string contents."""
    out: list[str] = []
    i = 0
    depth = 0
    while i < len(source):
        if depth:
            if source.startswith('/-', i):
                depth += 1; i += 2
            elif source.startswith('-/', i):
                depth -= 1; i += 2
            else:
                out.append('\n' if source[i] == '\n' else ' '); i += 1
        elif source.startswith('/-', i):
            depth = 1; out.append(' '); i += 2
        elif source.startswith('--', i):
            j = source.find('\n', i)
            i = len(source) if j < 0 else j
        elif source[i] == '"':
            out.append(' '); i += 1
            while i < len(source):
                if source[i] == '\\':
                    i += 2
                elif source[i] == '"':
                    i += 1; break
                else:
                    i += 1
        else:
            out.append(source[i]); i += 1
    return ''.join(out)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--lean', type=Path)
    p.add_argument('--repo', type=Path)
    p.add_argument('--download-pinned', action='store_true')
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--timeout', type=int, default=180)
    args = p.parse_args()
    if args.output.exists():
        p.error('--output must not exist; a clean build directory is required')
    args.output.mkdir(parents=True)
    receipt: dict = {'status': 'STARTED', 'source_commit': PIN, 'compiler': None,
                     'builds': [], 'sources': {}, 'axioms': {}, 'commands': [],
                     'independent_review': False}
    def finish(code: int, status: str, explanation: str = '') -> int:
        receipt['status'] = status
        receipt['explanation'] = explanation
        receipt['exit_code'] = code
        (args.output/'verification.json').write_text(json.dumps(receipt, indent=2)+'\n')
        print(json.dumps({'status': status, 'explanation': explanation, 'exit_code': code}, indent=2))
        return code
    lean = str(args.lean) if args.lean else shutil.which('lean')
    if not lean or not Path(lean).is_file():
        return finish(2, 'BUILD_NOT_RUN_NO_LEAN_EXECUTABLE', 'No compiler execution or axiom audit occurred.')
    lean = str(Path(lean).resolve())
    try:
        ver = subprocess.run([lean, '--version'], capture_output=True, text=True, timeout=15)
        receipt['commands'].append([lean, '--version'])
        receipt['compiler'] = {'path': lean, 'stdout': ver.stdout, 'stderr': ver.stderr, 'exit_code': ver.returncode}
        if ver.returncode or '4.19.0' not in ver.stdout or '6caaee842e94' not in ver.stdout:
            return finish(2, 'TOOLCHAIN_MISMATCH', 'Expected official Lean 4.19.0, commit 6caaee842e94.')
        for module, relpath, expected_blob in DEPENDENCIES:
            if args.repo:
                data = (args.repo / relpath).read_bytes()
            elif args.download_pinned:
                with urlopen(f'https://raw.githubusercontent.com/{REPO}/{PIN}/{relpath}', timeout=30) as response:
                    data = response.read()
            else:
                return finish(2, 'DEPENDENCY_SOURCE_UNAVAILABLE', 'Supply --repo or explicitly enable --download-pinned.')
            if git_blob(data) != expected_blob:
                return finish(2, 'DEPENDENCY_HASH_MISMATCH', relpath)
            (args.output/(module+'.lean')).write_bytes(data)
            receipt['sources'][module] = {'path': relpath, 'git_blob_sha1': expected_blob, 'sha256': sha256(data)}
        theorem_names = []
        for module in NEW:
            data = (HERE/(module+'.lean')).read_bytes()
            text = data.decode()
            (args.output/(module+'.lean')).write_bytes(data)
            receipt['sources'][module] = {'path': module+'.lean', 'sha256': sha256(data)}
            theorem_names.extend(NS+n for n in re.findall(r'^theorem\s+([A-Za-z0-9_]+)', text, re.M))
        for module in [d[0] for d in DEPENDENCIES] + NEW:
            source = (args.output/(module+'.lean')).read_text()
            bad = re.findall(r'\b(?:sorry|admit|native_decide|sorryAx|axiom)\b', lean_code_only(source))
            if bad:
                return finish(2, 'FORBIDDEN_SOURCE_TOKEN', f'{module}: {sorted(set(bad))}')
        env = os.environ.copy()
        env['LEAN_PATH'] = str(args.output.resolve())
        order = [d[0] for d in DEPENDENCIES] + NEW
        audit = 'import FiniteOverflow\n\n' + '\n'.join('#print axioms '+n for n in theorem_names)+'\n'
        (args.output/'Agent5AxiomAudit.lean').write_text(audit)
        for module in order + ['Agent5AxiomAudit']:
            command = [lean, '-o', module+'.olean', module+'.lean']
            receipt['commands'].append(command)
            result = subprocess.run(command, cwd=args.output, env=env, capture_output=True,
                                    text=True, timeout=args.timeout)
            log = result.stdout + result.stderr
            (args.output/(module+'.log')).write_text(log)
            receipt['builds'].append({'module': module, 'exit_code': result.returncode,
                                      'log_sha256': sha256(log.encode())})
            if result.returncode:
                return finish(1, 'LEAN_BUILD_FAILED', module)
            if 'sorryAx' in log:
                return finish(1, 'AXIOM_GATE_FAILED', module)
        audit_log = (args.output/'Agent5AxiomAudit.log').read_text()
        for name in theorem_names:
            escaped = re.escape(name)
            empty = re.search(r"'?"+escaped+r"'? does not depend on any axioms", audit_log)
            listed = re.search(r"'?"+escaped+r"'? depends on axioms:\s*\[([^\]]*)\]", audit_log, re.S)
            if empty:
                axes = []
            elif listed:
                axes = [a.strip() for a in listed.group(1).split(',') if a.strip()]
            else:
                return finish(1, 'AXIOM_REPORT_INCOMPLETE', name)
            receipt['axioms'][name] = axes
            if set(axes) - ALLOWED:
                return finish(1, 'AXIOM_GATE_FAILED', name)
        return finish(0, 'LEAN_CHECKED_SELF_REBUILD', 'Independent review and accepted-build integration remain separate.')
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        return finish(2, 'VERIFICATION_INTERRUPTED', type(exc).__name__+': '+str(exc))

if __name__ == '__main__':
    sys.exit(main())
