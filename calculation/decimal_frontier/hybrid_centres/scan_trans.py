#!/usr/bin/env python3
"""scan_trans.py -- exact all-width hybrid decision (htrans.decide) over real neutral exterior streams.
usage: scan_trans.py <bases comma> <kmax> <Tmax> [cap]   prints SUCCESS lines + one summary line per stream."""
import sys, time, math, json
from htrans import decide
from runbase import loops
from streams_all import collect
S = collect()
bases = [int(x) for x in sys.argv[1].split(',')]
kmax = int(sys.argv[2]); Tmax = int(sys.argv[3]); cap = int(sys.argv[4]) if len(sys.argv) > 4 else 300000
for b in bases:
    for (g, e) in sorted(S.get(b, []), key=lambda x: (len(x[0]), x)):
        p = len(g)
        cnt = dict(SUCCESS=0, EXHAUSTED=0, CAP=0); t0 = time.time()
        for k in range(1, kmax + 1):
            for lp in loops(b):
                per = len(lp); T0 = p * k; T = T0 * per // math.gcd(T0, per)
                if T > Tmax: continue
                gam = [int(g[t % p]) for t in range(T)]; e1 = [int(e[t % p]) for t in range(T)]
                for s in range(per):
                    cs = [lp[(s + t) % per] for t in range(T)]
                    for A in range(0, sum(gam) // 2 + 1):
                        res = decide(b, gam, e1, cs, A, cap=cap)
                        cnt[res[0]] += 1
                        if res[0] == 'SUCCESS':
                            print(f"SUCCESS b={b} g={g} e={e} k={k} T={T} loop={lp} phase={s} A={A} layers={res[1]} v0path={res[2]}", flush=True)
                        elif res[0] == 'CAP':
                            print(f"CAP b={b} g={g} e={e} k={k} T={T} loop={lp} phase={s} A={A} {res[1:]}", flush=True)
        print(f"# b={b} {g}/{e} {cnt} {time.time()-t0:.1f}s", flush=True)
