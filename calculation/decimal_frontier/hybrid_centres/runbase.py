#!/usr/bin/env python3
"""runbase.py -- hybrid CP-SAT scan over (base, stream) controls and decimal.
usage: runbase.py <bases comma> <W0max> <kmax> <tl_per_inst> [outfile]
For every primitive neutral exterior stream of the base, every k<=kmax (k laps), every absorbing loop, every loop phase, every A: W0=0..W0max.
Stops per (stream,k,loop,phase,A) at the first hit."""
import sys, time, json, math
from hsat import solve
from streams_all import collect

def loops(b):
    N = b - 1
    f = {}
    for c in range(2 * b - 1):
        if c == N: continue
        k = 1 if c >= b else 0
        cp = 2 * ((c + k) % b)
        if cp != N: f[c] = cp
    # cycles of the functional graph
    seen = set(); cyc = []
    for c in f:
        path = []; x = c
        while x in f and x not in path and x not in seen:
            path.append(x); x = f[x]
        if x in path:
            i = path.index(x); cy = path[i:]
            m = min(cy); j = cy.index(m); cy = cy[j:] + cy[:j]
            if cy not in cyc: cyc.append(cy)
        seen.update(path)
    return cyc

def main():
    bases = [int(x) for x in sys.argv[1].split(',')]
    W0max = int(sys.argv[2]); kmax = int(sys.argv[3]); tl = float(sys.argv[4])
    out = open(sys.argv[5], 'a') if len(sys.argv) > 5 else None
    S = collect()
    for b in bases:
        lps = loops(b)
        print(f"# base {b} loops {lps}", flush=True)
        for (g, e) in sorted(S.get(b, []), key=lambda x: (len(x[0]), x)):
            p = len(g)
            for k in range(1, kmax + 1):
                for lp in lps:
                    per = len(lp)
                    T0 = p * k
                    T = T0 * per // math.gcd(T0, per)
                    if T > 66: continue
                    gam = [int(g[t % p]) for t in range(T)]; e1 = [int(e[t % p]) for t in range(T)]
                    Sg = sum(gam)
                    for s in range(per):
                        cs = [lp[(s + t) % per] for t in range(T)]
                        for A in range(0, Sg // 2 + 1):
                            for W0 in range(0, W0max + 1):
                                t0 = time.time()
                                st, Q0 = solve(b, gam, e1, cs, W0, A, tl=tl)
                                if st in ('OPTIMAL', 'FEASIBLE'):
                                    line = f"HIT b={b} g={g} e={e} k={k} T={T} loop={lp} phase={s} A={A} W0={W0} Q0={Q0} cs0={cs[0]} ({time.time()-t0:.1f}s)"
                                    print(line, flush=True)
                                    if out: out.write(json.dumps(dict(b=b, g=g, e=e, k=k, T=T, loop=lp, phase=s, A=A, W0=W0, Q0=Q0, cs=cs)) + '\n'); out.flush()
                                    break
                                elif st != 'INFEASIBLE':
                                    print(f"  ?? {st} b={b} g={g} e={e} k={k} loop={lp} s={s} A={A} W0={W0} ({time.time()-t0:.1f}s)", flush=True)
            print(f"# done b={b} stream {g}/{e}", flush=True)
if __name__ == '__main__':
    main()
