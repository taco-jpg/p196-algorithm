#!/usr/bin/env python3
"""Untouched-source strict compiler replication; each invocation is a fresh closure."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import subprocess
import time
from source_scanner import lean_code_tokens

p = argparse.ArgumentParser()
p.add_argument('--source-root', type=Path, required=True)
p.add_argument('--build-dir', type=Path, required=True)
p.add_argument('--evidence-dir', type=Path, required=True)
p.add_argument('--lean', type=Path, required=True)
p.add_argument('--memory-mib', type=int, default=8192)
p.add_argument('--module-timeout-seconds', type=int, default=600)
a = p.parse_args()
here = Path(__file__).resolve().parent
root, build, evidence = a.source_root.resolve(), a.build_dir.resolve(), a.evidence_dir.resolve()
build.mkdir(parents=True, exist_ok=False)
evidence.mkdir(parents=True, exist_ok=False)
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda path, value: path.write_text(json.dumps(value, indent=2) + '\n')
for name in ['replay.py', 'source_scanner.py', 'AuditTemplate.lean.txt', 'source-pins.json', 'closure.json']:
    (evidence / name).write_bytes((here / name).read_bytes())
manifest = json.loads((here / 'source-pins.json').read_text())
closure = json.loads((here / 'closure.json').read_text())
source_commit = closure['source_commit']
modules = {x['module']: x for x in manifest}
order = closure['requested_build_order']
assert len(order) == 17 and set(order) == set(modules)
(evidence / 'compiled-sources').mkdir()
for name in order:
    entry = modules[name]
    data = (root / entry['path']).read_bytes()
    assert sha(data) == entry['sha256'], name
    assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == entry['git_blob'], name
    assert data == subprocess.check_output(['git', 'show', source_commit + ':' + entry['path']], cwd=root), name
    assert [line.split()[1] for line in data.decode().splitlines() if line.startswith('import ')] == entry['imports'], name
    forbidden = re.findall(r'\b(?:sorry|admit|native_decide|sorryAx|axiom)\b|Lean\.ofReduceBool', lean_code_tokens(data.decode()))
    assert not forbidden, (name, forbidden)
    (build / (name + '.lean')).write_bytes(data)
    (evidence / 'compiled-sources' / (name + '.lean')).write_bytes(data)
compiler = {'path': str(a.lean), 'sha256': sha(a.lean.read_bytes()),
            'version': subprocess.check_output([str(a.lean), '--version'], text=True).strip()}
assert 'version 4.19.0' in compiler['version'] and '6caaee842e94' in compiler['version']
assert compiler['sha256'] == '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
dump(evidence / 'compiler.json', compiler)
dump(evidence / 'preflight.json', {'status': 'PASS', 'source_commit': source_commit,
    'all_source_bytes_match_commit': True, 'module_count': 17,
    'minimal_root_closure_count': 16, 'extra_control_root': 'Agent105PredecessorControls9df76b',
    'source_objects_reused': False, 'source_scan': 'nested comments and strings masked'})
env = dict(os.environ, LEAN_PATH=str(build))
results = []
started = time.monotonic()

def limit_child():
    cap = a.memory_mib * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (cap, cap))

def run(module, output=True):
    cmd = [str(a.lean), '--trust=0', '-j1', '-DElab.async=false']
    if output:
        cmd += ['-o', module + '.olean']
    cmd += [module + '.lean']
    start = time.monotonic()
    try:
        proc = subprocess.run(cmd, cwd=build, env=env, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, timeout=a.module_timeout_seconds, preexec_fn=limit_child)
        out, code, timed_out = proc.stdout, proc.returncode, False
    except subprocess.TimeoutExpired as exc:
        out, code, timed_out = (exc.stdout or b'') + b'\nCOMMAND_TIMEOUT\n', 124, True
    (evidence / (module + '.log')).write_bytes(out)
    results.append({'module': module, 'argv': cmd, 'cwd': str(build), 'LEAN_PATH': env['LEAN_PATH'],
        'exit_code': code, 'timed_out': timed_out, 'seconds': time.monotonic() - start,
        'address_space_mib': a.memory_mib, 'timeout_seconds': a.module_timeout_seconds,
        'stack': 'compiler default', 'log_sha256': sha(out),
        'object_exists': (build / (module + '.olean')).is_file()})
    dump(evidence / 'commands.json', results)
    print(module + ': exit ' + str(code), flush=True)
    if code:
        print(out.decode(), flush=True)
        dump(evidence / 'verification.json', {'status': 'FAIL', 'source_commit': source_commit,
            'failed_module': module, 'completed_commands': len(results),
            'successful_module_compilations': sum(x['exit_code'] == 0 for x in results),
            'full_origin_audit_completed': False, 'second_fresh_requested_only_if_first_passes': True,
            'seconds': time.monotonic() - started, 'source_changes': False})
        raise SystemExit(code)

for module in order:
    run(module)
print('FIRST_COMPILATION_GATE_PASS: all 17 modules', flush=True)

audit = (here / 'AuditTemplate.lean.txt').read_text().replace('SELECTED', ', '.join(json.dumps(x) for x in order))
public_theorems = ['backwardLayer_zero_spec', 'backwardLayer_zero_nodup', 'preimagesNat_zero']
public_definitions = ['targetWord', 'targetDigitFn', 'preimagesNat', 'backwardLayer',
    'PreimagesSpec', 'BackwardLayerSpec', 'BackwardLayerNodup', 'EmptyLayerPersistence']
for name in public_theorems + public_definitions:
    full = 'Agent105BackwardLayers9df76b.' + name
    audit += '\n#check ' + full + '\n#print axioms ' + full + '\n'
(build / 'ReplicationAudit.lean').write_text(audit)
(evidence / 'ReplicationAudit.lean').write_text(audit)
run('ReplicationAudit', output=False)
log = (evidence / 'ReplicationAudit.log').read_text()
assert not re.search(r'sorryAx|Lean\.ofReduceBool|DISALLOWED_', log)
for name in public_theorems + public_definitions:
    assert 'Agent105BackwardLayers9df76b.' + name in log
origin = lambda prefix: len(re.findall('^' + prefix + ' ', log, re.M))
new_origin = lambda prefix: len(re.findall('^' + prefix + r' Agent105BackwardLayers9df76b ', log, re.M))
dump(evidence / 'verification.json', {'status': 'PASS', 'source_commit': source_commit,
    'module_count': 17, 'commands': len(results), 'full_origin_theorems': origin('AUDIT_THEOREM'),
    'full_origin_safe_definitions': origin('AUDIT_SAFE_DEFINITION'),
    'new_origin_theorems': new_origin('AUDIT_THEOREM'),
    'new_origin_safe_definitions': new_origin('AUDIT_SAFE_DEFINITION'),
    'public_new_theorems': public_theorems, 'public_new_definitions': public_definitions,
    'unsafe_axioms_inventoried': origin('UNSAFE_IMPLEMENTATION_AXIOM'),
    'nonsafe_definitions_inventoried': origin('NONSAFE_DEFINITION'),
    'unsafe_opaque_inventoried': origin('UNSAFE_OPAQUE'),
    'source_changes': False, 'source_objects_reused': False,
    'seconds': time.monotonic() - started})
print((evidence / 'verification.json').read_text(), flush=True)
