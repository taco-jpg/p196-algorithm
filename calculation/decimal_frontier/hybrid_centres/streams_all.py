#!/usr/bin/env python3
"""collect distinct primitive neutral exterior streams (b, g, e) from W1's output files; rotation classes."""
import re, glob, collections, json
def prim(g, e):
    p = len(g)
    for q in range(1, p + 1):
        if p % q == 0 and g[:q] * (p // q) == g and e[:q] * (p // q) == e:
            return g[:q], e[:q]
    return g, e
def canon(g, e):
    q = len(g); best = None
    for r in range(q):
        x = (g[r:] + g[:r], e[r:] + e[:r])
        if best is None or x < best: best = x
    return best
def collect():
    S = collections.defaultdict(set)
    for fn in glob.glob('/home/claude/research/w1_bases/out/ext4/*.txt') + glob.glob('/home/claude/research/w1_bases/out/ext_b*_p*.txt'):
        for line in open(fn, errors='ignore'):
            if not line.startswith('ACCEPT'): continue
            m = re.match(r'ACCEPT b=(\d+) p=(\d+) g=(\d+) e=(\d+)', line)
            if not m: continue
            b = int(m[1]); g, e = prim(m[3], m[4])
            S[b].add(canon(g, e))
    return S
if __name__ == '__main__':
    S = collect()
    for b in sorted(S):
        print(b, sorted(S[b], key=lambda x: (len(x[0]), x)))
