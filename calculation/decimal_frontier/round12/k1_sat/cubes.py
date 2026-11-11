#!/usr/bin/env python3
"""r12d cubes.py -- fixed-centre exact return by cube-and-conquer on the OUTERMOST centre symbols.
One incremental CaDiCaL instance (the exact tsat encoding, built once); every cube = an assignment of the first
`depth` folded centre symbols c0..c(depth-1) (outermost = adjacent to the lattice), solved under assumptions;
learned clauses are kept between cubes.  The union of the cubes is the whole centre space, so "all cubes UNSAT"
is exactly "the instance is UNSAT".  A SAT cube is decoded and re-checked by independent simulation.
usage: cubes.py LAT q0 K L depth [c0_lo c0_hi] [--noamo]"""
import sys, time, itertools, argparse
from tsat import *
from tsrun import indep_sim

ap = argparse.ArgumentParser()
ap.add_argument('lat'); ap.add_argument('q0', type=int); ap.add_argument('K', type=int); ap.add_argument('L', type=int)
ap.add_argument('depth', type=int)
ap.add_argument('lo', type=int, nargs='?', default=0); ap.add_argument('hi', type=int, nargs='?', default=19)
ap.add_argument('--noamo', action='store_true')
ap.add_argument('--solver', default='cadical195')
a = ap.parse_args()
from pysat.solvers import Solver
lat = load_lattice(a.lat); S = steps_per_block(lat, a.K)
c0 = fixed_centre_specs(a.L)
I = Inst(lat, a.q0, S, a.K, c0, list(c0))
t0 = time.time()
sol = Solver(name=a.solver)
E = I.build(solver=sol, amo_inner=not a.noamo)
h = (a.L + 1) // 2
depth = min(a.depth, h)
mid = (a.L - 1) // 2 if a.L % 2 else None
def dom(j):
    return range(0, 19, 2) if (mid is not None and j == mid) else range(19)
print(f'CUBES {I.describe()} depth={depth} c0 in [{a.lo},{a.hi}) vars={E.nv} clauses={E.cl.n} enc={time.time()-t0:.1f}s', flush=True)
nun = nsat = 0; tmax = 0.0
doms = [range(a.lo, a.hi)] + [dom(j) for j in range(1, depth)]
if depth >= 1 and mid == 0: doms[0] = [v for v in range(a.lo, a.hi) if v % 2 == 0]
for cube in itertools.product(*doms):
    assum = [I.free[f'c{j}'][v] for j, v in enumerate(cube)]
    t1 = time.time(); r = sol.solve(assumptions=assum); dt = time.time() - t1; tmax = max(tmax, dt)
    if not r:
        nun += 1
        if dt > 30: print(f'cube {cube} UNSAT {dt:.1f}s', flush=True)
        continue
    nsat += 1
    vals = I.decode_free(sol.get_model()); P0 = I.word0(vals); PS = I.wordS(vals)
    rows, gam = indep_sim(lat, P0, S)
    good = rows[-1] == PS and gam == [lat.g[t % lat.p] for t in range(S)]
    print(f'cube {cube} SAT C={I.realise(c0, vals)} indep_exact={good} {dt:.1f}s', flush=True)
    if good: print(f'!!! CANDIDATE fixed centre lat={a.lat} q0={a.q0} K={a.K} C={I.realise(c0, vals)}', flush=True)
print(f'RESULT {"UNSAT" if nsat == 0 else "SAT"} cubes lat={a.lat} q0={a.q0} K={a.K} L={a.L} depth={depth} c0=[{a.lo},{a.hi}) '
      f'unsat_cubes={nun} sat_cubes={nsat} max_cube={tmax:.1f}s total={time.time()-t0:.1f}s', flush=True)
