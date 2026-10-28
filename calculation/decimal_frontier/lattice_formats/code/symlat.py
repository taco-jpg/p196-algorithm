#!/usr/bin/env python3
# symlat.py b word dumpfile [-maxlev N] [-each] : symbolic backward co-reachability from the union of all lattice states listed in a
# latenum dump (self-mirror lattices of the word).  CLOSED without start successor in the cone  => none of those lattices is reachable.
import sys, time
from symfwd import Sym

def load(dumpfile, S):
    lats = []
    f = open(dumpfile)
    lines = f.read().splitlines()
    i = 0
    ng = sum(S.g)
    while i < len(lines):
        if lines[i].startswith('LAT'):
            parts = lines[i].split(); m = int(parts[1]); sts = []
            for k in range(m):
                v = [int(x) for x in lines[i + 1 + k].split()]
                Lq, Hq, Y = v[0], v[1], v[2:2 + ng]
                sts.append(S.state_cube([(Lq >> t) & 1 for t in range(S.p)], [(Hq >> t) & 1 for t in range(S.p)], Y))
            lats.append(sts); i += m + 2
        else:
            i += 1
    return lats

def main():
    b = int(sys.argv[1]); gs = sys.argv[2]; dumpfile = sys.argv[3]
    maxlev = 10**9; each = False
    for i, a in enumerate(sys.argv):
        if a == '-maxlev': maxlev = int(sys.argv[i + 1])
        if a == '-each': each = True
    t0 = time.time()
    S = Sym(b, gs); p = S.p; bdd = S.bdd
    T1 = S.build_T(True); T = S.build_T(False)
    Hst = [1 if c else 0 for c in S.g]
    start = S.state_cube([0] * p, Hst, [1] * sum(S.g))
    succ0 = S.image(start, T1)
    inv = {sv: pv for pv, sv in S.ren.items()}
    def pre(B):
        return bdd.exist(S.pvars, bdd.apply('and', T, bdd.let(inv, B)))
    lats = load(dumpfile, S)
    print(f"lattices={len(lats)} states={sum(len(x) for x in lats)} T nodes={len(T)} t={time.time()-t0:.0f}s", flush=True)
    groups = [(f"lat{i}", [x]) for i, x in enumerate(lats)] if each else [("ALL", lats)]
    for name, gl in groups:
        U = bdd.false
        for L in gl:
            for c in L: U = U | c
        Back = U; Fr = U; lev = 0
        st = 'HIT' if (succ0 & Back) != bdd.false else None
        while st is None:
            if lev >= maxlev: st = 'STOP'; break
            new = pre(Fr) & ~Back
            if new == bdd.false: st = 'CLOSED'; break
            Back = Back | new; Fr = new; lev += 1
            if (succ0 & Back) != bdd.false: st = 'HIT'
            if lev % 5 == 0:
                print(f"  {name} lev={lev} new={S.count(new)} total={S.count(Back)} nodes={len(Back)} t={time.time()-t0:.0f}s", flush=True)
        print(f"LATCONE {name} {st} depth={lev} cone={S.count(Back)} nodes={len(Back)} t={time.time()-t0:.0f}s", flush=True)

if __name__ == '__main__':
    main()
