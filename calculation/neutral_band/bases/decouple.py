#!/usr/bin/env python3
"""Decoupled exterior / interior form of the neutral one-band map (exact, derived from A120Template).

Facts used (all follow from the definitions of hyp / nextB / nextC in neutral_band_search.py):
  * hyp demands e1(B) != e2(B,C); both are carries in {0,1}, hence e2 = 1 - e1.  With e2 forced, nextB, u and the
    overflow bit gam depend on B ALONE  ->  the exterior orbit is autonomous:  B_{t+1} = G_b(B_t).
  * nextC depends on C, on the carry-in e1 = e1(B) and on gam only (y = (b-1)*e1).  Moreover the flip condition
    "carry-out of C with carry-in e1 is 1-e1" holds iff  e1 = [val(C) < b^|C| - 1]  and val(C) != b^|C| - 1.
    So the interior is autonomous too, with ONE exogenous input: the overflow word gam_t.
  * Cycle bookkeeping: length closure forces sum(u) = sum(gam) and 2*sum(v) = sum(gam) hence
    sumGain = 1.5 * sumGam: 'gain >= overflows' is automatic for any closed cycle; the real content is closure.
"""
import sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from nb_mirror import (norm, e1 as E1, DB, gam as GAM, xd, hyp, step, cycleOK, _lean_certs, trim, run, is_cert)


def val(b, w):
    return sum(v * b ** i for i, v in enumerate(w))


def G_ext(b, B):
    """Exterior map with e2 := 1 - e1. Returns (B2, u, E, gam) or None if head is 0 / bound violated."""
    if any(v > 2 * (b - 1) or v < 0 for v in B) or (B and B[0] == 0):
        return None
    e1 = E1(b, B); e2 = 1 - e1
    dB = DB(b, B)
    dR, g = norm(b, B[::-1], e2)
    x = (b - 1) * (1 - e1)
    rdR = dR[::-1]
    if g == 0:
        nb = [p + q for p, q in zip(dB, rdR)]
    else:
        nb = [p + q for p, q in zip(dB + [x], [1] + rdR)]
    u = 0
    while nb and nb[-1] == b - 1:
        nb = nb[:-1]; u += 1
    return nb, u, e1, g


def H_int(b, C, E, g):
    """Interior map with carry-in E, e2 = 1-E, overflow g. Returns (C2, v) or None if carry-out != 1-E."""
    dC, co = norm(b, C, E)
    if co != 1 - E:
        return None
    y = (b - 1) * E
    if g == 0:
        nc = [p + q for p, q in zip(dC, dC[::-1])]
    else:
        nc = [p + q for p, q in zip(dC + [y], [y] + dC[::-1])]
    v = 0
    while len(nc) >= 2 and nc[0] == b - 1 and nc[-1] == b - 1:
        nc = nc[1:-1]; v += 1
    return nc, v


def E_of_C(b, C):
    """the carry-in bit the interior itself forces (None = break: value is exactly b^c - 1)."""
    s, cap = val(b, C), b ** len(C)
    if s == cap - 1: return None
    return 1 if s < cap - 1 else 0


def check_certs():
    """For every kernel-checked certificate: (i) Lean edge lists obey the length bookkeeping, (ii) the canonical
    (maximally trimmed) run from its base state is a cycle and G_ext / H_int / E_of_C reproduce each of its edges."""
    ok = True
    for b, es in _lean_certs():
        sg_l = sum(GAM(b, e[0], e[1]) for e in es); su_l = sum(e[4] for e in es); sv_l = sum(e[5] for e in es)
        bk = (su_l == sg_l) and (2 * sv_l == sg_l)
        r = run(b, es[0][0], es[0][1])
        assert r[0] == 'cycle'
        cyc = r[1]
        good = True; sg = su = sv = 0
        for (B, C, B2, C2, u, v) in cyc:
            x = G_ext(b, B)
            if x is None or (x[0], x[1]) != (B2, u): good = False
            E, g = x[2], x[3]
            h = H_int(b, C, E, g)
            if h is None or (h[0], h[1]) != (C2, v): good = False
            if E_of_C(b, C) != E: good = False
            sg += g; su += u; sv += v
        bk2 = (su == sg) and (2 * sv == sg)
        print(f"base {b:2d}: Lean edges {len(es)} (sumGam {sg_l}, sumU {su_l}, sumV {sv_l}, bookkeeping {bk}); "
              f"canonical cycle {len(cyc)} edges (sumGam {sg}, sumU {su}, sumV {sv}, bookkeeping {bk2}); "
              f"G_ext/H_int/E_of_C reproduce every canonical edge: {good}")
        ok &= good and bk and bk2
    print("DECOUPLING VALIDATION", "PASSED" if ok else "FAILED")
    return ok


def ext_bits(b, B, maxsteps=200):
    """follow the autonomous exterior orbit; return ('cycle', [(B,E,gam,u)...]) / ('break',t) / ('long',)"""
    seen = {}; seq = []
    cur = tuple(B)
    for t in range(maxsteps):
        if cur in seen:
            return 'cycle', seq[seen[cur]:]
        seen[cur] = t
        r = G_ext(b, list(cur))
        if r is None: return 'break', t
        seq.append((cur, r[2], r[3], r[1]))
        cur = tuple(r[0])
    return 'long', None


if __name__ == '__main__':
    sys.exit(0 if check_certs() else 1)
