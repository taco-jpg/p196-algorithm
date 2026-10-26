#!/usr/bin/env python3
"""Enumerate periodic orbits of the autonomous exterior map G_b on all words B with |B| <= Lmax.
usage: ext_cycles.py b Lmax  -> prints the cycles (period, lengths, E-word, gam-word, u-word)"""
import sys, itertools, time
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from decouple import G_ext

def all_states(b, Lmax):
    yield ()
    for L in range(1, Lmax + 1):
        for first in range(1, 2 * b - 1):
            for rest in itertools.product(range(2 * b - 1), repeat=L - 1):
                yield (first,) + rest

def cycles(b, Lmax):
    fate = {}      # state -> 'x' (escape/break) or cycle id
    cyc_list = []
    nxt = {}
    for s in all_states(b, Lmax):
        if s in fate: continue
        path = []; pos = {}
        cur = s
        while True:
            if cur in fate:
                res = fate[cur]; break
            if cur in pos:
                res = len(cyc_list); cyc_list.append(path[pos[cur]:]); break
            pos[cur] = len(path); path.append(cur)
            r = G_ext(b, list(cur))
            if r is None or len(r[0]) > Lmax:
                res = 'x'; break
            cur = tuple(r[0])
        for p in path: fate[p] = res
    return cyc_list

def describe(b, cyc):
    E = ''; Gm = ''; U = ''
    for s in cyc:
        r = G_ext(b, list(s)); E += str(r[2]); Gm += str(r[3]); U += str(r[1])
    return len(cyc), [len(s) for s in cyc], E, Gm, U

if __name__ == '__main__':
    b = int(sys.argv[1]); Lmax = int(sys.argv[2]); t0 = time.time()
    cl = cycles(b, Lmax)
    print(f"base {b} Lmax {Lmax}: {len(cl)} exterior cycles ({time.time()-t0:.1f}s)")
    for c in sorted(cl, key=lambda c: (len(c), c)):
        p, ls, E, Gm, U = describe(b, c)
        print(f"  period {p} lens {ls} E={E} gam={Gm} u={U} first={list(c[0])}")
