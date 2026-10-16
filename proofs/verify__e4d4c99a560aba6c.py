#!/usr/bin/env python3
"""Clean-build the explicitly accepted Agent 12 modules and audit every export."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time

FORBIDDEN = re.compile(r"\b(sorry|admit|axiom|native_decide)\b|Lean\.(ofReduceBool|trustCompiler)\b")
AXIOM_LINE = re.compile(r"'([^']+)' (?:depends on axioms: \[([^]]*)\]|does not depend on any axioms)")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def lean_code(text: str) -> str:
    """Remove nested Lean comments and strings before checking source tokens."""
    output: list[str] = []
    i = depth = 0
    while i < len(text):
        if depth:
            if text.startswith('/-', i):
                depth += 1
                i += 2
            elif text.startswith('-/', i):
                depth -= 1
                i += 2
            else:
                output.append('\n' if text[i] == '\n' else ' ')
                i += 1
        elif text.startswith('/-', i):
            depth = 1
            output.append(' ')
            i += 2
        elif text.startswith('--', i):
            j = text.find('\n', i)
            i = len(text) if j < 0 else j
        elif text[i] == '"':
            output.append(' ')
            i += 1
            while i < len(text):
                if text[i] == '\\':
                    i += 2
                elif text[i] == '"':
                    i += 1
                    break
                else:
                    i += 1
            else:
                raise ValueError('Unterminated Lean string')
        else:
            output.append(text[i])
            i += 1
    if depth:
        raise ValueError('Unterminated Lean block comment')
    return ''.join(output)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lean', default=shutil.which('lean'))
    parser.add_argument('--log-dir', type=Path, required=True)
    args = parser.parse_args()
    if not args.lean:
        parser.error('Lean 4.19.0 is required: supply --lean or put lean on PATH')
    lean = Path(args.lean).resolve()
    root = Path(__file__).resolve().parents[3]
    manifest = json.loads(Path(__file__).with_name('accepted.json').read_text())
    out = args.log_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    report: dict = {'agent': 12, 'status': 'INCOMPLETE', 'commands': [],
                    'source_snapshot': manifest['source_snapshot'],
                    'independent_semantic_review': False,
                    'build_kind': 'fresh-directory source rebuild',
                    'sources': [], 'axioms': {}}
    try:
        version = subprocess.check_output([str(lean), '--version'], text=True).strip()
        report.update(lean_version=version, lean_binary_sha256=digest(lean))
        (out / 'lean-version.log').write_text(version + '\n')
        if 'version 4.19.0,' not in version or manifest['lean_commit'] not in version:
            raise ValueError(f'Unexpected Lean compiler: {version}')
        expected = [name for m in manifest['modules'] for name in m['theorems']]
        if len(expected) != len(set(expected)):
            raise ValueError('Duplicate accepted theorem name')
        records = manifest['dependencies'] + manifest['modules']
        with tempfile.TemporaryDirectory(prefix='agent12-clean-') as tmp:
            clean = Path(tmp)
            env = dict(os.environ, LEAN_PATH=str(clean))
            for record in records:
                src = root / record['path']
                actual_hash = digest(src)
                if 'sha256' in record and actual_hash != record['sha256']:
                    raise ValueError(f"Changed pinned source: {record['path']}")
                text = src.read_text()
                code = lean_code(text)
                rejected = FORBIDDEN.search(code)
                if rejected:
                    raise ValueError(f"Rejected source token {rejected[0]} in {record['path']}")
                if record in manifest['modules']:
                    short_names = re.findall(r'^\s*(?:private\s+)?(?:theorem|lemma)\s+([\w\'.]+)', code, re.M)
                    prefix = record['namespace']
                    discovered = {prefix + '.' + n for n in short_names}
                    if discovered != set(record['theorems']):
                        raise ValueError(f"Manifest does not cover every theorem in {record['path']}")
                name = record['module']
                destination = clean / f'{name}.lean'
                destination.write_bytes(src.read_bytes())
                retained = out / 'sources' / record['path']
                retained.parent.mkdir(parents=True, exist_ok=True)
                retained.write_bytes(src.read_bytes())
                report['sources'].append({'path': record['path'], 'sha256': actual_hash})
                command = [str(lean), '-o', f'{name}.olean', f'{name}.lean']
                started = time.monotonic()
                with (out / f'{name}.log').open('w') as log:
                    result = subprocess.run(command, cwd=clean, env=env, stdout=log,
                                            stderr=subprocess.STDOUT, timeout=600, check=False)
                report['commands'].append({'args': command, 'module': name,
                    'exit_code': result.returncode, 'seconds': round(time.monotonic()-started, 3)})
                if result.returncode:
                    raise RuntimeError(f'Lean build failed for {name}: exit {result.returncode}')
            audit = '\n'.join('import ' + m['module'] for m in manifest['modules'])
            audit += '\n\n' + '\n'.join('#print axioms ' + n for n in expected) + '\n'
            (clean / 'Audit.lean').write_text(audit)
            (out / 'Audit.lean').write_text(audit)
            command = [str(lean), 'Audit.lean']
            started = time.monotonic()
            result = subprocess.run(command, cwd=clean, env=env, capture_output=True,
                                    text=True, timeout=600, check=False)
            output = result.stdout + result.stderr
            (out / 'axioms.log').write_text(output)
            report['commands'].append({'args': command, 'module': 'Audit',
                'exit_code': result.returncode, 'seconds': round(time.monotonic()-started, 3)})
            if result.returncode:
                raise RuntimeError(f'Axiom audit failed: exit {result.returncode}')
            parsed = AXIOM_LINE.findall(output)
            if len(parsed) != len(expected) or {name for name, _ in parsed} != set(expected):
                raise ValueError('Missing, duplicate, or unexpected theorem axiom output')
            allowed = set(manifest['allowed_axioms'])
            for name, axiom_list in parsed:
                axioms = [a.strip() for a in axiom_list.split(',') if a.strip()]
                if set(axioms) - allowed:
                    raise ValueError(f'Disallowed transitive axioms for {name}: {axioms}')
                report['axioms'][name] = axioms
            report['status'] = 'LEAN_CHECKED'
            report['accepted_theorems'] = len(expected)
    except Exception as error:
        report['error'] = f'{type(error).__name__}: {error}'
        raise
    finally:
        (out / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'theorems': len(report['axioms']),
                      'log_directory': str(out)}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
