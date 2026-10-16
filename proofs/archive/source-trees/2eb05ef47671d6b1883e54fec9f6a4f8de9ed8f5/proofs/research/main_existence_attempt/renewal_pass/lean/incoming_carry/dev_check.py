"""Retain each incoming-carry source snapshot and compilation attempt."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import time

here = Path(__file__).resolve().parent
compiler = Path('/workspace/scratch/fe6abe1df721/lean-runtime/lean')
dependency = here.parent / 'prefix/fresh_build'
logs = here / 'development_checks'
logs.mkdir(exist_ok=True)
number = len(list(logs.glob('attempt_*.log'))) + 1
source = here / 'IncomingCarrySensitivity.lean'
source_text = source.read_text()
(logs / f'attempt_{number:03d}.lean').write_text(source_text)
started = time.monotonic()
result = subprocess.run([str(compiler), str(source)], capture_output=True, text=True,
                        env=dict(os.environ, LEAN_PATH=str(dependency)))
record = {'source': source.name, 'exit_code': result.returncode,
          'seconds': time.monotonic() - started,
          'source_sha256': hashlib.sha256(source_text.encode()).hexdigest()}
text = json.dumps(record) + '\n' + result.stdout + result.stderr
(logs / f'attempt_{number:03d}.log').write_text(text)
print(text, end='')
raise SystemExit(result.returncode)
