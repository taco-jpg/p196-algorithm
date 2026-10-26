"""ccycle_padded.py -- C-block periodic orbit given the bit streams (e1(t), gam(t)) of a B-cycle.  CP-SAT.

Model (validated: recovers the exact C of the Lean certificates in bases 4, 16, 26 and a valid C in base 17):
  * C is a symmetric word surrounded by the neutral vacuum (b-1) on both sides.  Fixed array of Mc cells; cells 0,1 and Mc-2,Mc-1 are vacuum.
  * Left-aligned absolute frame: C'_j sits at the same index j as C_j (trimming = cells that become b-1).  The mirror axis of the array at time t
    is Z_t/2 with Z_t = Z_0 + (number of overflows before t); so no length / trim schedule has to be enumerated.
    After one full period the pattern is the same shifted right by k = (sum gam)/2.
  * lam_j / rho_j = polarity of nearest non-neutral cell below / above j; lam_{0}=e1(t), rho_{top}=e1(t) (the carry that the wire delivers
    on both sides), and the emitted carry e2 = rho_{-1} must be 1 - e1(t).
  * cell rule (no overflow):  C'_j = 2C_j + lam_j + rho_j - b(lam_{j+1} + rho_{j-1})
    cell rule (overflow)   :  C'_j = C_j + lam_j - b lam_{j+1} + C_{j-1} + rho_{j-1} - b rho_{j-2}      (C_{-1}= vacuum)
solve_C(b, e1s, gams, Z0, tl, workers) -> ('OPTIMAL'|'INFEASIBLE'|'UNKNOWN', C_at_time_0 or None).
Z0 = (index of first real cell + index of last real cell) at time 0, in a frame whose first allowed real cell is index 2;
  half-length capacity grows with Z0, so scan Z0 upward (c0 ~ Z0 - 3 if the left edge sits at index 2)."""
from ortools.sat.python import cp_model


def solve_C(b, e1s, gams, Z0, tl=60, workers=1, hint=None):
    n = b - 1
    p = len(e1s)
    k2 = sum(gams)
    if k2 % 2:
        return 'ODD', None
    k = k2 // 2
    Mc = Z0 + k + 5
    Z = [Z0]
    for t in range(p):
        Z.append(Z[-1] + gams[t])
    m = cp_model.CpModel()
    V = [[m.NewIntVar(0, 2 * n, '') for j in range(Mc)] for t in range(p + 1)]
    for t in range(p + 1):
        for j in range(Mc):
            if j < 2 or j >= Mc - 2:
                m.Add(V[t][j] == n)
            mj = Z[t] - j
            if 0 <= mj < Mc:
                if mj > j:
                    m.Add(V[t][j] == V[t][mj])
            else:
                m.Add(V[t][j] == n)
    for j in range(Mc):
        if j + k < Mc:
            m.Add(V[p][j + k] == V[0][j])
        else:
            m.Add(V[0][j] == n)
        if j < k:
            m.Add(V[p][j] == n)
    for t in range(p):
        e1 = e1s[t]
        g = gams[t]
        H = [m.NewBoolVar('') for j in range(Mc)]
        Nn = [m.NewBoolVar('') for j in range(Mc)]
        for j in range(Mc):
            x = V[t][j]
            m.Add(x >= b).OnlyEnforceIf(H[j]); m.Add(x <= n).OnlyEnforceIf(H[j].Not())
            m.Add(x == n).OnlyEnforceIf(Nn[j]); m.Add(x != n).OnlyEnforceIf(Nn[j].Not())
            m.AddImplication(Nn[j], H[j].Not())
        lam = [m.NewBoolVar('') for j in range(Mc + 1)]
        m.Add(lam[0] == e1)
        for j in range(Mc):
            z = m.NewBoolVar(''); m.AddMultiplicationEquality(z, [Nn[j], lam[j]]); m.Add(lam[j + 1] == H[j] + z)
        R = [m.NewBoolVar('') for q in range(Mc + 1)]        # R[q] = rho_{q-1}
        m.Add(R[Mc] == e1)
        for j in range(Mc - 1, -1, -1):
            z = m.NewBoolVar(''); m.AddMultiplicationEquality(z, [Nn[j], R[j + 1]]); m.Add(R[j] == H[j] + z)
        m.Add(R[0] == 1 - e1)                                 # e2 = 1 - e1
        rho = lambda j: R[j + 1]
        for j in range(Mc):
            if not g:
                expr = 2 * V[t][j] + lam[j] + rho(j) - b * (lam[j + 1] + rho(j - 1))
            elif j == 0:
                expr = V[t][0] + lam[0] - b * lam[1] + n * e1
            else:
                expr = V[t][j] + lam[j] - b * lam[j + 1] + V[t][j - 1] + rho(j - 1) - b * rho(j - 2)
            m.Add(V[t + 1][j] == expr)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = tl
    s.parameters.num_workers = workers
    st = s.Solve(m)
    nm = s.StatusName(st)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        rows = [[s.Value(x) for x in V[t]] for t in range(p)]
        return 'OPTIMAL', rows
    return nm, None


def real_part(b, row):
    n = b - 1
    lo = 0
    hi = len(row)
    while lo < hi and row[lo] == n: lo += 1
    while hi > lo and row[hi - 1] == n: hi -= 1
    return row[lo:hi]
