#!/usr/bin/env python3
"""Recover the independently built source snapshot from exact committed bytes."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    report = json.loads((here / 'verification.json').read_text())
    args.output.mkdir(parents=True, exist_ok=False)
    for module, rec in sorted(report['sources'].items()):
        blob = subprocess.check_output(['git', 'show', report['source_commit'] + ':' + rec['original_path']], cwd=args.repo)
        assert hashlib.sha256(blob).hexdigest() == rec['sha256'], module
        assert len(blob) == rec['bytes'], module
        target = args.output / (module.replace('.', '/') + '.lean')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(blob)
    audit = (here / 'AllExportedAxioms.lean').read_bytes()
    assert hashlib.sha256(audit).hexdigest() == report['audit_source_sha256']
    (args.output / 'AllExportedAxioms.lean').write_bytes(audit)
    print(f'Recovered and SHA256-verified {len(report["sources"])} committed sources and the exact audit source.')


if __name__ == '__main__':
    main()
