#!/usr/bin/env python3
"""Interior (center) solver by CP-SAT, given an exterior cycle's carry word E and overflow word s (period p).

Exact model (validated against H_int / the Lean-mirror): the 'padded register' R^(t) = [neutral pads + center + pads]
(symmetric, entries 0..2b-2, neutral = b-1).  One step:  D = digits of R with carry-in E_t, carry-out forced = 1-E_t;
if s_t = 1 append the top digit y_t=(b-1)E_t;  R^(t+1) = D~ + reverse(D~) (so the width grows by s_t).
A center cycle of period P = k*p is  R^(P) = N^V R^(0) N^V  with V = (W_P - W_0)/2   (N = b-1).
usage:  interior_cp.py b s E k W0min W0max [timelimit_per_instance]
"""
import sys, time
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from ortools.sat.python import cp_model


TABLE = True
TUP = {}
def _tuples(b):
    if b not in TUP:
        TUP[b] = [(r, k, (r + k) % b, (r + k) // b) for r in range(2 * b - 1) for k in (0, 1)]
    return TUP[b]


def solve_interior(b, s, E, k, W0, tl=60.0, workers=1):
    p = len(s); P = p * k
    S = [s[t % p] for t in range(P)]
    Et = [E[t % p] for t in range(P)]
    W = [W0]
    for t in range(P): W.append(W[-1] + S[t])
    if (W[P] - W[0]) % 2: return 'skip', None
    V = (W[P] - W[0]) // 2
    _tuples(b)
    m = cp_model.CpModel()
    R = [[m.NewIntVar(0, 2 * b - 2, f"R{t}_{i}") for i in range(W[t])] for t in range(P + 1)]
    for i in range(W0):                               # symmetric start
        m.Add(R[0][i] == R[0][W0 - 1 - i])
    for t in range(P):
        Wt = W[t]
        D = [m.NewIntVar(0, b - 1, f"D{t}_{i}") for i in range(Wt)]
        K = [m.NewBoolVar(f"K{t}_{i}") for i in range(Wt + 1)]
        m.Add(K[0] == Et[t]); m.Add(K[Wt] == 1 - Et[t])
        for i in range(Wt):
            if TABLE:
                m.AddAllowedAssignments([R[t][i], K[i], D[i], K[i + 1]], TUP[b])
            else:
                m.Add(R[t][i] + K[i] == D[i] + b * K[i + 1])
        Dt = list(D)
        if S[t]:
            Dt = Dt + [(b - 1) * Et[t]]
        Wn = W[t + 1]; assert len(Dt) == Wn
        for i in range(Wn):
            m.Add(R[t + 1][i] == Dt[i] + Dt[Wn - 1 - i])
    # closure
    for i in range(V): m.Add(R[P][i] == b - 1); m.Add(R[P][W[P] - 1 - i] == b - 1)
    for i in range(W0): m.Add(R[P][V + i] == R[0][i])
    sol = cp_model.CpSolver()
    sol.parameters.max_time_in_seconds = tl
    sol.parameters.num_workers = workers
    st = sol.Solve(m)
    name = sol.StatusName(st)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return name, [sol.Value(R[0][i]) for i in range(W0)]
    return name, None


if __name__ == '__main__':
    b = int(sys.argv[1]); s = [int(c) for c in sys.argv[2]]; E = [int(c) for c in sys.argv[3]]
    k = int(sys.argv[4]); w0lo = int(sys.argv[5]); w0hi = int(sys.argv[6]); tl = float(sys.argv[7]) if len(sys.argv) > 7 else 60
    for W0 in range(w0lo, w0hi + 1):
        t0 = time.time(); st, C0 = solve_interior(b, s, E, k, W0, tl)
        print(f"W0={W0} k={k}: {st} {C0 if C0 else ''} ({time.time()-t0:.1f}s)", flush=True)
