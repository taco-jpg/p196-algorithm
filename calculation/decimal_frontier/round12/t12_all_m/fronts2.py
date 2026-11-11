#!/usr/bin/env python3
"""r12f3: second, independent computation of the U-band cone radii (uses mindep.py's own cyclic_background /
own_fronts, which share no code with mdefect.py / cones_m.py).  Usage: fronts2.py --m M.
Prints, for every rotation of every (9,a,18-a), the junction-side front l and the centre-side front r after
120*j steps for j = 1..M (epoch increments), and the maxima."""
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import mindep as mi
MM = mi.STEPS // 120
out = {}
for idx, V in enumerate(mi.rotations()):
    bg, last = mi.cyclic_background(V)
    assert last == list(V)
    l = 0; r = 0; ls = []; rs = []
    for t in range(mi.STEPS):
        row = bg[t][0]
        l += 1 + (1 if row[l % 3] == 9 else 0)
        r += 1 + (1 if row[(-r - 1) % 3] == 9 else 0) - mi.gamma(t)
        if (t + 1) % 120 == 0:
            ls.append(l); rs.append(r)
    out[idx] = (ls, rs)
    print(f"U{idx} {tuple(V)}: l at epochs {ls}  r at epochs {rs}")
L = [out[i][0][-1] for i in out]; R = [out[i][1][-1] for i in out]
print(f"m={MM}: max junction-side {max(L)} (= 150m+2: {max(L) == 150*MM+2}), max centre-side {max(R)} (= 120m+2: {max(R) == 120*MM+2})")
inc = set()
for i in out:
    ls, rs = out[i]
    for j in range(1, len(ls)):
        inc.add((ls[j] - ls[j-1], rs[j] - rs[j-1]))
print("per-epoch increments after the first epoch (l, r):", sorted(inc))
