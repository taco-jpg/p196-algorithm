#!/usr/bin/env python3
"""r12f2: separation threshold for the gap cases.  Over Ttot = 120m steps with the clock standard for t < tf and
arbitrary afterwards, max junction-side front lam (left edge of a pure band, any rotation) and max centre-side
front rho (right edge, any rotation): exact DP over (tail word, front phase).  Seam/centre agreement needs
3k >= lam + rho + 2 (FINAL sec. 3.2), i.e. k >= kgap = ceil((lam+rho+2)/3)."""
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import bfree as bf
W = bf.WORDS


def dp(T, tf, side):
    best = 0
    for j0 in range(30):
        cur = {(j0, 0): 0}
        for t in range(T):
            nb = {}
            for (j, ph), v in cur.items():
                gs = ((1 if t % 4 == 0 else 0),) if t < tf else (0, 1)
                for g in gs:
                    if side == 'L':
                        v2 = v + 1 + (W[j][ph % 3] == 9); ph2 = v2 % 3
                    else:
                        v2 = v + 1 + (W[j][(-v - 1) % 3] == 9) - g; ph2 = v2 % 3
                    jj = bf.F1[j] if g else bf.F0[j]
                    k = (jj, ph2)
                    if nb.get(k, -1) < v2:
                        nb[k] = v2
            cur = nb
        best = max(best, max(cur.values()))
    return best


for m, qs in ((1, [7]), (2, [14, 15, 16, 17]), (3, [17, 20, 23, 24, 25, 26, 27])):
    T = 120 * m
    for q in qs:
        tf = min(T, 12 * q + 40) if q < 10 * m - 3 else T
        lam = dp(T, tf, 'L'); rho = dp(T, tf, 'R')
        print(f'm={m} q={q} tf={tf}: lam={lam} rho={rho} -> k >= {-(-(lam + rho + 2) // 3)}', flush=True)
