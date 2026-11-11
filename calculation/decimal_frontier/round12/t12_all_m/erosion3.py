#!/usr/bin/env python3
"""r12f3: multi-epoch version of r12f2's erosion_check.py (consistency check of Theorem A's mechanism on GENUINE
big-integer orbits; not a result).  Template P = B0 W0^q J U^K C rev(.) with q = 30 (the exterior cone forces the
standard clock for t < 12q+40 = 400), K = 400, random J of length 0..30, random palindromic centre C.
y_j = start of the maximal U-band-correct run ending at the fixed column base+600 at t = 120j (j = 0..3); the cones
(junction <= 452, centre <= 362 after 360 steps) keep [base+452, base+1200-362) protected.  B_1 = empty predicts
y_0 < y_1 < y_2 < y_3 (the band start moves right in EVERY epoch).  FAIL if not, or if the clock is not standard."""
import sys, random
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import mdefect as md
WORDS = md.us()
rnd = random.Random(20261108); q = 30; K = 400; T = 360; bad = 0; tot = 0; steps = []
for u in range(30):
    U = WORDS[u]
    for trial in range(6):
        J = [rnd.randrange(19) for _ in range(rnd.randrange(0, 31))]
        h = [rnd.randrange(19) for _ in range(rnd.randrange(1, 4))]; C = h + h[::-1]
        H = list(md.B0) + list(md.W0) * q + J + list(U) * K
        base = 34 + 9 * q + len(J)
        orb = md.orbit(md.realize(H + C + H[::-1]), T, base + 700)
        if not all(orb[t]['g'] == (t % 4 == 0) for t in range(T)):
            bad += 1; print('FAIL clock', u, J, flush=True); continue
        end = base + 600
        def start(t):
            i = end
            while i - 1 >= 0 and orb[t]['P'][i - 1] == U[(i - 1 - base) % 3]:
                i -= 1
            return i
        ys = [start(120 * j) for j in range(4)]
        tot += 1; steps.append(tuple(ys[j + 1] - ys[j] for j in range(3)))
        if not all(ys[j + 1] > ys[j] for j in range(3)):
            bad += 1; print('FAIL', u, U, 'J', J, 'y', ys, flush=True)
    print(f'U{u} {U}: last y-increments {steps[-1]}', flush=True)
flat = [d for s in steps for d in s]
print(f'orbits {tot}, epochs checked {3*tot}, band-start increments per epoch min {min(flat)} max {max(flat)}; '
      f'violations {bad}:', 'PASS' if bad == 0 else 'FAIL')
