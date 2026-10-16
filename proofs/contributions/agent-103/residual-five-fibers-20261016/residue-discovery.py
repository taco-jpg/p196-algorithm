#!/usr/bin/env python3
"""有限诊断：独立逐字复现 Agent101 数位枚举的数学定义。

本程序不提供 Lean 证明。正式命题仍须从原 numericFiber 建立。
数位始终从低位到高位；不得把数位和词当成整数枚举。
"""

from collections import Counter
from itertools import product
import json


def pair_choices(outer, total):
    return [(a, b) for a in range(10) for b in range(10)
            if a + b == total and (not outer or b > 0)]


def numeric_fiber(r):
    choices = [pair_choices(True, 2), pair_choices(False, 12)]
    choices.extend([pair_choices(False, 9)] * r)
    for pairs in product(*choices):
        ds = [a for a, _ in pairs] + [b for _, b in reversed(pairs)]
        n = sum(d * 10 ** i for i, d in enumerate(ds))
        assert ds[-1] > 0 and all(0 <= d <= 9 for d in ds)
        assert [a + b for a, b in zip(ds, reversed(ds))] == [2, 12] + [9] * (2*r) + [12, 2]
        assert n + int(str(n)[::-1]) == 33 * 10 ** (2*r + 2) + 22
        yield n


def run():
    results = []
    previous = None
    for r in range(5):
        values = list(numeric_fiber(r))
        histogram = Counter(n % 99 for n in values)
        count = histogram[77]
        expected = (14 * 10 ** r + (8 if r % 2 == 0 else -8)) // 11
        assert len(values) == len(set(values)) == 14 * 10 ** r
        assert all(n % 9 == 5 for n in values)
        assert sum(n % 11 == 0 for n in values) == count == expected
        if previous is not None:
            assert count + previous == 14 * 10 ** (r - 1)
        results.append({'r': r, 'total': len(values), 'count_77': count,
                        'histogram': dict(sorted(histogram.items())),
                        'qualifying_values': [n for n in values if n % 99 == 77] if r == 0 else None})
        previous = count
    return {'status': 'FINITE_DIAGNOSTIC_ONLY', 'definition_source': 'Agent101.numericFiber / canonicalWords / pairChoices', 'results': results}


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, indent=2))
