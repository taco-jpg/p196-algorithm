import os
#!/usr/bin/env python3
"""For fixed p, which bases b have an exterior cycle of minimal period p (any overflow word), L<=Lmax.  usage: ext_exist.py p blo bhi Lmax"""
import sys, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ext_transfer import exterior_cycles, to_B0
from decouple import G_ext
p, blo, bhi, Lmax = map(int, sys.argv[1:5])
words = [s for s in itertools.product((0, 1), repeat=p) if any(s) and s == min(s[i:] + s[:i] for i in range(p))]
hits = {}
for b in range(blo, bhi + 1):
    for s in words:
        fd = exterior_cycles(b, p, s, Lmax)
        for L, items in fd.items():
            for pth, cw in items:
                B0 = to_B0(b, pth)
                # minimal period check
                cur = list(B0); orb = []
                for t in range(p): orb.append(tuple(cur)); cur = G_ext(b, cur)[0]
                if len(set(orb)) == p:
                    hits.setdefault(b, set()).add(''.join(map(str, s)))
print(f"p={p}: bases with a minimal-period-{p} exterior (L<={Lmax}):")
print(sorted(hits))
for b in sorted(hits): print(b, sorted(hits[b]), 'b mod', {m: b % m for m in (2**p - 1, 2**(p - 1) - 1) if m > 1})
