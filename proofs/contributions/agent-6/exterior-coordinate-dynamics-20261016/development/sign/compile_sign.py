#!/usr/bin/env python3
"""Build the pinned sign closure and preserve every attempted source and log."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

ROOT = Path('/workspace/scratch/f8aedc6d7adf')
WORK = ROOT / 'landscape-agent6'
BUILD = WORK / 'sign-build'
ATTEMPTS = WORK / 'sign-attempts'
LEAN = ROOT / 'runtime-agent6/lean-4.19.0-linux/bin/lean'
SOURCE = ROOT / 'agent6-work/proofs/contributions/agent-6/exterior-coordinate-dynamics-20261016/CoordinateSign.lean'
UPSTREAM = ROOT / 'runtime-agent6/review-update/source'
DEPENDENCIES = [
    ('OuterFinite', UPSTREAM / 'OuterFinite.lean', '3376873da457c698850f604ddda82aeba3e67f4196e5c33d8142bed945c5f3f6'),
    ('TARGET', UPSTREAM / 'TARGET.lean', 'db5346737c58d3d6e6e62397d0d9270b81ebf62fd5d2eb0073e739ef0dffc717'),
    ('ExteriorFactorizationProof', UPSTREAM / 'ExteriorFactorizationProof.lean', 'eb682657cfd7916b4b56dde5069cc7316d65f8e69da6fff42981c23dc9a97301'),
    ('ExteriorObservationInjective', UPSTREAM / 'ExteriorObservationInjective.lean', '891207ca4daadfc65c435b5dd5477478cfe59347afb9404660ce458ed7103cbf'),
    ('ExteriorUpdateLaw', UPSTREAM / 'ExteriorUpdateLaw.lean', 'd384cb9a3598b210ec1a0c7cc310297ca2b34cf1e6b0588e03516f0da75331b9'),
    ('CoordinateThreshold', SOURCE.with_name('CoordinateThreshold.lean'), 'c50a07ee9dc4d3eff6e25b623235037850bc5a883ec057655503cc7a6cd068d8'),
    ('CoordinateDynamics', ROOT / 'agent6-dev/attempts/CoordinateDynamics-004/CoordinateDynamics.lean', 'f6e77f1105cd7a22cb146c187e160472b09af117e3aff9f0e9c1516af39944f8'),
]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def compile_one(module, src, evidence, env):
    source_copy = BUILD / (module + '.lean')
    shutil.copyfile(src, source_copy)
    shutil.copyfile(src, evidence / (module + '.lean'))
    command = [str(LEAN), '--trust=0', '-j1', '-DElab.async=false', '-o', module + '.olean', module + '.lean']
    started = time.time()
    run = subprocess.run(command, cwd=BUILD, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=240)
    log = evidence / (module + '.log')
    log.write_bytes(run.stdout)
    result = {'module': module, 'command': command, 'cwd': str(BUILD),
              'source_sha256': sha(source_copy), 'source_path': str(src),
              'exit_code': run.returncode, 'seconds': time.time() - started,
              'log': str(log), 'log_sha256': sha(log)}
    if run.returncode == 0:
        result['object_sha256'] = sha(BUILD / (module + '.olean'))
    print(module, run.returncode, flush=True)
    if run.stdout:
        print(run.stdout.decode('utf-8', errors='replace'), end='', flush=True)
    return result

def main():
    BUILD.mkdir(exist_ok=True)
    ATTEMPTS.mkdir(exist_ok=True)
    index = 1
    while (ATTEMPTS / ('attempt-%03d' % index)).exists():
        index += 1
    evidence = ATTEMPTS / ('attempt-%03d' % index)
    evidence.mkdir()
    if sha(LEAN) != '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023':
        raise RuntimeError('Compiler hash mismatch')
    env = dict(os.environ, LEAN_PATH=str(BUILD))
    results = []
    receipt = WORK / 'sign-dependencies.json'
    if not receipt.exists():
        for name, src, expected in DEPENDENCIES:
            if sha(src) != expected:
                raise RuntimeError('Pinned dependency hash mismatch: ' + name)
            rec = compile_one(name, src, evidence, env)
            results.append(rec)
            if rec['exit_code']:
                (evidence / 'verification.json').write_text(json.dumps(results, indent=2) + '\n')
                return rec['exit_code']
        receipt.write_text(json.dumps(results, indent=2) + '\n')
    else:
        old = json.loads(receipt.read_text())
        for rec in old:
            name = rec['module']
            if sha(BUILD / (name + '.lean')) != rec['source_sha256']:
                raise RuntimeError('Changed cached dependency source: ' + name)
            if sha(BUILD / (name + '.olean')) != rec['object_sha256']:
                raise RuntimeError('Changed cached dependency object: ' + name)
        results.append({'dependencies': str(receipt), 'status': 'REUSED_HASH_VERIFIED'})
    rec = compile_one('CoordinateSign', SOURCE, evidence, env)
    results.append(rec)
    (evidence / 'verification.json').write_text(json.dumps(results, indent=2) + '\n')
    print('EVIDENCE', evidence, flush=True)
    return rec['exit_code']

if __name__ == '__main__':
    sys.exit(main())
