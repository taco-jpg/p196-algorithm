#!/usr/bin/env python3
"""scan_sat2.py <stream:p11|p12> <loopkey 0|18|6|2> <kmin> <kmax> <W0> [tl]  -- CP-SAT register model for the genuine decimal streams; one line per (k,phase,A-list)."""
import sys, time
from hsat import solve
from runsat import stream
name = sys.argv[1]; lk = sys.argv[2]; kmin = int(sys.argv[3]); kmax = int(sys.argv[4]); W0 = int(sys.argv[5]); tl = float(sys.argv[6]) if len(sys.argv) > 6 else 60
loop = {'0': [0], '18': [18], '6': [6, 12], '2': [2, 4, 8, 16, 14, 10]}[lk]
cyc = stream(name); p = len(cyc)
for k in range(kmin, kmax + 1):
    T = p * k
    if T % len(loop): continue
    gam = [cyc[t % p][1] for t in range(T)]; e1 = [cyc[t % p][2] for t in range(T)]
    for s in range(len(loop)):
        cs = [loop[(s + t) % len(loop)] for t in range(T)]
        t0 = time.time(); res = []
        for A in range(0, sum(gam) // 2 + 1):
            st, Q0 = solve(10, gam, e1, cs, W0, A, tl=tl)
            res.append(st[:3])
            if Q0: print('HIT', name, lk, k, s, A, W0, Q0, flush=True)
        print(f"{name} loop={lk} k={k} T={T} phase={s} W0={W0}: {''.join(r[0] for r in res)} ({time.time()-t0:.1f}s)  [I=INFEASIBLE O=OPTIMAL U=UNKNOWN]", flush=True)
