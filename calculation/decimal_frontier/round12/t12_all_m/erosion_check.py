#!/usr/bin/env python3
"""r12f2: falsifiable consequence of B_1 = empty on GENUINE big-integer orbits (standard clock).
For the T12 template P = B0 W0^q J U^K C rev(.) (q = 20, K = 200, random J of length 1..30, random palindromic C)
the band start y0 = start of the maximal U-band-correct run ending at column y0+300 at t = 0, and y1 the same at
t = 120 (run ending at the same column).  B_1 group instance UNSAT for the a of U predicts y1 > y_g >= y0, where y_g
in {y0, y0+1, y0+2} is the position at which the group rotation (U2,U5,U6,U9,U12,U15,U18,U21,U26,U27) has phase 0.
Prints per-U statistics of y1 - y0; FAIL if any orbit has y1 <= y_g (or the clock is not standard)."""
import sys, random
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import mdefect as md

GROUP = {0: 2, 2: 5, 4: 6, 6: 9, 8: 12, 10: 15, 12: 18, 14: 21, 16: 26, 18: 27}
WORDS = md.us()
rnd = random.Random(12345); q = 20; K = 200; T = 120; bad = 0; tot = 0
for u in range(30):
    U = WORDS[u]; a_val = 2 * (u // 3)          # us() order: index 3*(a/2) + rotation
    G = WORDS[GROUP[a_val]]
    diffs = []
    for trial in range(20):
        J = [rnd.randrange(19) for _ in range(rnd.randrange(1, 31))]
        h = [rnd.randrange(19) for _ in range(3)]; C = h + h[::-1]
        H = list(md.B0) + list(md.W0) * q + J + list(U) * K
        base = 34 + 9 * q + len(J)               # U phase 0 at base
        orb = md.orbit(md.realize(H + C + H[::-1]), T, base + 400)
        assert all(orb[t]['g'] == (t % 4 == 0) for t in range(T)), 'clock'
        ok = lambda t, i: orb[t]['P'][i] == U[(i - base) % 3]
        end = base + 300
        def start(t):
            i = end
            while i - 1 >= 0 and ok(t, i - 1):
                i -= 1
            return i
        y0, y1 = start(0), start(T)
        # group position: G has phase 0 at columns i with G == rotation of U starting at i
        yg = next(y for y in (y0, y0 + 1, y0 + 2) if tuple(U[(y - base + j) % 3] for j in range(3)) == tuple(G))
        tot += 1
        if y1 <= yg:
            bad += 1; print('FAIL', u, U, 'J', J, 'y0', y0, 'yg', yg, 'y1', y1, flush=True)
        diffs.append(y1 - y0)
    print(f'U{u} {U} group {GROUP[a_val]}: y1-y0 over 20 random J: min {min(diffs)} max {max(diffs)} mean {sum(diffs)/len(diffs):.1f}', flush=True)
print(f'orbits {tot}, violations {bad}:', 'PASS' if bad == 0 else 'FAIL')
