"""Retain every development source and complete Lean compiler result."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
COMPILER = Path('/workspace/scratch/fe6abe1df721/lean-runtime/lean')
DEPENDENCY = PROJECT / 'main_existence_attempt/renewal_pass/lean/raw_symmetry/fresh_build'
source = HERE / (sys.argv[1] if len(sys.argv) > 1 else 'IntrinsicSeam.lean')
logs = HERE / 'development_checks' / source.stem
logs.mkdir(parents=True, exist_ok=True)
number = len(list(logs.glob('attempt_*.log'))) + 1
source_text = source.read_text()
(logs / f'attempt_{number:03d}.lean').write_text(source_text)
started = time.monotonic()
result = subprocess.run([str(COMPILER), '-o', str(HERE / (source.stem + '.olean')), str(source)],
                        capture_output=True, text=True,
                        env=dict(os.environ, LEAN_PATH=f'{HERE}:{DEPENDENCY}'))
record = {'source': source.name, 'exit_code': result.returncode,
          'seconds': time.monotonic() - started,
          'source_sha256': hashlib.sha256(source_text.encode()).hexdigest()}
output = json.dumps(record) + '\n' + result.stdout + result.stderr
(logs / f'attempt_{number:03d}.log').write_text(output)
print(output, end='')
raise SystemExit(result.returncode)
