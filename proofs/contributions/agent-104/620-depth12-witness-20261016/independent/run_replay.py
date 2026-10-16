#!/usr/bin/env python3
"""Run one independent replay worker with recorded commands and resource caps."""
from datetime import datetime, timezone
import argparse
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import sys
import time


def limits():
    resource.setrlimit(resource.RLIMIT_AS, (256 * 1024 * 1024, 256 * 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_CPU, (10, 11))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    directory = Path(__file__).resolve().parent
    command = [sys.executable, str(directory / 'verify_witness.py'),
               '--contribution', str(directory.parent),
               '--output', str(output / 'verification.json')]
    stdout_path, stderr_path = output / 'stdout.log', output / 'stderr.log'
    record = {
        'status': 'RUNNING', 'started_at_utc': datetime.now(timezone.utc).isoformat(),
        'command': command, 'cwd': str(directory.parent),
        'worker_count': 1, 'wall_timeout_seconds': 15,
        'rlimit_as_bytes': 256 * 1024 * 1024, 'rlimit_cpu_seconds': [10, 11],
        'interval_search_started': False, 'compilation_or_lean_build_started': False,
        'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (output / 'command.json').write_text(json.dumps(record, indent=2) + '\n')
    started = time.monotonic()
    try:
        with stdout_path.open('wb') as stdout, stderr_path.open('wb') as stderr:
            result = subprocess.run(command, cwd=directory.parent, stdout=stdout, stderr=stderr,
                                    timeout=15, preexec_fn=limits)
        record['exit_code'] = result.returncode
        record['status'] = 'PASS' if result.returncode == 0 else 'FAILED'
    except subprocess.TimeoutExpired:
        record['exit_code'] = None
        record['status'] = 'TIMEOUT'
    record['elapsed_seconds'] = time.monotonic() - started
    record['child_max_rss_kib'] = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    record['logs'] = {path.name: {'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                                'bytes': path.stat().st_size} for path in [stdout_path, stderr_path]}
    verification = output / 'verification.json'
    if verification.exists():
        record['verification_sha256'] = hashlib.sha256(verification.read_bytes()).hexdigest()
    (output / 'command.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record, indent=2))
    if record['status'] != 'PASS':
        sys.exit(1)


if __name__ == '__main__':
    main()
