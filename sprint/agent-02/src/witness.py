#!/usr/bin/env python3
"""Is the k-column projection of the last predecessor of a seed's first palindrome in F_k?
Usage: witness.py DATA_DIR SEED [K ...]   (reads DATA_DIR/F_k{K}.bits written by run.sh)"""
import mmap
import sys
sys.set_int_max_str_digits(0)
def T(n): return n + int(str(n)[::-1])
def pal(n): s = str(n); return s == s[::-1]
def pw(n):
    d = [int(c) for c in str(n)][::-1]; L = len(d)
    return [d[i] + d[L - 1 - i] for i in range(L)]
data, seed = sys.argv[1], int(sys.argv[2])
ks = [int(x) for x in sys.argv[3:]] or list(range(3, 9))
n, orb = seed, [seed]
while True:
    n = T(n); orb.append(n)
    if pal(n) or len(orb) > 1000: break
q = pw(orb[-2])
res = {}
for k in ks:
    with open(f'{data}/F_k{k}.bits', 'rb') as f:
        m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        idx = 0
        for x in q[:k]: idx = idx * 19 + x
        res[k] = bool((m[idx >> 3] >> (idx & 7)) & 1)
print({'seed': seed, 'steps': len(orb) - 1, 'palindrome_prefix': str(orb[-1])[:6], 'in_F_k': res})
