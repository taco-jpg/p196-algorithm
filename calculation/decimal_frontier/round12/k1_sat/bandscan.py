#!/usr/bin/env python3
"""r12d bandscan.py -- growing centre with an inner PERIODIC band (family G3; G2 = uniform core is m_U = 1).
Template (folded from the root):  B0 W0^q W0[:r] J U U U ... (up to the middle) + mirror,  J free (w symbols),
U free (m_U symbols, folded band anchored at the seam, periodic up to the middle).  After S steps the exterior
B0 W0^(q+Kb) W0[:r] J is the same and the band is again U-periodic up to the (moved) middle: the band absorbed
dh = G - 2 m Kb new coefficients.  A solution means the band closes on itself at the middle (self-mirror band),
so no gun is needed; the induction over the band length is the LatticeBand pumping lemma (U absorbing) -- a hit is
re-simulated for several band lengths.  UNSAT at a long band (seam cone cannot reach the middle within S steps)
excludes (lattice, S, Kb, r, w, m_U).
usage: bandscan.py LAT S Kb w mU [r_lo r_hi] [--l0 N]"""
import sys, time, argparse
from tsat import *
from tsrun import indep_sim

ap = argparse.ArgumentParser()
ap.add_argument('lat'); ap.add_argument('S', type=int); ap.add_argument('Kb', type=int); ap.add_argument('w', type=int)
ap.add_argument('mU', type=int)
ap.add_argument('r_lo', type=int, nargs='?', default=0); ap.add_argument('r_hi', type=int, nargs='?', default=None)
ap.add_argument('--l0', type=int, default=None, help='initial band length (unfolded)')
ap.add_argument('--q0', type=int, default=5)
ap.add_argument('--solver', default='cadical195')
a = ap.parse_args()
lat = load_lattice(a.lat); S = a.S
r_hi = a.r_hi if a.r_hi is not None else lat.m
G = sum(lat.g[t % lat.p] for t in range(S)); dh = G - 2 * lat.m * a.Kb
assert dh >= 0
l0 = a.l0 if a.l0 is not None else 2 * S + 10 + (2 * S + 10) % 2
t00 = time.time(); nun = nsat = 0
print(f'BANDSCAN lat={a.lat} S={S} Kb={a.Kb} w={a.w} mU={a.mU} r=[{a.r_lo},{r_hi}) l0={l0} dh={dh} q0={a.q0}', flush=True)

def band_spec(l):
    hb = (l + 1) // 2
    half = [('v', f'u{k % a.mU}') for k in range(hb)]
    return half + half[:l // 2][::-1]

for r in range(a.r_lo, r_hi):
    part = lat.W[0][:r]
    J = [('v', f'j{x}') for x in range(a.w)]
    c0 = part + J + band_spec(l0) + J[::-1] + part[::-1]
    cS = part + J + band_spec(l0 + dh) + J[::-1] + part[::-1]
    I = Inst(lat, a.q0, S, a.Kb, c0, cS)
    ok, model, E, tenc, tt, _ = solve_inst(I, a.solver)
    if not ok:
        nun += 1; print(f'RES UNSAT r={r} vars={E.nv} cls={E.cl.n} {tt:.1f}s', flush=True); continue
    nsat += 1
    vals = I.decode_free(model); P0 = I.word0(vals); PS = I.wordS(vals)
    rows, gam = indep_sim(lat, P0, S)
    good = rows[-1] == PS and gam == [lat.g[t % lat.p] for t in range(S)]
    Jv = [vals[f'j{x}'] for x in range(a.w)]; Uv = [vals[f'u{k}'] for k in range(a.mU)]
    print(f'RES SAT r={r} J={Jv} U={Uv} indep_exact={good} {tt:.1f}s', flush=True)
    if good:
        res = []
        for l in (l0 + 1, l0 + 2, l0 + a.mU, l0 + 2 * a.mU, l0 + 4 * a.mU + 1, 3 * l0):
            def realise(spec): return [vals[e[1]] if isinstance(e, tuple) else e for e in spec]
            P0l = I.half0 + realise(part + J + band_spec(l) + J[::-1] + part[::-1]) + I.half0[::-1]
            PSl = I.half1 + realise(part + J + band_spec(l + dh) + J[::-1] + part[::-1]) + I.half1[::-1]
            rl, gl = indep_sim(lat, P0l, S); res.append((l, rl[-1] == PSl))
        print(f'!!! CANDIDATE band lat={a.lat} S={S} Kb={a.Kb} r={r} J={Jv} U={Uv} other_l={res}', flush=True)
print(f'DONE lat={a.lat} S={S} Kb={a.Kb} w={a.w} mU={a.mU} r=[{a.r_lo},{r_hi}) unsat={nun} sat={nsat} {time.time()-t00:.0f}s', flush=True)
