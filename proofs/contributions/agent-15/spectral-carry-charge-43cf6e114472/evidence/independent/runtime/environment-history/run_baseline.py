#!/usr/bin/env python3
"""Run the authorized, isolated, one-module Agent 15 environment baseline."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path('/workspace/scratch/43cf6e114472/runtime')
SOURCE = ROOT / 'source_snapshots/original/proofs/research/continuation/LychrelDigitSums.lean'
BUILD = ROOT / 'baseline-001'
LEAN = Path('/tmp/p196-agent5-lean/lean-4.19.0-linux/bin/lean')
SOURCE_COMMIT = '5ff4f607535587d572fbc9e95ba9501d1fbe5fc5'
SOURCE_BLOB = '8a865176625283648a8a20dd2411ed77670eb0a2'
ENDPOINTS = ['FoldedDecimal.canonical_next_no_overflow', 'DecimalWidthGrowth.numeric_width_bounds']


def sha256(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main() -> int:
    BUILD.mkdir(exist_ok=False)
    source_dir = BUILD / 'source'
    source_dir.mkdir()
    logs = BUILD / 'logs'
    logs.mkdir()
    data = SOURCE.read_bytes()
    blob = hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()
    if blob != SOURCE_BLOB:
        raise RuntimeError(f'Source identity mismatch: {blob}')
    (source_dir / 'LychrelDigitSums.lean').write_bytes(data)
    audit = 'import LychrelDigitSums\n\n' + '\n'.join(
        f'#check {name}\n#print axioms {name}' for name in ENDPOINTS
    ) + '\n'
    (source_dir / 'BaselineAudit.lean').write_text(audit)
    compiler_files = [LEAN, *(LEAN.parent.parent / 'lib/lean').glob('*.so')]
    compiler_hashes = {str(path): sha256(path) for path in sorted(set(compiler_files))}
    report = {
        'purpose': 'Environment baseline only; not an accepted dependency or proof of the pending T/R target.',
        'status': 'RUNNING',
        'source_commit': SOURCE_COMMIT,
        'source_git_blob': blob,
        'source_sha256': hashlib.sha256(data).hexdigest(),
        'source_path': str(SOURCE),
        'source_imports': ['Std'],
        'build_directory': str(BUILD),
        'clean_project_objects': True,
        'official_toolchain_objects_reused': True,
        'sandbox_permissions': 'require_escalated',
        'compiler_files': compiler_hashes,
        'endpoints': ENDPOINTS,
        'axiom_audit_scope': 'Two explicitly selected existing endpoints; source also contains retained print-axioms commands.',
        'commands': [],
        'started_at_epoch': time.time(),
    }

    def save() -> None:
        (BUILD / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')

    env = os.environ.copy()
    env['LEAN_PATH'] = str(source_dir)

    def run(label: str, argv: list[str]) -> int:
        log = logs / (label + '.log')
        started = time.monotonic()
        with log.open('wb') as stream:
            try:
                result = subprocess.run(argv, cwd=source_dir, env=env, stdout=stream,
                                        stderr=subprocess.STDOUT, timeout=600)
                code = result.returncode
            except subprocess.TimeoutExpired:
                code = 124
        report['commands'].append({
            'label': label, 'argv': argv, 'cwd': str(source_dir),
            'environment_overrides': {'LEAN_PATH': str(source_dir)},
            'exit_code': code, 'elapsed_seconds': time.monotonic() - started,
            'log': str(log), 'log_sha256': sha256(log),
        })
        save()
        print(f'{label}: exit {code}; log {log}', flush=True)
        return code

    save()
    commands = [
        ('version', [str(LEAN), '--version']),
        ('LychrelDigitSums', [str(LEAN), '-j1', '-DElab.async=false', '--trust=0',
                            '-o', 'LychrelDigitSums.olean', 'LychrelDigitSums.lean']),
        ('BaselineAudit', [str(LEAN), '-j1', '-DElab.async=false', '--trust=0',
                          '-o', 'BaselineAudit.olean', 'BaselineAudit.lean']),
    ]
    try:
        for label, argv in commands:
            code = run(label, argv)
            if code:
                report['status'] = 'FAIL'
                report['failed_command'] = label
                return code
        if SOURCE.read_bytes() != data or (source_dir / 'LychrelDigitSums.lean').read_bytes() != data:
            raise RuntimeError('Source changed during baseline')
        if any(sha256(Path(path)) != value for path, value in compiler_hashes.items()):
            raise RuntimeError('Compiler files changed during baseline')
        report['status'] = 'PASS_ENVIRONMENT_BASELINE'
        report['audit_output'] = (logs / 'BaselineAudit.log').read_text()
        print(report['audit_output'], end='', flush=True)
        return 0
    except Exception as error:
        report['status'] = 'FAIL'
        report['error'] = repr(error)
        raise
    finally:
        report['finished_at_epoch'] = time.time()
        report['output_hashes'] = {str(p.relative_to(BUILD)): sha256(p)
                                  for p in sorted(BUILD.rglob('*'))
                                  if p.is_file() and p.name != 'verification.json'}
        save()


if __name__ == '__main__':
    raise SystemExit(main())
