#!/usr/bin/env python3
"""Parallel dependency-ordered Lean build. Usage: pbuild.py JOBS Module [Module...]
Builds the given modules (and any not-yet-built local imports among them) with up to JOBS
concurrent compilers; records timings via run.build."""
import os, re, sys, time
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
    jobs = int(sys.argv[1]); targets = sys.argv[2:]
    todo = set(targets); deps = {m: set(imports(m)) & todo for m in todo}
    done, running, failed = set(), {}, []
    with ThreadPoolExecutor(jobs) as ex:
        while todo - done:
            ready = [m for m in sorted(todo - done - set(running)) if deps[m] <= done]
            while ready and len(running) < jobs:
                m = ready.pop(0); running[m] = ex.submit(run.build, m)
            if not running:
                print('DEADLOCK or failure', failed); sys.exit(1)
            fin, _ = wait(list(running.values()), return_when=FIRST_COMPLETED)
            for m, f in list(running.items()):
                if f in fin:
                    del running[m]
                    if f.result() != 0:
                        failed.append(m); os.system(f'tail -20 {DIR}/logs/{m}.log'); sys.exit(1)
                    done.add(m)
    print('ALL OK', len(done))
if __name__ == '__main__':
    main()
