#!/usr/bin/env python3
"""r12f2: FREE-CLOCK band-restoration instance (removes every assumption on the overflow clock).

Facts used (clockscc.py, logs/clockscc.log): the 30 U3 words are closed under F_0 and F_1, every word has exactly one
isolated 9, so a pure U3 band stays a pure U3 band under ANY clock sequence and its carry fronts move <= 2 columns
per step; the exact maximal junction-side front over T steps and all clock sequences is computed below (DP).

Instance BF_T(w,R) (group form): window [y-R, y+M), M = (max front over T steps, all clocks) + 21 rounded to 3 | M.
  t=0: columns [y,y+M) = band w (w phase 0 at y), columns [y-R,y) free with (P_(y-3),P_(y-2),P_(y-1)) != (w0,w1,w2);
  clock bits gamma_0..gamma_(T-1) FREE; tail row Z_t (one-hot over the 30 words) with Z_0 = w, Z_(t+1) = F_(gamma_t)(Z_t);
  right port beta_(y+M)(t) = periodic beta of Z_t; left port FREE (alpha bit, high digit used when gamma_t = 1);
  folded two-carry law with P'_i = lo_i + (gamma_t ? hi_(i-1) : hi_i);
  t=T: columns [y,y+M) equal the tail row Z_T (band restored); NO constraint on [y-R,y).
  --stdclock: gamma_t fixed to [t%4==0] (then BF_120 = B_1 of brestore.py on a full rectangle; consistency check).
  --nofor: no triple constraint (positive control).  --full: also [y-R,y) returns (stdclock: = uleft m=1).
  --allsteps: band-correct on [y,y+M) at EVERY step s = 1..T (valid in the maximal-band-start argument over all
          times t, see FINAL; with a free clock any T works).
  --stdupto s0 / --nones n / --tailreturn: clock standard for t < s0, free (optionally exactly n overflows) for
          t >= s0, tail row back to w at t = T (the gap instances for q < 10m-3, see FINAL).
  --rootclock: restrict the free clock to sequences a root column can produce: P_0 >= 1 always (leading digit),
          gamma=0 gives P_0' = 2P_0+beta_1 (so at most 4 consecutive 0s), gamma=1 gives P_0' = P_0 mod 10 + 1 (so at
          most 3 consecutive 1s: 18 -> 9 -> 10 -> 1).  Clauses: no 00000, no 1111 inside the window of T steps.
Encoding helpers (one-hot pair values / digits, carry bits, constant folding) imported from mdefect.py.
"""
import sys, time, argparse
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import mdefect as md

WORDS = [tuple(u) for u in md.us()]


def F(w, g):
    a = [0] * 3; b = [0] * 3; c = 0
    for _ in range(3):
        for j in range(3):
            a[j] = c; c = md.Tc(w[j], c)
    c = 0
    for _ in range(3):
        for j in (2, 1, 0):
            c = md.Tc(w[j], c); b[j] = c
    lo = [(w[j] + a[j]) % 10 for j in range(3)]
    hi = [(w[j] + b[(j + 1) % 3]) % 10 for j in range(3)]
    return tuple(lo[j] + (hi[(j - 1) % 3] if g else hi[j]) for j in range(3)), a, b


F0 = [WORDS.index(F(w, 0)[0]) for w in WORDS]
F1 = [WORDS.index(F(w, 1)[0]) for w in WORDS]
BE = [F(w, 0)[2] for w in WORDS]      # BE[j][ph] = periodic beta_x of word j for x of phase ph (x -> x-1)


def max_front(T, j0, s0=0):
    """max over all clock sequences of the junction-side front l_T of a pure band (word j0 phase 0 at y);
    for t < s0 only the standard clock bit [t%4==0] is allowed."""
    best = {(j0, 0): 0}
    for t in range(T):
        nb = {}
        for (j, ph), l in best.items():
            l2 = l + 1 + (WORDS[j][ph] == 9)
            for jj in ((F1[j] if t % 4 == 0 else F0[j]),) if t < s0 else (F0[j], F1[j]):
                k = (jj, l2 % 3)
                if nb.get(k, -1) < l2:
                    nb[k] = l2
        best = nb
    return max(best.values())


def mux(E, g, h0, h1):
    if isinstance(h0, int) and isinstance(h1, int) and h0 == h1:
        return h0
    hs = E.onehot(10)
    for d in range(10):
        for sign, h in ((1, h0), (-1, h1)):          # sign 1: clause active when gamma = 0 ([g, ...])
            if isinstance(h, int):
                if h == d:
                    E.add([sign * g, hs[d]])
            else:
                E.add([sign * g, -h[d], hs[d]])
    return hs


