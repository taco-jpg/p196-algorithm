#!/usr/bin/env python3
"""r12f2: INDEPENDENT encoding of the partial/free-clock band-restoration group instance of bfree.py, written in the
enc2 style of mindep.py (direct relations X[t][i] one-hot 0..18, carry bits A (low) and C (high), no digit variables).
Shares only the CNF helper class of mindep.py; band successors, periodic carries, word table, front DP and all clauses
are re-implemented here.

Instance (group form, T steps): window [y-R, y+M), M = (max front, clock standard for t < s0, free after) + 21,
rounded to 3 | M.  t=0: [y,y+M) = band w (phase 0 at y), [y-R,y) free with (P_(y-3),P_(y-2),P_(y-1)) != w.
Clock bits g_t: = [t%4==0] for t < s0, free for t >= s0; root-realizable (no 00000, no 1111); exactly n ones among
t >= s0 (if --nones given); tail word Z_t one-hot over the 30 words, Z_0 = w, Z_(t+1) = succ(Z_t, g_t); right port
C[x1] = periodic high carry of Z_t; left port A[x0] and H (overflow-step high digit of column x0-1) free.
g_t = 0: X'[i] = (x+a)%10 + (x+b)%10 with x = X[i], a = A[i], b = C[i+1];
g_t = 1: X'[i] = (x+a)%10 + (w+b)%10 with w = X[i-1], b = C[i] (i > x0), X'[x0] = (x+a)%10 + H.
t=T: [y,y+M) equals the tail word Z_T; --tailreturn: Z_T = w.  No constraint on [y-R,y) at t=T.
"""
import sys, time, argparse
sys.path.insert(0, __file__.rsplit('/', 1)[0])
sys.argv += [] if '--m' in sys.argv else ['--m', '1']
import mindep as mi


def words():
    out = []
    for a in range(0, 19, 2):
        base = [9, a, 18 - a]
        for r in range(3):
            out.append(tuple(base[r:] + base[:r]))
    return out


WS = words()


def per_carries(row):
    n = 3; al = [0] * n; c = 0
    for _ in range(4):
        for j in range(n):
            al[j] = c; c = (row[j] + c) // 10
    be = [0] * n; c = 0                      # be[j] = carry entering column j from column j+1
    for _ in range(4):
        for j in reversed(range(n)):
            be[j] = c; c = (row[j] + c) // 10
    return al, be


def succ(row, g):
    al, be = per_carries(row)
    lo = [(row[j] + al[j]) % 10 for j in range(3)]
    hi = [(row[j] + be[j]) % 10 for j in range(3)]
    return tuple(lo[j] + (hi[j - 1] if g else hi[j]) for j in range(3))


S0T = [WS.index(succ(w, 0)) for w in WS]
S1T = [WS.index(succ(w, 1)) for w in WS]


def front(T, s0):
    best = 0
    for j0 in range(30):
        cur = {(j0, 0): 0}
        for t in range(T):
            nb = {}
            for (j, ph), v in cur.items():
                v2 = v + 1 + (1 if WS[j][ph] == 9 else 0)
                for g in (((1 if t % 4 == 0 else 0),) if t < s0 else (0, 1)):
                    k = ((S1T if g else S0T)[j], v2 % 3)
                    if cur is not None and nb.get(k, -1) < v2:
                        nb[k] = v2
            cur = nb
        best = max(best, max(cur.values()))
    return best


