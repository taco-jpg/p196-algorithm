#!/usr/bin/env python3
"""r12f2: validation of the FREE-CLOCK encoding (bfree.build) on GENUINE big-integer orbits with a NON-standard clock.
Number: pairword P = X J w^K C rev(.) with a RANDOM root block X (so the overflow clock is not (1000)^*), random J, C.
Window [y-R, y+M) at the start y of the w band.  Checks:
 (i)  genuine tail rows (read far right in the band) follow Z_(t+1) = F_(gamma_t)(Z_t) and the genuine beta at y+M
      equals the periodic beta of the tail row (right port of the encoding) at every t;
 (ii) genuine init + genuine left port + genuine clock + genuine final row  -> SAT;
 (iii) as (ii) with one final value changed -> UNSAT;
 (iv) clock left FREE, genuine init + port + final -> SAT (the genuine clock is one solution);
 (v)  number of steps whose gamma differs from [t%4==0] (must be > 0 for the test to exercise free clocks)."""
import sys, random, argparse
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import mdefect as md
import bfree as bf
from pysat.solvers import Solver

ap = argparse.ArgumentParser()
ap.add_argument('--U', type=int, default=2); ap.add_argument('--r', type=int, default=3)
ap.add_argument('--T', type=int, default=60); ap.add_argument('--seed', type=int, default=1)
ap.add_argument('--solver', default='kissat404')
a = ap.parse_args()
rnd = random.Random(a.seed); w = bf.WORDS[a.U]; R = a.r; T = a.T
lf = max(bf.max_front(T, j) for j in range(30)); M = 3 * ((lf + 21 + 2) // 3)
X = [rnd.randrange(1, 19)] + [rnd.randrange(19) for _ in range(39)]
J = [rnd.randrange(19) for _ in range(7)]
K = (4 * T + 3 * M) // 3 + 40
h = [rnd.randrange(19) for _ in range(5)]; C = h + h[::-1]
H = X + J + list(w) * K
y = len(X) + len(J); x0 = y - R; x1 = y + M
orb = md.orbit(md.realize(H + C + H[::-1]), T, x1 + 80)
clock = [orb[t]['g'] for t in range(T)]
nonstd = sum(clock[t] != (t % 4 == 0) for t in range(T))


def tailword(t):
    seg = orb[t]['P'][x1 + 60: x1 + 63]
    js = [j for j in range(30) if all(bf.WORDS[j][(i - y) % 3] == orb[t]['P'][i] for i in range(x1 + 60, x1 + 63))]
    assert len(js) == 1, (t, seg)
    return js[0]


Zs = [tailword(t) for t in range(T + 1)]
out = {'U': a.U, 'w': w, 'T': T, 'M': M, 'seed': a.seed, 'nonstandard_clock_steps': nonstd, 'clock': ''.join(map(str, clock))}
out['i_tail_follows_F'] = all(Zs[t + 1] == (bf.F1 if clock[t] else bf.F0)[Zs[t]] for t in range(T))
out['i_right_port_is_tail_beta'] = all(orb[t]['c'][orb[t]['L'] - x1] == bf.BE[Zs[t]][(x1 - y) % 3] for t in range(T))
init = {i: orb[0]['P'][i] for i in range(x0, x1)}
port = ([orb[t]['c'][x0] for t in range(T)], [orb[t]['e'][orb[t]['L'] - x0] for t in range(T)])
fin = {i: orb[T]['P'][i] for i in range(x0, x1)}
for test in ('ii', 'iii', 'iv'):
    S = Solver(name=a.solver); E = md.Enc(S)
    P0, PT, gam, Z = bf.build(E, w, R, T, M, y, False, init=init, port=port, clock=(clock if test != 'iv' else None))
    j = rnd.randrange(x0, x1); v = (fin[j] + 1 + rnd.randrange(17)) % 19
    for i in range(x0, x1):
        md.equal(E, PT[i], v if (test == 'iii' and i == j) else fin[i])
    out[test] = S.solve()
    if test == 'iv' and out[test]:
        m = set(x for x in S.get_model() if x > 0)
        out['iv_model_clock_equals_genuine'] = ''.join(str(int(g in m)) for g in gam) == out['clock']
    S.delete()
out['PASS'] = (nonstd > 0 and out['i_tail_follows_F'] and out['i_right_port_is_tail_beta'] and out['ii'] and not out['iii'] and out['iv'])
print(out, flush=True)
