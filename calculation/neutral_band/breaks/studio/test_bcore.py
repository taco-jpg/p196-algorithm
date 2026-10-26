"""test_bcore.py -- validation of bcore.decide against the Lean-mirror library (each case seconds).  python3 test_bcore.py"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from bcore import decide, patterns


def replay(b, B, p, O, e1s):
    """iterate the autonomous B-system p times with the library: must return to B with the claimed O and e1 streams"""
    cur = list(B)
    for t in range(p):
        nb, u, E1, g = phiB(b, cur)
        if E1 != e1s[t] or g != O[t]:
            return False
        cur = nb
    return cur == list(B)


cases = [(26, 4), (11, 6), (16, 5), (4, 6), (10, 11), (5, 8), (14, 2), (17, 6), (10, 12), (10, 9), (10, 10)]
allok = True
for b, p in cases:
    t0 = time.time()
    tot = {}
    bad = 0
    for O in patterns(p, 1, None):
        st, ns, res = decide(b, p, O, 3_000_000, collect=True)
        tot[st] = tot.get(st, 0) + 1
        if res:
            for e1s, B in res:
                if not replay(b, B, p, O, e1s):
                    bad += 1
    print(f"base {b} p={p}: {tot}  replay failures {bad}  ({time.time()-t0:.1f}s)", flush=True)
    allok &= (bad == 0)
print("ALL REPLAYS OK" if allok else "REPLAY FAILURES")
