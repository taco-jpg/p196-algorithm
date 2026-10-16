"""Independent source compilation against a reused research-base olean.

This is deliberately not described as a clean rebuild of Lychrel196Research.
The repository's separate clean replay is responsible for that gate.
"""
from pathlib import Path
import hashlib
import json
import os
import subprocess

ROOT = Path('/workspace/scratch/28992391bdc2/p196-agent108')
SOURCE = ROOT / 'proofs/contributions/agent-108/modular-autonomy'
OUT = SOURCE / 'review'
BUILD = Path('/workspace/scratch/28992391bdc2/semantic-review-build')
BASE = Path('/workspace/scratch/28992391bdc2/modular-build')
LEAN = '/workspace/scratch/28992391bdc2/lean-runtime/lean-4.19.0-linux/bin/lean'
SHIM = '/workspace/scratch/28992391bdc2/runtime-diagnostics/libproc_self_readlink.so'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

env = os.environ.copy()
env['LD_PRELOAD'] = SHIM
env['LEAN_PATH'] = f'{BUILD}:{BASE}'
modules = ['AutonomyDefs', 'AutonomyBasic', 'DigitPerturbation', 'LeadingWitness', 'Necessity', 'ModularAutonomy']
record = {'verification_scope': 'all listed new module sources recompiled; existing base olean reused',
          'base_source_sha256': sha(ROOT / 'proofs/research/Lychrel196Research.lean'),
          'base_build_source_sha256': sha(BASE / 'Lychrel196Research.lean'),
          'base_olean_sha256': sha(BASE / 'Lychrel196Research.olean'),
          'modules': []}
for module in modules:
    src = SOURCE / (module + '.lean')
    snapshot = src.read_bytes()
    copy = BUILD / src.name
    copy.write_bytes(snapshot)
    result = subprocess.run([LEAN, '-o', str(BUILD / (module + '.olean')), str(copy)],
                            cwd=BUILD, env=env, text=True, capture_output=True)
    (OUT / (module + '.compile.log')).write_text(result.stdout + result.stderr)
    record['modules'].append({'module': module, 'sha256': hashlib.sha256(snapshot).hexdigest(),
                              'source_unchanged_after_compile': src.read_bytes() == snapshot,
                              'exit_code': result.returncode})
    print(module, result.returncode, flush=True)
    if result.returncode:
        break
(OUT / 'compile-check.json').write_text(json.dumps(record, indent=2) + '\n')
