"""Independent finite checks for the thirteen palindromic prefix theorem.

The unbounded-length proof is the carry argument and finite prefix tables in
the accompanying report. The integer scan here is a cross-check, not a
substitute for that proof. Python standard library only.
"""
from collections import defaultdict
from functools import lru_cache
from itertools import product

BOUNDS = {(1, 0): 1, (2, 0): 2, (3, 2): 2, (4, 0): 3,
          (4, 1): 3, (6, 0): 3, (6, 4): 3, (6, 5): 6,
          (7, 6): 3, (8, 0): 4, (8, 1): 4, (8, 2): 4, (8, 3): 4}
SHARP_ROOTS = {(1, 0): 100, (2, 0): 1005000, (3, 2): 12090,
               (4, 0): 1008000, (4, 1): 1008400, (6, 0): 1103090,
               (6, 4): 1203090, (6, 5): 1203290, (7, 6): 17590,
               (8, 0): 1009000, (8, 1): 1009200, (8, 2): 1006500,
               (8, 3): 1009400}


def T(n):
    return n + int(str(n)[::-1])


def pal(n):
    a = str(n)
    return a == a[::-1]


def normalize(s):
    out, carry = [], 0
    for u in s:
        carry, d = divmod(u + carry, 10)
        out.append(d)
    if carry:
        out.append(carry)
    return tuple(out)


def forward(s):
    d = normalize(s)
    return tuple(a + b for a, b in zip(d, d[::-1]))


@lru_cache(None)
def inv_nongrowth(p):
    # Read the known outer columns from the two ends. Leave the interior free.
    states = {((), 0, 0)}
    for i, v in enumerate(p):
        nxt = set()
        for word, x, y in states:
            for s in range(1 if i == 0 else 0, 19):
                xx = (s + x) // 10
                for yy in (0, 1):
                    if ((s + yy) // 10 == y
                            and 2 * s + x + yy - 10 * (xx + y) == v):
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
                digit = v - word[-1] - yy + 10 * y
                if not 0 <= digit <= 9:
                    continue
                for xx in (0, 1):
                    s = digit + 10 * xx - x
                    if 0 <= s <= 18:
                        nxt.add((word + (s,), xx, yy))
        states = nxt
    # There must be a legal carry entering the last known high column.
    return frozenset(word for word, x, y in states
                     if any((word[-1] + z) // 10 == y for z in (0, 1)))


@lru_cache(None)
def inv_prefix(p):
    return inv_nongrowth(p) | inv_growth(p)


def raw_words(n):
    half = n // 2
    for first in range(1, 19):
        for tail in product(range(19), repeat=half - 1):
            left = (first,) + tail
            if n % 2:
                for center in range(0, 19, 2):
                    yield left + (center,) + left[::-1]
            else:
                yield left + left[::-1]


def coverage_check():
    count = growth_count = gn_count = 0
    for n in range(3, 8):
        for s in raw_words(n):
            d = normalize(s)
            p = forward(s)
            grow = len(d) > n
            inverse = inv_growth if grow else inv_nongrowth
            assert s[:3] in inverse(p[:3]), (s, p)
            if grow:
                growth_count += 1
                # A growth step followed by a carry-free step cannot make
                # a palindrome with a descending first digit pair.
                if max(p) <= 9:
                    assert p[1] >= p[0], (s, p)
                    gn_count += 1
            count += 1
    # A two-digit source growing to three digits has a special short boundary.
    for s in range(10, 19):
        assert forward((s, s)) == (s - 9, 2 * (s - 9), s - 9)
    return count, growth_count, gn_count


def prefix_certificates():
    all_layers = {}
    for ab, bound in BOUNDS.items():
        layer = {(ab[0], ab[1], c) for c in range(10)}
        layers = [layer]
        for depth in range(1, bound + 1):
            inverse = inv_nongrowth if depth == 1 else inv_prefix
            layer = {s for p in layer for s in inverse(p)}
            layers.append(layer)
        assert not layers[-1], (ab, layers[-1])
        assert all(layers[:-1])
        all_layers[ab] = layers
    return all_layers


def actual_integer_check(limit=1_000_000):
    # Exact heights for all targets below limit: T(n)>n, so ascending dynamic
    # programming has already seen every predecessor when it processes n.
    heights = bytearray(limit)
    checked = 0
    for n in range(1, limit):
        value = T(n)
        if value < limit:
            heights[value] = max(heights[value], heights[n] + 1)
        ds = str(n)
        if len(ds) >= 3 and ds == ds[::-1]:
            ab = (int(ds[0]), int(ds[1]))
            if ab in BOUNDS:
                assert heights[n] <= BOUNDS[ab], (n, heights[n])
                checked += 1
    return checked


def sharpness_check():
    result = {}
    for ab, root in SHARP_ROOTS.items():
        path = [root]
        for _ in range(BOUNDS[ab]):
            path.append(T(path[-1]))
        assert not any(map(pal, path[:-1]))
        assert pal(path[-1])
        assert str(path[-1]).startswith(''.join(map(str, ab)))
        result[ab] = path
    assert SHARP_ROOTS[(6, 5)] % 11 == 0
    orbit = [196]
    for _ in range(max(BOUNDS.values())):
        orbit.append(T(orbit[-1]))
    assert orbit == [196, 887, 1675, 7436, 13783, 52514, 94039]
    assert not any(map(pal, orbit))
    return result


if __name__ == '__main__':
    layers = prefix_certificates()
    print('Exact finite prefix certificates:')
    for ab, chain in layers.items():
        print(''.join(map(str, ab)), [len(s) for s in chain])
    print('Direct carry-coverage checks:', coverage_check())
    print('Palindrome targets checked below one million:', actual_integer_check())
    print('Sharp first-hit paths:')
    for ab, path in sharpness_check().items():
        print(''.join(map(str, ab)), path)
    print('All checks passed. This does not prove the full 196 conjecture.')