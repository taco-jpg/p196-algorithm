#!/usr/bin/env python3
"""SAT version of the bottom-of-kink edge relaxation, periodic in the centre frame.
Window [c(t), c(t)+K) at the bottom of the kink, c(t) moves exactly like the centre h(t).
Free inputs: Din_t (descending carry from cell c+K) every step, ghost_t (e-digit of cell c+K) on frame shifts.
Constraints: exact local dynamics (klib.window_step semantics), lattice below the frame stays exact,
window(T) == window(0), and
  acc  : bottom cell off-lattice at some t            (always imposed)
  never: window never entirely lattice                (option 'never')
usage: relsat.py lat K T orbit_index [never] [seedcheck]
A kink of ANY width >= K and time period T (in the frame) whose frame is normalised to its deepest
first defect gives a solution with 'acc' (and with 'never' if its first defect always stays within K cells)."""
import sys, time
from pysat.solvers import Cadical153
from klib import *

class Enc:
    def __init__(s): s.nv = 0; s.cl = []
    def new(s): s.nv += 1; return s.nv
    def onehot(s, D):
        g = [s.new() for _ in range(D)]
        s.cl.append(list(g))
        for i in range(D):
            for j in range(i + 1, D): s.cl.append([-g[i], -g[j]])
        return g
    def gate(s, f, Dout, *ins):
        """inputs: int constants or one-hot lists (bits are one-hot lists of length 2)"""
        if all(isinstance(x, int) for x in ins): return f(*ins)
        out = s.onehot(Dout)
        vi = [k for k, x in enumerate(ins) if not isinstance(x, int)]
        def rec(pos, vals):
            if pos == len(vi):
                args = list(ins)
                for k, v in zip(vi, vals): args[k] = v
                r = f(*args)
                s.cl.append([-ins[k][v] for k, v in zip(vi, vals)] + [out[r]])
                return
            for v in range(len(ins[vi[pos]])): rec(pos + 1, vals + [v])
        rec(0, [])
        return out
    def neq_const(s, sig, val):
        """literal that is true iff sig != val (sig one-hot or const)"""
        if isinstance(sig, int): return None if sig == val else True
        return -sig[val]
    def eq(s, a, b, D):
        if isinstance(a, int) and isinstance(b, int):
            if a != b: s.cl.append([])
            return
        if isinstance(a, int): a, b = b, a
        if isinstance(b, int):
            s.cl.append([a[b]]); return
        for v in range(D):
            s.cl.append([-a[v], b[v]]); s.cl.append([a[v], -b[v]])

def orbits(lat):
    """phase orbits (t mod p, j, par); return one representative with t=0 per orbit and orbit length"""
    seen = set(); reps = []
    for j in range(lat.m):
        for par in range(2):
            ph = (0, j, par)
            if ph in seen: continue
            orb = []; x = ph
            while x not in orb:
                orb.append(x); seen.add(x)
                t, jj, pp = x; g = lat.g[t]; dh = 1 if (g == 1 and pp == 0) else 0
                x = ((t + 1) % lat.p, (jj + dh) % lat.m, (pp + g) % 2)
            reps.append((ph, len(orb)))
    return reps

