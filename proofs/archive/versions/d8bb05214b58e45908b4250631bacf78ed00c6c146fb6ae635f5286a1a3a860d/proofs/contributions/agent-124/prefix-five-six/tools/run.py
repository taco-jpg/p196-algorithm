#!/usr/bin/env python3
"""Compile Lean modules in order; record wall time, user time and max RSS per module."""
import os, resource, subprocess, sys, time, json
LEAN = '/home/claude/toolchain/lean-4.19.0-linux/bin/lean'
DIR = os.path.dirname(os.path.abspath(__file__))
env = dict(os.environ, LEAN_PATH=f'{DIR}:/home/claude/toolchain/lean-4.19.0-linux/lib/lean')
def build(m):
    t0 = time.time()
    with open(f'{DIR}/logs/{m}.log', 'w') as log:
        p = subprocess.Popen([LEAN, '-o', f'{DIR}/{m}.olean', '-i', f'{DIR}/{m}.ilean', f'{DIR}/{m}.lean'],
                             stdout=log, stderr=subprocess.STDOUT, env=env)
        _, status, ru = os.wait4(p.pid, 0)
    rc = os.waitstatus_to_exitcode(status)
    rec = {'module': m, 'rc': rc, 'wall': round(time.time() - t0, 1), 'user': round(ru.ru_utime, 1),
           'maxrss_mb': round(ru.ru_maxrss / 1024)}
    with open(f'{DIR}/logs/timings.jsonl', 'a') as f:
        f.write(json.dumps(rec) + '\n')
    print(('OK ' if rc == 0 else 'FAIL ') + json.dumps(rec), flush=True)
    return rc
if __name__ == '__main__':
    for m in sys.argv[1:]:
        if build(m) != 0:
            os.system(f'tail -30 {DIR}/logs/{m}.log')
            sys.exit(1)
