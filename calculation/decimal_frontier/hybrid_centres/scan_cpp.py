#!/usr/bin/env python3
"""scan_cpp.py -- run code/htrans over all real neutral exterior streams.
usage: scan_cpp.py <bases comma|all> <kmax> <Tmax> [cap] [stream-filter-prefix]"""
import sys, os, time, math, subprocess, json
from runbase import loops
from streams_all import collect
S = collect()
arg = sys.argv[1]
bases = sorted(S) if arg == 'all' else [int(x) for x in arg.split(',')]
kmax = int(sys.argv[2]); Tmax = int(sys.argv[3]); cap = int(sys.argv[4]) if len(sys.argv) > 4 else 300000
tot = dict(SUCCESS=0, EXHAUSTED=0, CAP=0)
for b in bases:
    for (g, e) in sorted(S.get(b, []), key=lambda x: (len(x[0]), x)):
        p = len(g); inst = []; meta = []
        for k in range(1, kmax + 1):
            for lp in loops(b):
                per = len(lp); T0 = p * k; T = T0 * per // math.gcd(T0, per)
                if T > Tmax: continue
                gs = ''.join(g[t % p] for t in range(T)); es = ''.join(e[t % p] for t in range(T))
                for s in range(per):
                    cs = [lp[(s + t) % per] for t in range(T)]
                    for A in range(0, sum(int(x) for x in gs) // 2 + 1):
                        inst.append(f"{b} {T} {gs} {es} {A} {cap} " + ' '.join(map(str, cs))); meta.append((k, lp, s, A, T))
        if not inst: continue
        t0 = time.time()
        r = subprocess.run([os.environ.get('HTRANS','code/htrans3')], input='\n'.join(inst) + '\n', capture_output=True, text=True)
        lines = r.stdout.strip().splitlines()
        cnt = dict(SUCCESS=0, EXHAUSTED=0, CAP=0); maxlay = 0; maxvis = 0
        for (k, lp, s, A, T), ln in zip(meta, lines):
            f = ln.split(); st = f[1]; cnt[st] += 1; tot[st] += 1
            maxlay = max(maxlay, int(f[2])); maxvis = max(maxvis, int(f[3]))
            if st == 'SUCCESS':
                print(f"SUCCESS b={b} g={g} e={e} k={k} T={T} loop={lp} phase={s} A={A} layers={f[2]} v0path={f[4:]}", flush=True)
            elif st == 'CAP':
                print(f"CAP b={b} g={g} e={e} k={k} T={T} loop={lp} phase={s} A={A} layers={f[2]} visited={f[3]}", flush=True)
        print(f"# b={b} {g}/{e} n={len(inst)} {cnt} maxlayer={maxlay} maxvisited={maxvis} {time.time()-t0:.1f}s", flush=True)
print('TOTAL', tot)
