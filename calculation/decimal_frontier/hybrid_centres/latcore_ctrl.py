#!/usr/bin/env python3
"""control for latcore.py: the N-pad (neutral band) as the 'lattice', base 4, stream gam=101100 e1=101010 (known hybrid, A=0, c=4, loop {2,4}) and decimal p11/p12."""
import sys
sys.path.insert(0, '.'); sys.path.insert(0, 'lat')
from latcore import run
from runsat import stream
from runbase import loops
def pad_links(b, gam, e1):
    p = len(gam); N = b - 1
    a = list(e1); G = [1 - x for x in e1]; dd = [N * x for x in e1]
    W = [[N] for _ in range(p)]
    return (p, 1, b, gam, W, a, G, dd)
b = 4
gam = [1, 0, 1, 1, 0, 0]; e1 = [1, 0, 1, 0, 1, 0]
print('base 4 control:', run(None, 0, 4, verbose=False, links=pad_links(b, gam, e1), loops=loops(4)))
for name in ('p11', 'p12'):
    cyc = stream(name)
    g = [c[1] for c in cyc]; e = [c[2] for c in cyc]
    print(name, 'decimal N-pad:', run(None, 0, 4, verbose=False, links=pad_links(10, g, e)))
