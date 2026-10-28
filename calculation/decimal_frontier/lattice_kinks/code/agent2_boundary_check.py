#!/usr/bin/env python3
"""Independent exact 3-cell graph / numerical boundary regression, base 10 rec0.

Run from repository root:
  python3 calculation/decimal_frontier/lattice_kinks/code/agent2_boundary_check.py
Input data are reconstructed from the existing p8_scc.txt by agent2_boundary_data.
This checks necessary stationary-first-defect conditions; it does not certify an orbit.
"""
from collections import deque
from agent2_boundary_data import rows

raw = rows()
W = [list(r) for r in zip(*raw[:20])]
B = [list(r) for r in zip(*raw[20:])]
GAM = (1, 0, 1, 0, 1, 0, 1, 0)
MOD = 19
L = 8 * MOD ** 3

def lat(t, x):
    return B[t % 8][x] if x < 39 else W[t % 8][(x - 39) % 20]

def cup(t, x):
    # Away from the transient exterior, the nearest non-nine fixes carry.
    for z in range(x - 1, x - 61, -1):
        if lat(t, z) != 9:
            return int(lat(t, z) >= 10)
    raise ValueError('ambiguous ascending carry')

def dcarry(t, x):
    for z in range(x + 1, x + 61):
        if lat(t, z) != 9:
            return int(lat(t, z) >= 10)
    raise ValueError('ambiguous descending carry')

def pack(t, a, b, c):
    return ((t * 19 + c) * 19 + b) * 19 + a

def unpack(n):
    a = n % 19; n //= 19
    b = n % 19; n //= 19
    c = n % 19; n //= 19
    return n, a, b, c

def successors(n, x):
    t, a, b, c = unpack(n)
    vals = (a, b, c)
    if a == lat(t, x):
        return ()
    asc = [cup(t, x)]
    up = []
    for v in vals:
        up.append((v + asc[-1]) % 10)
        asc.append(int(v + asc[-1] >= 10))
    out = set()
    for high in (0, 1):
        ds = [0] * 4
        ds[3] = high
        dn = [0] * 3
        for i in range(2, -1, -1):
            dn[i] = (vals[i] + ds[i + 1]) % 10
            ds[i] = int(vals[i] + ds[i + 1] >= 10)
        left = lat(t, x - 1)
        if (GAM[t] == 0 or left == 9) and ds[0] != dcarry(t, x - 1):
            continue
        nv = []
        for i in range(3):
            partner = dn[i] if GAM[t] == 0 else (left + ds[0]) % 10 if i == 0 else dn[i - 1]
            nv.append(up[i] + partner)
        if nv[0] != lat(t + 1, x):
            out.add(pack((t + 1) % 8, *nv))
    return tuple(sorted(out))

def graph(j):
    x = 119 + j
    valid = [pack(t, a, b, c) for t in range(8) for c in range(19)
             for b in range(19) for a in range(19) if a != lat(t, x)]
    indeg = [0] * L
    for state in valid:
        for v in successors(state, x):
            indeg[v] += 1
    q = deque(i for i in valid if indeg[i] == 0)
    dist = [0] * L
    seen = 0
    while q:
        n = q.popleft(); seen += 1
        for v in successors(n, x):
            dist[v] = max(dist[v], dist[n] + 1)
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return len(valid) - seen, max(dist[i] for i in valid) if seen == len(valid) else None

def numeric_counterexample():
    n = 400; x = 119
    half = [lat(0, i) for i in range(n // 2)]
    half[x:x + 2] = [0, 0]
    P = half + half[::-1]
    d = [min(v, 9) for v in half] + [v - min(v, 9) for v in half[::-1]]
    assert len(d) == n and d[-1] > 0
    number = int(''.join(str(v) for v in d[::-1]))
    assert len(str(number)) == n
    numeric = number + int(str(number)[::-1])
    dd = list(map(int, str(numeric)[::-1]))
    q = [dd[i] + dd[-1-i] for i in range(len(dd))]
    assert len(q) == n + 1
    assert q[:x] == [lat(1, i) for i in range(x)]
    # Descending carry into mirror(x-1) computed from exact full digits.
    carry = 0; carries = [0]
    for v in P:
        carry = int(v + carry >= 10)
        carries.append(carry)
    actual = carries[n - x]
    expect = dcarry(0, x - 1)
    assert (actual, expect) == (0, 1)
    assert (q[x], lat(1, x)) == (4, 12)
    return actual, expect

if __name__ == '__main__':
    print('numeric counterexample carry actual/nominal:', numeric_counterexample())
    expected = [(0,14),(0,32),(0,26),(0,18),(2189,None)]
    for j in range(20):
        got = graph(j)
        assert got == expected[j % 5], (j, got, expected[j % 5])
        print('j', j, 'unpeeled', got[0], 'maxfinitepath', got[1])
    print('ALL CENTRE-COLUMN CONTROLS PASSED')