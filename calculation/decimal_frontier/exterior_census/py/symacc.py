#!/usr/bin/env python3
# symacc.py (W5): SYMBOLIC (BDD) decision of the decimal exterior question for ONE overflow word g, using W3's position-automaton
# encoding (py/symfwd_w3.py = copy of w3_formats/code/symfwd.py, same transition semantics as W5's bx.cpp; cross-checked below).
#   fwd : forward reachability from the start state, stop at first level that meets ACC  (-> ACCEPT) or when no new state (-> EXHAUSTED)
#   bwd : backward co-reachability from ACC; HIT iff a successor of the start state lies in the cone (-> ACCEPT), CLOSED => EXHAUSTED
# ACC = { L_t + H_t = 1 for all t, Y_i = (b-1) L_{t_i} }  (same as bx.cpp accepting()).
# usage: symacc.py b word [-mode fwd|bwd|both] [-maxlev N] [-part] [-quiet] [-sec S] [-e]
import sys, time
sys.path.insert(0, '/home/claude/research/w5_exterior/py')
from symfwd_w3 import Sym

def acc_set(S):
    bdd = S.bdd; b = S.b
    r = bdd.true
    for t in range(S.p):
        one = S.lit(S.Ln[t], 1) & S.lit(S.Hn[t], 0)
        zero = S.lit(S.Ln[t], 0) & S.lit(S.Hn[t], 1)
        if S.g[t]:
            one = one & S.num(S.Yn[t], b - 1)
            zero = zero & S.num(S.Yn[t], 0)
        r = r & (one | zero)
    return r

def main():
    b = int(sys.argv[1]); gs = sys.argv[2]
    mode = 'bwd'; maxlev = 10**9; part = False; quiet = False; sec = 1e18
    i = 3
    while i < len(sys.argv):
        a = sys.argv[i]
        if a == '-mode': mode = sys.argv[i+1]; i += 1
        elif a == '-maxlev': maxlev = int(sys.argv[i+1]); i += 1
        elif a == '-part': part = True
        elif a == '-quiet': quiet = True
        elif a == '-sec': sec = float(sys.argv[i+1]); i += 1
        i += 1
    t0 = time.time()
    S = Sym(b, gs); p = S.p; bdd = S.bdd
    G = sum(S.g)
    if part:
        C1 = S.prep_slots(True); C = S.prep_slots(False)
        img1 = lambda F: S.image_part(F, C1)
        img = lambda F: S.image_part(F, C)
        T = None
    else:
        T1 = S.build_T(True); T = S.build_T(False)
        img1 = lambda F: S.image(F, T1)
        img = lambda F: S.image(F, T)
    print(f"built transition t={time.time()-t0:.1f}s", flush=True)
    Hst = [1 if c else 0 for c in S.g]
    start = S.state_cube([0]*p, Hst, [1]*G)
    ACC = acc_set(S)
    inv = {sv: pv for pv, sv in S.ren.items()}
    def pre_mono(B):
        Bp = bdd.let(inv, B)
        return bdd.exist(S.pvars, bdd.apply('and', T, Bp))
    Cs = S.prep_slots(False) if part else None
    def pre_part(B):
        acc = bdd.let(inv, B)
        for t in range(p):
            acc = acc & Cs[t]
            q = [S.Lpn[t], S.Hpn[t]] + (S.Ypn[t] if S.g[t] else [])
            if t > 0: q = q + S.Xn[t]
            acc = bdd.exist(q, acc)
        return bdd.exist(S.Xn[0], acc)
    pre = pre_part if part else pre_mono
    results = {}
    if mode in ('fwd', 'both'):
        F = img1(start); visited = start | F; Fr = F; lev = 1; status = None
        while True:
            n = S.count(Fr)
            if n == 0: status = 'EXHAUSTED'; break
            if (Fr & ACC) != bdd.false: status = 'ACCEPT'; break
            if not quiet or lev % 10 == 0:
                print(f"  fwd lev={lev} new={n} total={S.count(visited)} nodesFr={len(Fr)} nodesVis={len(visited)} t={time.time()-t0:.0f}s", flush=True)
            if lev >= maxlev: status = 'STOP'; break
            if time.time()-t0 > sec: status = 'CAPPED_time'; break
            new = img(Fr) & ~visited
            visited = visited | new; Fr = new; lev += 1
        print(f"FWD p={p} G={G} g={gs} {status} depth={lev} visited={S.count(visited)} nodes={len(visited)} t={time.time()-t0:.0f}s", flush=True)
        results['fwd'] = status
    if mode in ('bwd', 'both'):
        succ0 = img1(start)
        Back = ACC; Fr = ACC; lev = 0; status = None
        if (succ0 & Back) != bdd.false: status = 'ACCEPT'
        while status is None:
            if lev >= maxlev: status = 'STOP'; break
            if time.time()-t0 > sec: status = 'CAPPED_time'; break
            P = pre(Fr)
            new = P & ~Back
            if new == bdd.false: status = 'EXHAUSTED'; break
            Back = Back | new; Fr = new; lev += 1
            if (succ0 & Back) != bdd.false: status = 'ACCEPT'
            if not quiet or lev % 5 == 0:
                print(f"  bwd lev={lev} new={S.count(new)} cone={S.count(Back)} nodesCone={len(Back)} nodesFr={len(Fr)} t={time.time()-t0:.0f}s", flush=True)
        print(f"BWD p={p} G={G} g={gs} {status} depth={lev} cone={S.count(Back)} nodes={len(Back)} t={time.time()-t0:.0f}s", flush=True)
        results['bwd'] = status
    print("RES", gs, results, flush=True)

if __name__ == '__main__':
    main()
