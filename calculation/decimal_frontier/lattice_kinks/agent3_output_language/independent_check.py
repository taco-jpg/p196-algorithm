#!/usr/bin/env python3
"""Independent ordinary-digit checker for all-window g0 simulation and g1 forbidden word.
No imports from the primary C++ engine. Uses direct two-ended digit residues.
"""
from collections import deque
from pathlib import Path
from random import Random
import sys

BASE = 10
S = [(p, a, d) for p in range(19) for a in (0, 1) for d in (0, 1)]
LABEL = [(p & 1) | (a << 1) | (d << 2) for p, a, d in S]

def graph(g):
    # Different enumeration: all 76 x 76 source state pairs, not the primary's q,D construction.
    edges = [(i, j) for i, (p, a, d) in enumerate(S)
             for j, (q, A, D) in enumerate(S)
             if A == (p + a) // BASE and d == (q + D) // BASE]
    assert len(edges) == 1444
    by_source = [[] for _ in S]
    gnext = [[] for _ in S]
    for e, (i, j) in enumerate(edges):
        by_source[i].append(e)
        gnext[i].append(j)
    # These y-values are computed by the actual digit residues, not the bulk equations.
    yy = [((S[j][0] + S[j][1]) % BASE) +
          (((S[j][0] + S[j][2]) if g == 0 else (S[i][0] + S[i][2])) % BASE)
          for i, j in edges]
    labels = [(yy[e] & 1) | (a << 1) | (d << 2)
              for e in range(len(edges)) for a in (0, 1) for d in (0, 1)]
    H = [[] for _ in labels]
    RH = [[] for _ in labels]
    for e, (i, j) in enumerate(edges):
        for a in (0, 1):
            for d in (0, 1):
                u = 4 * e + 2 * a + d
                for f in by_source[j]:
                    for D in (0, 1):
                        if d != (yy[f] + D) // BASE:
                            continue
                        A = (yy[e] + a) // BASE
                        v = 4 * f + 2 * A + D
                        H[u].append(v)
                        RH[v].append(u)
    assert len(labels) == 5776 and sum(map(len, H)) == 109744
    return edges, gnext, labels, H, RH

def reach(root, adj):
    seen = {root}
    q = deque([root])
    while q:
        for v in adj[q.popleft()]:
            if v not in seen:
                seen.add(v)
                q.append(v)
    return seen

def verify_simulation(g0):
    edges, G, labels, H, RH = g0
    hub = 1563
    assert hub in H[hub]
    recurrent = reach(hub, H) & reach(hub, RH)
    assert len(recurrent) == 3116
    R0 = [{h for h in recurrent if labels[h] == LABEL[s]} for s in range(76)]
    R1 = [{h for h in R0[s] if all(any(k in R0[t] for k in H[h]) for t in G[s])}
          for s in range(76)]
    assert sum(map(len, R0)) == 29600
    assert sum(map(len, R1)) == 14924
    assert all(R1)
    assert all(any(k in R1[t] for k in H[h])
               for s in range(76) for h in R1[s] for t in G[s])
    print('INDEPENDENT g0 forward simulation: 76/76 states, R0=29600, R1=14924, recurrent=3116')

def forbidden_counts(g1):
    _, _, labels, H, _ = g1
    want = [722, 191, 133, 99, 81, 79, 71, 57, 36, 10, 0]
    for phase in (0, 1):
        cur = {i for i, x in enumerate(labels) if x == (7 if phase == 0 else 1)}
        counts = [len(cur)]
        for j in range(1, 11):
            symbol = (7 if (j + phase) % 2 == 0 else 1)
            cur = {v for u in cur for v in H[u] if labels[v] == symbol}
            counts.append(len(cur))
        assert counts == want, (phase, counts)
    print('INDEPENDENT g1 forbidden alternating 11-block: ' + ','.join(map(str, want)))

def cyclic_carries(P):
    n = len(P)
    a = [0] * n
    c = 0
    for x in P:
        c = (x + c) // BASE
    for i, x in enumerate(P):
        a[i] = c
        c = (x + c) // BASE
    d = [0] * n
    c = 0
    for x in reversed(P):
        c = (x + c) // BASE
    for i in range(n - 1, -1, -1):
        d[i] = c
        c = (P[i] + c) // BASE
    return a, d

def physical_labels(P):
    a, d = cyclic_carries(P)
    return [(x & 1) | (a[i] << 1) | (d[i] << 2) for i, x in enumerate(P)]

def schoolbook(P):
    h = len(P)
    n = 2 * h
    digits = [0] * n
    for i, p in enumerate(P):
        assert 0 <= p <= 18
        hi = min(9, p)
        digits[i] = p - hi
        digits[n - 1 - i] = hi
    assert digits[-1] > 0
    carry = 0
    output = []
    for i in range(n):
        total = digits[i] + digits[n - 1 - i] + carry
        output.append(total % BASE)
        carry = total // BASE
    if carry:
        output.append(carry)
    return output

def actual_image(P, g):
    # Literal ordinary decimal digits, with a canonical nonzero leading digit.
    root = 1 if g == 0 else 18
    R = [root] + P * 4
    O = schoolbook(R)
    n = 2 * len(R)
    assert len(O) == n + g
    start = 1 + len(P)
    return [O[j] + O[n - 1 - j + g] for j in range(start, start + len(P))]

def controls(g0, g1, root):
    data = [int(v) for v in root.joinpath('witness.txt').read_text().split()]
    n = data[0]
    assert n % 48 == 0 and n >= 48
    P = data[1:1 + n]
    Y = data[1 + n:1 + 2 * n]
    n1 = data[1 + 2 * n]
    assert n1 % 48 == 0 and n1 >= 48 and len(data) == 2 + 2 * n + 2 * n1
    P1 = data[2 + 2 * n:2 + 2 * n + n1]
    Y1 = data[2 + 2 * n + n1:]
    assert actual_image(P, 0) == Y
    assert physical_labels(Y)[:11] == [7, 1] * 5 + [7]
    assert actual_image(P1, 1) == Y1
    assert physical_labels(Y1)[:10] == [7, 1] * 5
    target = [1, 11] * 24
    assert physical_labels(target) == [7, 1] * 24
    print(f'INDEPENDENT real {2 * (1 + 4 * n)}-digit g0 witness, length {n}, alternating 11-mask PASS')
    print(f'INDEPENDENT real {2 * (1 + 4 * n1)}-digit g1 witness, length {n1}, alternating 10-mask PASS')
    rng = Random(0x1962026)
    for g, G in ((0, g0), (1, g1)):
        edges, _, labels, H, _ = G
        index = {edge: e for e, edge in enumerate(edges)}
        for rep in range(1000):
            P = [rng.randrange(19) for _ in range(48)]
            Y = actual_image(P, g)
            a, d = cyclic_carries(P)
            A, D = cyclic_carries(Y)
            path = []
            for i in range(48):
                prev = (i - 1) % 48
                u = (P[prev] * 2 + a[prev]) * 2 + d[prev]
                v = (P[i] * 2 + a[i]) * 2 + d[i]
                e = index[(u, v)]
                h = 4 * e + 2 * A[i] + D[i]
                assert labels[h] == ((Y[i] & 1) | (A[i] << 1) | (D[i] << 2))
                path.append(h)
            assert all(path[(i + 1) % 48] in H[path[i]] for i in range(48))
        print(f'INDEPENDENT 1000 genuine {g=} decimal normalization / transducer cyclic controls PASS')
    prefix = [int(v) for v in root.joinpath('rec2_prefix.txt').read_text().split()]
    W = [int(v) for v in root.joinpath('rec2_w0.txt').read_text().split()]
    assert len(prefix) == 88 and len(W) == 48
    first = W[:]
    for t in range(8):
        g = 1 - (t % 2)
        R = prefix[t * 11:(t + 1) * 11] + W * 4
        O = schoolbook(R)
        assert len(R) == 203 and len(O) == 406 + g
        Wnew = [O[j] + O[405 - j + g] for j in range(59, 107)]
        wrong = [O[j] + O[405 - j + (1 - g)] for j in range(59, 107)]
        assert Wnew != wrong
        W = Wnew
    assert W == first
    print('INDEPENDENT 8 rec2 real 406-digit phase controls + wrong-overflow negatives PASS')

if __name__ == '__main__':
    folder = Path(__file__).resolve().parent
    g0, g1 = graph(0), graph(1)
    verify_simulation(g0)
    forbidden_counts(g1)
    controls(g0, g1, folder)
    print('INDEPENDENT ALL CHECKS PASSED (local standalone, not repository verify.py)')
