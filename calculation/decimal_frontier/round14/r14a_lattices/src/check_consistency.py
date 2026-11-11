#!/usr/bin/env python3
"""check_consistency.py (r14a): for every (class,orbit) with both all-period and fixed-period logs: at every level E_acc(K,T) <= Cyc_acc(K), accepting counts <=; EMPTY level of E_acc <= EMPTY level of Cyc_acc."""
import os, re, glob, json
os.chdir(os.path.expanduser('~/p196_run/r14a'))
def levels(path):
    res = {}
    emp = None
    for l in open(path, errors='ignore'):
        if l.startswith('K '):
            p = l.split()
            res[int(p[1])] = (int(p[3]), int(p[5]))
        elif l.startswith('EMPTY at K='):
            emp = int(l.strip().split('=')[1])
    return res, emp
n = 0; bad = 0; lv = 0
for runlog in glob.glob('logs/sw_run_c*_o*.log'):
    m = re.search(r'sw_run_c(\d+)_o(\d+)', runlog)
    c, o = m.group(1), m.group(2)
    for scclog in (f'logs/rr_scc_c{c}_o{o}.log', f'logs/sw_scc_c{c}_o{o}.log'):
        if os.path.exists(scclog):
            break
    else:
        continue
    R, er = levels(runlog); S, es = levels(scclog)
    n += 1
    for K in R:
        if K in S:
            lv += 1
            if R[K][0] > S[K][0] or R[K][1] > S[K][1]:
                bad += 1
                print('VIOLATION', runlog, K, R[K], S[K])
    if er is not None and es is not None and er > es:
        bad += 1; print('EMPTY order violation', runlog, er, es)
print('pairs compared', n, 'levels', lv, 'violations', bad)
