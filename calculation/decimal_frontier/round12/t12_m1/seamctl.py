#!/usr/bin/env python3
"""r12a controls for the seam SAT encoding (seamsat.encode), at the J lengths of round 12.

neg  : J fixed to a random word, full return required          -> expect UNSAT
       (independently: seam_check.cone shows a mismatch for that J)
plant: J free, NO J-return constraint, target = exact 120-step cone image of a
       random J* (computed by cone_rows, independent of the SAT)  -> expect SAT,
       and the J found must reproduce the image under cone_rows.
wret : right background replaced by W itself (pure W band continues), J free,
       J-return required, target = initial window               -> expect SAT
       (J = the W continuation is a genuine return).
"""
import sys, random, time, argparse
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from seamsat import encode, cone_rows, alpha_at, beta_at
from seam_check import B, W, J0, us, cone
from pysat.solvers import Solver

def run(mode, Lj, Ui, seed, x0=64, margin=170):
    rnd = random.Random(seed)
    U = us()[Ui]
    if mode == "wret":
        R = list(W[Lj % 9:] + W[:Lj % 9]); margin = 250
    else:
        R = list(U)
    Js = [rnd.randrange(19) for _ in range(Lj)]
    if mode == "wret":
        Js = [W[(j) % 9] for j in range(Lj)]  # J0=160 is a W boundary (160-34=126=14*9)
    pref = list(B) + list(W) * 14 + Js + R * (700 // len(R))
    rows = cone_rows(pref)
    x1 = J0 + Lj + margin
    assert all(len(r) > x1 + 3 for r in rows), min(len(r) for r in rows)
    right = [beta_at(rows[t], x1) for t in range(120)]
    init = {i: pref[i] for i in range(x0, x1) if not (J0 <= i < J0 + Lj)}
    if mode == "neg":
        for j in range(Lj): init[J0 + j] = Js[j]
    if mode == "plant":
        final = {i: rows[120][i] for i in range(x0, x1)}
    else:
        final = {i: pref[i] for i in range(x0, x1) if not (J0 <= i < J0 + Lj)}
    S = Solver(name="cadical195")
    E, P, sig, P0 = encode(x0, x1, init, rows, right, final, solver=S)
    if mode in ("neg", "wret"):
        for j in range(Lj):
            for v in range(19): E.cl.append([-P0[J0 + j][v], P[J0 + j][v]])
    t0 = time.time(); r = S.solve(); dt = time.time() - t0
    out = {"mode": mode, "Lj": Lj, "U": U, "seed": seed, "sat": r, "solve_s": round(dt, 1), "J*": Js}
    if r:
        m = set(l for l in S.get_model() if l > 0)
        Jw = [next(v for v in range(19) if P0[J0 + j][v] in m) for j in range(Lj)]
        out["J_found"] = Jw
        if mode == "plant":
            rr = cone_rows(list(B) + list(W) * 14 + Jw + R * (700 // len(R)))
            out["replay_matches_target"] = all(rr[120][i] == final[i] for i in range(x0, x1))
        if mode == "wret":
            rr = cone_rows(list(B) + list(W) * 14 + Jw + R * (700 // len(R)))
            out["replay_returns"] = all(rr[120][i] == (list(B) + list(W) * 14 + Jw + R * 80)[i] for i in range(x0, x1))
    if mode == "neg":
        p = cone(list(B) + list(W) * 14 + Js + list(U) * 60)
        tg = list(B) + list(W) * 14 + Js + list(U) * 65
        out["cone_first_mismatch_relJ"] = next((i - J0 for i in range(len(p)) if p[i] != tg[i]), None)
    print(out, flush=True)
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode"); ap.add_argument("--Lj", type=int, default=10)
    ap.add_argument("--U", type=int, default=0); ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    run(a.mode, a.Lj, a.U, a.seed)
