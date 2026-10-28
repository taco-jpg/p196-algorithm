#!/usr/bin/env python3
"""random exploration of hybrid centre dynamics over the decimal exterior cycles"""
import sys, random, collections
from hyb import *
from ext import *

def load_ext(name):
    fn = {'p11': '/home/claude/research/w1_bases/out/ext4/b10_p11.txt', 'p12': '/home/claude/research/w1_bases/out/ext4/b10_p12.txt'}[name]
    a = parse_accepts(fn)[0]
    return cycle_from(10, a['Bs'][0])

LOOPS = {'0': [0], '18': [18], '6/12': [6, 12], '2..': [2, 4, 8, 16, 14, 10]}

def run_hybrid(b, cyc, C, c, t0=0, maxsteps=300, maxw=60):
    """simulate (C,c) driven by exterior cycle cyc starting at phase t0; return (steps survived, history)"""
    T = len(cyc)
    hist = []
    seen = {}
    for t in range(maxsteps):
        ph = (t0 + t) % T
        B, gam, e1, u = cyc[ph]
        key = (tuple(C), c, ph)
        if key in seen:
            return t, 'cycle', seen[key]
        seen[key] = t
        r = hstep_raw(b, B, C, c)
        if r is None:
            return t, 'die', len(C)
        # need e1 consistency with the exterior cycle's e1 and gam (B autonomous, so must match)
        assert r['e1'] == e1 and r['gam'] == gam
        B2, C2, u2, v, p = trim(b, r['B'], r['C'], r['c'])
        C, c = C2, r['c']
        if len(C) > maxw: return t, 'grow', len(C)
    return maxsteps, 'long', len(C)

if __name__ == '__main__':
    random.seed(1)
    for name in ('p11', 'p12'):
        cyc = load_ext(name)
        for lname, loop in LOOPS.items():
            hist = collections.Counter(); best = 0
            for trial in range(20000):
                m = random.randint(0, 8)
                C = [random.randint(0, 18) for _ in range(m)]
                # canonicalize: no N at bottom, no c at top
                c = random.choice(loop)
                t0 = random.randrange(len(cyc))
                st, why, aux = run_hybrid(10, cyc, C, c, t0)
                hist[min(st, 30)] += 1
                if why in ('cycle', 'long'): print('SURVIVOR', name, lname, C, c, t0, st, why)
                best = max(best, st)
            print(name, lname, 'max survival', best, sorted(hist.items())[:12])
