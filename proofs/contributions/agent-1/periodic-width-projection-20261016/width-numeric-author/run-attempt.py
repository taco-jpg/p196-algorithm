#!/usr/bin/env python3
"""Retain strict WidthNumeric author increments and full module-origin audits."""
from pathlib import Path
import hashlib
import json
import re
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
SOURCE = ROOT / 'proofs/Agent1PeriodicWidthNumeric.lean'
LEAN = Path('/workspace/p196-tools/lean-4.19.0-linux/bin/lean')
GUARD = Path('/workspace/p196-agent1-session-20261016/guard-parent-clean-001')
PUBLIC = ['Agent1.Periodic.periodic_decimalLength_mod_eight',
          'Agent1.Periodic.periodic_actual_step_decimalLength_mod_eight']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def run(command, folder, env, label):
    started = time.monotonic()
    observed_rss = 0
    observed_virtual = 0
    stop = None
    with (folder / (label + '.log')).open('wb') as output:
        process = subprocess.Popen(command, cwd=folder, env=env, stdout=output,
                                   stderr=subprocess.STDOUT)
        while process.poll() is None:
            try:
                status = Path(f'/proc/{process.pid}/status').read_text()
                rss = re.search(r'^VmRSS:\s+(\d+) kB$', status, re.M)
                virt = re.search(r'^VmSize:\s+(\d+) kB$', status, re.M)
                if rss:
                    observed_rss = max(observed_rss, int(rss.group(1)))
                if virt:
                    observed_virtual = max(observed_virtual, int(virt.group(1)))
                if observed_rss > 1500 * 1024:
                    stop = 'RSS exceeded 1500 MiB stop threshold'
                    process.kill()
                elif time.monotonic() - started > 600:
                    stop = '600 second timeout'
                    process.kill()
            except FileNotFoundError:
                pass
            time.sleep(0.01)
        rc = process.wait()
    receipt = {'status': 'PASS' if rc == 0 and stop is None else 'FAIL',
               'exit_code': rc, 'seconds': time.monotonic() - started,
               'command': command, 'environment': env,
               'observed_peak_rss_kib': observed_rss,
               'observed_peak_virtual_kib': observed_virtual,
               'kernel_children_peak_rss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
               'rss_watchdog_stop_threshold_mib': 1500,
               'rss_poll_interval_seconds': 0.01, 'address_space_limit_mib': None,
               'watchdog_reason': stop}
    write_json(folder / (label + '-receipt.json'), receipt)
    print(json.dumps({'phase': label, **receipt}), flush=True)
    return receipt


