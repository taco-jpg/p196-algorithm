"""CP-SAT model for B-cycles (the autonomous B-system).  Python 3 + ortools.
usage: python3 bcp.py b n0 g u  [timelimit]      e.g.  python3 bcp.py 26 8 01 01
 g, u are strings of length p (gam_t and u_t patterns); n_{t+1}=n_t+g_t-u_t must return to n0.
Finds B_0..B_{p-1} with B_p = B_0 (e1 stream is free: the solver decides).  Prints solution or INFEASIBLE."""
import sys
from ortools.sat.python import cp_model

def solve_b(b, n0, g, u, tl=60, workers=1, enum_all=False, extra=None):
    p = len(g)
    ns = [n0]
    for t in range(p): ns.append(ns[-1] + int(g[t]) - int(u[t]))
    if ns[-1] != n0 or min(ns) < 0: return 'badlen', None
    m = cp_model.CpModel()
    B = [[m.NewIntVar(0, 2*b-2, f"B{t}_{i}") for i in range(ns[t] + int(g[t]) + 1)] for t in range(p)]  # B[t][i], i<ns[t] used
    e = [m.NewBoolVar(f"e{t}") for t in range(p)]
    for t in range(p):
        n = ns[t]; gt = int(g[t])
        l = [m.NewBoolVar(f"l{t}_{i}") for i in range(n+1)]
        m.Add(l[0] == 0)
        DB = [m.NewIntVar(0, b-1, f"DB{t}_{i}") for i in range(n)]
        for i in range(n): m.Add(B[t][i] + l[i] == DB[i] + b*l[i+1])
        m.Add(e[t] == l[n])
        h = [m.NewBoolVar(f"h{t}_{i}") for i in range(n+1)]
        m.Add(h[0] == 1 - e[t])
        DR = [m.NewIntVar(0, b-1, f"DR{t}_{i}") for i in range(n)]
        for i in range(n): m.Add(B[t][n-1-i] + h[i] == DR[i] + b*h[i+1])
        m.Add(h[n] == gt)
        nxt = ns[t+1]; tgt = B[(t+1) % p]
        for k in range(n + gt):
            first = DB[k] if k < n else (b-1) - (b-1)*e[t]
            if gt == 1: second = 1 if k == 0 else DR[n-k]
            else: second = DR[n-1-k]
            val = first + second
            if k < nxt: m.Add(tgt[k] == val)
            else: m.Add(val == b-1)
        if n > 0: m.Add(B[t][0] >= 1)
    if extra: extra(m, B, e, ns)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = workers
    r = s.Solve(m)
    name = s.StatusName(r)
    if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        sol = [[s.Value(B[t][i]) for i in range(ns[t])] for t in range(p)]
        return name, (sol, [s.Value(x) for x in e])
    return name, None

if __name__ == "__main__":
    b = int(sys.argv[1]); n0 = int(sys.argv[2]); g = sys.argv[3]; u = sys.argv[4]
    tl = float(sys.argv[5]) if len(sys.argv) > 5 else 60
    st, sol = solve_b(b, n0, g, u, tl)
    print(st, sol)
