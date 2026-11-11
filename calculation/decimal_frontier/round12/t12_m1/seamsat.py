#!/usr/bin/env python3
"""r11c seam SAT: exact folded two-carry encoding of the rooted W9|J|U3 seam.

Folded columns i (root=0).  Row P_t.  Low carry alpha flows i->i+1 (inlet 0 at
root), high carry beta flows i+1->i.  lo_i=(P_i+alpha_i)%10,
hi_i=(P_i+beta_(i+1))%10, beta_i=T(P_i,beta_(i+1)).  gamma_t=[t%4==0] (forced,
AC46/T12).  P'_i = lo_i+hi_i (gamma 0) or lo_i+hi_(i-1) (gamma 1).
Window [x0,x1).  Left inputs alpha_x0(t), P_(x0-1)(t) are exact rooted-prefix
values (x0<69).  Right inlet beta_x1(t): either free bits sigma_t ('W' mode:
x1=J0, characterises which inlet sequences let the W side return) or the
periodic U value (x1 beyond the 152-column junction cone).
"""
import sys, argparse, time
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from seam_check import B, W, J0, us, norm

def cone_rows(p, steps=120):
    """Exact rooted-prefix rows (AC46 two-inlet cone).  Returns list of rows."""
    rows = [list(p)]
    for t in range(steps):
        n = len(p); d, _ = norm(p, 0); a0, g0 = norm(p[::-1], 0); a1, g1 = norm(p[::-1], 1)
        assert g0 == g1 == (t % 4 == 0)
        if g0:
            l0 = [d[0]+1]+[d[i]+a0[n-i] for i in range(1, n)]; l1 = [d[0]+1]+[d[i]+a1[n-i] for i in range(1, n)]
        else:
            l0 = [d[i]+a0[n-1-i] for i in range(n)]; l1 = [d[i]+a1[n-1-i] for i in range(n)]
        j = next((i for i in range(n) if l0[i] != l1[i]), n); p = l0[:j]; rows.append(p)
    return rows

def alpha_at(row, x):
    c = 0
    for i in range(x): c = (row[i]+c)//10
    return c

def beta_at(row, x):
    b0, b1 = 0, 1
    for i in range(len(row)-1, x-1, -1): b0 = (row[i]+b0)//10; b1 = (row[i]+b1)//10
    assert b0 == b1, 'beta not determined'
    return b0

class Sink:
    """Streams clauses straight into the solver (keeps RSS low)."""
    def __init__(s, solver): s.S = solver; s.n = 0
    def append(s, c): s.S.add_clause(c); s.n += 1
    def __len__(s): return s.n

class Enc:
    def __init__(s, solver=None): s.nv = 0; s.cl = Sink(solver) if solver is not None else []
    def new(s, k=1):
        r = list(range(s.nv+1, s.nv+1+k)); s.nv += k; return r
    def one(s, vs):
        s.cl.append(list(vs))
        for i in range(len(vs)):
            for j in range(i+1, len(vs)): s.cl.append([-vs[i], -vs[j]])
    def fix(s, var, b): s.cl.append([var] if b else [-var])

def encode(x0, x1, init, rows_bg, right, final, Jcols=(), Jdom=19, solver=None):
    """init: dict col->value for fixed initial cols; Jcols free (0..18).
    right: list of 120 ints or None (free sigma).  final: dict col->target."""
    E = Enc(solver)
    def onehots(): 
        r = {}
        for i in range(x0, x1):
            v = E.new(19); E.one(v); r[i] = v
        return r
    P = onehots(); P0 = P
    for i in range(x0, x1):
        if i in init: E.fix(P[i][init[i]], 1)
    sig = []
    for t in range(120):
        g = (t % 4 == 0)
        al = E.new(x1-x0+1); be = E.new(x1-x0+1)   # index i-x0
        E.fix(al[0], alpha_at(rows_bg[t], x0))
        if right is None:
            sig.append(be[-1])
        else:
            E.fix(be[-1], right[t])
        lo = {}; hi = {}
        for i in range(x0, x1):
            k = i-x0
            lo[i] = E.new(10); E.one(lo[i]); hi[i] = E.new(10); E.one(hi[i])
            for x in range(19):
                for b in (0, 1):
                    z = x+b
                    # alpha path
                    h = [-P[i][x], (-al[k] if b else al[k])]
                    E.cl.append(h+[lo[i][z % 10]]); E.cl.append(h+[al[k+1] if z >= 10 else -al[k+1]])
                    h = [-P[i][x], (-be[k+1] if b else be[k+1])]
                    E.cl.append(h+[hi[i][z % 10]]); E.cl.append(h+[be[k] if z >= 10 else -be[k]])
        Pn = onehots()
        if g:
            px = rows_bg[t][x0-1]
            # hi_(x0-1) = (P_(x0-1)+beta_x0)%10
            hl = E.new(10); E.one(hl)
            for b in (0, 1):
                E.cl.append([(-be[0] if b else be[0]), hl[(px+b) % 10]])
        for i in range(x0, x1):
            H = (hi[i-1] if i > x0 else hl) if g else hi[i]
            for a in range(10):
                for b in range(10):
                    E.cl.append([-lo[i][a], -H[b], Pn[i][a+b]])
        P = Pn
    for i, v in final.items(): E.fix(P[i][v], 1)
    return E, P, sig, P0