def build(E, w, R, T, M, y, stdclock, init=None, port=None, clock=None, snaps=None, stdupto=0):
    """returns P0 dict, PT dict, gammas list, Z_T (onehot or int).  init/port/clock: genuine data for validation.
    snaps: optional list, receives (row_s, Z_s) for s = 1..T."""
    x0 = y - R; x1 = y + M; jw = WORDS.index(tuple(w))
    row = {}
    for i in range(x0, x1):
        if init is not None:
            row[i] = E.onehot(19); E.add([row[i][init[i]]])
        elif i < y:
            row[i] = E.onehot(19)
        else:
            row[i] = w[(i - y) % 3]
    P0 = dict(row); Z = jw; gam = []
    for t in range(T):
        g = E.new(); gam.append(g)
        if stdclock or t < stdupto:
            E.add([g if t % 4 == 0 else -g])
        if clock is not None:
            E.add([g if clock[t] else -g])
        al = {x0: (E.new(),)}
        if port is not None:
            E.add([md.lit(al[x0], port[0][t])])
        for i in range(x0, x1):
            al[i + 1] = md.carry(E, row[i], al[i])
        # right port beta_(x1)(t) from the tail row Z_t
        ph = (x1 - y) % 3
        if isinstance(Z, int):
            be = {x1: BE[Z][ph]}
        else:
            bv = (E.new(),); be = {x1: bv}
            for j in range(30):
                E.add([-Z[j], md.lit(bv, BE[j][ph])])
        for x in range(x1 - 1, x0 - 1, -1):
            be[x] = md.carry(E, row[x], be[x + 1])
        hi = {i: md.digit(E, row[i], be[i + 1]) for i in range(x0, x1)}
        hl = E.onehot(10); hi[x0 - 1] = hl
        if port is not None:
            E.add([hl[port[1][t]]])
        new = {}
        for i in range(x0, x1):
            lo = md.digit(E, row[i], al[i])
            new[i] = md.psum(E, lo, mux(E, g, hi[i], hi[i - 1]))
        # tail transition
        Zn = E.onehot(30)
        if isinstance(Z, int):
            E.add([g, Zn[F0[Z]]]); E.add([-g, Zn[F1[Z]]])
        else:
            for j in range(30):
                E.add([-Z[j], g, Zn[F0[j]]]); E.add([-Z[j], -g, Zn[F1[j]]])
        Z = Zn; row = new
        if snaps is not None:
            snaps.append((row, Z))
    return P0, row, gam, Z


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['group', 'front'])
    ap.add_argument('--U', type=int, default=2)
    ap.add_argument('--r', type=int, default=3)
    ap.add_argument('--T', type=int, default=120)
    ap.add_argument('--stdclock', action='store_true')
    ap.add_argument('--nofor', action='store_true')
    ap.add_argument('--full', action='store_true')
    ap.add_argument('--rootclock', action='store_true')
    ap.add_argument('--stdupto', type=int, default=0, help='clock fixed to [t%%4==0] for t < stdupto, free after')
    ap.add_argument('--nones', type=int, default=-1, help='exactly this many overflows among the free steps t >= stdupto')
    ap.add_argument('--tailreturn', action='store_true', help='tail row returns: Z_T = w')
    ap.add_argument('--allsteps', action='store_true', help='band-correct on [y,y+M) at EVERY step s=1..T')
    ap.add_argument('--solver', default='kissat404')
    a = ap.parse_args()
    if a.mode == 'front':
        for T in (1, 2, 4, 12, 40, 120, 240):
            print('T', T, 'max front over all clocks', max(max_front(T, j) for j in range(30)),
                  'standard-clock fronts', sorted(set(md.fronts(WORDS[j], T, md.band_bg(WORDS[j], T)[0])[0][T] for j in range(30))) if T % 4 == 0 else '')
        return
    from pysat.solvers import Solver
    w = WORDS[a.U]; R = a.r; T = a.T; y = 5000; t0 = time.time()
    lf = max(max_front(T, j, T if a.stdclock else a.stdupto) for j in range(30)); M = 3 * ((lf + 21 + 2) // 3)
    S = Solver(name=a.solver); E = md.Enc(S)
    snaps = []
    P0, PT, gam, Z = build(E, w, R, T, M, y, a.stdclock, snaps=snaps, stdupto=a.stdupto)
    if a.tailreturn:
        E.add([Z[WORDS.index(tuple(w))]])
    if a.nones >= 0:
        from pysat.card import CardEnc, EncType
        cnf = CardEnc.equals(lits=gam[a.stdupto:], bound=a.nones, top_id=E.nv, encoding=EncType.seqcounter)
        for c in cnf.clauses:
            E.add(c)
        E.nv = max(E.nv, cnf.nv)
    for (Ps, Zs) in (snaps if a.allsteps else snaps[-1:]):
        for i in range(y, y + M):
            for j in range(30):
                E.add([-Zs[j], Ps[i][WORDS[j][(i - y) % 3]]])
    if a.full:
        for i in range(y - R, y):
            md.equal(E, PT[i], P0[i])
    if not a.nofor:
        E.add([-P0[y - 3 + j][w[j]] for j in range(3)])
    if a.rootclock:
        for t in range(T - 4):
            E.add([gam[t + d] for d in range(5)])
        for t in range(T - 3):
            E.add([-gam[t + d] for d in range(4)])
    print(f'bfree group U={a.U} w={w} R={R} T={T} maxfront={lf} M={M} stdclock={a.stdclock} rootclock={a.rootclock} stdupto={a.stdupto} nones={a.nones} tailreturn={a.tailreturn} allsteps={a.allsteps} nofor={a.nofor} full={a.full} '
          f'vars={E.nv} clauses={E.ncl} solver={a.solver} enc={time.time()-t0:.0f}s', flush=True)
    r = S.solve()
    if r:
        m = set(x for x in S.get_model() if x > 0)
        print('SAT free columns', [md.val(m, P0[i]) for i in range(y - R, y)], 'clock', ''.join(str(int(g in m)) for g in gam), flush=True)
    print('RESULT', 'BF=[sat]' if r else 'BF=[]', 'NONEMPTY' if r else 'EMPTY', f'{time.time()-t0:.0f}s', flush=True)


if __name__ == '__main__':
    main()
