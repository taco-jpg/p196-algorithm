"""Retain and verify each genuine NormalizedCarry author attempt."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import os
import subprocess
import time

BASE = Path('/workspace/scratch/f8aedc6d7adf')
EVIDENCE = BASE / 'landscape-agent6/carry-dev'
SOURCE = BASE / 'agent6-carry/proofs/contributions/agent-6/normalized-carry-accounting-20261016/NormalizedCarry.lean'
INHERITED = BASE / 'runtime-agent6/review-carry/inherited'
LEAN = BASE / 'runtime-agent6/lean-4.19.0-linux/bin/lean'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()

def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')

def utc():
    return datetime.now(timezone.utc).isoformat()

attempts = sorted(EVIDENCE.glob('attempt-*'))
attempt = EVIDENCE / f'attempt-{len(attempts) + 1:03d}'
attempt.mkdir()
raw = SOURCE.read_bytes()
captured = attempt / SOURCE.name
captured.write_bytes(raw)
source_pin = {'source': str(SOURCE), 'captured': str(captured),
              'bytes': len(raw), 'sha256': sha(raw), 'git_blob': blob(raw)}
save(attempt / 'source-pin.json', source_pin)
manifest_raw = (INHERITED / 'source-manifest.json').read_bytes()
ready_raw = (INHERITED / 'OBJECTS_READY.json').read_bytes()
(attempt / 'dependency-source-manifest.json').write_bytes(manifest_raw)
(attempt / 'dependency-OBJECTS_READY.json').write_bytes(ready_raw)
manifest, ready = json.loads(manifest_raw), json.loads(ready_raw)
assert sha(manifest_raw) == ready['source_manifest_sha256']
modules = {m['module']: m for m in manifest['modules']}
needed = set()
def visit(name):
    if name in needed or name in manifest['external_modules']:
        return
    needed.add(name)
    for dep in modules[name]['imports']:
        visit(dep)
for name in ['OuterBridge', 'CoordinateThreshold']:
    visit(name)
verified = []
for name in manifest['build_order']:
    if name not in needed:
        continue
    m, obj = modules[name], ready['objects'][name]
    src = Path(m['path']).read_bytes()
    staged = (INHERITED / m['snapshot']).read_bytes()
    assert sha(src) == m['sha256'] and blob(src) == m['git_blob']
    assert src == staged
    assert sha(Path(obj['path']).read_bytes()) == obj['sha256']
    verified.append({'module': name, 'source': m, 'object': obj})
assert len(verified) == len(needed) == 8
compiler_hashes = manifest['prior_compiler']['files']
for path, expected in compiler_hashes.items():
    assert sha(Path(path).read_bytes()) == expected
dependency_pin = {'verification': 'inherited exact objects; no baseline compilation repeated',
                  'source_manifest_sha256': sha(manifest_raw),
                  'objects_ready_sha256': sha(ready_raw),
                  'direct_imports': ['OuterBridge', 'CoordinateThreshold'],
                  'module_count': len(verified), 'modules': verified,
                  'compiler': manifest['prior_compiler']}
save(attempt / 'dependency-pins.json', dependency_pin)
environment = dict(os.environ)
environment['LEAN_PATH'] = str(attempt) + os.pathsep + str(INHERITED / 'objects')
command = [str(LEAN), '--trust=0', '-j1', '-DElab.async=false',
           '-o', str(attempt / 'NormalizedCarry.olean'), str(captured)]
record = {'role': 'author', 'module': 'NormalizedCarry', 'source_pin': source_pin,
          'compiler_sha256': compiler_hashes[str(LEAN)], 'command': command,
          'cwd': str(attempt), 'lean_path': environment['LEAN_PATH'],
          'started_utc': utc(), 'dependency_pins': str(attempt / 'dependency-pins.json')}
save(attempt / 'compile-start.json', record)
started = time.monotonic()
with (attempt / 'compile.log').open('wb') as log:
    result = subprocess.run(command, cwd=attempt, env=environment,
                            stdout=log, stderr=subprocess.STDOUT)
record.update({'finished_utc': utc(), 'elapsed_seconds': time.monotonic() - started,
               'exit_code': result.returncode,
               'compile_log_sha256': sha((attempt / 'compile.log').read_bytes())})
obj = attempt / 'NormalizedCarry.olean'
if obj.exists():
    record['object'] = {'path': str(obj), 'sha256': sha(obj.read_bytes()),
                        'bytes': obj.stat().st_size}
save(attempt / 'compile-result.json', record)
print(json.dumps(record, indent=2))
print((attempt / 'compile.log').read_text())
raise SystemExit(result.returncode)
