#!/usr/bin/env python3
"""latscan.py -- exact spatial-transfer decision for a defect between a periodic p=8 (etc.) lattice below and the absorbing core above.
usage: latscan.py <latfile> <kmax> <cap> [loops=0,18,6,2]  (A = 0..floor(sum gam/2))
Start state = lattice link state at cell j0 = 0 (all departure phases are reached by walking along the lattice).
Output lines: SUCCESS/EXHAUSTED/CAP per (lattice, k, loop, core phase, A)."""
import sys, os, math, subprocess, time
sys.path.insert(0, 'lat')
from latcheck import load, carries
LOOPS = {'0': [0], '18': [18], '6': [6, 12], '2': [2, 4, 8, 16, 14, 10]}

def lat_state(p, m, b, gam, W, T, A, j0):
    Aup = []; G = []; dd = []
    for t in range(T):
        v = W[t % p]; a, dl = carries(v, b)
        Aup.append(a[j0 % m]); G.append(dl[(j0 - 1) % m])
        dd.append((v[(j0 - 1) % m] + dl[(j0 - 1) % m]) % b if gam[t % p] else 0)
    # closure: the first A cells above the wall must be lattice at time T (== phase 0), later cells v_i(T)=v_{i-A}(0)
    mem = [W[0][(j0 + i) % m] for i in range(A)]
    return Aup, G, dd, mem

def inst_line(b, T, gam, e1dummy, A, cap, cs, start, vac=None):
    Aup, G, dd, mem = start
    s = f"{b} {T} {''.join(str(gam[t % len(gam)]) for t in range(T))} {'0' * T} {A} {cap} " + ' '.join(map(str, cs))
    s += ' LAT ' + ' '.join(map(str, Aup + G + dd + mem))
    if vac is not None:
        s += ' VAC ' + ' '.join(map(str, vac[0] + vac[1] + vac[2] + vac[3]))
    return s

def run(lines):
    r = subprocess.run([os.environ.get('HTRANS','code/htrans3')], input='\n'.join(lines) + '\n', capture_output=True, text=True)
    return r.stdout.strip().splitlines()

if __name__ == '__main__':
    fn = sys.argv[1]; kmax = int(sys.argv[2]); cap = int(sys.argv[3])
    lk = sys.argv[4].split(',') if len(sys.argv) > 4 else ['0', '18', '6', '2']
    kmin = int(sys.argv[5]) if len(sys.argv) > 5 else 1
    p, nB, m, b, gam, W, cup = load(fn)
    S = sum(gam)
    for k in range(kmin, kmax + 1):
        T = p * k
        for L in lk:
            loop = LOOPS[L]; per = len(loop)
            if T % per: continue
            for s in range(per):
                cs = [loop[(s + t) % per] for t in range(T)]
                for A in range(0, S * k // 2 + 1):
                    # A = 0: one start suffices (walking along the lattice reaches every departure phase); A > 0: every phase j0
                    j0s = [0] if A == 0 else list(range(m))
                    lines = [inst_line(b, T, gam, None, A, cap, cs, lat_state(p, m, b, gam, W, T, A, j0)) for j0 in j0s]
                    t0 = time.time()
                    out = run(lines)
                    cnt = {'SUCCESS': 0, 'EXHAUSTED': 0, 'CAP': 0}; mx = 0
                    for j0, o in zip(j0s, out):
                        f = o.split(); cnt[f[1]] += 1; mx = max(mx, int(f[3]))
                        if f[1] != 'EXHAUSTED': print(f"   {f[1]} j0={j0} layers={f[2]} visited={f[3]} path={f[4:]}", flush=True)
                    print(f"{fn} m={m} k={k} T={T} loop={loop} phase={s} A={A} starts={len(j0s)}: {cnt} maxvisited={mx} ({time.time()-t0:.1f}s)", flush=True)
