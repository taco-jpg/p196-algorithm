import itertools, sys, time
from ctest import brute, check
from cauto2 import solve, lengths
def sweep(b, Ps, m0s, tl):
    t0 = time.time(); n = 0; feas = 0; bad = 0
    for P in Ps:
        for g in itertools.product((0,1), repeat=P):
            G = sum(g)
            if G == 0 or G % 2: continue
            for e in itertools.product((0,1), repeat=P):
                for pos in itertools.combinations(range(P), G//2):
                    v = [1 if t in pos else 0 for t in range(P)]
                    for m0 in m0s:
                        if lengths(list(g), v, m0) is None: continue
                        if time.time() - t0 > tl: return n, feas, bad, 'timeout'
                        n += 1
                        bs = brute(b, list(e), list(g), m0, v)
                        res = solve(b, list(e), list(g), m0, v)
                        f = res is not None and not isinstance(res, tuple)
                        if (bs > 0) != f: bad += 1; print("MISMATCH", b, e, g, m0, v, bs, f)
                        elif f:
                            feas += 1
                            if not check(res, b, list(e), list(g), m0, v): bad += 1; print("BADSOL")
    return n, feas, bad, 'done'
b = int(sys.argv[1]); Ps = [int(x) for x in sys.argv[2].split(',')]; m0s = range(1, int(sys.argv[3])+1)
print(b, Ps, sweep(b, Ps, m0s, float(sys.argv[4])))