ap = argparse.ArgumentParser()
ap.add_argument('--V', type=int, default=2); ap.add_argument('--R', type=int, default=3)
ap.add_argument('--T', type=int, default=120); ap.add_argument('--s0', type=int, default=0)
ap.add_argument('--nones', type=int, default=-1); ap.add_argument('--tailreturn', action='store_true')
ap.add_argument('--nofor', action='store_true'); ap.add_argument('--m', type=int, default=1)
ap.add_argument('--solver', default='kissat404')
a = ap.parse_args()
from pysat.solvers import Solver
w = WS[a.V]; R = a.R; T = a.T; t0 = time.time()
lf = front(T, a.s0); M = 3 * ((lf + 21 + 2) // 3)
y = 10000; x0 = y - R; x1 = y + M
S = Solver(name=a.solver); cnf = mi.CNF(S)
X = {i: cnf.onehot(19) for i in range(x0, x1)}
X0 = dict(X)
for i in range(y, x1):
    cnf.add([X[i][w[(i - y) % 3]]])
Z = cnf.onehot(30); cnf.add([Z[a.V]])
ph1 = (x1 - y) % 3                            # column x1 has phase ph1; C[x1] = carry entering column x1-1 from x1
BET = [per_carries(WS[j])[1][(ph1 - 1) % 3] for j in range(30)]
gam = []
for t in range(T):
    g = cnf.var(); gam.append(g)
    if t < a.s0:
        cnf.add([g if t % 4 == 0 else -g])
    A = {i: cnf.var() for i in range(x0, x1 + 1)}
    C = {i: cnf.var() for i in range(x0, x1 + 1)}
    for j in range(30):
        cnf.add([-Z[j], cnf.bit(C[x1], BET[j])])
    for i in range(x0, x1):
        for x in range(19):
            for b in (0, 1):
                cnf.add([-X[i][x], -cnf.bit(A[i], b), cnf.bit(A[i + 1], 1 if x + b >= 10 else 0)])
                cnf.add([-X[i][x], -cnf.bit(C[i + 1], b), cnf.bit(C[i], 1 if x + b >= 10 else 0)])
    Xn = {i: cnf.onehot(19) for i in range(x0, x1)}
    H = cnf.onehot(10)
    for i in range(x0, x1):
        for x in range(19):
            for aa in (0, 1):
                for b in (0, 1):
                    cnf.add([g, -X[i][x], -cnf.bit(A[i], aa), -cnf.bit(C[i + 1], b), Xn[i][(x + aa) % 10 + (x + b) % 10]])
    for x in range(19):
        for aa in (0, 1):
            for d in range(10):
                cnf.add([-g, -X[x0][x], -cnf.bit(A[x0], aa), -H[d], Xn[x0][(x + aa) % 10 + d]])
    for i in range(x0 + 1, x1):
        for x in range(19):
            for aa in (0, 1):
                for wv in range(19):
                    for b in (0, 1):
                        cnf.add([-g, -X[i][x], -cnf.bit(A[i], aa), -X[i - 1][wv], -cnf.bit(C[i], b),
                                 Xn[i][(x + aa) % 10 + (wv + b) % 10]])
    Zn = cnf.onehot(30)
    for j in range(30):
        cnf.add([-Z[j], g, Zn[S0T[j]]]); cnf.add([-Z[j], -g, Zn[S1T[j]]])
    X = Xn; Z = Zn
for i in range(y, x1):
    for j in range(30):
        cnf.add([-Z[j], X[i][WS[j][(i - y) % 3]]])
if a.tailreturn:
    cnf.add([Z[a.V]])
for t in range(T - 4):
    cnf.add([gam[t + d] for d in range(5)])
for t in range(T - 3):
    cnf.add([-gam[t + d] for d in range(4)])
if a.nones >= 0:
    from pysat.card import CardEnc, EncType
    cc = CardEnc.equals(lits=gam[a.s0:], bound=a.nones, top_id=cnf.nv, encoding=EncType.totalizer)
    for c in cc.clauses:
        cnf.add(c)
    cnf.nv = max(cnf.nv, cc.nv)
if not a.nofor:
    cnf.add([-X0[y - 3 + j][w[j]] for j in range(3)])
print(f'mbfree V={a.V} w={w} R={R} T={T} s0={a.s0} nones={a.nones} tailreturn={a.tailreturn} nofor={a.nofor} front={lf} M={M} '
      f'vars={cnf.nv} clauses={cnf.n} solver={a.solver} enc={time.time()-t0:.0f}s', flush=True)
r = S.solve()
if r:
    m = set(l for l in S.get_model() if l > 0)
    print('SAT free columns', [next(v for v in range(19) if X0[i][v] in m) for i in range(x0, y)],
          'clock', ''.join(str(int(gv in m)) for gv in gam), flush=True)
print('RESULT', 'BF=[sat]' if r else 'BF=[]', 'NONEMPTY' if r else 'EMPTY', f'{time.time()-t0:.0f}s', flush=True)
