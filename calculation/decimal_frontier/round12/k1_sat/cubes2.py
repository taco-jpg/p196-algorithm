#!/usr/bin/env python3
"""r12d cubes2.py -- adaptive cube-and-conquer for template returns (fixed centre, wall).
One incremental CaDiCaL instance with the exact tsat encoding.  A cube = values of the first k free symbols in the
order SPLIT (default: outermost centre symbols c0, c1, ...).  Each cube is solved under assumptions with a conflict
budget; an undecided cube is split on the next symbol over its full domain.  The leaves cover the whole symbol space
(every value of every split symbol is enumerated), so "every leaf UNSAT" is exactly "the formula is UNSAT".
usage: cubes2.py ret LAT q0 K L [--lo A --hi B] [--budget N] [--noamo]
       cubes2.py wall LAT S Kb w r core [--h0 H] ..."""
import sys, time, argparse
from tsat import *
from tsrun import indep_sim, core_orbit

ap = argparse.ArgumentParser()
ap.add_argument('kind', choices=['ret', 'wall'])
ap.add_argument('args', nargs='+')
ap.add_argument('--lo', type=int, default=0); ap.add_argument('--hi', type=int, default=19)
ap.add_argument('--budget', type=int, default=30000)
ap.add_argument('--noamo', action='store_true')
ap.add_argument('--h0', type=int, default=None)
ap.add_argument('--q0', type=int, default=None)
ap.add_argument('--solver', default='cadical195')
a = ap.parse_args()
from pysat.solvers import Solver
t0 = time.time()
if a.kind == 'ret':
    latn, q0, K, L = a.args[0], int(a.args[1]), int(a.args[2]), int(a.args[3])
    lat = load_lattice(latn); S = steps_per_block(lat, K)
    c0 = fixed_centre_specs(L); I = Inst(lat, q0, S, K, c0, list(c0))
    h = (L + 1) // 2; order = [f'c{j}' for j in range(h)]
    mids = {f'c{(L - 1) // 2}'} if L % 2 else set()
    tag = f'ret lat={latn} q0={q0} K={K} L={L}'
else:
    latn, S, Kb, w, r, core = a.args[0], int(a.args[1]), int(a.args[2]), int(a.args[3]), int(a.args[4]), int(a.args[5])
    lat = load_lattice(latn); b = lat.b
    q0 = a.q0 if a.q0 is not None else 5
    h0 = a.h0 if a.h0 is not None else 2 * S + 10
    G = sum(lat.g[t % lat.p] for t in range(S)); dh = G - 2 * lat.m * Kb
    orb = core_orbit(core, b, S); assert orb[S] == core
    part = lat.W[0][:r]; J = [('v', f'j{x}') for x in range(w)]
    c0 = part + J + [core] * h0 + J[::-1] + part[::-1]
    cS = part + J + [orb[S]] * (h0 + dh) + J[::-1] + part[::-1]
    I = Inst(lat, q0, S, Kb, c0, cS)
    order = [f'j{x}' for x in range(w)]; mids = set()
    tag = f'wall lat={latn} S={S} Kb={Kb} w={w} r={r} core={core}'
sol = Solver(name=a.solver)
E = I.build(solver=sol, amo_inner=not a.noamo)
print(f'CUBES2 {tag} {I.describe()} vars={E.nv} clauses={E.cl.n} enc={time.time()-t0:.1f}s budget={a.budget} first=[{a.lo},{a.hi})', flush=True)

def dom(name, k):
    d = range(0, I.D, 2) if name in mids else range(I.D)
    if k == 0: d = [v for v in d if a.lo <= v < a.hi]
    return d

stack = [(v,) for v in reversed(list(dom(order[0], 0)))]
leaves = 0; splits = 0; nsat = 0; bydepth = {}; tmax = 0.0
while stack:
    cube = stack.pop()
    assum = [I.free[order[j]][v] for j, v in enumerate(cube)]
    sol.conf_budget(a.budget)
    t1 = time.time(); res = sol.solve_limited(assumptions=assum); dt = time.time() - t1
    tmax = max(tmax, dt)
    if res is None and len(cube) < len(order):
        splits += 1
        nxt = order[len(cube)]
        for v in reversed(list(dom(nxt, len(cube)))): stack.append(cube + (v,))
        continue
    if res is None:   # all symbols fixed and still undecided: solve without budget
        sol.conf_budget(-1); res = sol.solve(assumptions=assum)
    leaves += 1; bydepth[len(cube)] = bydepth.get(len(cube), 0) + 1
    if res:
        nsat += 1
        vals = I.decode_free(sol.get_model()); P0 = I.word0(vals); PS = I.wordS(vals)
        rows, gam = indep_sim(lat, P0, I.S)
        good = rows[-1] == PS and gam == [lat.g[t % lat.p] for t in range(I.S)]
        print(f'cube {cube} SAT {I.realise(I.c0, vals)} indep_exact={good}', flush=True)
        if good: print(f'!!! CANDIDATE {tag} centre={I.realise(I.c0, vals)}', flush=True)
    if leaves % 500 == 0:
        print(f'progress leaves={leaves} splits={splits} stack={len(stack)} {time.time()-t0:.0f}s', flush=True)
print(f'RESULT {"UNSAT" if nsat == 0 else "SAT"} cubes2 {tag} first=[{a.lo},{a.hi}) leaves={leaves} splits={splits} '
      f'bydepth={dict(sorted(bydepth.items()))} sat={nsat} maxcall={tmax:.1f}s total={time.time()-t0:.1f}s', flush=True)
