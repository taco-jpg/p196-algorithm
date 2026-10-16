#!/usr/bin/env python3
"""Independently rebuild the frozen full registry and boundary review fixtures."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

PACKAGE = Path(__file__).resolve().parents[2]
REPO = PACKAGE.parents[3]
REGISTRY = PACKAGE / 'PROJECT_REGISTRY.json'
REGISTRY_SHA256 = 'ca9d1fa657f6fc786fa14ed0df2456333280ee8a5eb1a58cadeebb902ff16926'
BUILDER = PACKAGE / 'actual-dev/review-canonical/build_review.py'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    out = args.output.resolve()
    if out.exists():
        raise ValueError('Retain existing results and choose a new output path')
    if sha(REGISTRY) != REGISTRY_SHA256:
        raise ValueError('Final registry pin changed')
    spec = json.loads(REGISTRY.read_text())['projects']['agent7-odd-nooverflow-fibers']
    if spec['roots'] != ['OddComplete'] or len(spec['modules']) != 15:
        raise ValueError('Unexpected final project closure')
    command = [sys.executable, str(BUILDER)]
    for root in spec['roots']:
        command += ['--root', root]
    for module, record in spec['modules'].items():
        command += ['--expect', module + '=' + record['sha256']]
    for fixture in ['actual-dev/review-canonical/ReviewCanonical.lean',
                    'actual-dev/review-sharp/ReviewSharp.lean',
                    'actual-dev/review-sharp/ReviewComplete.lean']:
        command += ['--fixture', str(PACKAGE / fixture)]
    command += ['--output', str(out)]
    provenance = {
        'executor': 'Agent #7 /root/runtime',
        'registry_sha256': sha(REGISTRY),
        'builder_sha256': sha(BUILDER),
        'runner_sha256': sha(Path(__file__)),
        'command': command,
        'cwd': str(REPO),
    }
    result = subprocess.run(command, cwd=REPO)
    provenance['exit_code'] = result.returncode
    provenance['runner_and_registry_unchanged'] = (
        sha(REGISTRY) == provenance['registry_sha256'] and
        sha(BUILDER) == provenance['builder_sha256'] and
        sha(Path(__file__)) == provenance['runner_sha256'])
    if out.is_dir():
        (out / 'LAUNCH.json').write_text(json.dumps(provenance, indent=2) + '\n')
    raise SystemExit(result.returncode if provenance['runner_and_registry_unchanged'] else 1)

if __name__ == '__main__':
    main()
