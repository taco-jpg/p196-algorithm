#!/usr/bin/env python3
"""hwin.py -- BOTTOM-WINDOW relaxation of the hybrid cycle problem (proves non-existence for ALL widths when infeasible).
Window = bottom K cells of the (padded) register, present at all times.  Free input: descending carry into cell K-1 from above
(d[K](t) free bits).  Closure restricted to the window:  v_i(T)=N (i<A),  v_{A+i}(T)=v_i(0) (A+i<K).
EXACT consequence of the register model of hsat.py for any register of width >= K (every hybrid cycle of width<=W0 is represented by
a register of any larger width, see HYBRID.md)."""
import sys, time
from ortools.sat.python import cp_model
from hsat import tuples

def solve_window(b, gam, e1, K, A, tl=120.0, closure=True):
    T = len(gam); N = b - 1
    m = cp_model.CpModel(); TUP = tuples(b)
    Q = [[m.NewIntVar(0, 2 * b - 2, f"Q{t}_{i}") for i in range(K)] for t in range(T + 1)]
    for t in range(T):
        a = [m.NewBoolVar(f"a{t}_{i}") for i in range(K + 1)]
        d = [m.NewBoolVar(f"d{t}_{i}") for i in range(K + 1)]     # d[K] free
        da = [m.NewIntVar(0, b - 1, f"da{t}_{i}") for i in range(K)]
        dd = [m.NewIntVar(0, b - 1, f"dd{t}_{i}") for i in range(K)]
        m.Add(a[0] == e1[t]); m.Add(d[0] == 1 - e1[t])
        for i in range(K):
            m.AddAllowedAssignments([Q[t][i], a[i], da[i], a[i + 1]], TUP)
            m.AddAllowedAssignments([Q[t][i], d[i + 1], dd[i], d[i]], TUP)
        if gam[t] == 0:
            for i in range(K): m.Add(Q[t + 1][i] == da[i] + dd[i])
        else:
            wconst = N * e1[t]
            m.Add(Q[t + 1][0] == da[0] + wconst)
            for i in range(1, K): m.Add(Q[t + 1][i] == da[i] + dd[i - 1])
    if closure:
        for i in range(min(A, K)): m.Add(Q[T][i] == N)
        for i in range(K - A): m.Add(Q[T][A + i] == Q[0][i])
    sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = tl; sol.parameters.num_workers = 1
    st = sol.Solve(m)
    return sol.StatusName(st)

if __name__ == '__main__':
    from runsat import stream
    name = sys.argv[1]; k = int(sys.argv[2]); Kmax = int(sys.argv[3])
    cyc = stream(name); p = len(cyc); T = p * k
    gam = [cyc[t % p][1] for t in range(T)]; e1 = [cyc[t % p][2] for t in range(T)]
    S = sum(gam)
    for A in range(0, S // 2 + 1):
        res = []
        for K in range(1, Kmax + 1):
            t0 = time.time(); st = solve_window(10, gam, e1, K, A, 60)
            res.append((K, st[:3], round(time.time() - t0, 1)))
            if st == 'INFEASIBLE': break
        print(name, 'k', k, 'A', A, res, flush=True)
