#!/usr/bin/env python3
"""Parallel dependency-ordered Lean build with a heavy-module lock.
Usage: pbuild2.py JOBS HEAVYFILE Module [Module...]
HEAVYFILE lists module names (whitespace separated) that must not run concurrently
with another heavy module (memory bound). Records timings via run.build."""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor, FIRST_COMPLETED, wait
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run
DIR = run.DIR
def imports(m):
    deps = []
    for line in open(f'{DIR}/{m}.lean'):
        mm = re.match(r'import\s+(\S+)', line)
        if mm: deps.append(mm.group(1))
        elif line.strip() and not line.startswith('import'): break
    return [d for d in deps if os.path.exists(f'{DIR}/{d}.lean')]
def main():
    jobs = int(sys.argv[1]); heavy = set(open(sys.argv[2]).read().split()); targets = sys.argv[3:]
    todo = set(targets); deps = {m: set(imports(m)) & todo for m in todo}
    done, running = set(), {}
    with ThreadPoolExecutor(jobs) as ex:
        while todo - done:
            heavy_running = any(m in heavy for m in running)
            ready = [m for m in targets if m not in done and m not in running and deps[m] <= done]
            for m in ready:
                if len(running) >= jobs: break
                if m in heavy and heavy_running: continue
                running[m] = ex.submit(run.build, m)
                heavy_running = heavy_running or m in heavy
            if not running:
                print('DEADLOCK'); sys.exit(1)
            fin, _ = wait(list(running.values()), return_when=FIRST_COMPLETED)
            for m, f in list(running.items()):
                if f in fin:
                    del running[m]
                    if f.result() != 0:
                        os.system(f'tail -20 {DIR}/logs/{m}.log'); sys.exit(1)
                    done.add(m)
    print('ALL OK', len(done))
if __name__ == '__main__':
    main()
