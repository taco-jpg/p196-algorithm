#!/usr/bin/env python3
"""r12f3 (exploratory): structure of the region behind the band-erosion front in GENUINE T12 orbits.
Template q = 60 (standard clock forced for t < 760), K = 500, random J; 720 steps.  y_j = band start at t = 120j
(run ending at column base+1000).  Prints the increments y_(j+1)-y_j and, for epochs j = 3,4,5: the fraction of
columns i in [base+40, y_j) with P_(120j)(i) = P_(120(j+1))(i+60) (travelling-wave test, speed 60 per epoch), and the
best spatial period p <= 60 of the wake row at t = 720 on [base+40, y_6-20)."""
import sys, random
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import mdefect as md
WORDS = md.us(); rnd = random.Random(5); q = 60; K = 500; T = 720
for u in [0, 5, 13, 22, 27]:
    U = WORDS[u]
    J = [rnd.randrange(19) for _ in range(rnd.randrange(1, 15))]
    h = [rnd.randrange(19) for _ in range(3)]; C = h + h[::-1]
    H = list(md.B0) + list(md.W0) * q + J + list(U) * K
    base = 34 + 9 * q + len(J)
    orb = md.orbit(md.realize(H + C + H[::-1]), T, base + 1100)
    assert all(orb[t]['g'] == (t % 4 == 0) for t in range(T))
    end = base + 1000
    def start(t):
        i = end
        while i - 1 >= 0 and orb[t]['P'][i - 1] == U[(i - 1 - base) % 3]:
            i -= 1
        return i
    ys = [start(120 * j) for j in range(7)]
    inc = [ys[j + 1] - ys[j] for j in range(6)]
    tw = []
    for j in (3, 4, 5):
        lo = base + 40; hi = ys[j] - 5
        m = sum(orb[120 * j]['P'][i] == orb[120 * (j + 1)]['P'][i + 60] for i in range(lo, hi))
        tw.append(round(m / max(1, hi - lo), 3))
    row = orb[720]['P']; lo = base + 40; hi = ys[6] - 20
    best = max(((sum(row[i] == row[i + p] for i in range(lo, hi - p)) / max(1, hi - p - lo), p) for p in range(1, 61)))
    print(f"U{u} {U} |J|={len(J)} base={base}: band-start increments per epoch {inc}; wake width at t=720: {ys[6]-base}; "
          f"TW match(60/epoch) j=3,4,5: {tw}; best spatial period of wake (t=720): p={best[1]} match {best[0]:.3f}; "
          f"wake sample {row[base+40:base+64]}", flush=True)
