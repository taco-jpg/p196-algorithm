#!/usr/bin/env python3
"""Fresh author replay of the zero-period ordinary arithmetic bridge."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time


def sha(data):
    return hashlib.sha256(data).hexdigest()


p = argparse.ArgumentParser()
p.add_argument('--source-root', type=Path, required=True)
p.add_argument('--build-dir', type=Path, required=True)
p.add_argument('--evidence-dir', type=Path, required=True)
p.add_argument('--lean', required=True)
a = p.parse_args()
root, build, evidence = a.source_root.resolve(), a.build_dir.resolve(), a.evidence_dir.resolve()
build.mkdir(parents=True, exist_ok=False)
evidence.mkdir(parents=True, exist_ok=False)
registry = (root / 'proofs/Agent1PeriodicValidity.registry.json').read_bytes()
assert sha(registry) == '8a89e6f07294073b7496d7369d235a3921628ac5cecd72baa58f66a8043fa513'
registered = json.loads(registry)['projects']['agent1-periodic-validity']['modules']
modules = [(name, spec['path'], spec['sha256']) for name, spec in registered.items()]
modules += [
    ('Agent1PeriodicZeroPeriod', 'proofs/Agent1PeriodicZeroPeriod.lean',
     '3761744f62cabdf25cf69f8e2990ce81eec9ac75cfb2273a5e80974304795a8a'),
    ('Agent1PeriodicZeroNumeric', 'proofs/Agent1PeriodicZeroNumeric.lean',
     '8e561a621f18d783aa52ef0f2d6985b0a6cd0293b80fe4b174250665cee07b89'),
]
manifest = []
for name, path, expected in modules:
    data = (root / path).read_bytes()
    assert sha(data) == expected, path
    (build / (name + '.lean')).write_bytes(data)
    if name.startswith('Agent1PeriodicZero'):
        (evidence / (name + '.lean')).write_bytes(data)
    manifest.append(dict(module=name, path=path, sha256=expected))
(evidence / 'sources.json').write_text(json.dumps(manifest, indent=2) + '\n')
version = subprocess.run([a.lean, '--version'], text=True, capture_output=True, check=True)
(evidence / 'version.log').write_text(version.stdout + version.stderr)
assert 'version 4.19.0' in version.stdout and '6caaee842e94' in version.stdout
compiler_sha = sha(Path(a.lean).read_bytes())
assert compiler_sha == '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
results = []
for name, _, _ in modules:
    command = [a.lean, '--trust=0', '-j1', '-DElab.async=false',
               '-o', name + '.olean', name + '.lean']
    start = time.time()
    r = subprocess.run(command, cwd=build, env=dict(os.environ, LEAN_PATH=str(build)),
                       text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (evidence / (name + '.log')).write_text(r.stdout)
    results.append(dict(module=name, command=command, exit_code=r.returncode,
                        seconds=time.time()-start, log_sha256=sha(r.stdout.encode())))
    (evidence / 'commands.json').write_text(json.dumps(results, indent=2) + '\n')
    print(name + ': exit ' + str(r.returncode), flush=True)
    if r.returncode:
        print(r.stdout, end='')
        raise SystemExit(r.returncode)

source = (build / 'Agent1PeriodicZeroNumeric.lean').read_text()
exports = re.findall(r'^(?:def|theorem)\s+(\w+)', source, re.M)
expected = ['fixedDigits_getD_outputIn', 'normalize_length_nextWidth',
            'normalize_getD_output', 'normalize_getD_extended', 'zipAdd_getD',
            'pair_getD_columnSum', 'stepWord_length_nextWidth',
            'stepWord_getD_nextColumns', 'actual_step_representation',
            'zero_quotient_actual_step']
assert exports == expected, exports
for bad in ('sorry', 'admit', 'native_decide', 'Lean.ofReduceBool', 'unsafe', 'axiom '):
    assert bad not in source, bad
log = (evidence / 'Agent1PeriodicZeroNumeric.log').read_text()
parsed = re.findall(r"'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)", log)
assert [name for name, _ in parsed] == ['Agent1.Periodic.' + name for name in expected]
axioms = {x.strip() for _, values in parsed for x in values.split(',') if x.strip()}
assert axioms <= {'propext', 'Classical.choice', 'Quot.sound'}, axioms
for name, path, expected_sha in modules:
    assert sha((root / path).read_bytes()) == expected_sha, path
    assert sha((build / (name + '.lean')).read_bytes()) == expected_sha, name
(evidence / 'verification.json').write_text(json.dumps(dict(
    status='PASS', scope='Author clean replay; independent review not implied',
    fresh_empty_build_directory=True, project_object_reuse=False,
    modules_compiled=len(modules), explicit_exports=exports, explicit_export_count=len(exports),
    theorem_count=10, definition_count=0, axiom_union=sorted(axioms), source_drift=False,
    compiler_version=version.stdout.strip(), compiler_sha256=compiler_sha,
    runner_sha256=sha(Path(__file__).read_bytes()), build_dir=str(build),
    claim_commit='d5786f691f77c606f7343b1182cc67643f058a8f'), indent=2) + '\n')
print('PASS: nineteen fresh modules; ten complete explicit-export axiom audits', flush=True)
