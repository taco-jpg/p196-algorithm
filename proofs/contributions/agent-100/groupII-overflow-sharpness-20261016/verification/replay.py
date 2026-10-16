#!/usr/bin/env python3
"""Independently replay the pinned overflow closure in a new empty directory."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
REGISTRY_SHA256 = 'ac68e397f5a12326ed7a788a0e021edda22be46216bcc98c5bc45f71933c6533'
VERIFIER_SHA256 = 'c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a'


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lean', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        raise ValueError('Use a new empty output path; prior attempts must remain intact.')
    root = Path(subprocess.check_output(
        ['git', '-C', str(HERE), 'rev-parse', '--show-toplevel'], text=True).strip())
    registry = HERE / 'registry.json'
    registry_bytes = registry.read_bytes()
    if sha(registry_bytes) != REGISTRY_SHA256:
        raise ValueError('Frozen registry identity mismatch or source freeze incomplete.')
    verifier = root / 'proofs/verify_project__214bf7673efe116b.py'
    if sha(verifier.read_bytes()) != VERIFIER_SHA256:
        raise ValueError('The canonical verifier must remain unchanged.')
    spec = json.loads(registry_bytes)
    if spec['catalogue_complete'] is not False or not spec['catalogue_blockers']:
        raise ValueError('A scoped replay must not imply a complete global catalogue.')
    command = [sys.executable, str(verifier), '--registry', str(registry),
               '--project', 'groupii-overflow', '--lean', str(args.lean.resolve()),
               '--output', str(output)]
    receipt = {
        'executor': 'Agent #100 scope_audit independent child',
        'source_authorship': 'No new Lean theorem authored by this executor in this task.',
        'purpose': 'Fresh complete import closure build and complete module-origin axiom audit',
        'source_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(),
        'registry_sha256': sha(registry_bytes),
        'replay_sha256': sha(Path(__file__).read_bytes()),
        'canonical_verifier_sha256': VERIFIER_SHA256,
        'command': command,
        'started_at_epoch': time.time(),
        'check_only': False,
        'prior_author_oleans_used': False,
        'identity_note': 'The unchanged canonical verifier labels itself Agent #1; this receipt records the actual independent executor.',
    }
    rc = subprocess.run(command, cwd=root).returncode
    receipt['exit_code'] = rc
    receipt['finished_at_epoch'] = time.time()
    report = output / 'verification.json'
    if report.is_file():
        receipt['verification_sha256'] = sha(report.read_bytes())
        receipt['verification_status'] = json.loads(report.read_text())['status']
    if output.is_dir():
        (output / 'independent-invocation.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'exit_code': rc, 'output': str(output),
                      'verification_status': receipt.get('verification_status')}))
    return rc


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        print('Independent replay setup failed:', error, file=sys.stderr)
        raise SystemExit(2)
