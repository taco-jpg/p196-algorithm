#!/usr/bin/env python3
"""Strict incremental author check; preserve each source and actual failure."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

base = Path(__file__).resolve().parent
root = base.parents[4]
attempt = base / ('attempt-' + sys.argv[1].zfill(3))
attempt.mkdir(exist_ok=False)
source = root / 'proofs/Agent1PeriodicNinesClockStrip.lean'
(attempt / source.name).write_bytes(source.read_bytes())
(attempt / Path(__file__).name).write_bytes(Path(__file__).read_bytes())
deps = Path('/workspace/p196-agent1-session-20261016/nine-center-review-build-001')
modules = json.loads((root / 'proofs/Agent1PeriodicNinesCenter.registry.json').read_text())['projects']['agent1-periodic-nine-center']['modules']
checks = []
for module, pin in modules.items():
    p = deps / (module + '.lean')
    assert hashlib.sha256(p.read_bytes()).hexdigest() == pin['sha256']
    obj = deps / (module + '.olean')
    assert obj.is_file()
    checks.append({'module': module, 'source_sha256': pin['sha256'],
        'source_matches_reviewed_registry': True, 'object_reused': True,
        'object_sha256': hashlib.sha256(obj.read_bytes()).hexdigest()})
(attempt / 'dependencies.json').write_text(json.dumps(checks, indent=2) + '\n')
lean = '/workspace/p196-tools/lean-4.19.0-linux/bin/lean'
argv = [lean, '--trust=0', '-j1', '-DElab.async=false', '-o',
        'Agent1PeriodicNinesClockStrip.olean', source.name]
def limit():
    resource.setrlimit(resource.RLIMIT_AS, (8192*1024*1024, 8192*1024*1024))
start = time.monotonic()
beg = datetime.datetime.now(datetime.timezone.utc).isoformat()
p = subprocess.run(argv, cwd=attempt, env=dict(os.environ, LEAN_PATH=str(deps)),
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                   timeout=120, preexec_fn=limit)
(attempt / 'compile.log').write_text(p.stdout)
(attempt / 'command.json').write_text(json.dumps({
    'argv': argv, 'cwd': str(attempt), 'LEAN_PATH': str(deps), 'exit_code': p.returncode,
    'started_at_utc': beg, 'finished_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'seconds': time.monotonic()-start, 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'compiler_sha256': hashlib.sha256(Path(lean).read_bytes()).hexdigest(),
    'strict_incremental_compile': True, 'fresh_dependencies': False,
    'reused_dependency_count': len(checks), 'timeout_seconds': 120, 'memory_mib': 8192,
    'object_exists': (attempt / 'Agent1PeriodicNinesClockStrip.olean').is_file(),
}, indent=2) + '\n')
print(p.stdout, end='')
print('exit_code=' + str(p.returncode))
sys.exit(p.returncode)
