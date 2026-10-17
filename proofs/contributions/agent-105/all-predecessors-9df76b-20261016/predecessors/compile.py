from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time

evidence = Path(__file__).resolve().parent
root = Path(__file__).resolve().parents[5]
label = sys.argv[1]
if not label.isalnum():
    raise RuntimeError('The attempt label must be alphanumeric.')
attempt = evidence / label
attempt.mkdir(exist_ok=False)
source = root / 'proofs/Agent105Predecessors9df76b.lean'
snapshot = attempt / 'source.lean'
snapshot.write_bytes(source.read_bytes())
build = evidence / 'build'
build.mkdir(exist_ok=True)
new_contribution = root / 'proofs/contributions/agent-105/all-predecessors-9df76b-20261016'
decoder = Path('/workspace/scratch/9df76b503b84/agent105-decoder-work/proofs/contributions/agent-105/numeric-decoder-9df76b-20261016')
search = [new_contribution / 'decoded-fiber/build', new_contribution / 'word-fiber/build',
          decoder / 'scan/build', decoder / 'local/build',
          Path('/workspace/scratch/9df76b503b84/agent105-runtime/base-build')]
env = os.environ.copy()
env['LEAN_PATH'] = ':'.join(str(p) for p in search)
compiler = '/workspace/scratch/fb513c1676b0/agent102-runtime/lean-4.19.0-linux/bin/lean'
command = [compiler, '--trust=0', '-o', str(build / 'Agent105Predecessors9df76b.olean'), str(source)]
start = time.monotonic()
process = subprocess.run(command, cwd=root / 'proofs', env=env,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
(attempt / 'compile.log').write_text(process.stdout)
receipt = {'command': command, 'cwd': str(root / 'proofs'),
           'source_sha256': hashlib.sha256(snapshot.read_bytes()).hexdigest(),
           'source_unchanged_during_compile': source.read_bytes() == snapshot.read_bytes(),
           'lean_path': env['LEAN_PATH'], 'exit_code': process.returncode,
           'wall_seconds': time.monotonic() - start,
           'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'scope': 'Incremental author compile against recorded development caches, not the independent fresh closure.'}
(attempt / 'result.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
print(process.stdout)
sys.exit(process.returncode)
