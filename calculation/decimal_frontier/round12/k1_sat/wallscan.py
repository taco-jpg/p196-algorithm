#!/usr/bin/env python3
"""r12d wallscan.py -- growing centres with an absorbing core (families G2 stationary wall, G5 moving wall).
Template (pairword, folded from the root):  B0 W0^q W0[:r] J c^h rev(J) rev(W0[:r]) rev(W0)^q rev(B0),
core c absorbing (c != 9, on a doubling loop), wall J free (w symbols 0..18).
Return after S steps:  B0 W0^(q+Kb) W0[:r] J c(S)^(h + G - 2 m Kb) ...,   G = sum of the clock over S steps.
  Kb = 0  : stationary wall, every overflow goes into the core (core gains G per period);
  0<Kb<.. : moving wall (lattice gains Kb blocks per side, core gains the rest);
  Kb = S/80 (m=20): core length constant = fixed centre of the special form J c^h rev J with an arbitrarily long core.
The wall's influence enters the core at most one column per step (core cells != 9 absorb every carry), so for
h0 >= 2S+10 the two walls cannot interact within S steps and the exterior evolution is the same for every h >= h0
(absorbing-core lemma, PAPER PROOF; AbsorbingBand format).  A certificate must work for all large h, so UNSAT at h0
excludes (lattice, S, Kb, r, core, w); a SAT hit is re-simulated for several h.
usage: wallscan.py LAT S Kb W [r_lo r_hi] [--cores ..] [--q0 Q] [--h0 H]"""
import sys, time, argparse
from tsat import *
from tsrun import indep_sim, core_orbit

QT = {80: 5, 160: 8, 240: 11, 320: 15, 400: 18, 480: 21}            # rec0/rec1 shield thresholds (shield4.log)
QT2 = {192: 4, 384: 6, 576: 9}                                       # rec2

ap = argparse.ArgumentParser()
ap.add_argument('lat'); ap.add_argument('S', type=int); ap.add_argument('Kb', type=int); ap.add_argument('w', type=int)
ap.add_argument('r_lo', type=int, nargs='?', default=0); ap.add_argument('r_hi', type=int, nargs='?', default=None)
ap.add_argument('--cores', default=None)
ap.add_argument('--q0', type=int, default=None)
ap.add_argument('--h0', type=int, default=None)
ap.add_argument('--solver', default='cadical195')
a = ap.parse_args()
lat = load_lattice(a.lat); b = lat.b; S = a.S
if a.q0 is not None: q0 = a.q0
else:
    tab = QT2 if a.lat == 'rec2' else QT
    q0 = min(v for k, v in tab.items() if k >= S)
r_hi = a.r_hi if a.r_hi is not None else lat.m
h0 = a.h0 if a.h0 is not None else 2 * S + 10
G = sum(lat.g[t % lat.p] for t in range(S))
dh = G - 2 * lat.m * a.Kb
assert dh >= 0, 'lattice gains more than the clock allows'
if a.cores: cores = [int(x) for x in a.cores.split(',')]
else: cores = [c for c in range(0, 2 * b - 1) if c != b - 1 and core_orbit(c, b, S)[S] == c]
t0 = time.time(); nun = nsat = 0
print(f'SCAN lat={a.lat} S={S} Kb={a.Kb} w={a.w} r=[{a.r_lo},{r_hi}) cores={cores} q0={q0} h0={h0} core_gain={dh}', flush=True)
for r in range(a.r_lo, r_hi):
    for c in cores:
        orb = core_orbit(c, b, S)
        part = lat.W[0][:r]
        J = [('v', f'j{x}') for x in range(a.w)]
        c0 = part + J + [c] * h0 + J[::-1] + part[::-1]
        cS = part + J + [orb[S]] * (h0 + dh) + J[::-1] + part[::-1]
        I = Inst(lat, q0, S, a.Kb, c0, cS)
        ok, model, E, tenc, tt, _ = solve_inst(I, a.solver)
        if not ok:
            nun += 1
            print(f'RES UNSAT r={r} core={c} vars={E.nv} cls={E.cl.n} {tt:.1f}s', flush=True); continue
        nsat += 1
        vals = I.decode_free(model); P0 = I.word0(vals); PS = I.wordS(vals)
        rows, gam = indep_sim(lat, P0, S)
        good = rows[-1] == PS and gam == [lat.g[t % lat.p] for t in range(S)]
        Jv = [vals[f'j{x}'] for x in range(a.w)]
        print(f'RES SAT r={r} core={c} J={Jv} indep_exact={good} {tt:.1f}s', flush=True)
        if good:
            res = []
            for h in (h0 + 1, h0 + 7, h0 + 40, 3 * h0):
                P0h = I.half0 + part + Jv + [c] * h + Jv[::-1] + part[::-1] + I.half0[::-1]
                PSh = I.half1 + part + Jv + [orb[S]] * (h + dh) + Jv[::-1] + part[::-1] + I.half1[::-1]
                rh, gh = indep_sim(lat, P0h, S); res.append(rh[-1] == PSh)
            print(f'!!! CANDIDATE wall lat={a.lat} S={S} Kb={a.Kb} r={r} core={c} J={Jv} other_h={res}', flush=True)
print(f'DONE lat={a.lat} S={S} Kb={a.Kb} w={a.w} r=[{a.r_lo},{r_hi}) unsat={nun} sat={nsat} {time.time()-t0:.0f}s', flush=True)
