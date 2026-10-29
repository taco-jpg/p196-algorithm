#!/usr/bin/env python3
"""Independent Python finite-state and literal decimal-digit checker for rec2 g1->g0 rigidity.
No imports from primary.cpp or third-party packages. Exact all-k theorem via SCC, not sampling.
"""
from collections import defaultdict
from pathlib import Path
from random import Random
BASE, PERIOD = 10, 48
S = [(p, a, d) for p in range(19) for a in (0, 1) for d in (0, 1)]
def read_controls():
    lines = [line.strip() for line in Path(__file__).with_name('controls.txt').read_text().splitlines()
             if line.strip() and not line.startswith('#')]
    rows = [[int(x) for x in line.split()] for line in lines]
    assert len(rows) == 9 and [len(r) for r in rows] == [11] * 8 + [48]
    return rows[:8], rows[8]
def schoolbook_digits_from_pairs(P):
    n = 2 * len(P)
    digits = [0] * n
    for i, p in enumerate(P):
        assert 0 <= p <= 18
        digits[i] = p - min(p, 9)
        digits[n - 1 - i] = min(p, 9)
    assert digits[-1] != 0
    return digits
def ordinary_step(digits):
    carry, out = 0, []
    for i in range(len(digits)):
        v = digits[i] + digits[-1 - i] + carry
        out.append(v % 10)
        carry = v // 10
    if carry:out.append(carry)
    return out
def pair_segment(digits, start, count):
    n = len(digits)
    return [digits[i] + digits[n - 1 - i] for i in range(start, start + count)]
def cyclic_carries(P):
    a, d = [0] * len(P), [0] * len(P)
    c = 0
    for _ in range(3):
        for p in P:c = (p + c) // 10
    for i, p in enumerate(P):a[i], c = c, (p + c) // 10
    c = 0
    for _ in range(3):
        for p in reversed(P):c = (p + c) // 10
    for i in range(len(P) - 1, -1, -1):d[i], c = c, (P[i] + c) // 10
    return a, d
def cyclic_step(P, g):
    n = len(P)
    a, d = cyclic_carries(P)
    return [(P[j] + a[j]) % 10 + (P[(j - g) % n] + d[(j - g) % n]) % 10
            for j in range(n)]
def phase_rows(prefix, W0):
    W = W0[:]
    rows = [W]
    for phase in range(8):
        P = prefix[phase] + W * 4
        digit = schoolbook_digits_from_pairs(P)
        out = ordinary_step(digit)
        g = 1 if phase % 2 == 0 else 0
        assert len(out) == len(digit) + g
        new = pair_segment(out, 11 + 48, 48)
        assert new == cyclic_step(W, g)
        rows.append(new)
        W = new
    assert rows[-1] == W0
    print('INDEPENDENT 8 genuine 406/407-digit rec2 controls PASS')
    return rows
def build_edges():
    successors = [[] for _ in S]
    for i, (p, a, d) in enumerate(S):
        for j, (q, A, D) in enumerate(S):
            if (p + a) // 10 == A and (q + D) // 10 == d:
                successors[i].append(j)
    assert sum(map(len, successors)) == 1444
    return successors
def g0(t):
    p, a, d = S[t]
    return (p + a) % 10 + (p + d) % 10
def g1(s, next_s):
    p, a, d = S[s]
    q, A, D = S[next_s]
    return (q + A) % 10 + (p + d) % 10
def build_two_phase(target, succ):
    byz = [[t for t in range(76) if g0(t) == z] for z in range(19)]
    nodes = [(j, s, t) for j, z in enumerate(target)
             for s in range(76) for t in byz[z]]
    index = {v: i for i, v in enumerate(nodes)}
    adj, rev = [[] for _ in nodes], [[] for _ in nodes]
    for u, (j, s, t) in enumerate(nodes):
        next_col = (j + 1) % len(target)
        allowed = defaultdict(list)
        for tt in succ[t]:
            if g0(tt) == target[next_col]:
                allowed[S[tt][0]].append(tt)
        for ss in succ[s]:
            for tt in allowed[g1(s, ss)]:
                v = index[(next_col, ss, tt)]
                adj[u].append(v)
                rev[v].append(u)
    return nodes, adj, rev
