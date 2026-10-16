#!/usr/bin/env python3
"""Prepare an immutable sparse checkout and invoke the unmodified verifier.

One Lean worker; the canonical verifier makes its own empty source/build
directory. No author .olean is copied. Git source hydration and actual commands
are recorded separately from the untouched canonical receipt.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import time
import traceback


COMMIT = '8f254e9b43bb319a6c43b208cd181ffc005153ec'
CHECKER_PATH = 'proofs/verify_project__214bf7673efe116b.py'
CHECKER_SHA = 'c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a'
PROJECT = 'agent104_620_witness'


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(test: bool, detail: object):
    if not test:
        raise AssertionError(detail)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--git-source', type=Path, required=True)
    parser.add_argument('--checkout', type=Path, required=True)
    parser.add_argument('--lean', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--registry', type=Path, default=Path(__file__).with_name('Agent104620Witness.registry.json'))
    parser.add_argument('--prepare-only', action='store_true')
    args = parser.parse_args()
    output, checkout, source = args.output.resolve(), args.checkout.resolve(), args.git_source.resolve()
    require(not checkout.exists(), 'checkout must be new')
    output.mkdir(parents=True, exist_ok=False)
    registry_path = args.registry.resolve()
    registry_bytes = registry_path.read_bytes()
    registry = json.loads(registry_bytes)
    modules = registry['projects'][PROJECT]['modules']
    require(len(modules) == 11, 'witness closure must contain exactly 11 modules')
    expected = {record['path']: record['sha256'] for record in modules.values()}
    expected[CHECKER_PATH] = CHECKER_SHA
    record = {
        'status': 'PREPARING', 'reviewer': '/root/strategy_review',
        'started_at_utc': datetime.now(timezone.utc).isoformat(),
        'published_commit': COMMIT, 'source_checkout': str(checkout),
        'registry_sha256': sha(registry_bytes), 'unmodified_verifier_sha256': CHECKER_SHA,
        'runner_sha256': sha(Path(__file__).read_bytes()),
        'original_verifier_legacy_agent_field': 'Agent #1; preserved unmodified, not reviewer identity',
        'lean_worker_count': 1, 'author_objects_reused': False, 'commands': [],
    }

    def save():
        (output / 'launch.json').write_text(json.dumps(record, indent=2) + '\n')

    def run(label, command, stdin=None, binary_output=False):
        start = time.monotonic()
        completed = subprocess.run(command, input=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        log = output / (label + '.log')
        log.write_bytes((b'[binary payload omitted; its hash is recorded]\n' if binary_output else completed.stdout) + completed.stderr)
        item = {
            'label': label, 'command': [str(part) for part in command],
            'exit_code': completed.returncode, 'elapsed_seconds': time.monotonic() - start,
            'stdout_sha256': sha(completed.stdout), 'stderr_sha256': sha(completed.stderr),
            'log': log.name, 'log_sha256': sha(log.read_bytes()),
        }
        if stdin is not None:
            item['stdin_utf8'] = stdin.decode()
        record['commands'].append(item)
        save()
        if completed.returncode:
            raise RuntimeError('Failed ' + label + '; see retained log')
        return completed.stdout

    try:
        save()
        present = subprocess.run(['git', '-C', str(source), 'rev-parse', '--verify', COMMIT + '^{commit}'],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if present.returncode:
            run('fetch', ['git', '-C', str(source), 'fetch', '--no-tags', 'origin', COMMIT])
        batch_input = ''.join(COMMIT + ':' + path + '\n' for path in expected).encode()
        payload = run('published-blobs', ['git', '-C', str(source), 'cat-file', '--batch'],
                      stdin=batch_input, binary_output=True)
        stream = io.BytesIO(payload)
        links = {}
        for path, expected_sha in expected.items():
            header = stream.readline().decode().strip().split()
            require(len(header) == 3 and header[1] == 'blob', ('missing published blob', path, header))
            object_id, _, length = header
            data = stream.read(int(length))
            require(stream.read(1) == b'\n', 'batch separator')
            require(sha(data) == expected_sha, ('published SHA mismatch', path))
            require(hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == object_id,
                    ('published blob ID mismatch', path))
            links[path] = {'sha256': sha(data), 'bytes': len(data), 'git_blob': object_id}
        require(stream.read() == b'', 'unexpected batch payload')
        for name, module in modules.items():
            require(links[module['path']]['git_blob'] == module['git_blob'], ('registry Git blob', name))
        run('clone', ['git', 'clone', '--shared', '--no-checkout', '--no-hardlinks', str(source), str(checkout)])
        run('sparse-init', ['git', '-C', str(checkout), 'sparse-checkout', 'init', '--no-cone'])
        patterns = ''.join('/' + path + '\n' for path in expected).encode()
        run('sparse-set', ['git', '-C', str(checkout), 'sparse-checkout', 'set', '--no-cone', '--stdin'], stdin=patterns)
        run('checkout', ['git', '-C', str(checkout), 'checkout', '--detach', COMMIT])
        actual_commit = run('source-head', ['git', '-C', str(checkout), 'rev-parse', 'HEAD']).decode().strip()
        require(actual_commit == COMMIT, 'wrong source commit')
        clean = run('source-status', ['git', '-C', str(checkout), 'status', '--porcelain', '--untracked-files=no'])
        require(not clean, 'published source checkout is dirty')
        for path, link in links.items():
            require(sha((checkout / path).read_bytes()) == link['sha256'], ('checkout bytes', path))
        linkage = {
            'status': 'PASS_BYTE_EXACT_PUBLISHED_SOURCE_LINKAGE', 'published_commit': COMMIT,
            'source_checkout': str(checkout), 'source_tree_tracked_clean': True,
            'all_12_published_git_blobs_read_and_compared': True,
            'module_count': 11, 'checker_included': CHECKER_PATH, 'files': links,
        }
        (output / 'source-linkage.json').write_text(json.dumps(linkage, indent=2) + '\n')
        record['status'] = 'SOURCE_READY'
        save()
        print('Published source ready: 11 modules + unmodified verifier; clean detached checkout.', flush=True)
        if args.prepare_only:
            return
        command = [sys.executable, str(checkout / CHECKER_PATH), '--lean', str(args.lean.resolve()),
                   '--registry', str(registry_path), '--project', PROJECT,
                   '--output', str(output / 'canonical')]
        record['canonical_command'] = command
        record['status'] = 'LEAN_RUNNING'
        save()
        start = time.monotonic()
        with (output / 'canonical-launch.log').open('wb') as log:
            result = subprocess.run(command, cwd=checkout, stdout=log, stderr=subprocess.STDOUT)
        record['canonical_exit_code'] = result.returncode
        record['canonical_elapsed_seconds'] = time.monotonic() - start
        record['canonical_launch_log_sha256'] = sha((output / 'canonical-launch.log').read_bytes())
        require(registry_path.read_bytes() == registry_bytes, 'registry changed during replay')
        require(sha((checkout / CHECKER_PATH).read_bytes()) == CHECKER_SHA, 'canonical verifier changed')
        report_path = output / 'canonical/verification.json'
        record['canonical_report_sha256'] = sha(report_path.read_bytes())
        canonical = json.loads(report_path.read_text())
        require(result.returncode == 0 and canonical['status'] == 'PASS', 'canonical replay did not pass')
        require(canonical['source_commit'] == COMMIT and canonical['source_tree_clean'], 'canonical source metadata mismatch')
        record['status'] = 'PASS'
        print('Canonical witness replay PASS.', flush=True)
    except Exception:
        record['status'] = 'FAIL'
        (output / 'failure.txt').write_text(traceback.format_exc())
        raise
    finally:
        record['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
        save()


if __name__ == '__main__':
    main()
