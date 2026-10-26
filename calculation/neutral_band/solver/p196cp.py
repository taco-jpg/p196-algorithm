#!/usr/bin/env python3
"""Constraint encoding of 'closed chain of p neutral-band edges in base b with a given length schedule'.

See README_STUDIO.txt.  Exact mirror of A120Template/A120Certificate (Lean) via
/home/claude/p196-algorithm/calculation/neutral_band_search.py (imported as `mirror`, used only to
re-check decoded solutions with cycleOK).

SCHEDULE.  A cyclic sequence of interface lengths  S = ((n_0,m_0),...,(n_{p-1},m_{p-1})),
n_k = |B_k|, m_k = |C_k|.  Facts that make this a complete parametrisation of the cycle shape:
  * C_k is a palindrome in every cycle (nextC is a palindrome, trimming both ends equally);
  * |nextC| = m + gam, |C'| = m + gam - 2v   =>  gam_k = (m_{k+1} - m_k) mod 2, v_k = (m_k+gam_k-m_{k+1})/2
  * |nextB| = n + gam, |B'| = n + gam - u     =>  u_k = n_k + gam_k - n_{k+1}
  * so over a closed cycle sum(u) = sum(gam), sum(v) = sum(gam)/2, hence sum(u+v) = 1.5*sum(gam) >= sum(gam):
    EVERY closed chain of valid edges already satisfies the cycleOK gain condition.
"""
import sys, os, time, json, itertools
_here = os.path.dirname(os.path.abspath(__file__))
for _d in (os.environ.get("P196_MIRROR_DIR"), os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."), os.path.join(_here, "mirror_copy")):
    if _d and os.path.exists(os.path.join(_d, "neutral_band_search.py")):
        sys.path.insert(0, _d); break
import neutral_band_search as mirror

# ------------------------------------------------------------------ schedules
def derive(S):
    """returns list of (gam,u,v) per step, or None if the length schedule is not realisable."""
    p = len(S); out = []
    for k in range(p):
        n, m = S[k]; n2, m2 = S[(k + 1) % p]
        if n < 0 or m < 0: return None
        gam = (m2 - m) % 2
        u = n + gam - n2
        t = m + gam - m2
        if u < 0 or t < 0 or t % 2: return None
        out.append((gam, u, t // 2))
    return out

def canon(S):
    """canonical rotation (lexicographically least)"""
    p = len(S)
    return min(tuple(S[i:] + S[:i]) for i in range(p)) if p else tuple(S)

# ------------------------------------------------------------------ IR model
class Model:
    """tiny solver-independent IR: bounded integer variables + linear range constraints"""
    def __init__(self):
        self.vars = []      # (name, lo, hi, forbidden-values)
        self.cons = []      # (dict idx->coef, lo, hi)
        self.index = {}
    def var(self, name, lo, hi, forbid=()):
        i = len(self.vars); self.vars.append((name, lo, hi, tuple(forbid))); self.index[name] = i; return i
    def const(self, c): return ({}, c)
    def add(self, terms, lo, hi):
        """lo <= sum coef*var + const <= hi ; terms = ({idx:coef}, const)"""
        d, c = terms
        self.cons.append((dict(d), lo - c, hi - c))
    def eq(self, t1, t2):
        """t1 == t2  (both terms)"""
        d = dict(t1[0])
        for i, a in t2[0].items():
            d[i] = d.get(i, 0) - a
            if d[i] == 0: del d[i]
        c = t1[1] - t2[1]
        if not d:
            if c != 0: self.cons.append(({}, 1, 0))   # trivially infeasible
            return
        self.cons.append((d, -c, -c))

def lin(*parts):
    """build ({idx:coef}, const) from (coef, idx) pairs and ints"""
    d, c = {}, 0
    for p in parts:
        if isinstance(p, tuple) and not isinstance(p[0], dict):
            a, i = p; d[i] = d.get(i, 0) + a
        elif isinstance(p, tuple):
            for i, a in p[0].items(): d[i] = d.get(i, 0) + a
            c += p[1]
        else: c += p
    return ({i: a for i, a in d.items() if a}, c)
def scale(t, a): return ({i: a * x for i, x in t[0].items()}, a * t[1])
def plus(*ts):
    d, c = {}, 0
    for t in ts:
        for i, a in t[0].items(): d[i] = d.get(i, 0) + a
        c += t[1]
    return ({i: a for i, a in d.items() if a}, c)
def V(i): return ({i: 1}, 0)
def K(c): return ({}, c)

# ------------------------------------------------------------------ encoding
def encode(b, S, maximal=True, extra_nonzero_B0=True):
    """Model whose solutions are exactly the closed chains with length schedule S (see module doc)."""
    P = derive(S)
    if P is None: return None
    p = len(S); M = Model(); top = 2 * (b - 1)
    # state variables
    Bv, Cv = [], []
    for k in range(p):
        n, m = S[k]
        Bv.append([M.var(f"B{k}_{i}", 1 if (i == 0 and extra_nonzero_B0) else 0, top) for i in range(n)])
        Cv.append([M.var(f"C{k}_{j}", 0, top) for j in range((m + 1) // 2)])
    def Cf(k, j):
        m = S[k][1]; return V(Cv[k][min(j, m - 1 - j)])
    for k in range(p):
        n, m = S[k]; gam, u, v = P[k]; n2, m2 = S[(k + 1) % p]; k2 = (k + 1) % p
        # carries: low chain over B, over C, high chain over reversed B
        cb = [K(0)] + [V(M.var(f"cb{k}_{i}", 0, 1)) for i in range(1, n + 1)]
        cc = [cb[n]] + [V(M.var(f"cc{k}_{j}", 0, 1)) for j in range(1, m + 1)]
        cr = [cc[m]] + [V(M.var(f"cr{k}_{i}", 0, 1)) for i in range(1, n + 1)]
        e1, e2 = cb[n], cc[m]
        M.eq(plus(e1, e2), K(1))                      # Hyp.flip: e1 != e2 (both are bits)
        M.eq(cr[n], K(gam))                           # scheduled overflow = actual final carry
        def digit(x, cin, cout):                      # digit = x + cin - b*cout in [0,b-1]
            return plus(x, cin, scale(cout, -b))
        DB, DC, DR = [], [], []
        for i in range(n):
            d = digit(V(Bv[k][i]), cb[i], cb[i + 1]); M.add(d, 0, b - 1); DB.append(d)
        for j in range(m):
            d = digit(Cf(k, j), cc[j], cc[j + 1]); M.add(d, 0, b - 1); DC.append(d)
        for i in range(n):
            d = digit(V(Bv[k][n - 1 - i]), cr[i], cr[i + 1]); M.add(d, 0, b - 1); DR.append(d)
        xd = scale(plus(K(1), scale(e1, -1)), b - 1)   # (b-1)(1-e1)
        yd = scale(plus(K(1), scale(e2, -1)), b - 1)   # (b-1)(1-e2)
        # nextB, nextC exactly as in A120Template
        if gam == 0:
            nb = [plus(DB[i], DR[n - 1 - i]) for i in range(n)]
            nc = [plus(DC[j], DC[m - 1 - j]) for j in range(m)]
        else:
            a = DB + [xd]; r = [K(1)] + [DR[n - i] for i in range(1, n + 1)]
            nb = [plus(a[i], r[i]) for i in range(n + 1)]
            ac = DC + [yd]
            nc = [plus(ac[j], ac[m - j]) for j in range(m + 1)]
        assert len(nb) == n + gam and len(nc) == m + gam
        # trimming: nextB = B' ++ (b-1)^u ; nextC = (b-1)^v ++ C' ++ (b-1)^v
        for i in range(n2): M.eq(nb[i], V(Bv[k2][i]))
        for i in range(n2, n + gam): M.eq(nb[i], K(b - 1))
        for j in range(v): M.eq(nc[j], K(b - 1))
        for j in range((m2 + 1) // 2): M.eq(nc[v + j], V(Cv[k2][j]))
        if maximal:
            # canonical (maximal) trimming: WLOG, see README.  Forbid value b-1 at the trim boundary.
            if n2 > 0:
                i = Bv[k2][n2 - 1]; nm, lo, hi, fb = M.vars[i]; M.vars[i] = (nm, lo, hi, fb + (b - 1,))
            if m2 >= 2:
                i = Cv[k2][0]; nm, lo, hi, fb = M.vars[i]; M.vars[i] = (nm, lo, hi, fb + (b - 1,))
    return M

# ------------------------------------------------------------------ backends
def solve_cpsat(M, time_limit=None, workers=1, log=False, mem_mb=None):
    from ortools.sat.python import cp_model
    cm = cp_model.CpModel(); X = []
    for (nm, lo, hi, fb) in M.vars:
        if fb:
            vals = [x for x in range(lo, hi + 1) if x not in fb]
            if not vals: return "UNSAT", None
            X.append(cm.NewIntVarFromDomain(cp_model.Domain.FromValues(vals), nm))
        else: X.append(cm.NewIntVar(lo, hi, nm))
    for d, lo, hi in M.cons:
        if not d:
            if not (lo <= 0 <= hi): return "UNSAT", None
            continue
        e = sum(a * X[i] for i, a in d.items())
        if lo == hi: cm.Add(e == lo)
        else: cm.AddLinearConstraint(e, lo, hi)
    s = cp_model.CpSolver(); s.parameters.num_workers = workers; s.parameters.max_memory_in_mb = 6000
    if time_limit: s.parameters.max_time_in_seconds = time_limit
    s.parameters.log_search_progress = log
    st = s.Solve(cm)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE): return "SAT", [s.Value(x) for x in X]
    if st == cp_model.INFEASIBLE: return "UNSAT", None
    return "UNKNOWN", None

def solve_z3(M, time_limit=None):
    import z3
    s = z3.Solver()
    if time_limit: s.set("timeout", int(time_limit * 1000))
    X = []
    for (nm, lo, hi, fb) in M.vars:
        x = z3.Int(nm); X.append(x); s.add(x >= lo, x <= hi)
        for f in fb: s.add(x != f)
    for d, lo, hi in M.cons:
        e = sum(a * X[i] for i, a in d.items()) if d else z3.IntVal(0)
        if lo == hi: s.add(e == lo)
        else: s.add(e >= lo, e <= hi)
    r = s.check()
    if r == z3.sat:
        m = s.model(); return "SAT", [m.eval(x, model_completion=True).as_long() for x in X]
    if r == z3.unsat: return "UNSAT", None
    return "UNKNOWN", None

def solve(b, S, backend="cpsat", maximal=True, time_limit=None, workers=1):
    t0 = time.time(); M = encode(b, S, maximal=maximal)
    if M is None: return {"status": "INVALID_SCHEDULE", "time": 0.0}
    if backend == "cpsat": st, sol = solve_cpsat(M, time_limit, workers)
    else: st, sol = solve_z3(M, time_limit)
    res = {"status": st, "time": round(time.time() - t0, 3), "nvars": len(M.vars), "ncons": len(M.cons)}
    if st == "SAT":
        val = {M.vars[i][0]: sol[i] for i in range(len(M.vars))}
        res["certificate"] = decode(b, S, val)
    return res

# ------------------------------------------------------------------ decode + mirror check
def decode(b, S, val):
    p = len(S); P = derive(S); st = []
    for k in range(p):
        n, m = S[k]
        B = [val[f"B{k}_{i}"] for i in range(n)]
        Ch = [val[f"C{k}_{j}"] for j in range((m + 1) // 2)]
        C = [Ch[min(j, m - 1 - j)] for j in range(m)]
        st.append((B, C))
    es = []
    for k in range(p):
        B, C = st[k]; B2, C2 = st[(k + 1) % p]; gam, u, v = P[k]
        es.append((B, C, B2, C2, u, v))
    ok = mirror.cycleOK(b, es, st[0][0], st[0][1])
    return {"cycleOK_mirror": bool(ok), "base": b, "p": p, "start_B": st[0][0], "start_C": st[0][1],
            "edges": [list(map(lambda x: x, e)) for e in es], "sum_gam": sum(g for g, _, _ in P),
            "sum_gain": sum(e[4] + e[5] for e in es)}

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("b", type=int); ap.add_argument("sched", help='e.g. "1,2;2,3;1,3;2,4" = (n,m) pairs')
    ap.add_argument("--backend", default="cpsat"); ap.add_argument("--nonmax", action="store_true")
    ap.add_argument("--tl", type=float, default=100)
    a = ap.parse_args()
    S = tuple(tuple(int(x) for x in t.split(",")) for t in a.sched.split(";"))
    print(json.dumps(solve(a.b, S, a.backend, not a.nonmax, a.tl)))
