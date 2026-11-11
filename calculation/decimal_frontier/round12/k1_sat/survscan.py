#!/usr/bin/env python3
"""r12d survscan.py -- confined kinks of ANY period (KINK.md formulation, exact encoding of tsat.py).
A kink whose defect always lies in the top w folded columns (the moving frame [M_t - w, M_t), M_t = ceil(n_t/2))
survives forever.  Survival for H steps from time phase 0: the lattice is exact on every column below M_t - w at
every t <= H.  The relative phase of frame and lattice at times = 0 mod 8 is determined by o = n mod 4 (frame moves
2 columns per 8 steps), so 4 classes; one representative (r, |C|) per class.  If every class dies (UNSAT at some H),
no kink of confined width <= w exists, for any period.  Lifetime(o) = (first UNSAT H) - 1.
usage: survscan.py LAT W [Hstart] [--classes 0,1,2,3] [--hmax H]"""
import sys, time, argparse
from tsat import *
from tsrun import indep_sim

ap = argparse.ArgumentParser()
ap.add_argument('lat'); ap.add_argument('w', type=int)
ap.add_argument('Hstart', type=int, nargs='?', default=None)
ap.add_argument('--classes', default='0,1,2,3')
ap.add_argument('--hmax', type=int, default=200)
ap.add_argument('--solver', default='cadical195')
a = ap.parse_args()
lat = load_lattice(a.lat); w = a.w
Hs = a.Hstart if a.Hstart is not None else max(2 * w, 4 * w - 12)
t00 = time.time()
for o in map(int, a.classes.split(',')):
    rep = None
    for r in range(lat.m):
        for Lc in (2 * w, 2 * w - 1):
            H0 = lat.nB + lat.m * 5
            n = 2 * (H0 + r) + Lc
            if n % 4 == o: rep = (r, Lc); break
        if rep: break
    r, Lc = rep
    part = lat.W[0][:r]
    C = fixed_centre_specs(Lc)
    c0 = part + C + part[::-1]
    H = Hs; last_sat = None
    while H <= a.hmax:
        q0 = 5 if H <= 80 else (8 if H <= 160 else 11)
        if a.lat == 'rec2': q0 = 4 if H <= 192 else 6
        G = sum(lat.g[t % lat.p] for t in range(H))
        I = Inst(lat, q0, H, 0, c0, [None] * (len(c0) + G))
        ok, model, E, tenc, tt, _ = solve_inst(I, a.solver, prefix_k=0, confine_w=w)
        if ok:
            vals = I.decode_free(model); P0 = I.word0(vals)
            rows, gam = indep_sim(lat, P0, H)
            # independent check of the confinement on the simulated orbit
            okc = all(fold(rows[t])[i] == lat.cell(t, i) for t in range(H + 1) for i in range((len(rows[t]) + 1) // 2 - w))
            print(f'SURV lat={a.lat} w={w} o={o} r={r} Lc={Lc} H={H} SAT {tt:.1f}s indep_confined={okc} C={I.realise(C, vals)}', flush=True)
            last_sat = H
            if not okc: print('!!! MISMATCH between SAT model and independent simulation', flush=True); break
            H += 1
        else:
            print(f'SURV lat={a.lat} w={w} o={o} r={r} Lc={Lc} H={H} UNSAT {tt:.1f}s', flush=True)
            if last_sat is None and H > 2 * w:   # need a SAT below to know the exact lifetime: step down
                H -= 4; continue
            break
    print(f'LIFETIME lat={a.lat} w={w} o={o} lifetime={H - 1 if last_sat is not None else "<" + str(H)} (first UNSAT H={H})', flush=True)
print(f'DONE lat={a.lat} w={w} {time.time()-t00:.0f}s', flush=True)
