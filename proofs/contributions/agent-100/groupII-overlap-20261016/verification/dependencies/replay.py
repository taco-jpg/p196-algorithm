#!/usr/bin/env python3
"""Replay a source-pinned Group II closure in a fresh directory; never edit source."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
PINS_SHA256 = '5d163b816c28cff05aec26b25387f778aca1f9b913225fdd9345e755baf02475'
DEFAULT_REGISTRY_SHA256 = 'b77a67cb9a43d12d5ac8f0f4b77ee44e75524f46f813d6b6624701bf083bb37d'
VERIFIER_SHA256 = 'c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a'
EXPECTED_IMPORTS = {
    'LychrelDigitSums': ['Std'],
    'SafeDelay': ['LychrelDigitSums'],
    'DecimalSafeRuns': ['LychrelDigitSums'],
    'DecimalDelayBridge': ['SafeDelay', 'DecimalSafeRuns'],
    'PairDelayBridge': ['DecimalDelayBridge'],
    'DelayedOverlapGate': ['PairDelayBridge'],
}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lean', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--registry', type=Path, default=HERE / 'registry.json')
    parser.add_argument('--project', default='dev')
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        raise ValueError('Every checkpoint requires a new output directory: ' + str(output))
    root = Path(subprocess.check_output(['git', '-C', str(HERE), 'rev-parse', '--show-toplevel'], text=True).strip())
    verifier = root / 'proofs/verify_project__214bf7673efe116b.py'
    if sha(verifier.read_bytes()) != VERIFIER_SHA256:
        raise ValueError('Pinned verifier changed')
    pin_bytes = (HERE / 'source-pins.json').read_bytes()
    if sha(pin_bytes) != PINS_SHA256:
        raise ValueError('Dependency pins changed')
    registry_bytes = args.registry.read_bytes()
    if args.registry.resolve() == (HERE / 'registry.json').resolve() and sha(registry_bytes) != DEFAULT_REGISTRY_SHA256:
        raise ValueError('Default dependency registry changed')
    registry = json.loads(registry_bytes)
    modules = registry['projects'][args.project]['modules']
    if registry['catalogue_complete'] is not False or not registry['catalogue_blockers']:
        raise ValueError('A scoped checkpoint must preserve incomplete global catalogue status')
    checked = {}
    for pin in json.loads(pin_bytes):
        name = pin['module']
        rec = modules[name]
        expected = {'path': pin['current'], 'sha256': pin['sha256'], 'git_blob': pin['blob'], 'imports': EXPECTED_IMPORTS[name]}
        if any(rec.get(k) != v for k, v in expected.items()) or rec.get('adapter'):
            raise ValueError('Dependency path/hash/import contract changed: ' + name)
        source = root / rec['path']
        if source.is_symlink() or not source.resolve().is_relative_to(root):
            raise ValueError('Unsafe dependency path: ' + name)
        raw = source.read_bytes()
        if sha(raw) != rec['sha256'] or hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest() != rec['git_blob']:
            raise ValueError('Dependency bytes changed: ' + name)
        checked[name] = expected
    command = [sys.executable, str(verifier), '--registry', str(args.registry.resolve()), '--project', args.project,
               '--lean', str(args.lean.resolve()), '--output', str(output)]
    if args.check_only:
        command.append('--check-only')
    receipt = {'executor': 'Agent #100 runtime_setup independent child', 'purpose': 'Scoped local clean replay',
               'source_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(),
               'registry_sha256': sha(registry_bytes), 'replay_sha256': sha(Path(__file__).read_bytes()),
               'pinned_verifier_sha256': VERIFIER_SHA256, 'dependency_pins_sha256': PINS_SHA256,
               'dependencies': checked, 'command': command, 'started_at_epoch': time.time(),
               'check_only': args.check_only,
               'identity_note': 'The unchanged upstream verifier labels its own report Agent #1; this invocation receipt identifies the actual executor.'}
    rc = subprocess.run(command, cwd=root).returncode
    receipt['exit_code'] = rc
    receipt['finished_at_epoch'] = time.time()
    report = output / 'verification.json'
    if report.is_file():
        receipt['verification_sha256'] = sha(report.read_bytes())
        receipt['verification_status'] = json.loads(report.read_text())['status']
    if output.is_dir():
        (output / 'agent100-replay-invocation.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'exit_code': rc, 'output': str(output), 'verification_status': receipt.get('verification_status')}))
    return rc

if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        print('Replay setup failed: ' + str(error), file=sys.stderr)
        raise SystemExit(2)
