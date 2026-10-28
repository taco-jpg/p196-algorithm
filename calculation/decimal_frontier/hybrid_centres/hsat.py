#!/usr/bin/env python3
"""hsat.py -- CP-SAT search for hybrid centre cycles (register model, single worker).

Model (EXACT; see HYBRID.md): register Q_t (lower half between the neutral band and the core, with arbitrary N-padding at the
bottom and core-valued padding at the top), width w_t = w_0 + t.  rawstep: asc digits da[i]=(Q[i]+a[i])%b with a[0]=e1_t,
desc digits dd[i]=(Q[i]+d[i+1])%b with d[w]=k_t=[c_t>=b] and forced d[0]=e3=1-e1_t;  Q'[i]=da[i]+dd[i] (gam=0, plus top cell z+y)
or Q'[0]=da[0]+(N e1_t), Q'[i]=da[i]+dd[i-1], Q'[w]=z+dd[w-1] (gam=1),  z=c_t-b*k_t+a[w], y=(c_t+k_t)%b.
Cycle of T steps: Q_T = N^A Q_0 c^(T-A) with 0<=A<=floor(sum gam/2);  c_T=c_0 (loop-periodic).
usage: from hsat import solve; solve(b, gam, e1, cs, W0, A)
"""
import sys, time
from ortools.sat.python import cp_model

_TUP = {}
def tuples(b):
    if b not in _TUP:
        _TUP[b] = [(r, k, (r + k) % b, (r + k) // b) for r in range(2 * b - 1) for k in (0, 1)]
    return _TUP[b]

def solve(b, gam, e1, cs, W0, A, tl=120.0, workers=1, seed=0, want_all=False, log=False, fixQ0=None, closure=True, retQT=False):
    """gam,e1: lists of length T (stream over the cycle); cs: list of core values c_t (length T, c_T=c_0 implied).
       Returns (status, Q0 or None)."""
    T = len(gam); N = b - 1
    assert len(e1) == T and len(cs) == T
    ks = [1 if c >= b else 0 for c in cs]
    ys = [(c + k) % b for c, k in zip(cs, ks)]
    m = cp_model.CpModel()
    TUP = tuples(b)
    W = [W0 + t for t in range(T + 1)]
    Q = [[m.NewIntVar(0, 2 * b - 2, f"Q{t}_{i}") for i in range(W[t])] for t in range(T + 1)]
    for t in range(T):
        Wt = W[t]
        a = [m.NewBoolVar(f"a{t}_{i}") for i in range(Wt + 1)]
        d = [m.NewBoolVar(f"d{t}_{i}") for i in range(Wt + 1)]
        da = [m.NewIntVar(0, b - 1, f"da{t}_{i}") for i in range(Wt)]
        dd = [m.NewIntVar(0, b - 1, f"dd{t}_{i}") for i in range(Wt)]
        m.Add(a[0] == e1[t])
        m.Add(d[Wt] == ks[t])
        m.Add(d[0] == 1 - e1[t])
        for i in range(Wt):
            m.AddAllowedAssignments([Q[t][i], a[i], da[i], a[i + 1]], TUP)
            m.AddAllowedAssignments([Q[t][i], d[i + 1], dd[i], d[i]], TUP)
        # z + y top entry
        zexpr = cs[t] - b * ks[t] + a[Wt]          # z = (c+e2) mod b with carry exactly k
        if gam[t] == 0:
            for i in range(Wt):
                m.Add(Q[t + 1][i] == da[i] + dd[i])
            m.Add(Q[t + 1][Wt] == zexpr + ys[t])
        else:
            wconst = N * e1[t]                      # w = N(1-e3) = N*e1
            if Wt >= 1:
                m.Add(Q[t + 1][0] == da[0] + wconst)
                for i in range(1, Wt):
                    m.Add(Q[t + 1][i] == da[i] + dd[i - 1])
                m.Add(Q[t + 1][Wt] == zexpr + dd[Wt - 1])
            else:
                m.Add(Q[t + 1][0] == zexpr + wconst)
    if fixQ0 is not None:
        for i in range(W0): m.Add(Q[0][i] == fixQ0[i])
    if not closure:
        A = None
    # closure:  Q_T = N^A Q_0 c0^(T-A)
    for i in range(A if A is not None else 0):
        m.Add(Q[T][i] == N)
    if A is not None:
        for i in range(W0):
            m.Add(Q[T][A + i] == Q[0][i])
        for j in range(T - A):
            m.Add(Q[T][A + W0 + j] == cs[0])
    sol = cp_model.CpSolver()
    sol.parameters.max_time_in_seconds = tl
    sol.parameters.num_workers = workers
    sol.parameters.random_seed = seed
    sol.parameters.log_search_progress = log
    st = sol.Solve(m)
    name = sol.StatusName(st)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        if retQT: return name, [sol.Value(Q[T][i]) for i in range(W[T])]
        return name, [sol.Value(Q[0][i]) for i in range(W0)]
    return name, None

if __name__ == '__main__':
    pass
