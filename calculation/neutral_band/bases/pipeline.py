#!/usr/bin/env python3
"""Two-stage search for neutral one-band cycles in base b:
   stage 1 (exterior): transfer-graph BFS over carry bit-words -> all exterior cycles (p<=pmax, L<=Lmax); group by (s,E).
   stage 2 (interior): for each distinct (s,E) CP-SAT solves the padded-register interior for k=1..kmax exterior periods and
                       both parities of the register width W0<=W0max (wide register covers all narrower centers).
   Every hit is rebuilt as (B0,C0) and confirmed with the exact mirror (run -> cycle, cycleOK).
usage: pipeline.py b pmax Lmax kmax W0max tl_per_instance [total_time_limit]"""
import sys, time, itertools, json
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from ext_transfer import exterior_cycles, to_B0
from decouple import G_ext
from interior_cp import solve_interior
from nb_mirror import run, is_cert, cycleOK, gam as GAM


def exteriors(b, pmax, Lmax):
    out = {}
    for p in range(1, pmax + 1):
        for s in itertools.product((0, 1), repeat=p):
            if not any(s) or s != min(s[i:] + s[:i] for i in range(p)): continue
            for L, items in exterior_cycles(b, p, s, Lmax).items():
                for pth, cw in items:
                    B0 = to_B0(b, pth)
                    cur = list(B0); orb = []
                    for t in range(p): orb.append(tuple(cur)); cur = G_ext(b, cur)[0]
                    if len(set(orb)) != p: continue           # keep minimal period only
                    out.setdefault((s, tuple(cw)), []).append(B0)
    return out


def main():
    b, pmax, Lmax, kmax, W0max = map(int, sys.argv[1:6]); tl = float(sys.argv[6])
    total = float(sys.argv[7]) if len(sys.argv) > 7 else 1e9
    t0 = time.time()
    ex = exteriors(b, pmax, Lmax)
    print(f"base {b}: {sum(len(v) for v in ex.values())} exterior cycles, {len(ex)} distinct (s,E) words ({time.time()-t0:.1f}s)", flush=True)
    found = []
    for (s, E), Bs in sorted(ex.items(), key=lambda kv: (len(kv[0][0]), kv[0])):
        for k in range(1, kmax + 1):
            res = {}
            for par in (0, 1):
                W0 = W0max - ((W0max - par) % 2)
                if time.time() - t0 > total: print("  total time limit"); return
                st, C0 = solve_interior(b, list(s), list(E), k, W0, tl)
                res[par] = st
                if C0 is not None:
                    # try all exterior B0 sharing (s,E)
                    for B0 in Bs:
                        r = run(b, list(B0), list(C0), maxsteps=5000, maxlen=3000)
                        if r[0] == 'cycle':
                            es = r[1]
                            ok = cycleOK(b, es, es[0][0], es[0][1])
                            print(f"  *** CYCLE base {b} s={''.join(map(str,s))} E={''.join(map(str,E))} k={k} W0={W0}: "
                                  f"{len(es)} edges, sumGam {sum(GAM(b, e[0], e[1]) for e in es)}, cycleOK={ok}, |B0|={len(B0)}, |C0|={len(C0)}", flush=True)
                            found.append((s, E, k, B0, C0, ok)); break
            print(f"  s={''.join(map(str,s))} E={''.join(map(str,E))} k={k}: interior status even/odd {res}", flush=True)
    print(f"base {b}: full cycles found {len(found)} ({time.time()-t0:.1f}s)")
    return found

if __name__ == '__main__':
    main()
