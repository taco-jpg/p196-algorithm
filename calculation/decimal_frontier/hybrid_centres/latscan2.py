#!/usr/bin/env python3
"""latscan2.py -- exact spatial-transfer decision, lattice below / absorbing core above, ALL core loops at once (one BFS per (k,A,j0); the reachable
set is independent of the core; success = reaching ANY core vacuum link state).
usage: latscan2.py <latfile> <kmin> <kmax> <cap> [Amin] [Amax]"""
import sys, time, math, subprocess
sys.path.insert(0, 'lat')
from latcheck import load, carries
from latscan import lat_state, run
LOOPS = [[0], [18], [6, 12], [2, 4, 8, 16, 14, 10]]

def vac_state(b, T, gam, cs, A):
    Aup = []; G = []; dd = []
    for t in range(T):
        k = 1 if cs[t] >= b else 0; y = (cs[t] + k) % b
        Aup.append(k); G.append(k); dd.append(y if gam[t % len(gam)] else 0)
    return Aup + G + dd + [cs[0]] * A

def line(b, T, gam, A, cap, start, vacs):
    Aup, G, dd, mem = start
    s = f"{b} {T} {''.join(str(gam[t % len(gam)]) for t in range(T))} {'0' * T} {A} {cap} " + ' '.join(['0'] * T)
    s += ' LAT ' + ' '.join(map(str, Aup + G + dd + mem))
    s += f' VACS {len(vacs)} ' + ' '.join(' '.join(map(str, v)) for v in vacs)
    return s

if __name__ == '__main__':
    fn = sys.argv[1]; kmin = int(sys.argv[2]); kmax = int(sys.argv[3]); cap = int(sys.argv[4])
    p, nB, m, b, gam, W, cup = load(fn); S = sum(gam)
    for k in range(kmin, kmax + 1):
        T = p * k
        vacs = []
        for lp in LOOPS:
            per = len(lp)
            if T % per: continue
            for s in range(per):
                vacs.append((lp, s, [lp[(s + t) % per] for t in range(T)]))
        Amin = int(sys.argv[5]) if len(sys.argv) > 5 else 0
        Amax = int(sys.argv[6]) if len(sys.argv) > 6 else S * k // 2
        for A in range(Amin, Amax + 1):
            j0s = [0] if A == 0 else list(range(m))
            lines = [line(b, T, gam, A, cap, lat_state(p, m, b, gam, W, T, A, j0), [vac_state(b, T, gam, cs, A) for (_, _, cs) in vacs]) for j0 in j0s]
            t0 = time.time(); out = run(lines)
            cnt = {'SUCCESS': 0, 'EXHAUSTED': 0, 'CAP': 0}; mx = 0
            for j0, o in zip(j0s, out):
                f = o.split(); cnt[f[1]] += 1; mx = max(mx, int(f[3]))
                if f[1] != 'EXHAUSTED': print(f"   {f[1]} j0={j0} layers={f[2]} visited={f[3]} path={f[4:]}", flush=True)
            print(f"{fn} m={m} k={k} T={T} A={A} starts={len(j0s)} loops/phases={len(vacs)}: {cnt} maxvisited={mx} ({time.time()-t0:.1f}s)", flush=True)
