"""Build the exact all-base prerequisites into an external scratch directory.
Run with LEAN_BIN set, with any required LD_PRELOAD exported.
"""
from pathlib import Path
import argparse
import os
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('build_dir', type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parents[6]
build = args.build_dir.resolve()
build.mkdir(parents=True, exist_ok=True)
sources = [
    'proofs/contributions/2026-10-14-base-uniqueness-formal/SignedDigitUniqueness.lean',
    *[f'proofs/contributions/2026-10-15-base-reflection-formal/{name}.lean'
      for name in ['BaseReflection', 'ResetNormalization', 'PhysicalWidth', 'SeamSafety']],
    'proofs/contributions/2026-10-15-base-reverse-add-formal/ReverseAdd.lean',
]
env = dict(os.environ, LEAN_PATH=str(build))
lean = os.environ.get('LEAN_BIN', 'lean')
for source in sources:
    path = root / source
    with (build / f'{path.stem}.log').open('w') as log:
        result = subprocess.run(
            [lean, '-o', str(build / f'{path.stem}.olean'), str(path)],
            cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT)
    print(path.stem, result.returncode, flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)
