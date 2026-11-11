#!/usr/bin/env python3
"""r12g2 relsat_period.py -- per-period closure test of the bottom relaxation with the repo SAT encoding (relsat.py):
is there a closed walk of length T of R_K (phase orbit oi) through an ACCEPTING state (bottom cell off-lattice)?
UNSAT at depth K0 means: no centre of time period dividing T and depth >= K0 (its bottom K0 cells, frame h - depth, would
be such a walk).  Together with the all-period exclusion of depths < K0 this excludes period-T centres at ANY depth.
SAT models are replayed with klib.window_step (relsat.check_solution).
usage: relsat_period.py LAT K T oi"""
import sys, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../repo/calculation/decimal_frontier/lattice_kinks/edge_relaxation'))
from pysat.solvers import Cadical153
from klib import load
import relsat
name, K, T, oi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
lat = load(name); reps = relsat.orbits(lat); ph0, olen = reps[oi]
t0 = time.time()
E, layers, phs = relsat.build(lat, K, T, ph0)
tb = time.time() - t0
s = Cadical153(bootstrap_with=E.cl); r = s.solve()
print(f'{name} K={K} T={T} orbit={oi} ph0={ph0} (orbit length {olen}): {"SAT" if r else "UNSAT"} vars={E.nv} clauses={len(E.cl)} build {tb:.0f}s total {time.time()-t0:.0f}s', flush=True)
if r:
    ok, W = relsat.check_solution(lat, K, layers, phs, s.get_model())
    base = lat.nB + 5 * lat.m
    offl = sum(1 for t in range(T) if W[t][0] != lat.cell(phs[t][0], base + phs[t][1]))
    nonlat_cells = sum(1 for t in range(T) for i in range(K) if W[t][i] != lat.cell(phs[t][0], base + phs[t][1] + i))
    print(f'  replay with klib.window_step: {"OK" if ok else "FAIL"}; bottom off-lattice at {offl}/{T} steps; off-lattice cells {nonlat_cells}/{T*K}', flush=True)
    for t in range(0, T, max(1, T // 20)):
        tt, jj, pp = phs[t]; lw = [lat.cell(tt, base + jj + i) for i in range(K)]
        print('   t=%3d ' % t + ''.join('*' if a != b else '.' for a, b in zip(W[t], lw)), flush=True)
