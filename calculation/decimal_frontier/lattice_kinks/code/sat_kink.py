#!/usr/bin/env python3
"""W7: SAT encoding of the exact window dynamics (same map as win.h) -- periodic kink / horizon survival.
usage: sat_kink.py latfile w o mode [H|T] [M]
  mode 'per'  : time-periodic window orbit of period T (T = number of steps, wraps to layer 0)   -> SAT = bounded kink of width <= w
  mode 'hor'  : survive H steps from some free window (no wrap)                                    -> SAT = survivor exists
  mode 'free' : periodic orbit with NO frozen constraint (positive control of the encoding)
Signals: constants (int) or one-hot literal lists.  Single CaDiCaL thread."""
import sys, time
sys.path.insert(0, '/home/claude/research/w7_kink/code')
from pysat.solvers import Cadical153
BB = 10

def load_lat(fn):
    tok = open(fn).read().split()
    it = iter(tok)
    p = int(next(it)); nB = int(next(it)); m = int(next(it)); b = int(next(it))
    gam = [int(next(it)) for _ in range(p)]
    W = [[int(next(it)) for _ in range(m)] for _ in range(p)]
    cup = [[int(next(it)) for _ in range(m)] for _ in range(p)]
    return dict(p=p, nB=nB, m=m, gam=gam, W=W, cup=cup)

class Enc:
    def __init__(self):
        self.nv = 0; self.cl = []
    def new(self):
        self.nv += 1; return self.nv
    def group(self, D):
        """one-hot group of D new literals (exactly one)"""
        g = [self.new() for _ in range(D)]
        self.cl.append(list(g))
        for i in range(D):
            for j in range(i + 1, D):
                self.cl.append([-g[i], -g[j]])
        return g
    def gate(self, f, Dout, *ins):
        """output signal = f(in1, in2, ...); inputs const (int) or one-hot lists.  Returns const or group."""
        if all(isinstance(x, int) for x in ins):
            return f(*ins)
        out = self.group(Dout)
        # iterate over combinations of variable inputs
        varidx = [k for k, x in enumerate(ins) if not isinstance(x, int)]
        doms = [range(len(ins[k])) for k in varidx]
        def rec(pos, vals):
            if pos == len(varidx):
                args = [x if isinstance(x, int) else None for x in ins]
                for k, v in zip(varidx, vals): args[k] = v
                r = f(*args)
                clause = [-ins[k][v] for k, v in zip(varidx, vals)] + [out[r]]
                self.cl.append(clause)
                return
            for v in doms[pos]:
                rec(pos + 1, vals + [v])
        rec(0, [])
        return out
    def forbid_sum(self, u, d, target):
        """require u + d == target (u,d signals of digits)"""
        if isinstance(u, int) and isinstance(d, int):
            if u + d != target: self.cl.append([])   # contradiction
            return
        if isinstance(u, int):
            for dv in range(len(d)):
                if u + dv != target: self.cl.append([-d[dv]])
            return
        if isinstance(d, int):
            for uv in range(len(u)):
                if uv + d != target: self.cl.append([-u[uv]])
            return
        for uv in range(len(u)):
            for dv in range(len(d)):
                if uv + dv != target: self.cl.append([-u[uv], -d[dv]])

