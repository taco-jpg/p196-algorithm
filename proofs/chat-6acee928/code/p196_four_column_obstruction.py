"""Finite carry certificates; Python standard library only.

This is not a proof of the full 196 conjecture. The accompanying report
proves why these finite prefix certificates apply to unbounded lengths.
"""
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import product


def T(n):
    return n + int(str(n)[::-1])


def pal(n):
    a = str(n)
    return a == a[::-1]


def normalize(s):
    digits, carry = [], 0
    for u in s:
        carry, d = divmod(u + carry, 10)
        digits.append(d)
    if carry:
        digits.append(carry)
    return tuple(digits)


def forward(s):
    d = normalize(s)
    return tuple(a + b for a, b in zip(d, d[::-1]))


@lru_cache(None)
def inv_nongrowth(p):
    states = {((), 0, 0)}
    for i, v in enumerate(p):
        nxt = set()
        for word, x, y in states:
            for s in range(1 if i == 0 else 0, 19):
                xx = (s + x) // 10
                for yy in (0, 1):
                    if ((s + yy) // 10 == y
                            and 2*s + x + yy - 10*(xx + y) == v):
                        nxt.add((word + (s,), xx, yy))
        states = nxt
    return frozenset(word for word, _, _ in states)


@lru_cache(None)
def inv_growth(p):
    if p[0] > 10:
        return frozenset()
    first = p[0] + 9 if p[0] <= 9 else 9
    states = {((first,), first // 10, 1)}
    for v in p[1:]:
        nxt = set()
        for word, x, y in states:
            for yy in (0, 1):
                if (word[-1] + yy) // 10 != y:
                    continue
                digit = v - word[-1] - yy + 10*y
                if not 0 <= digit <= 9:
                    continue
                for xx in (0, 1):
                    s = digit + 10*xx - x
                    if 0 <= s <= 18:
                        nxt.add((word + (s,), xx, yy))
        states = nxt
    return frozenset(word for word, _, y in states
                     if any((word[-1] + z) // 10 == y for z in (0, 1)))


@lru_cache(None)
def inv_prefix(p):
    return inv_nongrowth(p) | inv_growth(p)


def graph_certificate():
    nodes = list(product(range(1, 19), range(19), range(19), range(19)))
    edges = {p: inv_prefix(p) for p in nodes}
    back = defaultdict(list)
    remaining = {p: len(vs) for p, vs in edges.items()}
    for p, vs in edges.items():
        for u in vs:
            back[u].append(p)
    queue = [p for p, n in remaining.items() if n == 0]
    rank = {p: 0 for p in queue}
    for u in queue:
        for p in back[u]:
            remaining[p] -= 1
            if remaining[p] == 0:
                rank[p] = 1 + max(rank[v] for v in edges[p])
                queue.append(p)
    # Check every assigned rank against every edge; no path is discarded.
    for p, h in rank.items():
        assert all(v in rank for v in edges[p])
        assert h == (1 + max(rank[v] for v in edges[p]) if edges[p] else 0)
    bounds = {}
    growth_pal_prefixes = {(1, 1, 0), (1, 1, 1), (1, 2, 1), (1, 2, 2)}
    for a, b, c in product(range(1, 10), range(10), range(10)):
        if (a, b, c) in growth_pal_prefixes:
            continue
        roots = {(a, b, c, d) for d in range(10)}
        inverse = inv_nongrowth if b < a else inv_prefix
        vs = {s for p in roots for s in inverse(p)}
        if not vs:
            bounds[100*a + 10*b + c] = 1
        elif all(s in rank for s in vs):
            bounds[100*a + 10*b + c] = 2 + max(rank[s] for s in vs)
    assert len(nodes) == 123462
    assert sum(map(len, edges.values())) == 185193
    assert len(rank) == 75482 and max(rank.values()) == 20
    assert len(bounds) == 360 and max(bounds.values()) == 14
    assert dict(sorted(Counter(bounds.values()).items())) == {
        1: 55, 2: 53, 3: 110, 4: 69, 5: 15, 6: 17, 7: 7,
        8: 13, 9: 5, 10: 4, 11: 2, 12: 7, 13: 1, 14: 2}
    return bounds


def raw_words(n):
    half = n // 2
    for first in range(1, 19):
        for tail in product(range(19), repeat=half-1):
            left = (first,) + tail
            if n % 2:
                for center in range(0, 19, 2):
                    yield left + (center,) + left[::-1]
            else:
                yield left + left[::-1]


def carry_coverage_check():
    count = 0
    for n in range(4, 9):
        for s in raw_words(n):
            d = normalize(s)
            p = forward(s)
            inverse = inv_growth if len(d) > n else inv_nongrowth
            assert s[:4] in inverse(p[:4]), (s, p)
            if len(d) > n and max(p) <= 9:
                assert p[1] >= p[0]
            count += 1
    assert count == 198702
    return count


def short_boundary_check(bounds):
    # If a (B+1)-step counterexample has any <4-digit entry, its initial
    # number is <1000, because T(n)>n. This is the entire small boundary.
    for root in range(1, 1000):
        n = root
        for k in range(1, max(bounds.values())+2):
            n = T(n)
            ds = str(n)
            if len(ds) >= 3 and ds == ds[::-1]:
                h = bounds.get(int(ds[:3]))
                assert h is None or k != h+1, (root, k, n, h)
        n = root
        for _ in range(6):
            n = T(n)
        assert not (pal(n) and str(n).startswith('33')), (root, n)


def prefix_33_check():
    layer = {(3, 3, c, d) for c, d in product(range(10), repeat=2)}
    counts = [len(layer)]
    for _ in range(5):
        layer = {s for p in layer for s in inv_prefix(p)}
        counts.append(len(layer))
    assert counts == [100, 346, 171, 107, 62, 0]
    path = [1109090]
    for _ in range(5):
        path.append(T(path[-1]))
    assert path == [1109090, 2018101, 3036203, 6062506, 12115112, 33266233]
    assert all(not pal(n) for n in path[:-1]) and pal(path[-1])
    return counts, path


def verify():
    bounds = graph_certificate()
    coverage = carry_coverage_check()
    short_boundary_check(bounds)
    counts, sharp_path = prefix_33_check()
    orbit = [196]
    for _ in range(14):
        orbit.append(T(orbit[-1]))
    assert not any(map(pal, orbit))
    delayed = [89]
    for _ in range(24):
        delayed.append(T(delayed[-1]))
    assert delayed[-1] == 8813200023188 and pal(delayed[-1])
    assert all(not pal(n) for n in delayed[:-1]) and 881 not in bounds
    return {'bounds': bounds, 'coverage': coverage, 'prefix_33_counts': counts,
            'sharp_path': sharp_path, 'orbit_through_14': orbit}


if __name__ == '__main__':
    result = verify()
    for k, v in result.items():
        print(k, v)
    print('All certificates passed. The full 196 conjecture remains unproved here.')
