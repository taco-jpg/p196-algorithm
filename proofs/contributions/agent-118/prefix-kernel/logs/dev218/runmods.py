#!/usr/bin/env python3
"""Dev runner: compile modules in dependency order with up to N workers, recording time and peak RSS.

usage: runmods.py --build DIR --src DIR [--src DIR ...] [--jobs N] MODULE...
Sources are copied into the build dir first. Stops scheduling new work after the first failure.
"""
import argparse, json, os, re, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED

LEAN = '/home/claude/lean-toolchain/lean-4.19.0-linux/bin/lean'
ap = argparse.ArgumentParser()
ap.add_argument('--build', required=True)
ap.add_argument('--src', action='append', required=True)
ap.add_argument('--jobs', type=int, default=1)
ap.add_argument('--log', default=None)
ap.add_argument('modules', nargs='+')
a = ap.parse_args()
B = os.path.abspath(a.build)

def find(m):
    for s in a.src:
        p = os.path.join(s, m + '.lean')
        if os.path.exists(p):
            return p
    return None

def imports(path):
    out = []
    for line in open(path):
        mm = re.match(r'^import\s+(\S+)', line)
        if mm: out.append(mm.group(1))
    return out

order, seen = [], set()
def visit(m):
    if m in seen: return
    seen.add(m)
    p = find(m)
    if p is None:
        return  # assumed prebuilt in B or in the Lean core library
    for i in imports(p): visit(i)
    order.append(m)
for m in a.modules: visit(m)
todo = [m for m in order if not (os.path.exists(os.path.join(B, m + '.olean')) and
        os.path.exists(os.path.join(B, m + '.lean')) and
        open(os.path.join(B, m + '.lean'), 'rb').read() == open(find(m), 'rb').read())]
deps = {m: set(i for i in imports(find(m)) if i in todo) for m in todo}
for m in todo: shutil.copyfile(find(m), os.path.join(B, m + '.lean'))
env = dict(os.environ); env['LEAN_PATH'] = B
logf = open(a.log, 'a') if a.log else None

def run(m):
    t = time.monotonic()
    with open(os.path.join(B, m + '.log'), 'w') as f:
        p = subprocess.Popen([LEAN, '-j1', '-DElab.async=false', '-o', m + '.olean', m + '.lean'],
                             cwd=B, env=env, stdout=f, stderr=subprocess.STDOUT)
        _, st, ru = os.wait4(p.pid, 0)
    rec = {'module': m, 'exit': os.waitstatus_to_exitcode(st), 'seconds': round(time.monotonic() - t, 2),
           'max_rss_mib': ru.ru_maxrss // 1024}
    line = json.dumps(rec)
    print(line, flush=True)
    if logf: logf.write(line + '\n'); logf.flush()
    return rec

done, failed, active = set(), [], {}
remaining = list(todo)
with ThreadPoolExecutor(max_workers=a.jobs) as pool:
    while (remaining and not failed) or active:
        ready = [m for m in remaining if deps[m] <= done] if not failed else []
        for m in ready[:a.jobs - len(active)]:
            active[pool.submit(run, m)] = m
            remaining.remove(m)
        if not active:
            break
        fin, _ = wait(active, return_when=FIRST_COMPLETED)
        for f in fin:
            m = active.pop(f)
            r = f.result()
            if r['exit'] == 0: done.add(m)
            else:
                failed.append(m)
                print(open(os.path.join(B, m + '.log')).read()[-3000:], flush=True)
print(json.dumps({'built': len(done), 'failed': failed, 'not_started': remaining}), flush=True)
sys.exit(1 if failed or remaining else 0)
