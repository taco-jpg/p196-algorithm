#!/usr/bin/env python3
"""hsurv.py -- max survival time S(W) of a hybrid state of REAL width <= W (no closure), by CP-SAT.
Register Q_t of width W+t whose leading N-run + trailing c_t-run have total length >= t (so the trimmed C has width <= W).
usage: hsurv.py <stream> <loop 0|18|6|2> <phase s> <t0 stream offset> <W> <Tmax> [tl]"""
import sys, time
from ortools.sat.python import cp_model
from hsat import tuples

def survive(b, gam, e1, cs, W, tl=60.0, wantQ=False):
    """gam,e1,cs of length T; returns status (FEASIBLE => some state of real width<=W survives T steps)"""
    T = len(gam); N = b - 1
    ks = [1 if c >= b else 0 for c in cs]
    ys = [(c + k) % b for c, k in zip(cs, ks)]
    m = cp_model.CpModel(); TUP = tuples(b)
    Wd = [W + t for t in range(T + 1)]
    Q = [[m.NewIntVar(0, 2 * b - 2, f"Q{t}_{i}") for i in range(Wd[t])] for t in range(T + 1)]
    for t in range(T):
        Wt = Wd[t]
        a = [m.NewBoolVar(f"a{t}_{i}") for i in range(Wt + 1)]
        d = [m.NewBoolVar(f"d{t}_{i}") for i in range(Wt + 1)]
        da = [m.NewIntVar(0, b - 1, f"da{t}_{i}") for i in range(Wt)]
        dd = [m.NewIntVar(0, b - 1, f"dd{t}_{i}") for i in range(Wt)]
        m.Add(a[0] == e1[t]); m.Add(d[Wt] == ks[t]); m.Add(d[0] == 1 - e1[t])
        for i in range(Wt):
            m.AddAllowedAssignments([Q[t][i], a[i], da[i], a[i + 1]], TUP)
            m.AddAllowedAssignments([Q[t][i], d[i + 1], dd[i], d[i]], TUP)
        zexpr = cs[t] - b * ks[t] + a[Wt]
        if gam[t] == 0:
            for i in range(Wt): m.Add(Q[t + 1][i] == da[i] + dd[i])
            m.Add(Q[t + 1][Wt] == zexpr + ys[t])
        else:
            wconst = N * e1[t]
            if Wt >= 1:
                m.Add(Q[t + 1][0] == da[0] + wconst)
                for i in range(1, Wt): m.Add(Q[t + 1][i] == da[i] + dd[i - 1])
                m.Add(Q[t + 1][Wt] == zexpr + dd[Wt - 1])
            else:
                m.Add(Q[t + 1][0] == zexpr + wconst)
    # bounded real width at every time t=1..T : leading N-run + trailing c_t-run >= t
    for t in range(1, T + 1):
        Wt = Wd[t]; ct = cs[t % T] if t < T else cs[0]
        # cs for time t: use the loop continuation
        isN = [m.NewBoolVar(f"iN{t}_{i}") for i in range(Wt)]
        isC = [m.NewBoolVar(f"iC{t}_{i}") for i in range(Wt)]
        for i in range(Wt):
            m.Add(Q[t][i] == N).OnlyEnforceIf(isN[i]); m.Add(Q[t][i] != N).OnlyEnforceIf(isN[i].Not())
            m.Add(Q[t][i] == ct).OnlyEnforceIf(isC[i]); m.Add(Q[t][i] != ct).OnlyEnforceIf(isC[i].Not())
        pre = [m.NewBoolVar(f"pre{t}_{i}") for i in range(Wt)]
        suf = [m.NewBoolVar(f"suf{t}_{i}") for i in range(Wt)]
        for i in range(Wt):
            if i == 0: m.Add(pre[0] == isN[0])
            else: m.AddBoolAnd([pre[i - 1], isN[i]]).OnlyEnforceIf(pre[i]); m.AddBoolOr([pre[i - 1].Not(), isN[i].Not()]).OnlyEnforceIf(pre[i].Not())
            j = Wt - 1 - i
            if i == 0: m.Add(suf[Wt - 1] == isC[Wt - 1])
            else: m.AddBoolAnd([suf[j + 1], isC[j]]).OnlyEnforceIf(suf[j]); m.AddBoolOr([suf[j + 1].Not(), isC[j].Not()]).OnlyEnforceIf(suf[j].Not())
        m.Add(sum(pre) + sum(suf) >= t)
    sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = tl; sol.parameters.num_workers = 1
    st = sol.Solve(m); name = sol.StatusName(st)
    if wantQ and st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return name, [sol.Value(Q[0][i]) for i in range(W)]
    return name, None

if __name__ == '__main__':
    from runsat import stream
    name = sys.argv[1]; lp = sys.argv[2]; s = int(sys.argv[3]); t0 = int(sys.argv[4]); W = int(sys.argv[5]); Tmax = int(sys.argv[6])
    tl = float(sys.argv[7]) if len(sys.argv) > 7 else 60
    loops = {'0': [0], '18': [18], '6': [6, 12], '2': [2, 4, 8, 16, 14, 10]}[lp]
    cyc = stream(name); p = len(cyc)
    for T in range(1, Tmax + 1):
        gam = [cyc[(t0 + t) % p][1] for t in range(T)]; e1 = [cyc[(t0 + t) % p][2] for t in range(T)]
        cs = [loops[(s + t) % len(loops)] for t in range(T)]
        t1 = time.time(); st, Q0 = survive(10, gam, e1, cs, W, tl, True)
        print(name, lp, s, t0, 'W', W, 'T', T, st, Q0, f"{time.time()-t1:.1f}s", flush=True)
        if st != 'OPTIMAL' and st != 'FEASIBLE': break
