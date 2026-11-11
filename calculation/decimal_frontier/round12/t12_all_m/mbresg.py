#!/usr/bin/env python3
"""r12f3: B_1^+(V,R,g) group instance in the INDEPENDENT encoding enc2 of mindep.py (cf. mbres.py): rectangle window
[y-R, y+M), M = 171, final condition "columns [y+g, y+M) are again the V band at t = 120", free left port, right port =
periodic background carry.  Run with --m 1.  UNSAT(g) => band start advances by >= g+1 columns per epoch (standard clock)."""
import sys, time, argparse
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import mindep as mi

ap = argparse.ArgumentParser()
ap.add_argument('--V', type=int, default=2)
ap.add_argument('--R', type=int, default=3)
ap.add_argument('--g', type=int, default=0)
ap.add_argument('--m', type=int, default=1)
ap.add_argument('--nofor', action='store_true')
ap.add_argument('--solver', default='kissat404')
a = ap.parse_args()
assert a.m == 1 and mi.STEPS == 120 and mi.M == 171
from pysat.solvers import Solver
V = mi.rotations()[a.V]; R = a.R; g = a.g; t0 = time.time()
y = 10000; x0 = y - R; x1 = y + mi.M
S = Solver(name=a.solver); cnf = mi.CNF(S)
init = {i: V[(i - y) % 3] for i in range(y, x1)}
X0, XT, Ap, Hp = mi.build(cnf, x0, x1, init, mi.right_port_bits(V))
for i in range(y + g, x1):
    cnf.add([XT[i][V[(i - y) % 3]]])
if not a.nofor:
    cnf.add([-X0[y - 3 + j][V[j]] for j in range(3)])
print(f'mbresg group V={a.V} {V} R={R} g={g} M={mi.M} nofor={a.nofor} vars={cnf.nv} clauses={cnf.n} solver={a.solver} enc={time.time()-t0:.0f}s', flush=True)
r = S.solve()
if r:
    m = set(l for l in S.get_model() if l > 0)
    print('SAT free columns', [next(v for v in range(19) if X0[i][v] in m) for i in range(x0, y)], flush=True)
print('RESULT', 'Bg=[sat]' if r else 'Bg=[]', 'NONEMPTY' if r else 'EMPTY', f'{time.time()-t0:.0f}s', flush=True)
