#!/usr/bin/env python3
"""Future reproduction: unchanged canonical build, then explicit trust-zero audit.

The historical canonical commands omitted --trust=0; Lean's default trust is max.
This additive launcher does not relabel or alter that historical execution.
Its own receipt identifies the current operator. The untouched verifier and
ledger extractor retain their historical embedded attribution labels.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
PROJECT = 'groupii-overflow'
REGISTRY_SHA256 = 'ac68e397f5a12326ed7a788a0e021edda22be46216bcc98c5bc45f71933c6533'
VERIFIER_SHA256 = 'c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a'
EXTRACTOR_SHA256 = 'ae7844d318fd59929b4966b90f9588ecd5fb6d04254b00b080eb0d98ca8b540f'
LEAN_SHA256 = '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def command_plan(root: Path, lean: Path, output: Path) -> dict:
    """Construct argv lists without launching a process or creating files."""
    run = output / 'canonical'
    source = run / PROJECT / 'source'
    return {
        'canonical': {
            'argv': [sys.executable, str(root / 'proofs/verify_project__214bf7673efe116b.py'),
                     '--registry', str(HERE / 'registry.json'), '--project', PROJECT,
                     '--lean', str(lean), '--output', str(run)],
            'cwd': str(root), 'log': str(output / 'canonical-launch.log')},
        'strict': {
            'argv': [str(lean), '--trust=0', '-j1', '-DElab.async=false', 'ProjectAudit.lean'],
            'cwd': str(source), 'log': str(output / 'ProjectAudit-trust0.log')},
        'extractor': {
            'argv': [sys.executable, str(HERE / 'extract_axiom_ledger.py'),
                     '--registry', str(HERE / 'registry.json'), '--run', str(run),
                     '--output', str(output / 'canonical-multiline-ledger.raw.json')],
            'cwd': str(root), 'log': str(output / 'ledger-extractor.log')},
    }


def execute(step: dict, env: dict | None = None, timeout: int | None = None) -> int:
    step['started_at_epoch'] = time.time()
    with Path(step['log']).open('xb') as stream:
        try:
            rc = subprocess.run(step['argv'], cwd=step['cwd'], env=env, stdout=stream,
                                stderr=subprocess.STDOUT, timeout=timeout).returncode
        except subprocess.TimeoutExpired:
            rc = 124
    step.update(exit_code=rc, finished_at_epoch=time.time(),
                log_sha256=sha(Path(step['log'])))
    return rc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lean', type=Path, required=True, help='Official Lean 4.19.0 Linux binary')
    parser.add_argument('--output', type=Path, required=True, help='New, nonexistent output directory')
    parser.add_argument('--executor', default='local reproduction operator',
                        help='Actual current operator, self-reported; no independence is inferred')
    args = parser.parse_args(argv)
    lean, output = args.lean.resolve(), args.output.resolve()
    require(bool(args.executor.strip()), '--executor must not be blank')
    require(not output.exists(), 'Use a new output path; never overwrite an earlier run')
    root = Path(subprocess.check_output(
        ['git', '-C', str(HERE), 'rev-parse', '--show-toplevel'], text=True).strip()).resolve()
    registry = HERE / 'registry.json'
    verifier = root / 'proofs/verify_project__214bf7673efe116b.py'
    extractor = HERE / 'extract_axiom_ledger.py'
    pinned = {registry: REGISTRY_SHA256, verifier: VERIFIER_SHA256,
              extractor: EXTRACTOR_SHA256, lean: LEAN_SHA256}
    for path, expected in pinned.items():
        require(sha(path) == expected, 'Pinned file identity mismatch: ' + str(path))
    spec = json.loads(registry.read_text())
    require(spec['catalogue_complete'] is False and bool(spec['catalogue_blockers']),
            'Scoped reproduction must retain the incomplete global catalogue')
    require(len(spec['projects'][PROJECT]['modules']) == 18, 'Expected the frozen 18-module closure')
    source_commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
    plan = command_plan(root, lean, output)
    output.mkdir(parents=True, exist_ok=False)
    receipt_path = output / 'reproduction-operator-receipt.json'
    receipt = {
        'status': 'RUNNING', 'executor': args.executor.strip(),
        'operator_identity_is_self_reported': True, 'independent_review_claimed': False,
        'historical_run_relabelled': False, 'source_commit': source_commit,
        'repo_root': str(root), 'launcher_sha256': sha(Path(__file__)),
        'registry_sha256': REGISTRY_SHA256, 'canonical_verifier_sha256': VERIFIER_SHA256,
        'extractor_sha256': EXTRACTOR_SHA256, 'official_lean_sha256': LEAN_SHA256,
        'canonical_commands_have_explicit_trust0': False,
        'additional_import_audit_explicit_trust_level': 0,
        'prior_author_oleans_used': False, 'repository_wide_pass': False,
        'attribution_note': 'Only this receipt identifies the current operator. The untouched '
            'canonical report agent and raw extractor executor are embedded historical labels, '
            'not evidence that those persons performed this reproduction.',
        'steps': plan, 'started_at_epoch': time.time(),
    }

    def save() -> None:
        receipt_path.write_text(json.dumps(receipt, indent=2) + '\n')

    save()
    rc = 1
    try:
        rc = execute(plan['canonical'])
        require(rc == 0, 'Canonical verifier failed; see canonical-launch.log')
        run = output / 'canonical'
        report_path = run / 'verification.json'
        report = json.loads(report_path.read_text())
        require(report['status'] == 'PASS', 'Canonical verification report did not PASS')
        require(report['registry_sha256'] == REGISTRY_SHA256, 'Canonical registry mismatch')
        receipt['canonical_verification_sha256'] = sha(report_path)
        receipt['canonical_report_embedded_agent_label'] = report.get('agent')
        source = run / PROJECT / 'source'
        audit = source / 'ProjectAudit.lean'
        manifest_path = run / 'FILES.json'
        manifest = json.loads(manifest_path.read_text())
        snapshots = {report_path: sha(report_path), manifest_path: sha(manifest_path)}
        for module, record in spec['projects'][PROJECT]['modules'].items():
            path = source / (module.replace('.', '/') + '.lean')
            require(sha(path) == record['sha256'], 'Fresh source mismatch: ' + module)
            snapshots[path] = sha(path)
            snapshots[path.with_suffix('.olean')] = sha(path.with_suffix('.olean'))
        require(sha(audit) == manifest[str(audit.relative_to(run))]['sha256'],
                'Generated ProjectAudit differs from canonical manifest')
        snapshots[audit] = sha(audit)
        compiler_pins = {Path(p): h for p, h in report['compiler']['files'].items()}
        snapshots.update(compiler_pins)
        snapshots.update(pinned)
        for path, expected in snapshots.items():
            require(sha(path) == expected, 'Pre-audit identity mismatch: ' + str(path))
        receipt['snapshots_before_strict_audit'] = {str(p): h for p, h in snapshots.items()}
        receipt['strict_audit_source_sha256'] = sha(audit)
        save()
        env = os.environ.copy()
        env['LEAN_PATH'] = str(source)
        plan['strict']['LEAN_PATH'] = str(source)
        rc = execute(plan['strict'], env=env, timeout=1800)
        require(rc == 0, 'Explicit --trust=0 ProjectAudit failed')
        save()
        rc = execute(plan['extractor'])
        require(rc == 0, 'Complete multiline ledger extraction failed')
        raw_path = output / 'canonical-multiline-ledger.raw.json'
        raw = json.loads(raw_path.read_text())
        receipt['raw_ledger_sha256'] = sha(raw_path)
        receipt['raw_ledger_embedded_executor_label'] = raw.get('executor')
        receipt['raw_ledger_embedded_executor_is_current_operator_evidence'] = False
        loader = importlib.util.spec_from_file_location('pinned_multiline_extractor', extractor)
        module = importlib.util.module_from_spec(loader)
        loader.loader.exec_module(module)
        strict_text = Path(plan['strict']['log']).read_text()
        strict_ledger = {}
        for match in module.AUDITED.finditer(strict_text):
            origin, name = match.group(1), match.group(2)
            require(name not in strict_ledger, 'Duplicate strict audit theorem: ' + name)
            strict_ledger[name] = {'module': origin,
                                   'axioms': module.bracket_list(strict_text, match.end() - 1)}
        expected = raw['full_module_origin_ledger']
        require(strict_ledger.keys() == expected.keys(), 'Strict/canonical theorem names differ')
        for name, entry in strict_ledger.items():
            require(entry['module'] == expected[name]['module'] and
                    set(entry['axioms']) == set(expected[name]['axioms']),
                    'Strict/canonical module or complete axiom set differs: ' + name)
        counts = re.findall(r'^FULL_MODULE_AUDIT theorems=(\d+) union=', strict_text, re.M)
        require(counts == [str(len(expected))], 'Strict audit final count mismatch')
        unsafe = re.findall(r'^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$', strict_text, re.M)
        require(sorted(unsafe) == sorted(tuple(x) for x in
                report['projects'][PROJECT]['unsafe_implementation_axioms']),
                'Strict unsafe implementation inventory mismatch')
        for path, expected_hash in snapshots.items():
            require(sha(path) == expected_hash, 'File changed during reproduction: ' + str(path))
        receipt.update(status='PASS_CANONICAL_PLUS_EXPLICIT_TRUST0',
                       strict_module_origin_theorem_count=len(strict_ledger),
                       strict_axiom_union=sorted({a for x in strict_ledger.values() for a in x['axioms']}),
                       strict_full_module_origin_ledger=strict_ledger,
                       strict_unsafe_implementation_inventory=unsafe,
                       complete_multiline_ledgers_agree=True,
                       canonical_report_and_source_olean_posthashes_unchanged=True)
        rc = 0
    except Exception as error:
        receipt.update(status='FAIL', error=repr(error))
        rc = rc if rc and rc > 0 else 1
    finally:
        receipt.update(exit_code=rc, finished_at_epoch=time.time())
        save()
    print(json.dumps({'status': receipt['status'], 'exit_code': rc,
                      'executor': receipt['executor'], 'receipt': str(receipt_path)}))
    return rc


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        print('Reproduction setup failed:', error, file=sys.stderr)
        raise SystemExit(2)
