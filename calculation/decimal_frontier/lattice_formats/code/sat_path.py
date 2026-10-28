#!/usr/bin/env python3
"""CP-SAT (1 worker) search for an exterior path start -> lattice state in the position automaton.
usage: sat_path.py b g K [--lattice rows_json | --uniform l0 ph] [--time T] [--target j]
Model mirrors code/bwd_common.h transitions(): positions k=0..K-1 each with column x[k][t]; state (L,H,Y) at k=0..K."""
import sys, json, argparse, time
from ortools.sat.python import cp_model

def phi_rows(r, gam, b):
    m = len(r)
    i0 = next((i for i in range(m) if r[i] != b - 1), None)
    if i0 is None: return None
    A = [0] * m; D = [0] * m
    A[(i0 + 1) % m] = 1 if r[i0] >= b else 0
    for s in range(1, m):
        i = (i0 + s) % m; j = (i0 + s + 1) % m; A[j] = (r[i] + A[i]) // b
    D[(i0 - 1) % m] = 1 if r[i0] >= b else 0
    for s in range(1, m):
        i = (i0 - s) % m; j = (i0 - s - 1) % m; D[j] = (r[i] + D[i]) // b
    e = [(r[i] + A[i]) % b for i in range(m)]; f = [(r[i] + D[i]) % b for i in range(m)]
    out = [e[i] + (f[(i - 1) % m] if gam else f[i]) for i in range(m)]
    return out, A, D, e, f

def lattice_states(rows, g, b):
    """rows[t][i], i in Z_m. returns list over positions k of dict(L=[..p], H=[..p], Y={t:val})"""
    p = len(rows); m = len(rows[0]); st = []
    info = [phi_rows(rows[t], g[t], b) for t in range(p)]
    for k in range(m):
        L = [info[t][1][k] for t in range(p)]
        H = [(rows[t][k] + info[t][2][k]) // b for t in range(p)]
        Y = {t: (rows[t][(k - 1) % m] + info[t][2][(k - 1) % m]) % b for t in range(p) if g[t]}
        st.append(dict(L=L, H=H, Y=Y))
    return st

def uniform_state(b, g, l0, ph):
    p = len(g)
    loop = []; x = l0
    while True:
        loop.append(x); c = 1 if x >= b else 0; x = 2 * ((x + c) % b)
        if x == l0: break
    u = [loop[(t + ph) % len(loop)] for t in range(p)]
    L = [1 if v >= b else 0 for v in u]; H = L[:]
    Y = {t: (u[t] + H[t]) % b for t in range(p) if g[t]}
    return dict(L=L, H=H, Y=Y), u

def solve(b, g, K, target, tlimit=60, seed=1, first_nonzero=True, log=False):
    p = len(g); M = cp_model.CpModel()
    x = [[M.NewIntVar(0, 2 * b - 2, f"x{k}_{t}") for t in range(p)] for k in range(K)]
    d = [[M.NewIntVar(0, b - 1, f"d{k}_{t}") for t in range(p)] for k in range(K)]
    f = [[M.NewIntVar(0, b - 1, f"f{k}_{t}") for t in range(p)] for k in range(K)]
    L = [[M.NewBoolVar(f"L{k}_{t}") for t in range(p)] for k in range(K + 1)]
    H = [[M.NewBoolVar(f"H{k}_{t}") for t in range(p)] for k in range(K + 1)]
    Y = [[(M.NewIntVar(0, b - 1, f"Y{k}_{t}") if g[t] else None) for t in range(p)] for k in range(K + 1)]
    for t in range(p):
        M.Add(L[0][t] == 0); M.Add(H[0][t] == g[t])
        if g[t]: M.Add(Y[0][t] == 1)
        M.Add(L[K][t] == target['L'][t]); M.Add(H[K][t] == target['H'][t])
        if g[t]: M.Add(Y[K][t] == target['Y'][t])
    for k in range(K):
        for t in range(p):
            tn = (t + 1) % p
            M.Add(x[k][t] + L[k][t] == b * L[k + 1][t] + d[k][t])
            M.Add(x[k][t] + H[k + 1][t] == b * H[k][t] + f[k][t])
            if g[t]:
                M.Add(x[k][tn] == d[k][t] + Y[k][t])
                M.Add(Y[k + 1][t] == f[k][t])
            else:
                M.Add(x[k][tn] == d[k][t] + f[k][t])
            if k == 0 and first_nonzero: M.Add(x[k][t] >= 1)
    S = cp_model.CpSolver(); S.parameters.num_workers = 1; S.parameters.max_time_in_seconds = tlimit; S.parameters.random_seed = seed
    S.parameters.log_search_progress = log
    r = S.Solve(M)
    name = S.StatusName(r)
    if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        cols = [[S.Value(x[k][t]) for t in range(p)] for k in range(K)]
        return name, cols, S.WallTime()
    return name, None, S.WallTime()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("b", type=int); ap.add_argument("g"); ap.add_argument("K", type=int)
    ap.add_argument("--uniform", nargs=2, type=int); ap.add_argument("--rows"); ap.add_argument("--target", type=int, default=0)
    ap.add_argument("--time", type=float, default=60); ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    g = [int(c) for c in a.g]
    if a.uniform: tgt, u = uniform_state(a.b, g, a.uniform[0], a.uniform[1])
    else:
        rows = json.loads(a.rows); tgt = lattice_states(rows, g, a.b)[a.target]
    name, cols, wt = solve(a.b, g, a.K, tgt, a.time, a.seed)
    print(name, "K=%d" % a.K, "wall=%.1fs" % wt)
    if cols: print(json.dumps(cols))
