#!/usr/bin/env python3
"""r12f2: B_1 band-restoration group instance in the INDEPENDENT encoding enc2 of mindep.py (r12a indep_defect.py
lineage: rectangle window [y-R, y+M), M = 171 for one epoch, direct relations, no digit variables, free left port
A[x0] / H, right port C[x1] = cyclic background).  Must be run with --m 1 (one epoch, T = 120).

group: columns [y-R,y) free with (P_(y-3),P_(y-2),P_(y-1)) != (V0,V1,V2); [y,x1) = V band at t=0; NO return constraint
       on [y-R,y); at t = 120 the columns [y,x1) are again the V band.
       --nofor drops the triple constraint (positive control, SAT expected).  --full adds the return of [y-R,y)
       (then = mindep uleft at m=1, consistency check).
"""
import sys, time, argparse
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import mindep as mi

ap = argparse.ArgumentParser()
ap.add_argument('mode', choices=['group'])
ap.add_argument('--V', type=int, default=0)
ap.add_argument('--R', type=int, default=3)
ap.add_argument('--m', type=int, default=1)
ap.add_argument('--nofor', action='store_true')
ap.add_argument('--full', action='store_true')
ap.add_argument('--solver', default='kissat404')
a = ap.parse_args()
assert a.m == 1 and mi.STEPS == 120 and mi.M == 171
from pysat.solvers import Solver
V = mi.rotations()[a.V]; R = a.R; t0 = time.time()
y = 10000; x0 = y - R; x1 = y + mi.M
S = Solver(name=a.solver); cnf = mi.CNF(S)
init = {i: V[(i - y) % 3] for i in range(y, x1)}
X0, XT, Ap, Hp = mi.build(cnf, x0, x1, init, mi.right_port_bits(V))
for i in range(y, x1):
    cnf.add([XT[i][V[(i - y) % 3]]])
if a.full:
    for i in range(x0, y):
        for v in range(19):
            cnf.add([-X0[i][v], XT[i][v]])
if not a.nofor:
    cnf.add([-X0[y - 3 + j][V[j]] for j in range(3)])
print(f'mbres group V={a.V} {V} R={R} M={mi.M} nofor={a.nofor} full={a.full} vars={cnf.nv} clauses={cnf.n} solver={a.solver} '
      f'enc={time.time()-t0:.0f}s', flush=True)
r = S.solve()
if r:
    m = set(l for l in S.get_model() if l > 0)
    print('SAT free columns', [next(v for v in range(19) if X0[i][v] in m) for i in range(x0, y)], flush=True)
print('RESULT', 'B=[sat]' if r else 'B=[]', 'NONEMPTY' if r else 'EMPTY', f'{time.time()-t0:.0f}s', flush=True)
