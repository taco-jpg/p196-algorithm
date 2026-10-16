#!/usr/bin/env python3
"""One bounded Lean process, with complete output and resource metadata."""
import argparse
import json
import os
from pathlib import Path
import resource
import subprocess
import time

p = argparse.ArgumentParser()
p.add_argument('--seconds', type=int, default=120)
p.add_argument('--memory', type=int, default=6144)
p.add_argument('--lean-path', required=True)
p.add_argument('--lean', required=True)
p.add_argument('--output', required=True)
p.add_argument('--log', required=True)
p.add_argument('source')
a = p.parse_args()
cmd = [a.lean, '-j', '1', '-o', a.output, a.source]
env = dict(os.environ, LEAN_PATH=a.lean_path)
start = time.monotonic()
status = 'completed'
with open(a.log, 'w') as log:
    log.write(json.dumps({'command':cmd, 'timeout_seconds':a.seconds, 'address_space_mib':a.memory, 'LEAN_PATH':a.lean_path})+'\n')
    log.flush()
    try:
        def limit_memory():
            cap = a.memory * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
        result = subprocess.run(cmd, env=env, stdout=log, stderr=subprocess.STDOUT,
                                timeout=a.seconds, preexec_fn=limit_memory)
        returncode = result.returncode
    except subprocess.TimeoutExpired:
        status, returncode = 'timeout', 124
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    info = {'status':status,'returncode':returncode,'elapsed_seconds':time.monotonic()-start,
            'max_rss_kib':usage.ru_maxrss,'user_seconds':usage.ru_utime,'system_seconds':usage.ru_stime}
    log.write(json.dumps(info)+'\n')
print(json.dumps(info))
raise SystemExit(returncode)