def build(lat, w, o, mode, nsteps, M=6, fixlow=True):
    p, nB, m, gam, W, cup = lat['p'], lat['nB'], lat['m'], lat['gam'], lat['W'], lat['cup']
    K = w + M; n0 = 400 + o
    E = Enc()
    def cell(t, pos): return W[t % p][(pos - nB) % m]
    def cupat(t, pos): return cup[t % p][(pos - nB) % m]
    # state of layer t: list of K signals (index i=0 bottom .. K-1 top)
    ns = [n0]
    for t in range(nsteps): ns.append(ns[-1] + gam[t % p])
    def lattice_layer(t):
        n = ns[t]; h = (n + 1) // 2
        return [cell(t, h - K + i) for i in range(K)]
    layers = []
    # layer 0
    L0 = lattice_layer(0)
    if mode == 'free':
        layers.append([E.group(19) for i in range(K)])
    else:
        layers.append(L0[:K - w] + [E.group(19) for _ in range(w)])
    # parity of top cell for odd n
    def parity_clause(t):
        if ns[t] % 2 == 1:
            top = layers[t][K - 1]
            if not isinstance(top, int):
                for v in range(1, 19, 2): E.cl.append([-top[v]])
    parity_clause(0)
    fz = K - w
    for t in range(nsteps):
        n = ns[t]; h = (n + 1) // 2; g = gam[t % p]; odd = (n & 1) == 1
        P = layers[t]
        n2 = n + g; h2 = (n2 + 1) // 2; dh = h2 - h
        cu = [None] * (K + 1); Oup = [None] * K
        cu[0] = cupat(t, h - K)
        for i in range(K):
            cu[i + 1] = E.gate(lambda pv, a: 1 if pv + a >= BB else 0, 2, P[i], cu[i]) if not (isinstance(P[i], int) and isinstance(cu[i], int)) else (1 if P[i] + cu[i] >= BB else 0)
            Oup[i] = E.gate(lambda pv, a: (pv + a) % BB, BB, P[i], cu[i])
        D = [None] * K; Odn = [None] * K
        if odd:
            D[K - 1] = cu[K - 1]; Odn[K - 1] = Oup[K - 1]; D[K - 2] = cu[K]; top = K - 2
        else:
            D[K - 1] = cu[K]; top = K - 1
            Odn[K - 1] = E.gate(lambda pv, d: (pv + d) % BB, BB, P[K - 1], D[K - 1])
        for i in range(top, -1, -1):
            if i < top:
                D[i] = E.gate(lambda pv, d: 1 if pv + d >= BB else 0, 2, P[i + 1], D[i + 1])
            Odn[i] = E.gate(lambda pv, d: (pv + d) % BB, BB, P[i], D[i])
        # new layer
        nxt = []
        for i2 in range(K):
            if i2 < 2:
                nxt.append(cell(t + 1, h2 - K + i2) if mode != 'free' else None); continue
            i = i2 + dh
            if g == 0:
                up = Oup[i]; part = Oup[i] if (odd and i == K - 1) else Odn[i]
            else:
                up = Oup[i] if i <= K - 1 else Odn[K - 1]
                part = Odn[i - 1]
            if mode != 'free' and i2 < fz:
                # frozen: sum must equal lattice
                E.forbid_sum(up, part, cell(t + 1, h2 - K + i2))
                nxt.append(cell(t + 1, h2 - K + i2))
            else:
                nxt.append(E.gate(lambda u, d: u + d, 19, up, part))
        if mode == 'free':
            # bottom two cells of the new buffer unknown in free mode: take them as fresh unconstrained groups
            for i2 in range(2):
                nxt[i2] = E.group(19)
        layers.append(nxt)
        if mode == 'per' or mode == 'free':
            if t == nsteps - 1:
                # periodic closure: layer nsteps == layer 0
                for i in range(K):
                    a = layers[nsteps][i]; b = layers[0][i]
                    if isinstance(a, int) and isinstance(b, int):
                        if a != b: E.cl.append([])
                    elif isinstance(a, int):
                        for v in range(19):
                            if v != a: E.cl.append([-b[v]])
                    elif isinstance(b, int):
                        for v in range(19):
                            if v != b: E.cl.append([-a[v]])
                    else:
                        for v in range(19):
                            E.cl.append([-a[v], b[v]]); E.cl.append([a[v], -b[v]])
        else:
            parity_clause(t + 1)
    return E, layers, K, ns

def solve(E, tl=None):
    s = Cadical153(bootstrap_with=E.cl)
    t0 = time.time()
    r = s.solve()
    model = s.get_model() if r else None
    s.delete()
    return r, model, time.time() - t0

if __name__ == '__main__':
    lat = load_lat(sys.argv[1]); w = int(sys.argv[2]); o = int(sys.argv[3]); mode = sys.argv[4]
    N = int(sys.argv[5]); M = int(sys.argv[6]) if len(sys.argv) > 6 else 6
    t0 = time.time()
    E, layers, K, ns = build(lat, w, o, mode, N, M)
    print(f'built vars={E.nv} clauses={len(E.cl)} in {time.time()-t0:.1f}s', flush=True)
    r, model, dt = solve(E)
    print(f'{mode} w={w} o={o} N={N}: {"SAT" if r else "UNSAT"} ({dt:.1f}s)', flush=True)
    if r:
        ms = set(x for x in model if x > 0)
        for t in range(min(3, len(layers))):
            row = []
            for sig in layers[t]:
                if sig is None: row.append('?'); continue
                if isinstance(sig, int): row.append(sig); continue
                row.append([v for v in range(19) if sig[v] in ms][0])
            print('layer', t, row)
