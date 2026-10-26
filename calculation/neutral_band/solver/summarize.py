#!/usr/bin/env python3
"""python3 summarize.py results/*.jsonl  -> table per (base,p,G): instances, UNSAT, SAT, UNKNOWN, solver-seconds, max seconds"""
import sys, json, collections
agg = collections.defaultdict(lambda: [0, 0, 0, 0, 0.0, 0.0, 0])
slow = []
for fn in sys.argv[1:]:
    for line in open(fn):
        r = json.loads(line)
        if "key" not in r: continue
        b, p, G = r["key"][:3]; a = agg[(b, p, G)]
        a[0] += r["n"]; a[1] += r["unsat"]; a[2] += r["sat"]; a[3] += r["unknown"]; a[4] += r["t_solver"]; a[5] = max(a[5], r["tmax"]); a[6] += 1
        slow += [(s[1], b, s[0], s[2]) for s in r["slow"]]
print("base  p  G |  units  instances      UNSAT  SAT  UNKNOWN | solver-s  max-s")
T = [0, 0, 0, 0, 0.0]
for (b, p, G), a in sorted(agg.items()):
    print(f"{b:4d} {p:2d} {G:2d} | {a[6]:6d} {a[0]:10d} {a[1]:10d} {a[2]:4d} {a[3]:7d} | {a[4]:9.1f} {a[5]:6.1f}")
    for i in range(4): T[i] += a[[0, 1, 2, 3][i]]
    T[4] += a[4]
print("TOTAL instances %d UNSAT %d SAT %d UNKNOWN %d solver-seconds %.0f" % tuple(T))
slow.sort(reverse=True)
print("slowest:", slow[:5])
