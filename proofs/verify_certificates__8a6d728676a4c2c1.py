#!/usr/bin/env python3
"""Verify the 33 and 77 prefix certificates using only the Python standard library, without the original repository.

By default, independently recompute every inverse edge, rank, short-number boundary, and example.
With --independent-forward, also exhaust every four-column/five-column input and inner carry;
use independent forward equations to check that the certificate is closed under every possible predecessor.
"""
from collections import defaultdict, Counter
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json


def T(n):
    return n + int(str(n)[::-1])


def palindrome(n):
    s = str(n)
    return s == s[::-1]


def normalize(s):
    digits, carry = [], 0
    for u in s:
        carry, d = divmod(u + carry, 10)
        digits.append(d)
    if carry:
        digits.append(carry)
    return tuple(digits)


def F(s):
    d = normalize(s)
    return tuple(x + y for x, y in zip(d, d[::-1]))


def raw_words(n):
    """All realizable symmetric sum words of length n, including even central entries at odd lengths."""
    if n == 1:
        yield from ((v,) for v in range(2, 19, 2))
        return
    for a in range(1, 19):
        for tail in product(range(19), repeat=n // 2 - 1):
            left = (a,) + tail
            if n % 2:
                for center in range(0, 19, 2):
                    yield left + (center,) + left[::-1]
            else:
                yield left + left[::-1]


# (output sum, incoming left carry, outgoing right carry) -> (source sum, outgoing left carry, incoming right carry)
LOCAL = {}
for p, x, y in product(range(19), range(2), range(2)):
    LOCAL[p, x, y] = [
        (s, (s + x) // 10, z)
        for s in range(19) for z in (0, 1)
        if (s + z) // 10 == y
        and 2 * s + x + z - 10 * ((s + x) // 10 + y) == p
    ]


def prefix_predecessors(p):
    """Include every actual predecessor prefix; ignored inner digits need not be simultaneously realizable."""
    states = {((), 0, 0)}
    for v in p:
        states = {
            (word + (s,), xx, yy)
            for word, x, y in states
            for s, xx, yy in LOCAL[v, x, y]
            if word or s > 0
        }
    answer = {word for word, _, _ in states}

    if p[0] > 10:
        return answer
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
    answer.update(
        word for word, _, y in states
        if any((word[-1] + z) // 10 == y for z in (0, 1))
    )
    return answer


def forward_prefixes(s):
    """Independent forward algorithm: enumerate the sole unobserved high-end inner carry and add columns directly."""
    k = len(s)
    low, carry = [], 0
    for v in s:
        carry, d = divmod(v + carry, 10)
        low.append(d)
    answer = set()
    for inner_carry in (0, 1):
        high, carry = [0] * k, inner_carry
        for i in range(k - 1, -1, -1):
            carry, high[i] = divmod(s[i] + carry, 10)
        if carry:
            p = (1 + low[0],) + tuple(
                low[i] + high[i - 1] for i in range(1, k)
            )
        else:
            p = tuple(a + b for a, b in zip(low, high))
        answer.add(p)
    return answer


def verify_one(path, independent=False):
    cert = json.loads(path.read_text())
    k = cert['width']
    initial = {tuple(p) for p in cert['initial']}
    rank = {tuple(row['word']): row['rank'] for row in cert['nodes']}
    assert len(rank) == len(cert['nodes'])
    if k == 4:
        expected = {(3, 3, c, d) for c, d in product(range(10), repeat=2)}
        expected.add((3, 3))
    elif k == 5:
        expected = {(7, 7, c, d, e) for c in range(1, 10)
                    for d, e in product(range(10), repeat=2)}
        expected.add((7, 7, 7, 7))
    else:
        raise AssertionError('Undeclared certificate width')
    assert initial == expected

    short_back = defaultdict(set)
    short_count = 0
    for n in range(1, k):
        for s in raw_words(n):
            short_back[F(s)].add(s)
            short_count += 1
    parents = {}
    for p, h in rank.items():
        assert isinstance(h, int) and h >= 0
        assert 1 <= len(p) <= k and p[0] > 0
        assert all(0 <= u <= 18 for u in p)
        ps = set(short_back[p])
        if len(p) == k:
            ps |= prefix_predecessors(p)
        else:
            assert p == p[::-1]
            assert len(p) % 2 == 0 or p[len(p) // 2] % 2 == 0
        parents[p] = ps
        assert ps <= rank.keys(), ('Certificate omits predecessors', p, ps - rank.keys())
        assert h == (0 if not ps else 1 + max(rank[q] for q in ps)), p
        assert all(rank[q] < h for q in ps)

    layer, counts, reachable = initial, [], set()
    while layer:
        counts.append(len(layer))
        reachable |= layer
        layer = {q for p in layer for q in parents[p]}
        assert len(counts) <= 100
    counts.append(0)
    assert reachable == rank.keys()
    assert counts == cert['layer_counts']
    bound = 1 + max(rank[p] for p in initial)
    assert bound == cert['palindrome_height_bound']
    if k == 5:
        by_digit = {str(c): 1 + max(rank[p] for p in initial if p[2] == c)
                    for c in range(1, 10)}
        assert by_digit == cert['third_digit_bounds']

    tested_forward = 0
    if independent:
        # Check every possible long source prefix, independently detecting any omitted inverse branch.
        for first in range(1, 19):
            for tail in product(range(19), repeat=k - 1):
                s = (first,) + tail
                for p in forward_prefixes(s):
                    if p in rank:
                        assert s in rank and rank[s] < rank[p], (s, p)
                tested_forward += 1
        # Also check every edge involving short numbers using actual complete addition.
        for n in range(1, k):
            for s in raw_words(n):
                p = F(s)
                if p in rank:
                    assert s in rank and rank[s] < rank[p], (s, p)

    return {'file': path.name, 'width': k, 'nodes': len(rank),
            'edges': sum(len(v) for v in parents.values()),
            'layer_counts': counts, 'height_bound': bound,
            'short_source_words': short_count,
            'independent_forward_prefixes': tested_forward,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def other_checks():
    root = 1203390
    sharp = [root]
    for _ in range(5):
        sharp.append(T(sharp[-1]))
    assert sharp == [1203390, 2136411, 3282723, 6555546, 13011102, 33122133]
    assert not any(palindrome(n) for n in sharp[:-1])
    assert palindrome(sharp[-1])
    orbit = [196]
    for _ in range(27):
        orbit.append(T(orbit[-1]))
    assert not any(palindrome(n) for n in orbit)

    # For every realizable source with <= 7 digits, compare column formulas with actual complete normalization.
    coverage = 0
    for n in range(1, 8):
        for s in raw_words(n):
            p = F(s)
            for k in (4, 5):
                if n >= k:
                    assert p[:k] in forward_prefixes(s[:k])
            coverage += 1
    assert coverage == 75447

    # Cross-check against independent integer dynamic programming; this finite scan is not an unbounded proof.
    limit = 1_000_000
    heights = bytearray(limit)
    checked_33 = checked_77 = 0
    for n in range(1, limit):
        target = T(n)
        if target < limit:
            heights[target] = max(heights[target], heights[n] + 1)
        s = str(n)
        if s == s[::-1]:
            if s.startswith('33'):
                assert heights[n] <= 5
                checked_33 += 1
            if len(s) >= 3 and s.startswith('77') and s[2] != '0':
                assert heights[n] <= 27
                checked_77 += 1
    return {'sharp_first_hit_33': sharp, 'orbit_196_through_27': orbit,
            'actual_raw_word_controls': coverage,
            'integer_scan_limit_exclusive': limit,
            'palindrome_targets_33': checked_33,
            'palindrome_targets_77_nonzero': checked_77}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--independent-forward', action='store_true')
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    results = [verify_one(directory / name, args.independent_forward)
               for name in ('certificate_33.json', 'certificate_77.json')]
    result = {'status': 'PASS', 'certificates': results, 'controls': other_checks(),
              'scope': 'Supports the listed all-length prefix theorems; neither a complete P196 proof nor a Lean formalization.'}
    print(json.dumps(result, ensure_ascii=False, indent=2))
