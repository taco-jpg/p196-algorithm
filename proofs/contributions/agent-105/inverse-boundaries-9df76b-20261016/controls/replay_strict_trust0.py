#!/usr/bin/env python3
"""Supplement an unchanged verifier PASS with an explicit --trust=0 replay.

This script reuses the verifier's exact source snapshots, build order, and
generated module-origin ProjectAudit. It does not replace that verifier's
registry, source policy, import checks, or allowed-axiom policy.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time
import traceback


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verification', type=Path, required=True)
    parser.add_argument('--registry', type=Path, required=True)
    parser.add_argument('--project', required=True)
    parser.add_argument('--lean', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()

    prior_bytes = args.verification.read_bytes()
    prior = json.loads(prior_bytes)
    if prior['status'] != 'PASS':
        raise ValueError('The unchanged verifier must already report PASS.')
    project = prior['projects'][args.project]
    if project['status'] != 'PASS':
        raise ValueError('The selected original project must report PASS.')
    registry_bytes = args.registry.read_bytes()
    if digest(registry_bytes) != prior['registry_sha256']:
        raise ValueError('Registry bytes differ from the unchanged verifier run.')
    lean = args.lean.resolve()
    if digest(lean.read_bytes()) != prior['compiler']['files'][str(lean)]:
        raise ValueError('Compiler bytes differ from the unchanged verifier run.')

    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    source = output / 'source'
    logs = output / 'logs'
    source.mkdir()
    logs.mkdir()
    original_source = args.verification.resolve().parent / args.project / 'source'
    order = project['build_order']
    if len(order) != len(set(order)) or set(order) != set(project['sources']):
        raise ValueError('The original build order does not cover its source map.')

    snapshots = {}
    for module in [*order, 'ProjectAudit']:
        relative = Path(*module.split('.')).with_suffix('.lean')
        data = (original_source / relative).read_bytes()
        if module != 'ProjectAudit':
            if digest(data) != project['sources'][module]['build_sha256']:
                raise ValueError('Original source snapshot changed: ' + module)
        target = source / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        snapshots[module] = {'sha256': digest(data), 'bytes': len(data)}

    (output / 'registry-used.json').write_bytes(registry_bytes)
    receipt = {
        'schema': 'agent105-explicit-trust0-replay-v1',
        'purpose': 'Supplemental explicit --trust=0 replay of unchanged verifier sources and audit.',
        'reviewer': 'Agent105/scope105/9df76b',
        'status': 'RUNNING',
        'source_commit': prior['source_commit'],
        'source_tree_clean_at_original_verification': prior['source_tree_clean'],
        'original_verification': str(args.verification.resolve()),
        'original_verification_sha256': digest(prior_bytes),
        'registry_sha256': digest(registry_bytes),
        'compiler': prior['compiler'],
        'project': args.project,
        'scope': project['scope'],
        'sources': snapshots,
        'build_order': order,
        'commands': [],
        'started_utc': datetime.now(timezone.utc).isoformat(),
        'repository_wide_pass': False,
    }

    def save() -> None:
        (output / 'strict-verification.json').write_text(json.dumps(receipt, indent=2) + '\n')

    env = {
        'PATH': str(lean.parent) + ':/usr/bin:/bin',
        'LANG': 'C.UTF-8',
        'LEAN_PATH': str(source),
        'LEAN_SYSROOT': str(lean.parent.parent),
    }
    receipt['environment'] = env
    save()

    def run(label: str, command: list[str]) -> str:
        path = logs / (label + '.log')
        start = time.monotonic()
        with path.open('wb') as stream:
            try:
                code = subprocess.run(command, cwd=source, env=env,
                                      stdin=subprocess.DEVNULL, stdout=stream,
                                      stderr=subprocess.STDOUT, timeout=1800).returncode
            except subprocess.TimeoutExpired:
                code = 124
        receipt['commands'].append({
            'label': label, 'argv': command, 'exit_code': code,
            'elapsed_seconds': round(time.monotonic() - start, 6),
            'log': str(path.relative_to(output)),
            'log_sha256': digest(path.read_bytes()),
        })
        save()
        print(label + ' exit=' + str(code), flush=True)
        if code:
            raise RuntimeError('Explicit trust=0 replay failed: ' + label)
        return path.read_text()

    try:
        run('official-help', [str(lean), '--help'])
        for module in order:
            relative = module.replace('.', '/')
            run(module, [str(lean), '--trust=0', '-j1', '-DElab.async=false',
                         '-o', relative + '.olean', relative + '.lean'])
        audit = run('ProjectAudit', [str(lean), '--trust=0', '-j1',
                                   '-DElab.async=false', 'ProjectAudit.lean'])
        summaries = re.findall(r'^FULL_MODULE_AUDIT theorems=(\d+) union=([^\n]*)$', audit, re.M)
        if len(summaries) != 1:
            raise ValueError('Missing unique original module-origin audit summary.')
        theorem_count = int(summaries[0][0])
        if theorem_count != project['theorem_count']:
            raise ValueError('The audit theorem count differs from the original run.')
        for module, info in snapshots.items():
            relative = Path(*module.split('.')).with_suffix('.lean')
            if digest((source / relative).read_bytes()) != info['sha256']:
                raise ValueError('Strict replay source snapshot changed: ' + module)
            if digest((original_source / relative).read_bytes()) != info['sha256']:
                raise ValueError('Original verifier source snapshot changed: ' + module)
        for path, expected in prior['compiler']['files'].items():
            if digest(Path(path).read_bytes()) != expected:
                raise ValueError('Compiler file changed during strict replay: ' + path)
        receipt['theorem_count'] = theorem_count
        receipt['axiom_union'] = summaries[0][1]
        receipt['status'] = 'PASS_EXPLICIT_TRUST_ZERO'
        return 0
    except Exception as error:
        receipt['status'] = 'FAIL'
        receipt['error'] = str(error)
        (output / 'failure.txt').write_text(traceback.format_exc())
        print('FAIL: ' + str(error), flush=True)
        return 1
    finally:
        receipt['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save()
        files = {
            str(path.relative_to(output)): {'bytes': path.stat().st_size,
                                           'sha256': digest(path.read_bytes())}
            for path in sorted(output.rglob('*'))
            if path.is_file() and path.suffix != '.olean' and path.name != 'FILES.json'
        }
        (output / 'FILES.json').write_text(json.dumps(files, indent=2) + '\n')


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError) as error:
        print('Strict replay preflight failed: ' + str(error), file=sys.stderr)
        raise SystemExit(2)
