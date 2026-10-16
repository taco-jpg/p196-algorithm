"""Compile pinned sources and require an explicit accepted audit for each theorem.

This is a build/report checker, not an extension to Lean's trusted kernel.
The source files must already be trusted to execute their elaborator commands.
"""
from __future__ import annotations
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}
PATTERN = re.compile(
    r"'([^']+)'\s+(?:does not depend on any axioms|depends on axioms:\s*\[([^\]]*)\])",
    re.MULTILINE)


def compile_and_audit(lean: Path, source: Path, output: Path) -> dict:
    source = source.resolve()
    output.mkdir(parents=True, exist_ok=True)
    text = source.read_text()
    declared = re.findall(r'^\s*theorem\s+([^\s(:]+)', text, re.MULTILINE)
    if re.search(r'^\s*(?:axiom|opaque)\s+', text, re.MULTILINE):
        raise RuntimeError(f'{source.name}: custom axiom/opaque declaration requires separate review')
    env = dict(os.environ, LEAN_PATH=str(source.parent))
    started = time.monotonic()
    p = subprocess.run([str(lean), '-j1', '-o', str(source.with_suffix('.olean')),
                        source.name], cwd=source.parent, env=env,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       text=True, timeout=360, check=False)
    log = p.stdout
    (output / (source.stem + '.log')).write_text(log)
    print(log, end='', flush=True)
    if p.returncode != 0:
        raise RuntimeError(f'{source.name}: compiler exited {p.returncode}')
    audits = {}
    for name, dependencies in PATTERN.findall(log):
        axioms = {x.strip() for x in dependencies.split(',') if x.strip()}
        if axioms - ALLOWED:
            raise RuntimeError(f'{name}: unexpected dependencies {sorted(axioms-ALLOWED)}')
        audits[name] = sorted(axioms)
    for name in declared:
        matches = [n for n in audits if n == name or n.endswith('.' + name)]
        if len(matches) != 1:
            raise RuntimeError(f'{source.name}: missing or ambiguous dependency audit for {name}')
    result = {'file': source.name, 'source_sha256': sha256(source.read_bytes()).hexdigest(),
              'compiler_exit': p.returncode, 'declared_theorems': len(declared),
              'audits': audits, 'log_sha256': sha256(log.encode()).hexdigest(),
              'elapsed_seconds': round(time.monotonic()-started, 4)}
    (output / (source.stem + '-audit.json')).write_text(json.dumps(result, indent=2)+'\n')
    return result


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--lean', type=Path, required=True)
    p.add_argument('--output', type=Path, default=Path('logs'))
    p.add_argument('sources', type=Path, nargs='+')
    args = p.parse_args()
    lean = args.lean.resolve()
    version = subprocess.check_output([str(lean), '--version'], text=True).strip()
    if 'version 4.19.0,' not in version:
        raise RuntimeError('This certificate is pinned to Lean 4.19.0')
    results = [compile_and_audit(lean, source, args.output) for source in args.sources]
    report = {'compiler': version, 'source_commit': os.environ.get('GITHUB_SHA'),
              'files': results, 'scope': 'Compiler and dependency audit; interpretation and originality require separate review.'}
    (args.output / 'audit-summary.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'compiler': version,
                      'theorems': sum(x['declared_theorems'] for x in results)}, indent=2))

if __name__ == '__main__':
    main()
