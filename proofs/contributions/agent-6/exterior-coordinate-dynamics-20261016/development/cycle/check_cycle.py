from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import time

root = Path('/workspace/scratch/f8aedc6d7adf')
module = sys.argv[1] if len(sys.argv) > 1 else 'CoordinateCycle'
scratch = root / 'claims-agent6/cycle-dev'
source = (root / 'agent6-work/proofs/contributions/agent-6/exterior-coordinate-dynamics-20261016/CoordinateCycle.lean'
          if module == 'CoordinateCycle' else scratch / (module + '.lean'))
attempts = scratch / 'attempts'
attempts.mkdir(parents=True, exist_ok=True)
number = 1 + len(list(attempts.glob(module + '-*')))
out = attempts / f'{module}-{number:03d}'
out.mkdir()
data = source.read_bytes()
(out / source.name).write_bytes(data)
build = scratch / 'build'
build.mkdir(exist_ok=True)
lean = root / 'runtime-agent6/lean-4.19.0-linux/bin/lean'
paths = [build, root / 'agent6-dev/build', root / 'landscape-agent6/sign-build',
         root / 'runtime-agent6/review-update/build/objects']
env = dict(os.environ)
env['LEAN_PATH'] = ':'.join(map(str, paths))
command = [str(lean), '--trust=0', '-j1', '-DElab.async=false', '-o', str(build / (module + '.olean')), str(out / source.name)]
dependencies = []
for folder in paths:
    for path in sorted(folder.glob('*.olean')):
        b = path.read_bytes()
        dependencies.append({'path': str(path), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()})
start = time.time()
with (out / 'compile.log').open('wb') as stream:
    result = subprocess.run(command, cwd=out, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=240)
status = result.returncode
report = {
    'module': module,
    'source_sha256': hashlib.sha256(data).hexdigest(),
    'lean_binary_sha256': hashlib.sha256(lean.read_bytes()).hexdigest(),
    'argv': command,
    'lean_path': list(map(str, paths)),
    'dependency_oleans': dependencies,
    'exit_code': status,
    'elapsed_seconds': time.time() - start,
}
(out / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k: v for k, v in report.items() if k != 'dependency_oleans'}, indent=2))
print((out / 'compile.log').read_text())
sys.exit(status)
