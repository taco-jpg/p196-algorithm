#!/usr/bin/env python3
"""exterior B-cycles (autonomous B evolution under the flip e3 = 1-e1)."""
import re, sys
from hyb import norm

def bstep(b, B):
    """B -> (B2 trimmed, gam, e1, u).  e3 = 1-e1 is imposed (neutral flip)."""
    N = b - 1
    DB, e1 = norm(b, B, 0)
    x = (N + e1) % b
    DR, gam = norm(b, B[::-1], 1 - e1)
    if gam == 0:
        Bp = [p + q for p, q in zip(DB, DR[::-1])]
    else:
        Bp = [p + q for p, q in zip(DB + [x], [1] + DR[::-1])]
    u = 0
    while Bp and Bp[-1] == N:
        Bp = Bp[:-1]; u += 1
    return Bp, gam, e1, u

def parse_accepts(path, gword=None):
    out = []
    for line in open(path):
        if not line.startswith('ACCEPT'): continue
        m = re.match(r'ACCEPT b=(\d+) p=(\d+) g=(\d+) e=(\d+) depth=\d+ states=\d+ B_t=(.*)$', line.strip())
        b, p, g, e, rest = int(m[1]), int(m[2]), m[3], m[4], m[5]
        Bs = [[int(v) for v in s.split(',') if v != ''] for s in re.findall(r'\[([^\]]*)\]', rest)]
        out.append(dict(b=b, p=p, g=g, e=e, Bs=Bs))
    return out

def cycle_from(b, B, maxsteps=5000):
    """iterate bstep from B until a state repeats; return list of (B,gam,e1,u) of the cycle"""
    seen = {}; seq = []
    cur = tuple(B)
    for t in range(maxsteps):
        if cur in seen:
            return seq[seen[cur]:]
        seen[cur] = t
        Bp, gam, e1, u = bstep(b, list(cur))
        seq.append((list(cur), gam, e1, u))
        cur = tuple(Bp)
        if len(cur) > 2000: return None
    return None

if __name__ == '__main__':
    for fn in ('/home/claude/research/w1_bases/out/ext4/b10_p11.txt', '/home/claude/research/w1_bases/out/ext4/b10_p12.txt'):
        for a in parse_accepts(fn):
            cyc = cycle_from(10, a['Bs'][0])
            if cyc is None: print('no cycle', a['g'], a['e']); continue
            gs = ''.join(str(x[1]) for x in cyc); es = ''.join(str(x[2]) for x in cyc)
            print(a['p'], 'file g', a['g'], 'e', a['e'], '| recomputed cycle len', len(cyc), 'gam', gs, 'e1', es, '|B|', [len(x[0]) for x in cyc], 'u', ''.join(str(x[3]) for x in cyc))
