#!/usr/bin/env python3
"""r12f2: INDEPENDENT encoding (enc2 style of mindep.py: one-hot X[t][i] in 0..18, carry bits A (low) / C (high), direct
relations, no digit variables, no constant folding) of the clock-rigidity instance W_m(q) of wclock.py.
Window [0,x1), x1 = 34+9q, X[0] = B0 W0^q (own copy of the published rows), A[t][0] = 0, C[t][x1] FREE (inlet),
gamma_t = C[t][0] (= beta_0, the overflow).  gamma=0: X'[i] = (x+a)%10 + (x+b)%10 (a = A[i], b = C[i+1]), all i;
gamma=1: X'[0] = x%10 + 1, X'[i] = (x+a)%10 + (w+b)%10 (w = X[i-1], b = C[i]) for i >= 1.  X[T] = X[0], exactly 30m
overflows, some gamma_t != [t%4==0] (mode rigid) / no deviation clause (mode nodev).  Shares only mindep.CNF."""
import sys, time, argparse
sys.path.insert(0, __file__.rsplit('/', 1)[0])
sys.argv += [] if '--m' in sys.argv else ['--m', '1']
import mindep as mi

B = [10, 4, 6, 6, 7, 12, 9, 16, 16, 13, 0, 2, 10, 17, 7, 0, 18, 6, 5, 18, 4, 18, 14, 9, 14, 8, 12, 17, 10, 4, 6, 4, 0, 5]
W = [5, 18, 4, 8, 1, 15, 4, 0, 5]
ap = argparse.ArgumentParser()
ap.add_argument('mode', choices=['rigid', 'nodev'])
ap.add_argument('--q', type=int, default=14); ap.add_argument('--m', type=int, default=2)
ap.add_argument('--solver', default='kissat404')
a = ap.parse_args()
from pysat.solvers import Solver
T = 120 * a.m; x1 = 34 + 9 * a.q; t0 = time.time()
init = B + W * a.q
S = Solver(name=a.solver); cnf = mi.CNF(S)
X = {i: cnf.onehot(19) for i in range(x1)}
for i in range(x1):
    cnf.add([X[i][init[i]]])
X0 = dict(X); gam = []
for t in range(T):
    A = {i: cnf.var() for i in range(x1 + 1)}
    C = {i: cnf.var() for i in range(x1 + 1)}
    cnf.add([-A[0]])
    g = C[0]; gam.append(g)
    for i in range(x1):
        for x in range(19):
            for b in (0, 1):
                cnf.add([-X[i][x], -cnf.bit(A[i], b), cnf.bit(A[i + 1], 1 if x + b >= 10 else 0)])
                cnf.add([-X[i][x], -cnf.bit(C[i + 1], b), cnf.bit(C[i], 1 if x + b >= 10 else 0)])
    Xn = {i: cnf.onehot(19) for i in range(x1)}
    for i in range(x1):
        for x in range(19):
            for aa in (0, 1):
                for b in (0, 1):
                    cnf.add([g, -X[i][x], -cnf.bit(A[i], aa), -cnf.bit(C[i + 1], b), Xn[i][(x + aa) % 10 + (x + b) % 10]])
    for x in range(19):
        cnf.add([-g, -X[0][x], Xn[0][x % 10 + 1]])
    for i in range(1, x1):
        for x in range(19):
            for aa in (0, 1):
                for wv in range(19):
                    for b in (0, 1):
                        cnf.add([-g, -X[i][x], -cnf.bit(A[i], aa), -X[i - 1][wv], -cnf.bit(C[i], b),
                                 Xn[i][(x + aa) % 10 + (wv + b) % 10]])
    X = Xn
for i in range(x1):
    cnf.add([X[i][init[i]]])
from pysat.card import CardEnc, EncType
cc = CardEnc.equals(lits=gam, bound=30 * a.m, top_id=cnf.nv, encoding=EncType.totalizer)
for c in cc.clauses:
    cnf.add(c)
cnf.nv = max(cnf.nv, cc.nv)
if a.mode == 'rigid':
    cnf.add([(-gam[t] if t % 4 == 0 else gam[t]) for t in range(T)])
print(f'mwclock {a.mode} q={a.q} m={a.m} T={T} window=[0,{x1}) vars={cnf.nv} clauses={cnf.n} solver={a.solver} enc={time.time()-t0:.0f}s', flush=True)
r = S.solve()
if r:
    mm = set(l for l in S.get_model() if l > 0)
    cl = ''.join(str(int(gv in mm)) for gv in gam)
    print('SAT clock', cl, 'deviations', [t for t in range(T) if int(cl[t]) != (t % 4 == 0)], flush=True)
print('RESULT', 'W=[sat]' if r else 'W=[]', 'NONEMPTY' if r else 'EMPTY', f'{time.time()-t0:.0f}s', flush=True)
