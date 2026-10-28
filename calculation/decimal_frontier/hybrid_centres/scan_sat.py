#!/usr/bin/env python3
"""scan_sat.py -- CP-SAT register-model scan for decimal (or any base): all (k, loop, phase, A) at one large width W0 (monotone => covers all widths <= W0).
usage: scan_sat.py <base> <stream index in collect() order> <kmin> <kmax> <W0> [tl] [Tmax]"""
import sys, time, math, json
from hsat import solve
from runbase import loops
from streams_all import collect
S = collect()
b = int(sys.argv[1]); si = int(sys.argv[2]); kmin = int(sys.argv[3]); kmax = int(sys.argv[4]); W0 = int(sys.argv[5])
tl = float(sys.argv[6]) if len(sys.argv) > 6 else 60; Tmax = int(sys.argv[7]) if len(sys.argv) > 7 else 100
(g, e) = sorted(S[b], key=lambda x: (len(x[0]), x))[si]
p = len(g)
print(f"# base {b} stream {g}/{e} p={p} W0={W0}", flush=True)
for k in range(kmin, kmax + 1):
    for lp in loops(b):
        per = len(lp); T0 = p * k; T = T0 * per // math.gcd(T0, per)
        if T > Tmax: continue
        if T != T0 and k > 1 and T % (p) != 0: continue
        gam = [int(g[t % p]) for t in range(T)]; e1 = [int(e[t % p]) for t in range(T)]
        Sg = sum(gam)
        for s in range(per):
            cs = [lp[(s + t) % per] for t in range(T)]
            res = []; t0 = time.time()
            for A in range(0, Sg // 2 + 1):
                st, Q0 = solve(b, gam, e1, cs, W0, A, tl=tl)
                res.append(st[:3])
                if Q0:
                    print(f"HIT b={b} {g}/{e} k={k} T={T} loop={lp} phase={s} A={A} W0={W0} Q0={Q0}", flush=True)
                    json.dump(dict(b=b, g=g, e=e, k=k, T=T, loop=lp, phase=s, A=A, W0=W0, Q0=Q0, cs=cs), open(f'out/HIT_b{b}_{g}_{e}_k{k}_T{T}_A{A}_s{s}.json', 'w'))
            print(f"k={k} T={T} S={Sg} loop={lp} phase={s}: {res} {time.time()-t0:.1f}s", flush=True)
