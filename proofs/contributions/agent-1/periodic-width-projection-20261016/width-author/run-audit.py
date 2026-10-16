#!/usr/bin/env python3
"""Audit the frozen author increment with a physical-memory watchdog."""
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


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    label = sys.argv[1]
    assert re.fullmatch(r'[a-zA-Z0-9_-]+', label)
    out = HERE / label
    out.mkdir(exist_ok=False)
    previous = json.loads((HERE / 'audit-002/receipt.json').read_text())
    compile_receipt = json.loads((HERE / 'attempt-002/receipt.json').read_text())
    assert compile_receipt['status'] == 'PASS'
    source = ROOT / 'proofs/Agent1PeriodicWidth.lean'
    object_path = HERE / 'attempt-002/Agent1PeriodicWidth.olean'
    source_hash = sha(source)
    object_hash = sha(object_path)
    assert source_hash == compile_receipt['source_sha256']
    assert all(sha(Path(pin['source'])) == pin['sha256'] and
               sha(Path(pin['object'])) == pin['object_sha256']
               for pin in compile_receipt['dependencies'].values())
    audit_source = HERE / 'audit-002/WidthAudit.lean'
    (out / audit_source.name).write_bytes(audit_source.read_bytes())
    env = dict(previous['environment'])
    env['LEAN_PATH'] = str(out) + ':' + ':'.join(env['LEAN_PATH'].split(':')[1:])
    command = previous['command']
    started = time.monotonic()
    observed_rss_kib = 0
    observed_virtual_kib = 0
    watchdog_reason = None
    with (out / 'audit.log').open('wb') as stream:
        process = subprocess.Popen(command, cwd=out, env=env, stdout=stream,
                                   stderr=subprocess.STDOUT)
        while process.poll() is None:
            try:
                proc_status = Path(f'/proc/{process.pid}/status').read_text()
                rss = re.search(r'^VmRSS:\s+(\d+) kB$', proc_status, re.M)
                virt = re.search(r'^VmSize:\s+(\d+) kB$', proc_status, re.M)
                if rss:
                    observed_rss_kib = max(observed_rss_kib, int(rss.group(1)))
                if virt:
                    observed_virtual_kib = max(observed_virtual_kib, int(virt.group(1)))
                if observed_rss_kib > 1500 * 1024:
                    watchdog_reason = 'RSS exceeded 1500 MiB stop threshold'
                    process.kill()
                elif time.monotonic() - started > 600:
                    watchdog_reason = '600 second timeout'
                    process.kill()
            except FileNotFoundError:
                pass
            time.sleep(0.01)
        rc = process.wait()
    peak_rss_kib = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    log = (out / 'audit.log').read_text()
    totals = re.findall(r'^MODULE_AUDIT theorems=(\d+) definitions=(\d+) opaque=(\d+) union=(.*)$', log, re.M)
    rows = re.findall(r'^AUDIT_(THEOREM|SAFE_DEFINITION|SAFE_OPAQUE) (\S+) :', log, re.M)
    complete = (len(totals) == 1 and sum(map(int, totals[0][:3])) == len(rows) and
                set(previous['public_declarations']) <= {row[1] for row in rows})
    unchanged = (sha(source) == source_hash and sha(object_path) == object_hash and
                 all(sha(Path(pin['source'])) == pin['sha256'] and
                     sha(Path(pin['object'])) == pin['object_sha256']
                     for pin in compile_receipt['dependencies'].values()))
    passed = rc == 0 and watchdog_reason is None and peak_rss_kib < 2 * 1024 * 1024 and complete and unchanged
    receipt = {
        'status': 'PASS' if passed else 'FAIL', 'exit_code': rc,
        'seconds': time.monotonic() - started, 'command': command,
        'environment': env, 'source_sha256': source_hash,
        'object_sha256': object_hash, 'audit_sha256': sha(out / audit_source.name),
        'public_declarations': previous['public_declarations'],
        'new_module_totals': totals, 'audited_declarations': rows,
        'unsafe_implementation_axioms': re.findall(r'^UNSAFE_IMPLEMENTATION_AXIOM (.*)$', log, re.M),
        'non_safe_definitions': re.findall(r'^NON_SAFE_DEFINITION (.*)$', log, re.M),
        'unsafe_opaques': re.findall(r'^UNSAFE_OPAQUE (.*)$', log, re.M),
        'source_object_and_dependencies_unchanged': unchanged,
        'dependency_count': len(compile_receipt['dependencies']),
        'reused_dependency_receipt': '../attempt-002/receipt.json',
        'fresh_dependency_build': False,
        'address_space_limit_mib': None,
        'rss_watchdog_stop_threshold_mib': 1500, 'rss_poll_interval_seconds': 0.01,
        'watchdog_reason': watchdog_reason,
        'kernel_peak_rss_kib': peak_rss_kib,
        'observed_peak_rss_kib': observed_rss_kib,
        'observed_peak_virtual_kib': observed_virtual_kib,
        'scope': 'Full new-module origin theorem/safe-definition audit; author increment using pinned provided Quotient dependency objects. No fresh dependency closure rebuild.'
    }
    (out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k: receipt[k] for k in ['status', 'exit_code', 'seconds', 'new_module_totals', 'kernel_peak_rss_kib', 'observed_peak_virtual_kib', 'watchdog_reason']}))
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
