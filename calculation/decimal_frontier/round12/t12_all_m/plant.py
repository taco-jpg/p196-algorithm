#!/usr/bin/env python3
"""r12f planted positive control of the m-epoch seam encoding (mdefect.build_seam).
(a) solve the m=1 instance D_R^(1)(V) with the defect letter fixed to v (known SAT, r12a D_1 tables) and read the
    model's free columns and free-port values (alpha bits, overflow-step digits);
(b) m-epoch instance (T=120m) with the same letter/free columns and the port fixed to the m-fold repetition:
    must be SAT (the window is back to its start at t=120 and the right side is 120-periodic);
(c) as (b) with one port value of the LAST epoch changed: informational (deterministic window, SAT iff it still returns).
"""
import sys, time, argparse, random
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import mdefect as md
from pysat.solvers import Solver

ap = argparse.ArgumentParser()
ap.add_argument('--U', type=int, default=5); ap.add_argument('--r', type=int, default=1)
ap.add_argument('--v', type=int, default=6); ap.add_argument('--m', type=int, default=3)
ap.add_argument('--solver', default='kissat404'); ap.add_argument('--seed', type=int, default=1)
a = ap.parse_args()
V = md.us()[a.U]; R = a.r; y = 3000; t0 = time.time()


def inst(T, fixcols=None, port=None):
    S = Solver(name=a.solver); E = md.Enc(S)
    P0, PT, ports, (x0, b, l, *_) = md.build_seam(E, V, R, T, y=y)
    for i in range(x0, b[T]):
        md.equal(E, PT[i], P0[i] if i < b[0] else V[(i - y) % 3])
    E.add([P0[y - 1][a.v]])
    if fixcols:
        for i, c in zip(range(x0, y), fixcols):
            E.add([P0[i][c]])
    if port:
        al, hl = port
        for t in range(T):
            E.add([md.lit(ports[t]['al'], al[t])])
            if 'hl' in ports[t]:
                E.add([ports[t]['hl'][hl[t]]])
    return S, E, P0, ports, x0


S, E, P0, ports, x0 = inst(120)
r = S.solve(); print('(a) m=1 instance with letter', a.v, 'SAT' if r else 'UNSAT', f'{time.time()-t0:.0f}s', flush=True)
assert r, 'expected SAT (D_R^(1)(V) contains v)'
mm = set(x for x in S.get_model() if x > 0)
cols = [md.val(mm, P0[i]) for i in range(x0, y)]
al = [int(ports[t]['al'][0] in mm) for t in range(120)]
hl = {t: md.val(mm, ports[t]['hl']) for t in range(120) if 'hl' in ports[t]}
S.delete()
print('free columns', cols, 'port alpha', ''.join(map(str, al)), 'hl', [hl[t] for t in sorted(hl)], flush=True)
T = 120 * a.m
alm = [al[t % 120] for t in range(T)]; hlm = {t: hl[t % 120] for t in range(T) if t % 4 == 0}
S, E, P0, ports, x0 = inst(T, cols, (alm, hlm))
r = S.solve(); print(f'(b) m={a.m} instance, port repeated {a.m}x:', 'SAT' if r else 'UNSAT', f'{time.time()-t0:.0f}s', flush=True)
S.delete()
rnd = random.Random(a.seed); tt = T - 120 + rnd.randrange(120)
alc = list(alm); alc[tt] ^= 1
S, E, P0, ports, x0 = inst(T, cols, (alc, hlm))
r2 = S.solve(); print(f'(c) one alpha bit changed at t={tt}:', 'SAT' if r2 else 'UNSAT', '(informational)', f'{time.time()-t0:.0f}s', flush=True)
print('PASS' if r else 'FAIL', flush=True)
