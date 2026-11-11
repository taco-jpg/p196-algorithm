#!/usr/bin/env python3
"""r12f2: all-m proof inputs for q_c(m) = 10m-3.  (a) protected prefix length l_j of the two-inlet rooted cone of
B0 W0^q at the epoch boundaries t = 120j (must follow l_1 = l_0 - 91, l_(j+1) = l_j - 90 while the edge is in W);
(b) l* = least protected length l such that the cone started from the reference prefix (B0 W0^inf)[0,l) at phase 0
keeps the clock forced (= [t%4==0]) for 120 steps, and monotonicity in l (checked for l = 40..140)."""
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from seam_check import B, W, norm


def cone(p, steps, t0=0):
    lens = [len(p)]
    for t in range(t0, t0 + steps):
        n = len(p)
        if n == 0:
            return False, lens
        d, _ = norm(p, 0); a0, g0 = norm(p[::-1], 0); a1, g1 = norm(p[::-1], 1)
        if g0 != g1 or g0 != (t % 4 == 0):
            return False, lens
        if g0:
            l0 = [d[0] + 1] + [d[i] + a0[n - i] for i in range(1, n)]; l1 = [d[0] + 1] + [d[i] + a1[n - i] for i in range(1, n)]
        else:
            l0 = [d[i] + a0[n - 1 - i] for i in range(n)]; l1 = [d[i] + a1[n - 1 - i] for i in range(n)]
        j = next((i for i in range(n) if l0[i] != l1[i]), n); p = l0[:j]
        lens.append(len(p))
    return True, lens


ref = list(B) + list(W) * 40
# (a)
for q in (17, 27, 37, 57):
    m = (q + 3) // 10
    ok, lens = cone(list(B) + list(W) * q, 120 * m)
    lj = [lens[120 * j] for j in range(m + 1) if 120 * j < len(lens)]
    print(f'q={q} m={m}: forced={ok}; l_j at t=120j: {lj}; differences {[lj[i]-lj[i+1] for i in range(len(lj)-1)]}', flush=True)
# (b)
res = {}
for l in range(40, 141):
    ok, _ = cone(ref[:l], 120)
    res[l] = ok
lstar = min(l for l in res if res[l] and all(res[x] for x in range(l, 141)))
print('one-epoch forced lengths: l* =', lstar, '; forced set below l*:', [l for l in range(40, lstar) if res[l]],
      '; monotone above l*:', all(res[x] for x in range(lstar, 141)), flush=True)