def main():
    label = sys.argv[1]
    assert re.fullmatch(r'[a-zA-Z0-9_-]+', label)
    out = HERE / label
    out.mkdir(exist_ok=False)
    source_bytes = SOURCE.read_bytes()
    (out / SOURCE.name).write_bytes(source_bytes)
    width_author = HERE.parent / 'width-author'
    width_receipt = json.loads((width_author / 'attempt-002/receipt.json').read_text())
    width_audit = json.loads((width_author / 'audit-003/receipt.json').read_text())
    assert width_receipt['status'] == width_audit['status'] == 'PASS'
    quotient_registry = ROOT / 'proofs/Agent1PeriodicQuotient.registry.json'
    guard_registry = ROOT / 'proofs/Agent1PeriodicGuard.registry.json'
    registry = json.loads(quotient_registry.read_text())['projects']['agent1-periodic-quotient']['modules']
    guard_pins = json.loads(guard_registry.read_text())['projects']['agent1-periodic-guard']['modules']
    for name, pin in guard_pins.items():
        if name in registry:
            assert registry[name] == pin
    registry.update(guard_pins)
    pins = dict(width_receipt['dependencies'])
    pins['Agent1PeriodicWidth'] = {
        'source': str(width_author / 'attempt-002/Agent1PeriodicWidth.lean'),
        'sha256': width_receipt['source_sha256'],
        'object': str(width_author / 'attempt-002/Agent1PeriodicWidth.olean'),
        'object_sha256': width_audit['object_sha256']}
    registry['Agent1PeriodicWidth'] = {
        'path': 'proofs/Agent1PeriodicWidth.lean',
        'sha256': width_receipt['source_sha256'],
        'git_blob': width_receipt['source_git_blob'],
        'imports': ['Agent1PeriodicQuotient']}
    guard_report = json.loads((GUARD / 'verification.json').read_text())
    guard_files = json.loads((GUARD / 'FILES.json').read_text())
    assert guard_report['status'] == 'PASS'
    assert guard_report['projects']['agent1-periodic-guard']['status'] == 'PASS'
    assert guard_report['projects']['agent1-periodic-guard']['sources']['Agent1PeriodicNumeric']['sha256'] == guard_pins['Agent1PeriodicNumeric']['sha256']
    for name in guard_pins:
        relative = f'agent1-periodic-guard/source/{name}.lean'
        assert sha(GUARD / relative) == guard_files[relative]['sha256']
        assert sha(GUARD / f'agent1-periodic-guard/source/{name}.lean') == guard_pins[name]['sha256']
    numeric_path = ROOT / guard_pins['Agent1PeriodicNumeric']['path']
    numeric_bytes = numeric_path.read_bytes()
    assert sha(numeric_path) == guard_pins['Agent1PeriodicNumeric']['sha256']
    assert hashlib.sha1(b'blob ' + str(len(numeric_bytes)).encode() + b'\0' + numeric_bytes).hexdigest() == guard_pins['Agent1PeriodicNumeric']['git_blob']
    assert re.findall(r'^import\s+(\S+)', numeric_bytes.decode(), re.M) == guard_pins['Agent1PeriodicNumeric']['imports']
    assert all(d in pins for d in guard_pins['Agent1PeriodicNumeric']['imports'])
    (out / numeric_path.name).write_bytes(numeric_bytes)
    for name, pin in pins.items():
        source = Path(pin['source'])
        data = source.read_bytes()
        rec = registry[name]
        assert sha(source) == pin['sha256'] == rec['sha256']
        assert sha(Path(pin['object'])) == pin['object_sha256']
        assert (ROOT / rec['path']).read_bytes() == data
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == rec['git_blob']
        deps = re.findall(r'^import\s+(\S+)', data.decode(), re.M)
        assert deps == rec['imports']
        assert all(d in pins or d.split('.')[0] in {'Init', 'Std', 'Lean'} for d in deps)
        pin.update({'repository_path': rec['path'], 'git_blob': rec['git_blob'], 'imports': deps})
        (out / (name + '.lean')).write_bytes(data)
        (out / (name + '.olean')).write_bytes(Path(pin['object']).read_bytes())
    assert len(pins) == 15
    version = subprocess.check_output([str(LEAN), '--version'], text=True).strip()
    assert 'version 4.19.0,' in version and 'commit 6caaee842e94' in version
    assert sha(LEAN) == width_receipt['compiler_sha256']
    manifest = {'source_sha256': sha(SOURCE), 'source_git_blob': hashlib.sha1(
        b'blob ' + str(len(source_bytes)).encode() + b'\0' + source_bytes).hexdigest(),
        'compiler_version': version, 'compiler_sha256': sha(LEAN),
        'reused_dependencies': pins, 'reused_dependency_count': len(pins),
        'dependency_count': len(pins) + 1,
        'fresh_existing_module': dict(guard_pins['Agent1PeriodicNumeric']),
        'guard_verification_report': str(GUARD / 'verification.json'),
        'guard_verification_sha256': sha(GUARD / 'verification.json'),
        'guard_files_sha256': sha(GUARD / 'FILES.json'),
        'registry_sha256': {str(p): sha(p) for p in [quotient_registry, guard_registry]},
        'fresh_dependency_build': False,
        'scope': 'Strict author increment; 14 pinned Quotient closure objects and frozen Width object reused. Existing unchanged Numeric module compiled fresh before the new wrapper.'}
    write_json(out / 'source-and-dependencies.json', manifest)
    env = {'PATH': str(LEAN.parent) + ':/usr/bin:/bin', 'LANG': 'C.UTF-8', 'LEAN_PATH': str(out)}
    flags = [str(LEAN), '--trust=0', '-j1', '-DElab.async=false']
    numeric_compilation = run(flags + ['-o', numeric_path.stem + '.olean', numeric_path.name], out, env, 'existing-numeric-compile')
    if numeric_compilation['status'] != 'PASS':
        return 1
    manifest['fresh_existing_module']['object_sha256'] = sha(out / (numeric_path.stem + '.olean'))
    write_json(out / 'source-and-dependencies.json', manifest)
    compilation = run(flags + ['-o', SOURCE.stem + '.olean', SOURCE.name], out, env, 'compile')
    if compilation['status'] != 'PASS':
        return 1
    template = (width_author / 'audit-003/WidthAudit.lean').read_text()
    body = template[template.index('run_cmd do'):].replace('Agent1PeriodicWidth', 'Agent1PeriodicWidthNumeric')
    audit = 'import Agent1PeriodicWidthNumeric\nimport Lean.Elab.BuiltinEvalCommand\nopen Lean Elab Command\nset_option maxRecDepth 100000\nset_option maxHeartbeats 0\n'
    audit += '\n'.join('#check @' + name + '\n#print axioms ' + name for name in PUBLIC) + '\n' + body
    (out / 'WidthNumericAudit.lean').write_text(audit)
    audit_receipt = run(flags + ['WidthNumericAudit.lean'], out, env, 'audit')
    log = (out / 'audit.log').read_text()
    totals = re.findall(r'^MODULE_AUDIT theorems=(\d+) definitions=(\d+) opaque=(\d+) union=(.*)$', log, re.M)
    rows = re.findall(r'^AUDIT_(THEOREM|SAFE_DEFINITION|SAFE_OPAQUE) (\S+) :', log, re.M)
    complete = len(totals) == 1 and sum(map(int, totals[0][:3])) == len(rows) and set(PUBLIC) <= {r[1] for r in rows}
    unchanged = SOURCE.read_bytes() == source_bytes and numeric_path.read_bytes() == numeric_bytes and all(
        sha(Path(p['source'])) == p['sha256'] and sha(Path(p['object'])) == p['object_sha256'] and
        sha(ROOT / p['repository_path']) == p['sha256'] for p in pins.values())
    final = {'status': 'PASS' if audit_receipt['status'] == 'PASS' and complete and unchanged else 'FAIL',
             'source_sha256': sha(SOURCE), 'source_git_blob': manifest['source_git_blob'],
             'object_sha256': sha(out / (SOURCE.stem + '.olean')),
             'audit_sha256': sha(out / 'WidthNumericAudit.lean'), 'public_declarations': PUBLIC,
             'new_module_totals': totals, 'audited_declarations': rows,
             'unsafe_implementation_axioms': re.findall(r'^UNSAFE_IMPLEMENTATION_AXIOM (.*)$', log, re.M),
             'non_safe_definitions': re.findall(r'^NON_SAFE_DEFINITION (.*)$', log, re.M),
             'unsafe_opaques': re.findall(r'^UNSAFE_OPAQUE (.*)$', log, re.M),
             'source_object_and_dependency_pins_unchanged': unchanged,
             'fresh_dependency_build': False, 'dependency_count': len(pins) + 1,
             'reused_dependency_count': len(pins), 'fresh_existing_module_count': 1}
    write_json(out / 'receipt.json', final)
    print(json.dumps(final), flush=True)
    return 0 if final['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
