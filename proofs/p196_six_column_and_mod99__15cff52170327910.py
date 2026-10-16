"""Six-position carry certificates and the block-replication lemma.

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


@lru_cache(200000)
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


@lru_cache(200000)
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


@lru_cache(200000)
def inv_prefix(p):
    return inv_nongrowth(p) | inv_growth(p)


CASES = {'78': 40, '85': 38, '119': 8, '213': 23, '216': 10,
         '217': 28, '218': 36, '257': 16, '276': 31, '277': 31,
         '278': 31, '348': 16, '377': 8, '384': 7, '385': 8,
         '426': 24, '429': 22, '474': 7, '674': 5, '737': 12,
         '755': 12, '777': 27, '778': 25, '905': 11, '906': 11,
         '923': 7, '935': 10}

EXPECTED_78 = [10000, 66383, 36630, 19665, 11773, 6557, 3796, 6251,
               8403, 4979, 4730, 1761, 4425, 2531, 7923, 4595, 2244,
               1304, 964, 350, 515, 650, 424, 342, 141, 344, 305, 918,
               778, 455, 342, 257, 116, 197, 267, 215, 118, 44, 41, 35, 0]
EXPECTED_85 = [10000, 6231, 3919, 2594, 3354, 5634, 7851, 4704, 4601,
               1879, 3869, 2386, 6921, 4129, 2045, 1160, 755, 297, 472,
               599, 416, 318, 133, 344, 305, 918, 778, 455, 342, 257,
               116, 197, 267, 215, 118, 44, 41, 35, 0]


def certificates():
    records, shared = {}, {}
    for prefix, bound in CASES.items():
        inv_prefix.cache_clear()
        inv_nongrowth.cache_clear()
        inv_growth.cache_clear()
        pre = tuple(map(int, prefix))
        layer = {pre + p for p in product(range(10), repeat=6-len(pre))}
        counts = [len(layer)]
        for depth in range(1, bound+1):
            inverse = (inv_nongrowth if depth == 1 and pre[1] < pre[0]
                       else inv_prefix)
            layer = {s for p in layer for s in inverse(p)}
            counts.append(len(layer))
            if prefix in ('78', '85') and depth == bound-15:
                shared[prefix] = layer.copy()
            if prefix in ('78', '85') and depth == bound-1:
                assert len(layer) == 35
                assert {p[:3] for p in layer} == {(1, 8, 3), (1, 9, 6)}
            if not layer:
                break
        assert len(counts) == bound+1 and not layer, (prefix, counts)
        if prefix == '78':
            assert counts == EXPECTED_78
        if prefix == '85':
            assert counts == EXPECTED_85
        records[prefix] = counts
    assert shared['78'] == shared['85'] and len(shared['78']) == 344
    assert not inv_prefix((1, 8, 3))
    assert not inv_prefix((1, 9, 6))
    return records


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


def carry_coverage():
    count = 0
    for n in range(6, 9):
        for s in raw_words(n):
            d, p = normalize(s), forward(s)
            inverse = inv_growth if len(d) > n else inv_nongrowth
            assert s[:6] in inverse(p[:6]), (s, p)
            count += 1
    assert count == 194940
    return count


def short_boundary():
    at_step = defaultdict(list)
    for prefix, bound in CASES.items():
        at_step[bound+1].append(prefix)
    for root in range(1, 100000):
        n = root
        for k in range(1, 42):
            n = T(n)
            ds = str(n)
            if ds == ds[::-1]:
                assert all(not ds.startswith(p) for p in at_step[k]), (root, k, n)


def constructive_checks():
    examples = {'78': 1009100, '85': 1023944}
    for prefix, root in examples.items():
        path = [root]
        for _ in range(6):
            path.append(T(path[-1]))
        assert not any(map(pal, path[:-1])) and pal(path[-1])
        assert str(path[-1]).startswith(prefix)
    A = 1031001007250916996999909039935
    path = [A]
    for _ in range(10):
        path.append(T(path[-1]))
    assert path[-1] == int('55' + '0'*30 + '55')
    assert not any(map(pal, path[:-1])) and pal(path[-1])
    assert max(map(lambda n: len(str(n)), path)) == 34
    assert A % 99 == 44 and A % 11 == 0
    for L in (34, 35, 40):
        S = sum(10**(j*L) for j in range(7))
        b = A*S
        assert b % 99 == 7436 % 99 == 11
        for k, a in enumerate(path):
            assert b == a*S
            assert pal(b) == (k == 10)
            assert b % 99 == 11*pow(2, k, 99) % 99
            b = T(b)
    return path


def verify():
    records = certificates()
    print('27 finite inverse certificates passed.', flush=True)
    coverage = carry_coverage()
    print('Six-position carry coverage:', coverage, flush=True)
    short_boundary()
    print('All 99999 short roots passed through step 41.', flush=True)
    path = constructive_checks()
    orbit = [196]
    for _ in range(40):
        orbit.append(T(orbit[-1]))
    assert not any(map(pal, orbit))
    return {'counts': records, 'first_hit_10_path': path,
            'N40': orbit[-1], 'coverage': coverage}


if __name__ == '__main__':
    result = verify()
    print(result)
    print('This verifies partial results, not the full 196 conjecture.')


