# validate the CP-SAT register model against direct simulation (hyb.hstep_raw) for random fixed Q0
import random, sys
from hyb import *
from ext import *
from hsat import solve
from sim1 import load_ext, LOOPS
random.seed(5)
b = 10
bad = 0; nsurv = 0; ntot = 0
for name in ('p11', 'p12'):
    cyc = load_ext(name)
    Tp = len(cyc)
    for trial in range(250):
        T = random.randint(2, 7)
        t0 = random.randrange(Tp)
        loop = random.choice(list(LOOPS.values()))
        c0 = random.choice(loop)
        # core values sequence
        cs = []; c = c0
        for t in range(T):
            cs.append(c); k = 1 if c >= b else 0; c = 2 * ((c + k) % b)
        W0 = random.randint(0, 6)
        Q0 = [random.randint(0, 18) for _ in range(W0)]
        # direct raw simulation
        Q = list(Q0); alive = True
        for t in range(T):
            B, gam, e1, u = cyc[(t0 + t) % Tp]
            r = hstep_raw(b, B, Q, cs[t])
            if r is None: alive = False; break
            assert r['gam'] == gam and r['e1'] == e1 and r['c'] == (cs[t+1] if t+1 < T else r['c'])
            Q = r['C']
        gam_l = [cyc[(t0 + t) % Tp][1] for t in range(T)]
        e1_l = [cyc[(t0 + t) % Tp][2] for t in range(T)]
        st, QT = solve(b, gam_l, e1_l, cs, W0, 0, fixQ0=Q0, closure=False, retQT=True, tl=20)
        ntot += 1
        if alive:
            nsurv += 1
            if st not in ('OPTIMAL', 'FEASIBLE') or QT != Q:
                bad += 1; print('BAD(alive)', name, T, t0, Q0, st, QT, Q)
        else:
            if st in ('OPTIMAL', 'FEASIBLE'):
                bad += 1; print('BAD(dead but sat)', name, T, t0, Q0, cs, st)
print('tested', ntot, 'alive', nsurv, 'bad', bad)
