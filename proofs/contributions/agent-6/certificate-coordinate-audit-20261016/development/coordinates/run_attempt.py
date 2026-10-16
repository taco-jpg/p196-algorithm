#!/usr/bin/env python3
"""Compile one preserved author snapshot against the fresh, pinned dependencies."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time

base = Path('/workspace/scratch/f8aedc6d7adf')
attempt = Path(sys.argv[1]).resolve()
evidence = base / 'landscape-agent6/checker-dev'
assert attempt.parent == evidence
pin = json.loads((attempt / 'source-pin.json').read_text())
source = attempt / 'CertificateCoordinates.lean'
assert hashlib.sha256(source.read_bytes()).hexdigest() == pin['source_sha256']
lean = Path(pin['lean'])
assert hashlib.sha256(lean.read_bytes()).hexdigest() == \
    '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
deps = Path(pin['dependency_objects'])
for module in ['CertificateExterior', 'CertificateAccounting', 'CoordinateCycle']:
    assert (deps / (module + '.olean')).is_file(), module
manifest = Path(pin['dependency_source_manifest'])
(attempt / 'dependency-source-manifest.json').write_bytes(manifest.read_bytes())
env = os.environ.copy()
env['LEAN_PATH'] = str(attempt) + os.pathsep + str(deps)
cmd = [str(lean), '--trust=0', '-j1', '-DElab.async=false', '-o',
       str(attempt / 'CertificateCoordinates.olean'), str(source)]
record = {
    'command': cmd, 'cwd': str(attempt), 'LEAN_PATH': env['LEAN_PATH'],
    'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'source_sha256': pin['source_sha256'],
    'dependency_manifest_sha256': hashlib.sha256(manifest.read_bytes()).hexdigest(),
    'dependency_mode': 'Reused unchanged 17-module fresh runtime build',
}
start = time.monotonic()
with (attempt / 'compile.log').open('w') as log:
    proc = subprocess.run(cmd, cwd=attempt, env=env, stdout=log,
                          stderr=subprocess.STDOUT, check=False)
record['exit_code'] = proc.returncode
record['elapsed_seconds'] = time.monotonic() - start
record['finished_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
obj = attempt / 'CertificateCoordinates.olean'
if obj.exists():
    record['object_sha256'] = hashlib.sha256(obj.read_bytes()).hexdigest()
(attempt / 'compile-result.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
print((attempt / 'compile.log').read_text())
sys.exit(proc.returncode)
