#!/usr/bin/env python3
"""Minimal independent import-DAG builder: compile every module in DIR (except
listed exclusions) once its project imports are built; WORKERS concurrent."""
import json, os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor, FIRST_COMPLETED, wait
D, LEAN, WORKERS = sys.argv[1], sys.argv[2], int(sys.argv[3])
EXCLUDE = set(sys.argv[4].split(',')) if len(sys.argv) > 4 else set()
mods = sorted(f[:-5] for f in os.listdir(D) if f.endswith('.lean') and f[:-5] not in EXCLUDE)
imports = {}
for m in mods:
    src = re.sub(r'/-.*?-/', '', open(f'{D}/{m}.lean').read(), flags=re.S)
    imports[m] = [t for l in re.findall(r'^import\s+([^\n]+)', src, re.M) for t in l.split() if t in mods]
done, pending, running, log = set(), list(mods), {}, open(f'{D}/../dagbuild.jsonl', 'a')
env = dict(os.environ, LEAN_PATH=D)
def build(m):
    t = time.time()
    with open(f'{D}/{m}.log', 'wb') as out:
        p = subprocess.run(['bash', '-c', f'ulimit -v 6500000; exec {LEAN} -j1 -DElab.async=false -o {m}.olean {m}.lean'],
                           cwd=D, env=env, stdout=out, stderr=subprocess.STDOUT)
    return m, p.returncode, round(time.time() - t, 2)
with ThreadPoolExecutor(WORKERS) as pool:
    while pending or running:
        for m in list(pending):
            if len(running) >= WORKERS: break
            if all(d in done for d in imports[m]):
                pending.remove(m); running[pool.submit(build, m)] = m
        if not running:
            print('STUCK', pending); sys.exit(2)
        fin, _ = wait(list(running), return_when=FIRST_COMPLETED)
        for f in fin:
            running.pop(f); m, rc, secs = f.result()
            rec = dict(module=m, exit=rc, seconds=secs); log.write(json.dumps(rec) + '\n'); log.flush()
            print(json.dumps(rec), flush=True)
            if rc != 0:
                # retry once alone (memory pressure)
                while running:
                    wait(list(running)); [running.pop(x) for x in list(running) if x.done()]
                    for x in [x for x in list(running)]: pass
                m, rc, secs = build(m)
                rec = dict(module=m, exit=rc, seconds=secs, retry=True); log.write(json.dumps(rec) + '\n'); log.flush()
                print(json.dumps(rec), flush=True)
                if rc != 0: print('FAILED', m); sys.exit(1)
            done.add(m)
print('ALL_DONE', len(done))