def bg(Lj, U, K=220):
    p = list(B)+list(W)*14+[0]*Lj+list(U)*K
    return cone_rows(p)

def sigma_W():
    rows = cone_rows(list(B)+list(W)*60)
    return [beta_at(rows[t], J0) for t in range(120)]

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('mode')
    ap.add_argument('--x0', type=int, default=64)
    ap.add_argument('--U', type=int, default=0)
    ap.add_argument('--Lj', type=int, default=0)
    ap.add_argument('--margin', type=int, default=170)
    ap.add_argument('--cap', type=int, default=20)
    ap.add_argument('--fixJ', default='')
    ap.add_argument('--solver', default='cadical195')
    ap.add_argument('--ctrl', action='store_true')
    a = ap.parse_args()
    from pysat.solvers import Solver
    t0 = time.time()
    if a.mode == 'W':
        rows = cone_rows(list(B)+list(W)*14)
        init = {i: rows[0][i] for i in range(a.x0, J0)}
        final = dict(init)
        E, P, sig, P0 = encode(a.x0, J0, init, rows, None, final)
        sw = sigma_W()
        print('sigma_W', ''.join(map(str, sw)), 'vars', E.nv, 'clauses', len(E.cl), flush=True)
        with Solver(name=a.solver, bootstrap_with=E.cl) as S:
            k = 0
            while k < a.cap and S.solve():
                m = set(l for l in S.get_model() if l > 0)
                s = [1 if v in m else 0 for v in sig]
                print('ACCEPT', ''.join(map(str, s)), 'diff_vs_W', [t for t in range(120) if s[t] != sw[t]], f'{time.time()-t0:.0f}s', flush=True)
                S.add_clause([(-v if s[t] else v) for t, v in enumerate(sig)]); k += 1
            print('DONE', k, 'accepted sequences', 'exhausted' if k < a.cap else 'cap', f'{time.time()-t0:.0f}s', flush=True)
    else:  # seam: free J of length Lj, given U
        U = us()[a.U]; Lj = a.Lj
        rows = bg(Lj, U)
        x1 = J0+Lj+a.margin
        right = [beta_at(rows[t], x1) for t in range(120)]
        init = {i: rows[0][i] for i in range(a.x0, x1) if not (J0 <= i < J0+Lj)}
        tgt = list(B)+list(W)*14+[None]*Lj+list(U)*200
        fx = [int(v) for v in a.fixJ.split(',')] if a.fixJ else None
        if fx:
            for j, v in enumerate(fx): init[J0+j] = v
        # final: whole window must equal target, J columns equal initial J
        final = {i: tgt[i] for i in range(a.x0, x1) if tgt[i] is not None}
        if a.ctrl:  # positive control: target = exact cone image of the fixed J
            cr = cone_rows(list(B)+list(W)*14+fx+list(U)*220)[120]
            assert len(cr) >= x1
            final = {i: cr[i] for i in range(a.x0, x1)}
            print('ctrl: cone image differs from return target at', [i-J0 for i in range(a.x0, x1) if tgt[i] is not None and tgt[i] != cr[i]][:5], flush=True)
        S = Solver(name=a.solver)
        E, P, sig, P0 = encode(a.x0, x1, init, rows, right, final, solver=S)
        for j in range(Lj if not a.ctrl else 0):
            for v in range(19): E.cl.append([-P0[J0+j][v], P[J0+j][v]])
        print(f'U={U} Lj={Lj} x1={x1} vars={E.nv} clauses={len(E.cl)} enc={time.time()-t0:.0f}s', flush=True)
        if True:
            r = S.solve()
            if r:
                m = set(l for l in S.get_model() if l > 0)
                Jw = [next(v for v in range(19) if P0[J0+j][v] in m) for j in range(Lj)]
                print('RESULT SAT J=', Jw, f'{time.time()-t0:.0f}s', flush=True)
            else:
                print('RESULT UNSAT', f'{time.time()-t0:.0f}s', flush=True)
