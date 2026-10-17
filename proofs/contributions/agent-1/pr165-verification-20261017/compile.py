#!/usr/bin/env python3
"""Fresh untouched-source two-module PR165 compilation. Never changes author files."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import resource
import shutil
import subprocess
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
HEAD = 'cb273afa5b2827e3427d7098e2e13564701d349a'
LEAN = Path('/workspace/p196-tools/lean-4.19.0-linux/bin/lean')
COMPILER_SHA = '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
PINS = {
    'Agent105DecoderLocal9df76b': {
        'path': 'proofs/contributions/agent-103/residual-five-third-gate-20261016/vendor/Agent105DecoderLocal9df76b.lean',
        'git_blob': 'e03c9a6cc7aadb7e882c47417411e3e091264683',
        'sha256': '820d28d68005208ac21dd498dcd27660b58d2d147de265dbcd0cf0d7c250e872',
        'imports': ['Std']},
    'ResidualFivePredecessorFilter': {
        'path': 'proofs/contributions/agent-103/residual-five-predecessor-filter-count-20261016/ResidualFivePredecessorFilter.lean',
        'git_blob': '73887468f8915540fc76a9654116d54db24b593e',
        'sha256': 'e5e1187f750ce73181c6294c724052eaca1d6f30d81d7533c266a79b5bf58aee',
        'imports': ['Agent105DecoderLocal9df76b']}}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def save(path, obj):
    path.write_text(json.dumps(obj, indent=2) + '\n')


run = HERE / 'fresh-001'
run.mkdir(exist_ok=False)
source = run / 'source'
source.mkdir()
shutil.copy2(__file__, run / 'compile.py')
report = {'status': 'RUNNING', 'source_commit': HEAD,
          'claim_commit': '1004f1f804eac1eaec8cb01fc433fe2c5032fcd0',
          'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'fresh_project_module_count': 2, 'dependency_objects_reused': False,
          'initial_build_directory_empty': not any(source.iterdir()),
          'source_pins': PINS, 'commands': [], 'audit_status': 'NOT_RUN'}
save(run / 'result.json', report)
try:
    assert digest(LEAN.read_bytes()) == COMPILER_SHA
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == HEAD
    version = subprocess.check_output([str(LEAN), '--version'], text=True).strip()
    assert version == 'Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)'
    (run / 'lean-version.txt').write_text(version + '\n')
    report['compiler'] = {'path': str(LEAN), 'sha256': COMPILER_SHA, 'version': version}
    for name, pin in PINS.items():
        raw = (ROOT / pin['path']).read_bytes()
        assert digest(raw) == pin['sha256'] and git_blob(raw) == pin['git_blob']
        assert raw == subprocess.check_output(['git', 'show', HEAD + ':' + pin['path']], cwd=ROOT)
        (source / (name + '.lean')).write_bytes(raw)
    save(run / 'source-pins.json', PINS)
    env = {'PATH': str(LEAN.parent) + ':/usr/bin:/bin', 'LANG': 'C.UTF-8', 'LEAN_PATH': str(source)}
    report['environment'] = env
    report['cwd'] = str(source)
    for name, pin in PINS.items():
        command = [str(LEAN), '--trust=0', '-j1', '-DElab.async=false',
                   '-o', name + '.olean', name + '.lean']
        started = time.monotonic()
        with (run / (name + '.log')).open('wb') as log:
            process = subprocess.run(command, cwd=source, env=env,
                                     stdout=log, stderr=subprocess.STDOUT)
        record = {'module': name, 'command': command, 'exit_code': process.returncode,
                  'elapsed_seconds': time.monotonic() - started,
                  'cumulative_children_max_rss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                  'log_sha256': digest((run / (name + '.log')).read_bytes())}
        obj = source / (name + '.olean')
        if obj.exists(): record['object_sha256'] = digest(obj.read_bytes())
        report['commands'].append(record)
        save(run / 'result.json', report)
        print(json.dumps(record), flush=True)
        if process.returncode:
            report['status'] = 'UNTOUCHED_SOURCE_COMPILE_FAILED'
            report['failed_module'] = name
            break
    else:
        report['status'] = 'FRESH_TWO_MODULE_COMPILE_PASS_AUDIT_PENDING'
    for name, pin in PINS.items():
        assert digest((ROOT / pin['path']).read_bytes()) == pin['sha256']
        assert digest((source / (name + '.lean')).read_bytes()) == pin['sha256']
    report['author_sources_and_snapshots_unchanged'] = True
except Exception as error:
    report['status'] = 'SETUP_OR_EXECUTION_ERROR'
    report['error'] = repr(error)
    raise
finally:
    report['finished_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save(run / 'result.json', report)
    print(json.dumps({'status': report['status'], 'result': str(run / 'result.json')}), flush=True)

if report['status'] != 'FRESH_TWO_MODULE_COMPILE_PASS_AUDIT_PENDING':
    raise SystemExit(1)
