#!/usr/bin/env python3
"""Replay Agent #14's pinned selected-source Lean audit in a NEW directory.

Use early-root at f49d2fa... and late-root at eb893f0..., or byte-identical
source snapshots validated against selected_manifest.json. No project objects
are reused. This audits a fixed named inventory, not every repository claim.
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
import time
from datetime import datetime, timezone


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--early-root', required=True, type=Path)
    parser.add_argument('--late-root', required=True, type=Path)
    parser.add_argument('--lean', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--manifest', type=Path,
                        default=Path(__file__).with_name('selected_manifest.json'))
    parser.add_argument('--timeout', type=int, default=600)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    lean = args.lean.resolve(strict=True)
    if sha(lean) != manifest['compiler_sha256']:
        raise ValueError('Compiler hash differs from the pinned Linux release.')
    output = args.output.resolve()
    if output.exists():
        raise ValueError('Output must not already exist: clean build is required.')
    output.mkdir(parents=True)
    build, logs = output/'build', output/'logs'
    build.mkdir(); logs.mkdir()
    roots = {'early': args.early_root.resolve(), 'late': args.late_root.resolve()}
    report = {'agent': 14, 'started_utc': stamp(), 'status': 'IN_PROGRESS',
              'source_pins': manifest['source_pins'], 'initial_project_entries': [],
              'compiler_sha256': sha(lean), 'commands': [], 'sources': []}
    report_path = output/'execution.json'
    env = os.environ.copy()
    env['LEAN_PATH'] = str(build)
    env.pop('LEAN_SYSROOT', None)
    env.pop('LD_PRELOAD', None)

    def save() -> None:
        report_path.write_text(json.dumps(report, indent=2)+'\n')

    def execute(label: str, argv: list[str]) -> str:
        entry = {'label': label, 'argv': argv, 'cwd': str(build),
                 'LEAN_PATH': str(build), 'started_utc': stamp(),
                 'timeout_seconds': args.timeout}
        report['commands'].append(entry)
        save()
        t0 = time.monotonic()
        try:
            result = subprocess.run(argv, cwd=build, env=env,
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    timeout=args.timeout, check=False)
            raw, exit_code = result.stdout, result.returncode
        except subprocess.TimeoutExpired as exc:
            raw, exit_code = exc.stdout or b'', 'TIMEOUT'
        log = logs/(label+'.log')
        log.write_bytes(raw)
        entry.update(exit_code=exit_code, elapsed_seconds=time.monotonic()-t0,
                     log=str(log.relative_to(output)), log_sha256=sha(log),
                     finished_utc=stamp())
        save()
        if exit_code != 0:
            raise RuntimeError(f'{label} did not pass; inspect {log}')
        print(f'PASS {label}', flush=True)
        return raw.decode('utf-8', errors='strict')

    try:
        report['compiler_version'] = execute('00-version', [str(lean), '--version']).strip()
        if 'version 4.19.0' not in report['compiler_version']:
            raise ValueError('Unexpected Lean version.')
        for i, item in enumerate(manifest['modules'], start=1):
            source = roots[item['snapshot']]/item['path']
            if sha(source) != item['sha256']:
                raise ValueError(f'Source hash differs: {source}')
            local = build/source.name
            if local.exists():
                raise ValueError(f'Duplicate module filename: {source.name}')
            shutil.copyfile(source, local)
            record = dict(item)
            report['sources'].append(record)
            execute(f'{i:02d}-{local.stem}',
                    [str(lean), '-j1', '-o', local.with_suffix('.olean').name, local.name])
            record['source_unchanged'] = sha(source) == sha(local) == item['sha256']
            if not record['source_unchanged']:
                raise ValueError(f'Source changed during replay: {source}')
            record['object_sha256'] = sha(local.with_suffix('.olean'))
            save()
        names = manifest['theorem_names']
        driver = build/'Agent14SelectedAudit.lean'
        text = '\n'.join('import '+Path(m['path']).stem for m in manifest['modules'])
        text += '\n\n'+'\n'.join('#print axioms '+n for n in names)+'\n'
        text += '\n'.join('#check '+n for n in manifest['endpoint_queries'])+'\n'
        driver.write_text(text)
        report['audit_driver_sha256'] = sha(driver)
        stdout = execute('25-Agent14SelectedAudit', [str(lean), '-j1', driver.name])
        # A complete named result is required for every query. Multiline axiom
        # lists are parsed as one result, rather than accidentally ignored.
        pattern = re.compile(r"'([^']+)'\s+(?:does not depend on any axioms|depends on axioms:\s*\[([^\]]*)\])")
        found: dict[str, list[str]] = {}
        allowlist = set(manifest['allowed_axioms'])
        for name, body in pattern.findall(stdout):
            axioms = [part.strip() for part in body.split(',') if part.strip()]
            if name in found:
                raise ValueError(f'Duplicate audit result: {name}')
            if not set(axioms) <= allowlist:
                raise ValueError(f'Forbidden axiom dependency in {name}: {axioms}')
            found[name] = axioms
        if set(found) != set(names) or len(names) != len(set(names)):
            raise ValueError('Axiom output does not match the exact named inventory.')
        report['axiom_audit'] = found
        report['audited_distinct_names'] = len(found)
        report['successful_source_modules'] = len(manifest['modules'])
        report['status'] = 'PASS'
        print(f'PASS complete: {len(manifest["modules"])} modules, {len(found)} named axiom queries', flush=True)
    except Exception as exc:
        report['status'] = 'FAILED'
        report['error'] = f'{type(exc).__name__}: {exc}'
        print(report['error'], file=sys.stderr, flush=True)
    finally:
        report['finished_utc'] = stamp()
        save()
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
