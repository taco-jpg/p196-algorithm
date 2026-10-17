#!/usr/bin/env python3
"""Retain every return-core source attempt before a bounded incremental check."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import time

evidence = Path(__file__).resolve().parent
root = evidence.parents[4]
build = evidence / 'build'
is_audit = len(sys.argv) > 2 and sys.argv[2] == 'audit'
name = 'ReturnCoreAudit' if is_audit else 'Agent1PeriodicReturnCore'
lean = '/workspace/p196-tools/lean-4.19.0-linux/bin/lean'
attempt = evidence / sys.argv[1]
attempt.mkdir(exist_ok=False)
source = evidence / (name + '.lean') if is_audit else root / 'proofs' / (name + '.lean')
data = source.read_bytes()
(attempt / (name + '.lean')).write_bytes(data)
(build / (name + '.lean')).write_bytes(data)
(build / (name + '.olean')).unlink(missing_ok=True)
command = [lean, '--trust=0', '-j1', '-DElab.async=false', '-o', name + '.olean', name + '.lean']

started = time.time()
rss_limit_kib = 1500 * 1024
max_rss_kib = 0
memory_limit_hit = False
with (attempt / 'build.log').open('w') as log:
    process = subprocess.Popen(command, cwd=build, env=dict(os.environ, LEAN_PATH=str(build)),
                               stdout=log, stderr=subprocess.STDOUT)
    while process.poll() is None:
        try:
            status = Path(f'/proc/{process.pid}/status').read_text()
            rss = next(int(line.split()[1]) for line in status.splitlines()
                       if line.startswith('VmRSS:'))
            max_rss_kib = max(max_rss_kib, rss)
            if rss > rss_limit_kib:
                memory_limit_hit = True
                process.terminate()
                try:
                    process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    process.kill()
                break
        except (FileNotFoundError, ProcessLookupError, StopIteration):
            pass
        time.sleep(0.05)
    exit_code = process.wait()
(attempt / 'result.json').write_text(json.dumps({
    'command': command, 'source_sha256': hashlib.sha256(data).hexdigest(),
    'exit_code': exit_code, 'elapsed_seconds': time.time() - started,
    'rss_limit_kib': rss_limit_kib, 'peak_sampled_rss_kib': max_rss_kib,
    'memory_limit_hit': memory_limit_hit,
    'verification_scope': 'new module only; pinned dependency objects reused'
}, indent=2) + '\n')
print((attempt / 'build.log').read_text(), end='')
print('exit', exit_code)
sys.exit(exit_code)
