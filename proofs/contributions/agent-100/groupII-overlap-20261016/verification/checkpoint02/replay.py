#!/usr/bin/env python3
"""Independently rebuild all ten pinned modules and audit all 53 exported endpoints."""
import argparse
import hashlib
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REGISTRY_SHA256 = 'ac31d0cfd710df17bc7ab4bc8eba102bc63d9a93875abd19fe0fa904cab5c36c'
SHARED_REPLAY_SHA256 = '575b013fd96475cc869f082af94dbde91493da90e5e447a4da1f23c8884d9bd3'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lean', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    registry = HERE / 'registry.json'
    shared = HERE.parent / 'dependencies/replay.py'
    for path, expected in [(registry, REGISTRY_SHA256), (shared, SHARED_REPLAY_SHA256)]:
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Pinned replay component changed: ' + str(path))
    return subprocess.run([sys.executable, str(shared), '--registry', str(registry), '--project', 'groupii-full',
                           '--lean', str(args.lean.resolve()), '--output', str(args.output.resolve())]).returncode

if __name__ == '__main__':
    raise SystemExit(main())
