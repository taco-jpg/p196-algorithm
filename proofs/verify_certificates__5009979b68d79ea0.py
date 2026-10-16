#!/usr/bin/env python3
"""核验七列首部证书。仅用 Python 标准库，不需要原仓库。

默认：重算全部逆向边、秩和短数边界，并用正向方程逐边核对。
逆向公式逐状态重算全部允许前驱，正向公式逐边交叉检查。
无限长度覆盖依据配套证明；本程序不是完整 P196 猜想的形式化证明。
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
    """长度 n 的全部可实现对称和字，含奇数长度的中心偶数条件。"""
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


# (输出和, 左入进位, 右出进位) -> (来源和, 左出进位, 右入进位)
LOCAL = {}
for p, x, y in product(range(19), range(2), range(2)):
    LOCAL[p, x, y] = [
        (s, (s + x) // 10, z)
        for s in range(19) for z in (0, 1)
        if (s + z) // 10 == y
        and 2 * s + x + z - 10 * ((s + x) // 10 + y) == p
    ]


def prefix_predecessors(p):
    """包含所有真实前驱前缀；不要求被忽略的内侧数位能同时实现。"""
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
    """独立正向算法：枚举唯一未观测的高端内侧进位，直接做列加法。"""
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


def verify_one(path):
    cert = json.loads(path.read_text())
    k = cert['width']
    initial = {tuple(p) for p in cert['initial']}
    rank = {tuple(row['word']): row['rank'] for row in cert['nodes']}
    assert len(rank) == len(cert['nodes'])
    assert k == 7
    abc = tuple(map(int, cert['prefix']))
    assert cert['prefix'] in ('217', '218', '620', '739', '777')
    expected = {abc + tail for tail in product(range(10), repeat=k - 3)}
    for n in range(3, k):
        for half in product(range(10), repeat=(n + 1) // 2):
            p = half + half[:n // 2][::-1]
            if p[:3] == abc and (n % 2 == 0 or p[n // 2] % 2 == 0):
                expected.add(p)
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
        assert ps <= rank.keys(), ('证书缺失前驱', p, ps - rank.keys())
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
    long_layer = {p for p in initial if len(p) == k}
    long_counts = []
    while long_layer:
        long_counts.append(len(long_layer))
        long_layer = {q for p in long_layer for q in parents[p] if len(q) == k}
    long_counts.append(0)
    assert long_counts == cert['long_only_layer_counts']
    discovery = json.loads((path.parent / 'accepted_cpp_results.json').read_text())
    assert discovery[cert['prefix']]['counts'] == long_counts
    assert discovery[cert['prefix']]['depth'] == bound
    # Every stored long inverse edge also satisfies the independent forward equations.
    forward_edges = 0
    for p, ps in parents.items():
        for q in ps:
            if len(q) == k:
                assert p in forward_prefixes(q), (q, p)
                forward_edges += 1
            else:
                assert F(q) == p, (q, p)

    return {'file': path.name, 'width': k, 'nodes': len(rank),
            'edges': sum(len(v) for v in parents.values()),
            'layer_counts': counts, 'height_bound': bound,
            'short_source_words': short_count,
            'forward_edges_checked': forward_edges,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def other_checks():
    orbit = [196]
    for _ in range(39):
        orbit.append(T(orbit[-1]))
    assert not any(palindrome(n) for n in orbit)
    coverage = 0
    for n in (7, 8):
        for s in raw_words(n):
            p = F(s)
            assert p[:7] in forward_prefixes(s[:7])
            coverage += 1
    assert coverage == 188442
    # Fixed reproducible long-word controls. These are checks, not the unbounded proof.
    import random
    rng = random.Random(196739)
    long_controls = 0
    for n in (9, 10, 15, 16, 31, 32, 63, 64, 127, 128):
        for _ in range(200):
            left = (rng.randrange(1, 19),) + tuple(rng.randrange(19) for _ in range(n // 2 - 1))
            s = left + ((rng.randrange(10) * 2,) if n % 2 else ()) + left[::-1]
            assert F(s)[:7] in forward_prefixes(s[:7])
            long_controls += 1
    bounds = {'217': 23, '218': 34, '620': 12, '739': 39, '777': 25}
    limit = 1_000_000
    heights = bytearray(limit)
    checked = dict.fromkeys(bounds, 0)
    for n in range(1, limit):
        target = T(n)
        if target < limit:
            heights[target] = max(heights[target], heights[n] + 1)
        s = str(n)
        if s == s[::-1] and s[:3] in bounds:
            assert heights[n] <= bounds[s[:3]]
            checked[s[:3]] += 1
    old = json.loads((Path(__file__).resolve().parent / 'baseline_396.json').read_text())
    assert len(old) == 396 and '739' not in old
    for prefix in ('217', '218', '620', '777'):
        assert bounds[prefix] < old[prefix]
    assert len(set(old) | {'739'}) == 397
    return {'orbit_196_through_39': orbit, 'actual_raw_word_controls': coverage,
            'long_word_controls': long_controls, 'integer_scan_limit_exclusive': limit,
            'palindrome_targets_checked': checked, 'baseline_prefixes': 396,
            'extended_prefixes': 397}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    results = [verify_one(directory / name)
               for name in ('certificate_217.json', 'certificate_218.json', 'certificate_620.json', 'certificate_739.json', 'certificate_777.json')]
    result = {'status': 'PASS', 'certificates': results, 'controls': other_checks(),
              'scope': '支持所列全长度前缀定理；不是完整 P196 证明，也未作 Lean 形式化。'}
    print(json.dumps(result, ensure_ascii=False, indent=2))
