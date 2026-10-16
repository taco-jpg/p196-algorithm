#!/usr/bin/env python3
"""Reviewer's own dependency-ordered clean build (independent of the author's check.py).

Usage: build.py LEAN_BIN BUILD_DIR LOG_DIR TARGET [JOBS]

Parses `import X` lines of each X.lean in BUILD_DIR (flat layout, module name =
file stem), computes the import closure of TARGET, and compiles every module with
`lean -j1 -o X.olean X.lean` (LEAN_PATH=BUILD_DIR), at most JOBS at a time, in
dependency order. Records per-module exit code, wall time, peak RSS (from
resource.getrusage of children is aggregate, so we sample /proc), and log file.
"""
import json
import os
import re
import subprocess
import sys
import time

lean, bdir, logdir, target = sys.argv[1:5]
jobs = int(sys.argv[5]) if len(sys.argv) > 5 else 2

IMPORT_RE = re.compile(r'^import\s+(\S+)\s*$')


def imports_of(mod):
    out = []
    with open(os.path.join(bdir, mod + '.lean'), encoding='utf-8') as fh:
        for line in fh:
            m = IMPORT_RE.match(line.strip())
            if m:
                out.append(m.group(1))
    return out


# closure
closure = {}
stack = [target]
while stack:
    m = stack.pop()
    if m in closure:
        continue
    if m in ('Std', 'Init', 'Lean'):
        closure[m] = []
        continue
    path = os.path.join(bdir, m + '.lean')
    if not os.path.exists(path):
        print('MISSING', m, file=sys.stderr)
        sys.exit(2)
    deps = imports_of(m)
    closure[m] = deps
    stack.extend(deps)

local = {m: [d for d in deps if d not in ('Std', 'Init', 'Lean')]
         for m, deps in closure.items() if m not in ('Std', 'Init', 'Lean')}
print('closure size', len(local), flush=True)

env = dict(os.environ)
env['LEAN_PATH'] = bdir
done = {}
running = {}
results = {}
order = []
t_start = time.time()


def peak_rss(pid):
    try:
        with open(f'/proc/{pid}/status') as fh:
            for line in fh:
                if line.startswith('VmHWM:'):
                    return int(line.split()[1])
    except OSError:
        return None
    return None


while len(done) < len(local):
    # launch
    ready = [m for m in sorted(local) if m not in done and m not in running
             and all(d in done and done[d] == 0 for d in local[m])]
    failed_dep = [m for m in sorted(local) if m not in done and m not in running
                  and any(d in done and done[d] != 0 for d in local[m])]
    for m in failed_dep:
        done[m] = -999
        results[m] = {'exit': None, 'skipped': 'dependency failed'}
    while ready and len(running) < jobs:
        m = ready.pop(0)
        log = open(os.path.join(logdir, m + '.log'), 'w')
        cmd = [lean, '-j1', '-o', m + '.olean', m + '.lean']
        p = subprocess.Popen(cmd, cwd=bdir, env=env, stdout=log, stderr=subprocess.STDOUT)
        running[m] = (p, time.time(), log, 0)
        print(f'[{time.time()-t_start:8.1f}s] start {m}', flush=True)
    # poll
    time.sleep(1)
    for m in list(running):
        p, t0, log, hwm = running[m]
        h = peak_rss(p.pid)
        if h is not None and h > hwm:
            running[m] = (p, t0, log, h)
            hwm = h
        rc = p.poll()
        if rc is not None:
            log.close()
            dt = time.time() - t0
            done[m] = rc
            results[m] = {'exit': rc, 'seconds': round(dt, 1), 'peak_rss_kb': hwm,
                          'cmd': f'lean -j1 -o {m}.olean {m}.lean'}
            order.append(m)
            del running[m]
            print(f'[{time.time()-t_start:8.1f}s] done  {m} exit={rc} {dt:.1f}s rss={hwm}kB', flush=True)
    if not running and not any(m not in done for m in local if all(d in done and done[d] == 0 for d in local[m])):
        if len(done) < len(local):
            # remaining modules blocked
            for m in local:
                if m not in done:
                    done[m] = -999
                    results[m] = {'exit': None, 'skipped': 'blocked'}

summary = {'target': target, 'lean': lean, 'build_dir': bdir, 'jobs': jobs,
           'total_seconds': round(time.time() - t_start, 1),
           'order': order, 'results': results,
           'all_ok': all(r.get('exit') == 0 for r in results.values()),
           'imports': local}
with open(os.path.join(logdir, 'build-summary.json'), 'w') as fh:
    json.dump(summary, fh, indent=1, sort_keys=True)
print('ALL_OK' if summary['all_ok'] else 'FAILURES', flush=True)
