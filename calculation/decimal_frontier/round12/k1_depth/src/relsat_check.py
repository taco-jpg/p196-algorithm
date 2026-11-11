#!/usr/bin/env python3
"""r12g relsat_check.py -- independent cross-check of a relaxation cyclic set against the repo's SAT encoding relsat.py:
solve R_K for a fixed period T in phase orbit oi (repo code, CaDiCaL), replay the model with klib.window_step (repo code), and
test that EVERY state of the SAT cycle lies in the kink6/kink7 cyclic-set file (it must: a T-cycle of R_K is a cycle).
usage: relsat_check.py LAT K T oi CYCFILE"""
import sys, os, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../repo/calculation/decimal_frontier/lattice_kinks/edge_relaxation'))
from pysat.solvers import Cadical153
from klib import load
import relsat

name, K, T, oi, cf = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
lat = load(name); base = lat.nB + 5 * lat.m
reps = relsat.orbits(lat); ph0, olen = reps[oi]
t0 = time.time()
E, layers, phs = relsat.build(lat, K, T, ph0)
s = Cadical153(bootstrap_with=E.cl); r = s.solve()
print(f'{name} K={K} T={T} orbit={oi} ph0={ph0}: {"SAT" if r else "UNSAT"} vars={E.nv} clauses={len(E.cl)} {time.time()-t0:.0f}s', flush=True)
if not r: sys.exit(0)
ok, W = relsat.check_solution(lat, K, layers, phs, s.get_model())
offl = sum(1 for t in range(T) if W[t][0] != lat.cell(phs[t][0], base + phs[t][1]))
print(f'  replay with klib.window_step: {"OK" if ok else "FAIL"}; bottom off-lattice at {offl}/{T} steps', flush=True)
a = np.fromfile(cf, dtype=np.uint64).reshape(-1, 2)
lo, hi = a[:, 0], a[:, 1]
PS = 100 if K <= 20 else 118
def member(key):
    h = np.uint64(key >> 64); l = np.uint64(key & ((1 << 64) - 1))
    i0 = np.searchsorted(hi, h, 'left'); i1 = np.searchsorted(hi, h, 'right')
    j = i0 + np.searchsorted(lo[i0:i1], l, 'left')
    return j < i1 and lo[j] == l
inside = 0
for t in range(T):
    tt, jj, pp = phs[t]
    key = (((tt * lat.m + jj) * 2 + pp) << PS) | sum(v << (5 * i) for i, v in enumerate(W[t]))
    inside += member(key)
print(f'  states of the SAT cycle inside {os.path.basename(cf)}: {inside}/{T}', flush=True)
