#!/usr/bin/env python3
"""Interior search for a given exterior cycle: find symmetric C0 (width <= cmax) such that the autonomous interior map
H_int, driven by the overflow word s, reproduces the exterior's carry word E at every step and returns to C0 after
k*p steps (k <= kmax).  Each hit is re-checked with the exact mirror (run / cycleOK).
usage: interior_search.py b B0(comma list) s E cmax kmax"""
import sys, itertools, time
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from decouple import H_int, E_of_C, G_ext
from nb_mirror import run, is_cert, cycleOK, gam as GAM


def sym_words(b, c):
    h = (c + 1) // 2
    for half in itertools.product(range(2 * b - 1), repeat=h):
        yield list(half) + list(half[:c // 2][::-1])


def search(b, B0, s, E, cmax, kmax, verbose=True, tl=1e9):
    p = len(s); hits = []; t0 = time.time()
    for c in range(0, cmax + 1):
        n = 0
        for C0 in sym_words(b, c):
            n += 1
            C = C0; ok = True
            for t in range(p * kmax):
                e = E_of_C(b, C)
                if e is None or e != E[t % p]: ok = False; break
                r = H_int(b, C, e, s[t % p])
                if r is None: ok = False; break
                C = r[0]
                if (t + 1) % p == 0 and C == C0:
                    hits.append((C0, (t + 1) // p)); break
            if time.time() - t0 > tl: break
        if verbose: print(f"  width {c}: {n} symmetric starts, hits so far {len(hits)}  ({time.time()-t0:.1f}s)", flush=True)
        if time.time() - t0 > tl: break
    return hits


def confirm(b, B0, C0):
    r = run(b, list(B0), list(C0), maxsteps=5000, maxlen=2000)
    if r[0] != 'cycle': return None
    es = r[1]
    return len(es), is_cert(b, es), cycleOK(b, es, es[0][0], es[0][1]), sum(GAM(b, e[0], e[1]) for e in es), es


if __name__ == '__main__':
    b = int(sys.argv[1]); B0 = [int(x) for x in sys.argv[2].split(',')]; s = [int(c) for c in sys.argv[3]]
    E = [int(c) for c in sys.argv[4]]; cmax = int(sys.argv[5]); kmax = int(sys.argv[6])
    hits = search(b, B0, s, E, cmax, kmax, tl=100)
    for C0, k in hits:
        cf = confirm(b, B0, C0)
        print("HIT C0", C0, "k", k, "confirm:", None if cf is None else cf[:4])
