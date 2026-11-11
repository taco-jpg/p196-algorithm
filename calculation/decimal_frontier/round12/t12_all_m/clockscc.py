#!/usr/bin/env python3
"""r12f2: clock rigidity of a pure U3 band under ARBITRARY clock sequences.

Row graph: nodes = 3-periodic band rows w (absolute phase fixed), edges w -> F_g(w) for g in {0,1} (exact periodic
folded successor, same formula as cut.py / cones_m.F: lo_i=(w_i+alpha_i)%10, hi_i=(w_i+beta_(i+1))%10 with the
unique periodic carries; P'_i = lo_i+hi_i (g=0), lo_i+hi_(i-1) (g=1)).  A row with no non-9 (9,9,9) has no unique
periodic carry: all four carry choices are added as successors (superset).
For each of the 30 U: forward closure from U, backward closure to U inside it, SCC(U) = both.
Claim checked: SCC(U) = the 120 standard rows U_0..U_119 and for every t the non-standard successor
F_(1-gamma_t)(U_t) is outside SCC(U)  =>  every closed walk through U is a power of the standard cycle.
Also reported: size of the forward closure, whether (9,9,9) is reachable, max cyclic run of 9s in reachable rows.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from cones_m import F, us, G


def succ(w):
    if all(x == 9 for x in w):
        out = set()
        for al in (0, 1):
            for be in (0, 1):
                v = (9 + al) % 10 + (9 + be) % 10
                out.add(((v, v, v), 0)); out.add(((v, v, v), 1))
        return out
    return {(F(w, 0), 0), (F(w, 1), 1)}


def run9(w):
    if all(x == 9 for x in w):
        return 99
    best = 0
    for s in range(3):
        r = 0
        while r < 3 and w[(s + r) % 3] == 9:
            r += 1
        best = max(best, r)
    return best


allok = True
for idx, U in enumerate(us()):
    U = tuple(U)
    fwd = {U}; st = [U]; edges = {}
    while st:
        w = st.pop(); edges[w] = succ(w)
        for v, g in edges[w]:
            if v not in fwd:
                fwd.add(v); st.append(v)
    rev = {}
    for w, es in edges.items():
        for v, g in es:
            rev.setdefault(v, set()).add(w)
    bwd = {U}; st = [U]
    while st:
        w = st.pop()
        for p in rev.get(w, ()):
            if p not in bwd:
                bwd.add(p); st.append(p)
    scc = fwd & bwd
    std = [U]
    for t in range(120):
        std.append(F(std[-1], G(t)))
    assert std[120] == U
    cyc = set(std[:120])
    off = [t for t in range(120) if F(std[t], 1 - G(t)) in scc]
    ok = (scc == cyc) and not off and len(cyc) == 120
    allok &= ok
    print(f'U{idx} {U}: forward closure {len(fwd)} rows, (9,9,9) reachable: {(9,9,9) in fwd}, max 9-run in reachable rows '
          f'{max(run9(w) for w in fwd)}, |SCC| = {len(scc)}, SCC == standard 120-cycle: {scc == cyc}, '
          f'non-standard successors inside SCC at t = {off}  -> {"OK" if ok else "FAIL"}', flush=True)
print('ALL OK' if allok else 'NOT ALL OK')
