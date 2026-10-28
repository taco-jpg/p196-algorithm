#!/usr/bin/env python3
"""replay.py -- build + replay hybrid certificates with plain big-int reverse-and-add.
Functions:
  find_cycles(b, cyc, Wmax, cvals)  -> list of hybrid cycles (small widths) over the exterior cycle `cyc` (list of (B,gam,e1,u))
  verify_cycle(b, cyc, ph, C0, c0)  -> dict with edges, A, Sgam, ok flags
  replay(b, cyc, ph, C0, c0, steps, g0, h0) -> checks template at every step vs plain integer reverse-and-add
"""
import sys, itertools, json
from hyb import *
from ext import *

def run_cycle(b, cyc, ph, C0, c0, maxT=400):
    """follow the canonical hybrid dynamics from (C0,c0) at exterior phase ph until the state repeats (or dies).
    returns (status, edges, closing index) ; edge = (t, B, C, c, B2, C2, c2, gam, u, v, p)"""
    T = len(cyc); seen = {}; edges = []
    C, c = list(C0), c0
    for s in range(maxT):
        key = (tuple(C), c, (ph + s) % T)
        if key in seen: return 'cycle', edges, seen[key]
        seen[key] = s
        B, gam, e1, u = cyc[(ph + s) % T]
        r = hstep(b, B, C, c)
        if r is None: return 'die', edges, s
        B2, C2, c2, gam2, u2, v, p, raw = r
        assert gam2 == gam and raw['e1'] == e1
        Bn = cyc[(ph + s + 1) % T][0]
        assert B2 == Bn, (B2, Bn)
        edges.append((s, B, C, c, B2, C2, c2, gam, u2, v, p))
        C, c = C2, c2
    return 'long', edges, None

def verify_cycle(b, cyc, ph, C0, c0):
    st, edges, i0 = run_cycle(b, cyc, ph, C0, c0)
    if st != 'cycle' or i0 != 0: return dict(ok=False, status=st, start=i0)
    es = edges
    Sg = sum(e[7] for e in es); A = sum(e[9] for e in es); Su = sum(e[8] for e in es); Sp = sum(e[10] for e in es)
    return dict(ok=True, T=len(es), Sgam=Sg, A=A, Su=Su, Sp=Sp, dg=Su + A - Sg, dh=Sg - 2 * A, edges=es,
                hybrid_ok=(Sg - 2 * A >= 0 and Su + A - Sg >= 0))

def replay(b, cyc, ph, C0, c0, steps, g0=None, h0=None, verbose=True):
    """integer replay: X_0 = val(P_0), P_s = tmpl(B_s,C_s,c_s,g_s,h_s);  pairs(digits(X_s)) must equal P_{s+1}, X_s non-palindromic."""
    vc = verify_cycle(b, cyc, ph, C0, c0)
    assert vc['ok'] and vc['hybrid_ok'], vc
    es = vc['edges']; T = vc['T']
    N = b - 1
    if g0 is None: g0 = 3 + 2 * T
    if h0 is None: h0 = 3 + 3 * T + 2 * vc['Sp']
    B, C, c = es[0][1], es[0][2], es[0][3]
    g, h = g0, h0
    X = val(b, tmpl(b, B, C, c, g, h))
    Bs, Cs, cs = B, C, c
    minL = (g, h)
    for s in range(steps):
        e = es[s % T]
        # template for step s: (B,C,c,g,h) = state s ; next template (after trims) state s+1
        assert (e[1], e[2], e[3]) == (Bs, Cs, cs)
        gam, u, v, p = e[7], e[8], e[9], e[10]
        d = digits(b, X)
        if d == d[::-1]:
            return dict(ok=False, why='palindrome at step %d' % s)
        # predicted: pair word of X_s (=val(P_s)) is P_{s+1} with exponents g-gam, h-2+gam  *before* trims; compare after trims
        g1 = g - gam + u + v; h1 = h - 2 + gam + 2 * p
        Pn = tmpl(b, e[4], e[5], e[6], g1, h1)
        act = pairs(d)
        if act != Pn:
            return dict(ok=False, why='template mismatch at step %d' % s, act=act[:60], pred=Pn[:60])
        if g1 < 3 or h1 < 3: return dict(ok=False, why='g/h too small at step %d' % s)
        minL = (min(minL[0], g1), min(minL[1], h1))
        X = X + val(b, d[::-1])
        Bs, Cs, cs, g, h = e[4], e[5], e[6], g1, h1
    return dict(ok=True, steps=steps, T=T, g_final=g, h_final=h, min_g=minL[0], min_h=minL[1], digits=len(digits(b, X)), vc={k: vc[k] for k in ('Sgam', 'A', 'Su', 'Sp', 'dg', 'dh')})

def find_cycles(b, cyc, Wmax, cvals, maxcount=50):
    T = len(cyc); N = b - 1
    out = []
    seenkeys = set()
    for w in range(0, Wmax + 1):
        for C in itertools.product(range(2 * b - 1), repeat=w):
            if w and (C[0] == N): continue
            for c in cvals:
                if w and C[-1] == c: continue
                for ph in range(T):
                    st, edges, i0 = run_cycle(b, cyc, ph, list(C), c, maxT=200)
                    if st == 'cycle' and i0 == 0:
                        key = (tuple(C), c, ph)
                        out.append((list(C), c, ph))
                        if len(out) >= maxcount: return out
    return out

if __name__ == '__main__':
    # control: base 4
    import glob
    from streams_all import canon
    b = 4
    for fn in glob.glob('/home/claude/research/w1_bases/out/ext4/b4_p12.txt'):
        for a in parse_accepts(fn):
            cyc = cycle_from(b, a['Bs'][0])
            if cyc is None: continue
            gs = ''.join(str(x[1]) for x in cyc); es_ = ''.join(str(x[2]) for x in cyc)
            print('stream', gs, es_, len(cyc))
            cvals = [c for c in range(2 * b - 1) if c != b - 1]
            cs = find_cycles(b, cyc, 1, cvals, maxcount=3)
            for (C, c, ph) in cs:
                vc = verify_cycle(b, cyc, ph, C, c)
                print('  cycle C=%s c=%d ph=%d T=%d Sgam=%d A=%d dh=%d dg=%d hybrid_ok=%s' % (C, c, ph, vc['T'], vc['Sgam'], vc['A'], vc['dh'], vc['dg'], vc['hybrid_ok']))
                if vc['hybrid_ok']:
                    r = replay(b, cyc, ph, C, c, 2000)
                    print('   replay', {k: v for k, v in r.items() if k != 'act'})
