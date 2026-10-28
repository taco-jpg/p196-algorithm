#!/usr/bin/env python3
# symbwd.py : SYMBOLIC (BDD) backward co-reachability of uniform-band target states in the position automaton (see symfwd.py).
# For each uniform loop / phase target T*: Back_0 = {T*}; Back_{j+1} = Back_j u Pre(Back_j); stop when fixpoint or when a successor of the
# start state lies in Back (HIT).  Fixpoint without hit = the stream is DECIDED (no uniform band reachable) -- exactly like the explicit cone.
# usage: symbwd.py b word [-maxlev N] [-quiet] [-only loop0:ph]
import sys, time
from symfwd import Sym, uniform_targets
import dd.cudd as cudd

def main():
    b = int(sys.argv[1]); gs = sys.argv[2]
    maxlev = 10**9; quiet = False; only = None; part = False; union = False; full = False
    i = 3
    while i < len(sys.argv):
        a = sys.argv[i]
        if a == '-maxlev': maxlev = int(sys.argv[i+1]); i += 1
        elif a == '-quiet': quiet = True
        elif a == '-part': part = True
        elif a == '-union': union = True
        elif a == '-full': full = True
        elif a == '-only': only = tuple(int(x) for x in sys.argv[i+1].split(':')); i += 1
        i += 1
    t0 = time.time()
    S = Sym(b, gs)
    p = S.p
    T1 = S.build_T(True); T = S.build_T(False)
    print(f"built T: nodes first={len(T1)} std={len(T)} t={time.time()-t0:.1f}s", flush=True)
    Hst = [1 if c else 0 for c in S.g]
    start = S.state_cube([0]*p, Hst, [1]*sum(S.g))
    succ0 = S.image(start, T1)
    if succ0 == S.bdd.false:
        print("STARTDEAD"); return
    bdd = S.bdd
    inv = {sv: pv for pv, sv in S.ren.items()}   # unprimed -> primed
    def pre_mono(B):
        Bp = bdd.let(inv, B)
        G = bdd.apply('and', T, Bp)
        return bdd.exist(S.pvars, G)
    Cs = S.prep_slots(False) if part else None
    def pre_part(B):
        acc = bdd.let(inv, B)
        for t in range(p):
            acc = acc & Cs[t]
            q = [S.Lpn[t], S.Hpn[t]] + (S.Ypn[t] if S.g[t] else [])
            if t > 0:
                q = q + S.Xn[t]
            acc = bdd.exist(q, acc)
        return bdd.exist(S.Xn[0], acc)
    pre = pre_part if part else pre_mono
    tg = uniform_targets(S)
    if union:
        U = bdd.false
        for (_, _, tc) in tg: U = U | tc
        tg = [(-1, -1, U)]
    res = []
    # complement symmetry: cone(CS(tau)) = CS(cone(tau)), so one cone serves both tau and CS(tau)
    csd = S.cs_dict(); dom = S.dom(); domU = S.dom(False)
    def cs(u): return bdd.let(csd, u)
    if not union:
        chk = cs(T) & dom
        assert chk == (T & dom), "complement symmetry check FAILED"
    succ0c = (cs(succ0) & domU) if not union else None
    cspartner = {}
    if not union:
        for i, (l0, ph, tc) in enumerate(tg):
            ctc = cs(tc) & domU
            for j, (l1, ph1, tc1) in enumerate(tg):
                if tc1 == ctc: cspartner[i] = j
    handled = set()
    for i, (l0, ph, tc) in enumerate(tg):
        if i in handled: continue
        j = cspartner.get(i, None) if not union else None
        if only and (l0, ph) != only and not (j is not None and (tg[j][0], tg[j][1]) == only): continue
        handled.add(i)
        if j is not None: handled.add(j)
        Back = tc; Fr = tc; lev = 0; status = None
        pair = (j is not None and j != i)
        hl1 = hl2 = None   # first level at which each member of the CS-orbit is hit
        def upd():
            nonlocal hl1, hl2
            if hl1 is None and (succ0 & Back) != bdd.false: hl1 = lev
            if pair and hl2 is None and (succ0c & Back) != bdd.false: hl2 = lev
        upd()
        while True:
            if hl1 is not None and (hl2 is not None or not pair): status = 'HIT'; break
            if lev >= maxlev: status = 'STOP'; break
            P = pre(Back if full else Fr)
            new = P & ~Back
            if new == bdd.false: status = 'CLOSED'; break
            Back = Back | new; Fr = new; lev += 1
            upd()
            if not quiet or lev % 5 == 0:
                print(f"  loop0={l0} ph={ph} lev={lev} new={S.count(new)} total={S.count(Back)} nodesBack={len(Back)} nodesFr={len(Fr)} t={time.time()-t0:.0f}s", flush=True)
        cone = S.count(Back)
        def st(h):
            return f"HIT@{h}" if h is not None else ('CLOSED' if status == 'CLOSED' else 'unresolved')
        print(f"TARGET p={p} g={gs} loop0={l0} ph={ph} {st(hl1)} depth={lev} cone={cone} nodes={len(Back)} t={time.time()-t0:.0f}s", flush=True)
        if pair:
            print(f"TARGET p={p} g={gs} loop0={tg[j][0]} ph={tg[j][1]} {st(hl2)} depth={lev} cone={cone} nodes={len(Back)} t={time.time()-t0:.0f}s CS-partner", flush=True)
        res.append(status)
    print("RESULT", gs, ' '.join(res))

if __name__ == '__main__':
    main()
