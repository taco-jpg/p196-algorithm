#!/usr/bin/env python3
"""Compare my level counts (mc13b) with r13b's eset3 logs, level by level: (E_acc, accepting, parents kept, exact orbits)."""
import re, os, sys
H = os.path.expanduser('~/p196_run')
def mine(fn):
    out = {}
    if not os.path.exists(fn): return out
    for l in open(fn):
        m = re.match(r'K (\d+) Eacc (\d+) accepting (\d+) parents (\d+) exact (\d+)', l)
        if m: out[int(m[1])] = tuple(map(int, m.groups()[1:]))
    return out
def theirs(fn):
    out = {}
    if not os.path.exists(fn): return out
    for l in open(fn):
        m = re.match(r'K=(\d+) T=\d+ Lo=\d+ orbit=\d+ parents=\d+ parentsKept=(\d+) .* E=(\d+) accepting=(\d+) foldSuccInE=\d+ exactOrbits=(\d+)', l)
        if m:
            out[int(m[1])] = (int(m[3]), int(m[4]), int(m[2]), int(m[5]))
    return out
def cmp1(a, b):
    ks = sorted(set(a) | set(b))
    diff = [k for k in ks if a.get(k) != b.get(k)]
    return ks, diff
for lat, tname, orbs in [('rec0', 'T80', range(4)), ('rec1', 'T80', range(4)), ('rec2', 'T192', range(4))]:
    for o in orbs:
        a = mine(f'{H}/mchk13b/logs/{lat}_o{o}.log')
        b = theirs(f'{H}/r13b/logs/acc_{lat}_o{o}_{tname}.log')
        if not a:
            print(lat, 'orbit', o, 'mine: no data yet'); continue
        if not b:
            ka = sorted(a)
            print(lat, 'orbit', o, 'r13b has no direct log (symmetry orbit); my levels', ka[0], '..', ka[-1], 'last', a[ka[-1]])
            continue
        ks, diff = cmp1(a, b)
        ka = sorted(a)
        last = ka[-1]
        print(lat, 'orbit', o, 'levels compared', len(ks), 'differences', len(diff), diff[:6], 'my last level', last, a[last], 'total of exact orbits', sum(v[3] for v in a.values()))
        if diff:
            k = diff[0]
            print('   first diff K=', k, 'mine', a.get(k), 'r13b', b.get(k))
