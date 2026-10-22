"""Check: prefixPredecessors(p) == {s valid : exists e<=1, forwardPrefix(s,e)=p} for all p, k<=3 (and k=4)."""
import itertools, sys, time
from collections import defaultdict
from defs import forwardPrefix, prefixPredecessors

kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 3
for k in range(1, kmax + 1):
    t0 = time.time()
    inv = defaultdict(set)
    for s in itertools.product(range(19), repeat=k):
        if s[0] == 0:
            continue
        for e in (0, 1):
            inv[tuple(forwardPrefix(list(s), e))].add(s)
    bad = 0
    targets = 0
    # all possible targets: any word of length k with entries 0..18 (also check entries up to 19 to be safe)
    for p in itertools.product(range(20), repeat=k):
        pp = prefixPredecessors(list(p))
        sp = set(tuple(x) for x in pp)
        if len(sp) != len(pp):
            print("duplicate in prefixPredecessors", p)
        if sp != inv.get(p, set()):
            bad += 1
            if bad < 5:
                print("MISMATCH k", k, p, sorted(sp), sorted(inv.get(p, set())))
        targets += 1
    extra = [p for p in inv if any(v > 19 for v in p)]
    print(f"k={k}: targets checked={targets}, mismatches={bad}, forward targets outside 0..19 range={len(extra)}, {time.time()-t0:.1f}s")
