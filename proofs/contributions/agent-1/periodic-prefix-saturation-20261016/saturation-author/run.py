#!/usr/bin/env python3
"""Strict incremental author build and complete new-module axiom audit.

Reuses only source-hash-checked dependency objects from the recorded original
build directories. This is not a fresh full-closure or independent review.
Every execution gets a new attempt directory and retains exact input source.
"""
from pathlib import Path
import hashlib
import json
import os
import resource
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
LEAN = Path('/workspace/p196-tools/lean-4.19.0-linux/bin/lean')
MODULE = 'Agent1PeriodicSaturation'
CLOCK = Path('/workspace/p196-agent1-session-20261016/periodic-clock-parent-clean-001/agent1-periodic-return-clock/source')
PROFILE = Path('/workspace/p196-agent1-onboarding/saturated-profile-build/agent2-saturated-profile/source')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')

def limits():
    resource.setrlimit(resource.RLIMIT_AS, (4 * 1024**3, 4 * 1024**3))

def main():
    attempt = HERE / sys.argv[1]
    prefix = Path(sys.argv[2]).resolve()
    attempt.mkdir(exist_ok=False)
    shutil.copyfile(__file__, attempt / 'run.py')
    shutil.copyfile(REPO / 'proofs' / (MODULE + '.lean'), attempt / (MODULE + '.lean'))
    paths = [prefix, CLOCK, PROFILE]
    records = {}
    for filename in ['Agent1PeriodicReturnClock.registry.json', 'Agent2SaturatedProfile.registry.json']:
        registry = json.loads((REPO / 'proofs' / filename).read_text())
        for spec in registry['projects'].values():
            for name, rec in spec['modules'].items():
                if name in records:
                    assert records[name]['sha256'] == rec['sha256'], name
                    assert records[name]['imports'] == rec['imports'], name
                records[name] = rec
    prefix_source = REPO / 'proofs/Agent1PeriodicPrefix.lean'
    records['Agent1PeriodicPrefix'] = {
        'path': 'proofs/Agent1PeriodicPrefix.lean',
        'sha256': sha(prefix_source),
        'imports': ['Agent1PeriodicOuter', 'SaturationTheorem']}
    required = set()
    def visit(name):
        if name in required or name == 'Std' or name.startswith('Lean.'):
            return
        for imp in records[name]['imports']:
            visit(imp)
        required.add(name)
    for name in ['Agent1PeriodicPrefix', 'Agent1PeriodicReturnClock', 'Agent2SaturatedProfile']:
        visit(name)
    dependencies = []
    for name in sorted(required):
        rec = records[name]
        original = REPO / rec['path']
        assert sha(original) == rec['sha256'], name
        directory = next(p for p in paths if (p / (name + '.olean')).is_file())
        source = directory / (name + '.lean')
        obj = directory / (name + '.olean')
        assert sha(source) == rec['sha256'], (name, str(source))
        dependencies.append({'module': name, 'original': str(original),
            'source': str(source), 'source_sha256': sha(source),
            'object': str(obj), 'object_sha256': sha(obj)})
    write(attempt / 'dependencies.json', dependencies)
    env = os.environ.copy()
    env['LEAN_PATH'] = ':'.join(str(p) for p in [attempt, *paths])
    version = subprocess.check_output([str(LEAN), '--version'], text=True)
    assert 'version 4.19.0' in version and '6caaee842e94' in version, version
    (attempt / 'lean-version.txt').write_text(version)
    commands = []
    def run(name, command):
        rec = {'name': name, 'command': command, 'cwd': str(attempt),
            'LEAN_PATH': env['LEAN_PATH'], 'compiler_sha256': sha(LEAN),
            'address_space_limit_bytes': 4 * 1024**3}
        start = time.monotonic()
        with (attempt / (name + '.log')).open('w') as log:
            result = subprocess.run(command, cwd=attempt, env=env,
                stdout=log, stderr=subprocess.STDOUT, preexec_fn=limits, timeout=600)
        rec.update(exit_code=result.returncode, elapsed_seconds=time.monotonic()-start,
            max_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        commands.append(rec)
        write(attempt / 'commands.json', commands)
        print((attempt / (name + '.log')).read_text(), end='', flush=True)
        return result.returncode
    flags = [str(LEAN), '--trust=0', '-j1', '-DElab.async=false']
    result = run('compile', flags + ['-o', MODULE + '.olean', MODULE + '.lean'])
    if result == 0:
        shutil.copyfile(HERE / 'SaturationAudit.lean', attempt / 'SaturationAudit.lean')
        result = run('audit', flags + ['SaturationAudit.lean'])
    record = {'status': 'PASS' if result == 0 else 'FAIL', 'exit_code': result,
        'claim': '8a8e6b9d748cbd25892e4836ff1a25fc55a78ca2',
        'source_sha256': sha(attempt / (MODULE + '.lean')),
        'dependency_count': len(dependencies), 'dependency_objects_reused': True,
        'full_new_module_audit': result == 0,
        'fresh_full_closure': False, 'independent_review': False,
        'source_unchanged_during_run': sha(REPO / 'proofs' / (MODULE + '.lean')) == sha(attempt / (MODULE + '.lean'))}
    write(attempt / 'result.json', record)
    (attempt / 'exit-code.txt').write_text(str(result) + '\n')
    print(json.dumps(record, indent=2), flush=True)
    return result

if __name__ == '__main__':
    sys.exit(main())
