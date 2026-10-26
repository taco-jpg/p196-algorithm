import os
#!/usr/bin/env python3
"""Exterior-cycle table: for each base, number of exterior cycles (p<=pmax, L<=Lmax) by minimal period, and smallest L.
usage: base_table.py b_lo b_hi pmax Lmax"""
import sys, time, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ext_transfer import scan
lo, hi, pmax, Lmax = map(int, sys.argv[1:5])
for b in range(lo, hi + 1):
    t0 = time.time()
    res = scan(b, pmax, Lmax, verbose=False)
    # minimal period of each found cycle B0 (dedupe cycles by their set of phases)
    from decouple import G_ext
    seen = set(); bycnt = collections.Counter(); minL = {}
    bad = 0
    for p, s, L, B0, cw, ok in res:
        bad += (not ok)
        cur = list(B0); orb = []
        for t in range(p):
            orb.append(tuple(cur)); cur = G_ext(b, cur)[0]
        key = frozenset(orb)
        if key in seen: continue
        seen.add(key)
        pp = len(set(orb)) if False else None
        # minimal period = number of distinct states in orbit
        per = len(key)
        bycnt[per] += 1
        Lx = max(len(x) for x in key)
        minL[per] = min(minL.get(per, 10**9), Lx)
    print(f"base {b:2d}: distinct exterior cycles {len(seen):3d}  by period {dict(sorted(bycnt.items()))}  "
          f"min max-length by period {dict(sorted(minL.items()))}  unverified {bad}  ({time.time()-t0:.1f}s)", flush=True)
