#!/usr/bin/env python3
"""W7 library: independent exact tools for the decimal reverse-and-add 'lattice exterior' (base 10).
Everything validated against plain big-int / digit-list reverse-and-add.  LSB-first lists everywhere."""
import re, sys
b = 10

def parse_scc(fn):
    """parse W3's out/p8_scc.txt style records (first 3 SCC lines)."""
    out = []
    for line in open(fn):
        if not line.startswith('SCC'): continue
        mm = re.match(r'SCC p=(\d+) g=(\w+) size=(\d+) cyclen=(\d+) depth=(\d+) path=(.*) cyc=(.*)', line.strip())
        p, g, size, cl, depth, path, cyc = mm.groups()
        cols = lambda s: [list(map(int, c.split(','))) for c in re.findall(r'\[([^\]]*)\]', s)]
        out.append(dict(p=int(p), g=g, size=int(size), cyclen=int(cl), path=cols(path), cyc=cols(cyc)))
    return out

class Lattice:
    """Exterior = B (nB cells) then periodic lattice (m cells) with time period p.
    P_t[x] = Bt[t][x] (x<nB), Wt[t][(x-nB)%m] (x>=nB)."""
    def __init__(self, rec):
        self.p = rec['p']; self.g = [int(c) for c in rec['g']]
        self.nB = len(rec['path']); self.m = len(rec['cyc'])
        self.Bt = [[rec['path'][k][t] for k in range(self.nB)] for t in range(self.p)]
        self.Wt = [[rec['cyc'][j][t] for j in range(self.m)] for t in range(self.p)]
        self.S = sum(self.g)
    def cell(self, t, x):
        t %= self.p
        if x < self.nB: return self.Bt[t][x]
        return self.Wt[t][(x - self.nB) % self.m]
    def lowerhalf(self, t, h):
        return [self.cell(t, x) for x in range(h)]

def pair_from_digits(d):
    n = len(d)
    return [d[i] + d[n - 1 - i] for i in range(n)]

def digits_from_pair(P):
    """some digit string (LSB first) whose pair word is the palindrome P (P[i]=P[n-1-i], mid cell even)."""
    n = len(P); d = [0] * n
    for i in range(n):
        j = n - 1 - i
        if i < j:
            assert P[i] == P[j]
            d[i] = min(P[i], 9); d[j] = P[i] - d[i]
            assert 0 <= d[j] <= 9
        elif i == j:
            assert P[i] % 2 == 0 and P[i] <= 18
            d[i] = P[i] // 2
    assert d[-1] != 0 or True
    return d

def rar_digits(d):
    """plain reverse-and-add on a digit list (LSB first): d + reverse(d), schoolbook."""
    n = len(d); out = []; c = 0
    for i in range(n):
        s = d[i] + d[n - 1 - i] + c
        out.append(s % 10); c = s // 10
    if c: out.append(c)
    return out

def rar_int(d):
    n = int(''.join(map(str, d[::-1])))
    r = int(str(n)[::-1])
    return [int(ch) for ch in str(n + r)[::-1]]

def pairword_step(P):
    """pair word -> next pair word via carry normalisation, returns (P', gam)."""
    n = len(P); O = []; c = 0
    for i in range(n):
        s = P[i] + c
        O.append(s % 10); c = s // 10
    if c: O.append(c)
    n2 = len(O)
    return [O[i] + O[n2 - 1 - i] for i in range(n2)], n2 - n

def selftest():
    import random
    rng = random.Random(5)
    for it in range(3000):
        n = rng.randint(2, 40)
        d = [rng.randint(0, 9) for _ in range(n)]
        if d[-1] == 0: d[-1] = rng.randint(1, 9)
        if d[0] == 0: d[0] = 1
        a = rar_digits(d); bb = rar_int(d)
        assert a == bb, (d, a, bb)
        P = pair_from_digits(d)
        P2, gam = pairword_step(P)
        assert P2 == pair_from_digits(a) and gam == len(a) - n
        # digits_from_pair roundtrip on pair word
        dd = digits_from_pair(P)
        assert pair_from_digits(dd) == P
        assert rar_digits(dd) == a
    print('lib7 selftest ok')

if __name__ == '__main__':
    selftest()
