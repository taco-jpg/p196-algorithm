import os
#!/usr/bin/env python3
"""Count schedules (upper bound: without the base-10 covered-box filter) for a planned sweep.
usage: count_instances.py p_lo p_hi G nmax mmax"""
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sweep
plo, phi, G, NMAX, MMAX = map(int, sys.argv[1:6])
rate = 3.4e-3
tot_all = 0
for p in range(plo, phi + 1):
    if G > p: continue
    tot = 0
    for (b, pp, GG, gam, u) in sweep.units(10, [p], [G]):
        for v in sweep.wcomp(G // 2, p):
            sh = tuple(zip(gam, u, v))
            if not sweep.canonical_primitive(sh): continue
            pn = [0]; pm = [0]
            for (g, uu, vv) in sh[:-1]: pn.append(pn[-1] + g - uu); pm.append(pm[-1] + g - 2 * vv)
            wn = NMAX - max(0 - x for x in pn) - max(x for x in pn) + 0
            wn = (NMAX - max(pn)) - max(-x for x in pn) + 1
            wm = (MMAX - max(pm)) - max(-x for x in pm) + 1
            if wn > 0 and wm > 0: tot += wn * wm
    tot_all += tot
    print(f"G={G} p={p}: <= {tot} schedules", flush=True)
print(f"TOTAL <= {tot_all} schedules; at {rate*1e3:.1f} ms each: {tot_all*rate/3600:.1f} core-hours = {tot_all*rate/3600/30:.2f} h on 30 cores")
