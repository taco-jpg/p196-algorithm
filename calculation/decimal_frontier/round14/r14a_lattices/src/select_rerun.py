#!/usr/bin/env python3
"""select_rerun.py (r14a): choose BUDGET-limited all-period jobs that look close to death (accepting count at the last level at most THRESH and not growing fast), write (cid orbit) lines to logs/rerun_only.txt"""
import os, re, sys
os.chdir(os.path.expanduser('~/p196_run/r14a'))
THRESH = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
rows = []
for ln in open('logs/sweep_scc.txt'):
    m = re.match(r'scc class (\d+) L=(\d+) T=(\d+) orbit (\d+) rep (\S+) rc=(-?\d+) status=(\w+) lastK=(\S+) peak=(\d+)', ln)
    if not m or m.group(7) != 'BUDGET': continue
    cid, L, T, o = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
    ks = [l.split() for l in open(f'logs/sw_scc_c{cid}_o{o}.log') if l.startswith('K ')]
    if len(ks) < 2: continue
    acc = int(ks[-1][5]); accp = int(ks[-2][5])
    if acc <= THRESH and acc <= 1.3 * accp:
        rows.append((acc, cid, o))
rows.sort()
with open('logs/rerun_only.txt', 'w') as f:
    for acc, cid, o in rows:
        f.write(f'{cid} {o}\n')
print(len(rows), 'jobs selected; first:', rows[:8])