def build(lat, K, T, ph0, never=False, band=None, noacc=False):
    E = Enc(); base = lat.nB + 5 * lat.m
    t0, j, par = ph0
    layers = []; phs = []
    win = [E.onehot(19) for _ in range(K)]
    layers.append(win); phs.append(ph0)
    accl = []; neverl = []
    for t in range(T):
        tt, jj, pp = phs[-1]; g = lat.g[tt]; dh = 1 if (g == 1 and pp == 0) else 0
        c = base + jj
        P = layers[-1]
        # bookkeeping literals
        lw = [lat.cell(tt, c + i) for i in range(K)]
        accl.append(E.neq_const(P[0], lw[0]))
        neverl.append([E.neq_const(P[i], lw[i]) for i in range(K)])
        # ascending
        a = [None] * (K + 1); e = [None] * K
        a[0] = bulk_up_carry(lat, tt, c)
        for i in range(K):
            e[i] = E.gate(lambda v, x: (v + x) % 10, 10, P[i], a[i])
            a[i + 1] = E.gate(lambda v, x: (v + x) // 10, 2, P[i], a[i])
        # descending
        D = [None] * K; r = [None] * K
        D[K - 1] = E.onehot(2)                  # Din_t free
        for i in range(K - 1, 0, -1):
            D[i - 1] = E.gate(lambda v, x: (v + x) // 10, 2, P[i], D[i])
        for i in range(K):
            r[i] = E.gate(lambda v, x: (v + x) % 10, 10, P[i], D[i])
        Dlow = E.gate(lambda v, x: (v + x) // 10, 2, P[0], D[0])
        Lc1 = lat.cell(tt, c - 1); Dnom = bulk_down_carry(lat, tt, c - 1)
        if not (g == 1 and Lc1 != 9):
            E.eq(Dlow, Dnom, 2)
        rlow = E.gate(lambda x: (Lc1 + x) % 10, 10, Dlow)
        nw = []
        if band:
            q, R = band
            # top R cells periodic with period q, carries continue periodically upward
            for i in range(K - R, K - q): E.eq(P[i], P[i + q], 19)
            E.eq(D[K - 1], D[K - 1 - q], 2)
            E.eq(a[K], a[K - q], 2)
        for i in range(K + dh):
            if i < K: ex = e[i]
            else:
                ex = E.onehot(10)                     # ghost_t
                if band: E.eq(ex, e[K - band[0]], 10)
            src = i - g
            rr = r[src] if src >= 0 else rlow
            nw.append(E.gate(lambda u, v: u + v, 19, ex, rr))
        ph2 = ((tt + 1) % lat.p, (jj + dh) % lat.m, (pp + g) % 2)
        if dh:
            E.eq(nw[0], lat.cell(tt + 1, c), 19)
            nw = nw[1:]
        layers.append(nw); phs.append(ph2)
    assert phs[-1] == ph0, 'T must be a multiple of the phase orbit length'
    for i in range(K): E.eq(layers[T][i], layers[0][i], 19)
    # accepting: bottom off-lattice at some t
    lits = [x for x in accl if x is not None and x is not True]
    if noacc or any(x is True for x in accl): pass
    else: E.cl.append(lits)
    if never:
        for row in neverl:
            if any(x is True for x in row): continue
            E.cl.append([x for x in row if x is not None])
    return E, layers, phs

def decode(model, sig):
    if isinstance(sig, int): return sig
    ms = model
    return [v for v in range(len(sig)) if ms[sig[v] - 1] > 0][0]

def check_solution(lat, K, layers, phs, model):
    """replay the decoded cycle with the independent reference window_step"""
    base = lat.nB + 5 * lat.m
    W = [[decode(model, s) for s in L] for L in layers]
    for t in range(len(layers) - 1):
        tt, jj, pp = phs[t]
        ok_any = False
        for Din in (0, 1):
            for gh in range(10):
                new, ok = window_step(lat, tt, base + jj, 1000 + pp, W[t], Din, gh)
                if ok and new == W[t + 1]: ok_any = True; break
            if ok_any: break
        if not ok_any: return False, W
    return W[-1] == W[0], W

if __name__ == '__main__':
    name, K, T, oi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    never = 'never' in sys.argv[5:]
    band = None
    for a_ in sys.argv[5:]:
        if a_.startswith('band='): q_, R_ = map(int, a_[5:].split(',')); band = (q_, R_)
    lat = load(name)
    reps = orbits(lat)
    ph0, olen = reps[oi]
    t0 = time.time()
    E, layers, phs = build(lat, K, T, ph0, never, band, 'noacc' in sys.argv[5:])
    s = Cadical153(bootstrap_with=E.cl)
    r = s.solve()
    dt = time.time() - t0
    msg = f'{name} K={K} T={T} orbit={oi} ph0={ph0} never={never} band={band}: {"SAT" if r else "UNSAT"} vars={E.nv} clauses={len(E.cl)} {dt:.1f}s'
    if r:
        model = s.get_model()
        ok, W = check_solution(lat, K, layers, phs, model)
        base = lat.nB + 5 * lat.m
        offl = sum(1 for t in range(T) if W[t][0] != lat.cell(phs[t][0], base + phs[t][1]))
        msg += f' replay={"OK" if ok else "FAIL"} bottom-off-lattice-steps={offl}/{T}'
        if 'show' in sys.argv[5:]:
            for t in range(0, T, 4):
                tt, jj, pp = phs[t]
                lw = [lat.cell(tt, base + jj + i) for i in range(K)]
                print(' t=%3d' % t, ''.join('*' if a != b else '.' for a, b in zip(W[t], lw)), W[t])
    print(msg, flush=True)
