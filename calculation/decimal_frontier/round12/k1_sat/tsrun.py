#!/usr/bin/env python3
"""r12d tsrun.py -- driver for tsat.py.
modes:
  ret      fixed-centre exact return T^S(P(q0,C)) = P(q0+K,C), S = steps for K blocks, |C| = L free
  lat      same, final centre free (same length): any centre of length L that restores the lattice
  prefix   only the first k folded columns of the final word must match (validation against cen2 maxprefix)
  sim      C fixed (random or --idx), no final constraint; model compared with an independent pairword
           simulation at EVERY step and EVERY window cell (encoding validation)
  planted  target = exact image of a random C (positive control); C free
  wall     stationary wall + absorbing core:  B0 W0^q W0[:r] J c^h0 rev(J) ...  returns after T steps with the
           same exterior (lattice does not grow) and core c(T)^(h0 + T/2); J (width w) free
  grow     T^S(P(q0,C)) = P(q0+K-k, X C rev X), |X| = k*m, X and C free (centre gains a block, lattice less)
Every SAT answer is re-checked by an independent pairword simulation (klib.pairword_step for base 10)."""
import sys, os, time, argparse, random
from tsat import *


def centre_of_idx(idx, L):
    h, odd = L // 2, L % 2; r = idx; mid = None
    if odd: mid = 2 * (r % 10); r //= 10
    half = []
    for _ in range(h): half.append(r % 19); r //= 19
    half = half[::-1]
    return half + ([mid] if odd else []) + half[::-1]


def indep_sim(lat, P, S):
    """second implementation: klib.pairword_step for base 10, else pairword_step_b"""
    if lat.b == 10:
        from klib import pairword_step
        rows = [P]; gam = []
        for t in range(S):
            P, gg = pairword_step(P); rows.append(P); gam.append(gg)
        return rows, gam
    return simulate(lat, P, S)


