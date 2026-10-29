#!/usr/bin/env python3
"""All-width 240-step moving-q endpoint obstruction for the R18 phase-4 J24/C3 root.
Uses the repository's exact affine folded-pairword engine from R30; no width samples
are used for the symbolic result. Independent bigint controls live in moving_q_endpoint.cpp.
"""
from __future__ import annotations
import argparse
import importlib.util
import sys
from math import lcm
from pathlib import Path

B = [10,4,7,5,13,6,11,1,9,16,16,18,10,9,4,8,1,7,0,2,15,15,9,7,7,10,17,14,18,8,6,6,18,4]
W = [8,1,15,4,0,5,5,18,4]
J = [17,5,5,9,6,6,6,14,5,11,7,10,14,7,8,15,9,6,4,18,9,10,17,2]
C = [4,14,4]
QMIN = KMIN = 512

def load_engine(path: Path):
    spec = importlib.util.spec_from_file_location("r30_parametric", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load symbolic engine: {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod

def all_u3():
    out = []
    for a in range(0, 19, 2):
        base = [9, a, 18-a]
        for shift in range(3):
            u = tuple(base[shift:] + base[:shift])
            if u not in out:
                out.append(u)
    assert len(out) == 30
    return out

def symbolic_at(E, engine, seq, pos):
    start = E()
    for r in seq:
        end = start + r.length()
        if engine.choose(start, pos, QMIN, KMIN) == start and engine.choose(end, pos + E(c=1), QMIN, KMIN) == pos + E(c=1):
            delta = pos - start
            m = len(r.word)
            if delta.q % m or delta.k % m:
                raise engine.CannotProve(f"queried coefficient phase depends on q/k: {delta} mod {m}")
            return r.word[delta.val(QMIN, KMIN) % m]
        start = end
    raise engine.CannotProve(f"position outside symbolic output: {pos}")

def prefix_mismatch(E, engine, seq, expected):
    aa = engine.clean(seq)
    bb = engine.clean(expected)
    pos = E()
    while bb:
        if not aa:
            raise engine.CannotProve("actual output shorter than required prefix")
        a, b = aa[0], bb[0]
        amt = engine.choose(a.length(), b.length(), QMIN, KMIN)
        period = lcm(len(a.word), len(b.word)) if amt.q or amt.k else max(1, amt.c)
        cap = min(amt.val(QMIN, KMIN), period)
        for h in range(cap):
            x = a.word[h % len(a.word)]
            y = b.word[h % len(b.word)]
            if x != y:
                absolute = pos + E(c=h)
                offset = absolute - E(q=9, c=34)
                if offset.q or offset.k:
                    raise engine.CannotProve(f"mismatch offset is not constant: {offset}")
                return {"offset": offset.c, "absolute": str(absolute), "observed": x, "expected": y}
        if cap < period and (amt.q or amt.k):
            raise engine.CannotProve("periodic comparison interval too short for uniform proof")
        pos += amt
        aa = engine.eat(a, amt, QMIN, KMIN) + aa[1:]
        bb = engine.eat(b, amt, QMIN, KMIN) + bb[1:]
    return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--engine", type=Path, default=None,
                        help="override R30 engine path for local differential testing")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    engine_path = args.engine or (root / "calculation/new_structures/R30/parametric.py")
    engine = load_engine(engine_path)
    E = engine.E
    allowed = set(all_u3())
    w_triples = {tuple(W[(i+j) % len(W)] for j in range(3)) for i in range(len(W))}
    assert not (allowed & w_triples), (allowed & w_triples)
    results = []
    for U in all_u3():
        current = engine.tpl(B, W, J, list(U), C)
        gam = []
        for t in range(240):
            current, g = engine.step(current, QMIN, KMIN)
            gam.append(g)
            if len(current) > 10000:
                raise engine.CannotProve(f"symbolic atom explosion: {len(current)}")
        assert gam == [1,0,0,0] * 60 and sum(gam) == 60, (U, gam)
        mm = prefix_mismatch(E, engine, current, [engine.run(B), engine.R(tuple(W), engine.Q)])
        if mm is None or mm["offset"] not in (-24, -22):
            raise engine.CannotProve(f"unexpected W-prefix mismatch for {U}: {mm}")
        window = {s: symbolic_at(E, engine, current, E(q=9, c=34+s)) for s in range(-26, 16)}
        best_match = 0
        for s in range(-26, -1):
            for u2 in allowed:
                n = 0
                for h in range(12):
                    if window[s+h] != u2[h % 3]:
                        break
                    n += 1
                best_match = max(best_match, n)
        if best_match > 3:
            raise engine.CannotProve(f"target U3 prefix matched more than 3 coefficients: {U}, {best_match}")
        results.append((U, mm["offset"], best_match, len(current)))
        print(f"U={U} first_W_defect={mm['offset']} max_target_U_prefix={best_match} atoms={len(current)}")
    assert len(results) == 30 and max(r[2] for r in results) == 3
    print("ALL_WIDTH_MOVING_Q_NO_RETURN_PASS U=30 q,k>=512 epochs=2 steps=240 W_mismatch_offsets={-22,-24} max_local_U_prefix_match=3 W_triples_intersection=0 atoms_max=" + str(max(r[3] for r in results)))

if __name__ == "__main__":
    main()
