#!/usr/bin/env python3
"""r12f3: clock rigidity of the rooted exterior for an ARBITRARY window length c and horizon T (generalises wclock.py
of r12f2; same encoding: imports wclock.mux / mdefect helpers).
Instance W^(c)_(T,n): window [0,c) with initial row (B0 W0^inf)[0:c]; inlet beta_c(t) FREE for every t < T; clock
COMPUTED (gamma_t = beta_0(t)); exact folded law with the root rule; at t = T the window equals its initial row;
exactly n overflows in [0,T) (--count n; default T/4; --nocount: any number); some gamma_t != [t%4==0] (mode rigid).
c = 34+9q gives wclock.py W_m(q) (T = 120m, n = 30m).  Monotone: W^(c+1) SAT => W^(c) SAT (restriction).
Modes: rigid | nodev (no deviation clause) | refcheck (inlet = reference carries of a long reference orbit, positive
control, SAT with the standard clock expected)."""
import sys, time, argparse
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import mdefect as md
import wclock as wc


def build(E, c, T, port=None):
    row = {i: (md.B0[i] if i < 34 else md.W0[(i - 34) % 9]) for i in range(c)}
    P0 = dict(row); gams = []
    for t in range(T):
        al = {0: 0}
        for i in range(c - 1):
            al[i + 1] = md.carry(E, row[i], al[i])
        bv = (E.new(),)
        if port is not None:
            E.add([md.lit(bv, port[t])])
        be = {c: bv}
        for i in range(c - 1, -1, -1):
            be[i] = md.carry(E, row[i], be[i + 1])
        g = be[0]; gams.append(g)
        hi = {i: md.digit(E, row[i], be[i + 1]) for i in range(c)}
        new = {}
        for i in range(c):
            lo = md.digit(E, row[i], al[i])
            new[i] = md.psum(E, lo, wc.mux(E, g, hi[i], 1 if i == 0 else hi[i - 1]))
        row = new
    return P0, row, gams


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["rigid", "nodev", "refcheck"])
    ap.add_argument("--c", type=int, required=True)
    ap.add_argument("--T", type=int, required=True)
    ap.add_argument("--count", type=int, default=None)
    ap.add_argument("--nocount", action="store_true")
    ap.add_argument("--solver", default="kissat404")
    a = ap.parse_args()
    from pysat.solvers import Solver
    T = a.T; c = a.c; t0 = time.time()
    n = None if a.nocount else (a.count if a.count is not None else T // 4)
    port = None
    if a.mode == "refcheck":
        qq = (c + T + 200) // 9 + 2; K = T // 2 + 60
        orb = md.orbit(md.realize(md.make_word(md.us()[0], [], [8, 8], qq, K)), T, c + 5)
        port = [orb[t]["c"][orb[t]["L"] - c] for t in range(T)]
        assert all(orb[t]["g"] == (t % 4 == 0) for t in range(T))
    S = Solver(name=a.solver); E = md.Enc(S)
    P0, row, gams = build(E, c, T, port=port)
    for i in range(c):
        md.equal(E, row[i], P0[i])
    const_ones = sum(1 for g in gams if isinstance(g, int) and g == 1)
    const_dev = [t for t, g in enumerate(gams) if isinstance(g, int) and g != (t % 4 == 0)]
    var_t = [t for t, g in enumerate(gams) if not isinstance(g, int)]
    if n is not None:
        from pysat.card import CardEnc, EncType
        bound = n - const_ones
        if var_t and 0 <= bound <= len(var_t):
            cc = CardEnc.equals(lits=[gams[t][0] for t in var_t], bound=bound, top_id=E.nv, encoding=EncType.totalizer)
            for cl in cc.clauses:
                E.add(cl)
            E.nv = max(E.nv, cc.nv)
        elif not (bound == 0 and not var_t):
            z = E.new(); E.add([z]); E.add([-z])
    if a.mode == "rigid" and not const_dev:
        E.add([(-gams[t][0] if t % 4 == 0 else gams[t][0]) for t in var_t])
    print(f"wclock3 {a.mode} c={c} T={T} count={n} clock constant for t < {var_t[0] if var_t else T} "
          f"(constant deviations: {const_dev}) vars={E.nv} clauses={E.ncl} solver={a.solver} enc={time.time()-t0:.0f}s", flush=True)
    r = S.solve()
    if r:
        mm = set(x for x in S.get_model() if x > 0)
        cl = "".join(str(g if isinstance(g, int) else int(g[0] in mm)) for g in gams)
        print("SAT clock", cl, "ones", cl.count("1"), "deviations at", [t for t in range(T) if int(cl[t]) != (t % 4 == 0)], flush=True)
    print("RESULT", "W=[sat]" if r else "W=[]", "NONEMPTY" if r else "EMPTY", f"{time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
