#!/usr/bin/env python3
"""Replay the independent six-module audit with the unmodified repository checker.

The checker creates a new source/build directory and refuses an existing output.
No author olean files or author build directory are used.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lean', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[5]
    checker = root / 'proofs/verify_project__214bf7673efe116b.py'
    expected = 'c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a'
    if hashlib.sha256(checker.read_bytes()).hexdigest() != expected:
        raise RuntimeError('The pinned unmodified project checker has changed')
    command = [sys.executable, str(checker), '--lean', str(args.lean.resolve()),
               '--output', str(args.output.resolve()), '--project', 'agent104-exact-mass',
               '--registry', str(root / 'proofs/Agent104ExactMass.registry.json')]
    return subprocess.run(command, cwd=root).returncode


if __name__ == '__main__':
    sys.exit(main())