def core_orbit(c, b, T):
    out = [c]
    for t in range(T):
        k = 1 if c >= b else 0; c = 2 * ((c + k) % b); out.append(c)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['ret', 'lat', 'prefix', 'sim', 'planted', 'wall', 'grow', 'info'])
    ap.add_argument('--lat', default='rec1')
    ap.add_argument('--q0', type=int, default=5)
    ap.add_argument('--K', type=int, default=1)
    ap.add_argument('--L', type=int, default=17)
    ap.add_argument('--k', type=int, default=None)
    ap.add_argument('--idx', type=int, default=None)
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--T', type=int, default=16, help='wall: period')
    ap.add_argument('--r', type=int, default=0, help='wall: partial lattice block length before J')
    ap.add_argument('--w', type=int, default=6, help='wall: width of J')
    ap.add_argument('--core', type=int, default=0, help='wall: core value c(0)')
    ap.add_argument('--h0', type=int, default=8, help='wall: initial core length (full)')
    ap.add_argument('--kg', type=int, default=1, help='grow: blocks moved from lattice to centre')
    ap.add_argument('--solver', default='cadical195')
    ap.add_argument('--margin', type=int, default=2)
    ap.add_argument('--nounits', action='store_true')
    ap.add_argument('--noamo', action='store_true', help='drop implied AMO clauses of inner rows')
    ap.add_argument('--fix', default=None, help='cube: fix free symbols, e.g. c0=5,c1=3')
    ap.add_argument('--phase', action='store_true', help='set solver decision phases to the lattice values')
    ap.add_argument('--simfix', action='store_true', help='wall/grow: fix free symbols at random, compare with simulation')
    a = ap.parse_args()
    lat = load_lattice(a.lat); b = lat.b
    t0 = time.time()
    fixvals = None; planted = None; prefix_k = a.k
    if a.mode in ('ret', 'lat', 'prefix', 'sim', 'planted', 'info'):
        S = steps_per_block(lat, a.K)
        c0 = fixed_centre_specs(a.L)
        cS = list(c0) if a.mode != 'lat' else [None] * a.L
        I = Inst(lat, a.q0, S, a.K, c0, cS, a.margin)
        if a.mode in ('sim', 'planted'):
            rng = random.Random(a.seed)
            if b == 10:
                if a.idx is None: a.idx = rng.randrange(19 ** (a.L // 2) * (10 if a.L % 2 else 1))
                C = centre_of_idx(a.idx, a.L)
            else:
                C = [rng.randrange(2 * b - 1) for _ in range(a.L)]
                C = C[:(a.L + 1) // 2] + C[:a.L // 2][::-1]
                if a.L % 2: C[a.L // 2] = 2 * rng.randrange(b)
            vals = {f'c{j}': C[j] for j in range((a.L + 1) // 2)}
            if a.mode == 'sim':
                fixvals = vals; prefix_k = 0
            else:
                rows, _ = indep_sim(lat, I.word0(vals), S); planted = fold(rows[-1])
                print('planted from C', C, flush=True)
    elif a.mode == 'grow':
        S = steps_per_block(lat, a.K)
        c0 = fixed_centre_specs(a.L)
        xl = a.kg * lat.m
        X = [('v', f'x{j}') for j in range(xl)]
        cS = X + c0 + X[::-1]
        I = Inst(lat, a.q0, S, a.K - a.kg, c0, cS, a.margin)
    elif a.mode == 'wall':
        T = a.T; orb = core_orbit(a.core, b, T)
        assert orb[T] == a.core, f'core loop period does not divide T: {orb}'
        part = lat.W[0][:a.r]
        J = [('v', f'j{x}') for x in range(a.w)]
        c0 = part + J + [a.core] * a.h0 + J[::-1] + part[::-1]
        cS = part + J + [orb[T]] * (a.h0 + sum(lat.g[t % lat.p] for t in range(T))) + J[::-1] + part[::-1]
        I = Inst(lat, a.q0, T, 0, c0, cS, a.margin)
        S = T
    if a.simfix and a.mode in ('wall', 'grow'):
        rng = random.Random(a.seed)
        names = sorted(set(e[1] for e in I.c0 + I.cS if isinstance(e, tuple)))
        fixvals = {nm: rng.randrange(2 * b - 1) for nm in names}
        for e_i, e in enumerate(I.c0):   # odd midpoint must be even
            if isinstance(e, tuple) and len(I.c0) % 2 and e_i == len(I.c0) // 2: fixvals[e[1]] &= ~1
        prefix_k = 0
    if a.fix:
        fixvals = dict(fixvals or {})
        for kv in a.fix.split(','):
            k, v = kv.split('='); fixvals[k] = int(v)
    print('INST', a.mode, I.describe(), 'fix=' + str(a.fix), flush=True)
    if a.mode == 'info': return
    r, model, E, tenc, tt, stats = solve_inst(I, a.solver, prefix_k=prefix_k, units=not a.nounits,
                                              fixvals=fixvals, planted=planted, amo_inner=not a.noamo,
                                              phase_lattice=a.phase)
    tag = (f'mode={a.mode} fix={a.fix} lat={a.lat} q0={a.q0} K={a.K} L={a.L} k={a.k} T={a.T if a.mode=="wall" else S} '
           f'r={a.r} w={a.w} core={a.core} kg={a.kg} solver={a.solver}')
    print(f'ENC vars={E.nv} clauses={E.cl.n} enc={tenc:.1f}s', flush=True)
    if not r:
        print(f'RESULT UNSAT {tag} {tt:.1f}s', flush=True); return
    vals = I.decode_free(model)
    P0 = I.word0(vals); PS = I.wordS(vals)
    rows, gam = indep_sim(lat, P0, I.S)
    fin = rows[-1]
    clock_ok = gam == [lat.g[t % lat.p] for t in range(I.S)]
    pre = next((i for i in range(min(len(fin), len(PS))) if fin[i] != PS[i]), min(len(fin), len(PS)))
    cen0 = I.realise(I.c0, vals)
    print(f'RESULT SAT {tag} {tt:.1f}s centre0={cen0}', flush=True)
    print(f'CHECK indep-sim: clock_ok={clock_ok} exact_target={fin == PS} prefix={pre} len={len(fin)}/{len(PS)}', flush=True)
    if a.mode == 'sim' or a.simfix:
        mset = set(l for l in model if l > 0); bad = 0; cnt = 0
        for t, rw in enumerate(I.rows):
            ft = fold(rows[t])
            for i, v in rw.items():
                cnt += 1
                xv = [x for x in range(I.D) if v[x] in mset]
                if xv != [ft[i]]: bad += 1
            if I.R[t] != ft[:len(I.R[t])]: bad += 1
        print(f'SIMCHECK cells={cnt} mismatches={bad}', flush=True)
    if a.mode == 'planted':
        print(f'PLANTCHECK full_image_equal={fold(fin) == planted}', flush=True)
    if a.mode in ('ret', 'wall', 'grow') and not a.simfix and fin == PS and clock_ok:
        print('!!! CANDIDATE: exact template return verified by independent simulation -- see FINAL protocol', flush=True)


if __name__ == '__main__':
    main()
