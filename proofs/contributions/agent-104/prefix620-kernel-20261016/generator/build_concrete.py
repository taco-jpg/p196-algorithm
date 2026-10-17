#!/usr/bin/env python3
"""Bounded author build of the frozen Agent104 620 concrete modules.

The shared thirteen-module byte-exact dependency closure must already be built
by runtime_scout. This scheduler does not rebuild or edit those dependencies.
Sources, successes, failures, logs and resource records remain attributable to
this author build; they are not an independent review.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import threading
import time

HERE = Path(__file__).resolve().parent
PROOFS = HERE.parents[3]
DEFAULT_BUILD = Path('/tmp/agent104-prefix620-author')
DEFAULT_LEAN = Path('/workspace/scratch/a1d46b1077ac/agent103-runtime/toolchain/lean-4.19.0-linux/bin/lean')


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', choices=['data', 'pilot', 'finite-pilot', 'all'], required=True)
    parser.add_argument('--jobs', type=int, choices=[1, 2], default=2)
    parser.add_argument('--build', type=Path, default=DEFAULT_BUILD)
    parser.add_argument('--lean', type=Path, default=DEFAULT_LEAN)
    parser.add_argument('--label', required=True)
    args = parser.parse_args()
    manifest_path = HERE / 'GENERATION_MANIFEST.json'
    manifest = json.loads(manifest_path.read_text())
    order = manifest['build_order']
    build = args.build.resolve()
    assert build == DEFAULT_BUILD.resolve(), 'This author build is scoped to its isolated build directory'
    dependencies = ['PrefixCertificate', 'PrefixInverse', 'LongRowsBase', 'FastInverse',
                    'FastRowsBase', 'Agent124FastPred', 'LychrelDigitSums', 'ActualPrefix',
                    'PalindromeBridge', 'ShortBoundary', 'Agent124PrefixK', 'Agent124PrefixR',
                    'Agent124CodeCert']
    for dependency in dependencies:
        assert (build / (dependency + '.lean')).is_file(), dependency + ': source unavailable'
        assert (build / (dependency + '.olean')).is_file(), dependency + ': shared base build not ready'
    evidence = HERE / 'evidence' / args.label
    evidence.mkdir(parents=True, exist_ok=False)
    logs = evidence / 'logs'
    logs.mkdir()
    state_path = HERE / 'evidence' / 'successful-builds.json'
    previous = json.loads(state_path.read_text()) if state_path.exists() else {}
    source_hashes = {}
    imports = {}
    for module in order:
        original = PROOFS / (module + '.lean')
        expected = manifest['sources'][module]['sha256']
        assert sha(original) == expected, module + ': original source changed'
        data = original.read_bytes()
        dest = build / (module + '.lean')
        if dest.exists() and dest.read_bytes() != data:
            old = evidence / 'prior-build-sources' / (module + '.lean')
            old.parent.mkdir(exist_ok=True)
            old.write_bytes(dest.read_bytes())
        dest.write_bytes(data)
        source_hashes[module] = expected
        imports[module] = re.findall(r'^import\s+(\w+)\s*$', data.decode(), re.MULTILINE)

    if args.stage == 'data':
        selected = [m for m in order if m.startswith('Agent104Prefix620Data')]
    elif args.stage == 'pilot':
        selected = [f'Agent104Prefix620Rows{i:03d}' for i in [0, 64, 128, 192, 255]]
        selected += ['Agent104Prefix620RowsBranch', 'Agent104Prefix620ShortAll', 'Agent104Prefix620InitialAll']
    elif args.stage == 'finite-pilot':
        selected = list(manifest['finite_pilot_modules'])
    else:
        selected = list(order)
    for module in selected:
        assert module in source_hashes, 'Unknown selected module ' + module
    env = dict(os.environ)
    for name in ['LEAN_PATH', 'LEAN_SRC_PATH', 'LEAN_SYSROOT']:
        env.pop(name, None)
    env['LEAN_PATH'] = str(build)
    compiler = subprocess.run([str(args.lean), '--version'], capture_output=True, text=True, check=True)
    assert 'version 4.19.0' in compiler.stdout and 'commit 6caaee842e94' in compiler.stdout
    report = {'status': 'IN_PROGRESS', 'kind': 'AUTHOR_BUILD', 'independent_review': False,
              'stage': args.stage, 'jobs': args.jobs, 'compiler': compiler.stdout.strip(),
              'lean_sha256': sha(args.lean), 'build': str(build),
              'manifest_sha256': sha(manifest_path), 'selected': selected,
              'dependency_sources': {m: sha(build / (m + '.lean')) for m in dependencies},
              'dependency_objects': {m: sha(build / (m + '.olean')) for m in dependencies},
              'commands': [], 'reused_concrete_objects': []}
    report_path = evidence / 'verification.json'
    lock = threading.Lock()

    def save() -> None:
        report_path.write_text(json.dumps(report, indent=2) + '\n')
        state_path.write_text(json.dumps(previous, indent=2) + '\n')

    complete = set(dependencies)
    for module in order:
        record = previous.get(module)
        obj = build / (module + '.olean')
        # Invalidate transitively when an imported concrete definition changes,
        # even if a dependent proof's own source bytes are unchanged.
        import_objects = {m: sha(build / (m + '.olean')) for m in imports[module]
                          if m in complete}
        imports_valid = set(imports[module]) <= complete
        if record and 'import_object_sha256' in record:
            imports_valid = imports_valid and record['import_object_sha256'] == import_objects
        if record and imports_valid and record['source_sha256'] == source_hashes[module] and obj.exists() and sha(obj) == record['object_sha256']:
            complete.add(module)
            if module in selected:
                report['reused_concrete_objects'].append(module)
        else:
            previous.pop(module, None)
    pending = {m for m in selected if m not in complete}
    for module in pending:
        needed = set(imports[module]) - complete - pending
        if needed:
            raise RuntimeError(f'{module}: run data stage first; unavailable dependencies {sorted(needed)}')
    save()

    def run(module: str) -> dict:
        command = [str(args.lean), '-j1', '-DElab.async=false', '--trust=0',
                   '-o', module + '.olean', module + '.lean']
        started = time.monotonic()
        log = logs / (module + '.log')
        with log.open('w') as stream:
            proc = subprocess.Popen(command, cwd=build, env=env, stdout=stream, stderr=subprocess.STDOUT)
            _, status, usage = os.wait4(proc.pid, 0)
            proc.returncode = os.waitstatus_to_exitcode(status)
        record = {'module': module, 'command': command, 'exit_code': proc.returncode,
                  'seconds': round(time.monotonic() - started, 3),
                  'user_seconds': round(usage.ru_utime, 3), 'system_seconds': round(usage.ru_stime, 3),
                  'max_rss_kib': usage.ru_maxrss, 'source_sha256': source_hashes[module],
                  'import_object_sha256': {m: sha(build / (m + '.olean')) for m in imports[module]},
                  'log': str(log.relative_to(HERE)), 'log_sha256': sha(log)}
        if proc.returncode == 0:
            record['object_sha256'] = sha(build / (module + '.olean'))
        else:
            failed = evidence / 'failed-sources'
            failed.mkdir(exist_ok=True)
            (failed / (module + '.lean')).write_bytes((build / (module + '.lean')).read_bytes())
        return record

    started = time.monotonic()
    active = {}
    failure = False
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        while pending or active:
            ready = [m for m in order if m in pending and set(imports[m]) <= complete]
            if not failure:
                for module in ready[:args.jobs - len(active)]:
                    active[pool.submit(run, module)] = module
                    pending.remove(module)
            if not active:
                if pending and not failure:
                    report['failure'] = 'Dependency scheduler blocked: ' + ', '.join(sorted(pending))
                    failure = True
                break
            finished, _ = wait(active, return_when=FIRST_COMPLETED)
            for future in finished:
                module = active.pop(future)
                record = future.result()
                report['commands'].append(record)
                if record['exit_code'] == 0:
                    complete.add(module)
                    previous[module] = record
                else:
                    failure = True
                    report['failure'] = f'{module} exited {record["exit_code"]}'
                save()
                done = len(report['commands'])
                if done <= 2 or done % 16 == 0 or failure or args.stage in ['pilot', 'finite-pilot']:
                    print(json.dumps({'done': done, 'module': module, 'exit_code': record['exit_code'],
                                      'seconds': record['seconds'], 'max_rss_kib': record['max_rss_kib'],
                                      'pending': len(pending)}), flush=True)
            if failure and not active:
                break
    report['status'] = 'FAIL' if failure else 'PASS'
    report['wall_seconds'] = round(time.monotonic() - started, 3)
    report['compiled_this_stage'] = len(report['commands'])
    report['total_successful_concrete_modules'] = sum(m in complete for m in order)
    report['cpu_seconds_this_stage'] = round(sum(r['user_seconds'] + r['system_seconds'] for r in report['commands']), 3)
    report['max_rss_kib_this_stage'] = max((r['max_rss_kib'] for r in report['commands']), default=0)
    save()
    print(json.dumps({k: report[k] for k in ['status', 'wall_seconds', 'compiled_this_stage',
                                           'total_successful_concrete_modules', 'cpu_seconds_this_stage',
                                           'max_rss_kib_this_stage']}, indent=2), flush=True)
    return 1 if failure else 0


if __name__ == '__main__':
    raise SystemExit(main())