def components(adj, rev):
    n = len(adj)
    seen = bytearray(n)
    order = []
    for root in range(n):
        if seen[root]:continue
        seen[root] = 1
        stack = [(root, 0)]
        while stack:
            u, pos = stack[-1]
            if pos < len(adj[u]):
                v = adj[u][pos]
                stack[-1] = (u, pos + 1)
                if not seen[v]:
                    seen[v] = 1
                    stack.append((v, 0))
            else:
                order.append(u)
                stack.pop()
    seen = bytearray(n)
    cyclic = []
    for root in reversed(order):
        if seen[root]:continue
        part = []
        todo = [root]
        seen[root] = 1
        while todo:
            u = todo.pop()
            part.append(u)
            for v in rev[u]:
                if not seen[v]:
                    seen[v] = 1
                    todo.append(v)
        if len(part) > 1 or part[0] in adj[part[0]]:
            cyclic.append(part)
    return cyclic
def check_theorem(rows, succ):
    for phase in (0, 2, 4, 6):
        X, Y, Z = rows[phase:phase + 3]
        nodes, adj, rev = build_two_phase(Z, succ)
        cyclic = components(adj, rev)
        assert len(cyclic) == 1
        expected = 282 if phase % 4 == 0 else 310
        assert len(cyclic[0]) == expected
        assert len(nodes) == (14592 if phase % 4 == 0 else 15276)
        assert sum(map(len, adj)) == (14360 if phase % 4 == 0 else 16190)
        a, d = cyclic_carries(Y)
        forced = defaultdict(set)
        for u in cyclic[0]:
            j, _, t = nodes[u]
            forced[j].add(t)
        assert len(forced) == 48
        for j in range(48):
            assert len(forced[j]) == 1
            assert S[next(iter(forced[j]))] == (Y[j], a[j], d[j])
        xa, xd = cyclic_carries(X)
        idx = {v: i for i, v in enumerate(nodes)}
        trace = [idx[(j, S.index((X[j], xa[j], xd[j])), S.index((Y[j], a[j], d[j])))]
                 for j in range(48)]
        assert all(trace[(j + 1) % 48] in adj[trace[j]] for j in range(48))
        assert all(v in cyclic[0] for v in trace)
        print(f'INDEPENDENT phase {phase}: nodes={len(nodes)} edges={sum(map(len, adj))} '
              f'cyclic_scc={len(cyclic[0])}; exactly one intermediate physical state at each of 48 positions PASS')
def check_random_actual(prefix, rows):
    rng = Random(0x31962026)
    for phase in (0, 2, 4, 6):
        for _ in range(100):
            W = rows[phase][:]
            for _ in range(rng.randrange(1, 4)):
                j = rng.randrange(48)
                W[j] = rng.randrange(19)
            D = schoolbook_digits_from_pairs(prefix[phase] + W * 4)
            E = ordinary_step(D)
            F = ordinary_step(E)
            assert len(E) == len(D) + 1 and len(F) == len(E)
            assert pair_segment(E, 59, 48) == cyclic_step(W, 1)
            assert pair_segment(F, 59, 48) == cyclic_step(cyclic_step(W, 1), 0)
    print('INDEPENDENT 400 randomized actual 406->407->407-digit two-step normalizations PASS')
if __name__ == '__main__':
    prefix, W0 = read_controls()
    rows = phase_rows(prefix, W0)
    succ = build_edges()
    check_theorem(rows, succ)
    check_random_actual(prefix, rows)
    print('INDEPENDENT ALL CHECKS PASSED: exact all-k cyclic rigidity; no decimal Lychrel certificate')
