from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

root = Path('/workspace/scratch/f8aedc6d7adf')
module = sys.argv[1]
extra = sys.argv[2] if len(sys.argv) > 2 else ''
src = root / 'agent6-work/proofs/contributions/agent-6/exterior-coordinate-dynamics-20261016' / (module + '.lean')
attempts = root / 'agent6-dev/attempts'
attempts.mkdir(exist_ok=True)
number = 1 + len(list(attempts.glob(module + '-*')))
out = attempts / f'{module}-{number:03d}'
out.mkdir()
data = src.read_bytes()
(out / src.name).write_bytes(data)
build = root / 'agent6-dev/build'
build.mkdir(exist_ok=True)
lean = root / 'runtime-agent6/lean-4.19.0-linux/bin/lean'
env = dict(os.environ)
paths = [str(build), str(root / 'runtime-agent6/review-update/build/objects')]
if extra:
    paths.append(extra)
env['LEAN_PATH'] = ':'.join(paths)
command = [str(lean), '--trust=0', '-j1', '-DElab.async=false', '-o', str(build / (module + '.olean')), str(out / src.name)]
start = time.time()
with (out / 'compile.log').open('wb') as stream:
    status = subprocess.run(command, cwd=out, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=240).returncode
report = {'module': module, 'source_sha256': hashlib.sha256(data).hexdigest(), 'argv': command, 'lean_path': paths, 'exit_code': status, 'elapsed_seconds': time.time()-start}
(out / 'verification.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
print((out / 'compile.log').read_text())
sys.exit(status)
