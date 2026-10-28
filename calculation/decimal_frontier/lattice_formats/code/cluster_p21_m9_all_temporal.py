#!/usr/bin/env python3
"""Canonical equivalence classes of periodic bulk rows: spatial rotations and full 21-step time shifts."""
import re
import sys
from collections import Counter, defaultdict

B, M, G = 10, 9, '001001010101001010101'

def phi(row, gam):
    z = next((i for i, x in enumerate(row) if x != 9), None)
    if z is None:
        return None
    a, d = [0] * M, [0] * M
    a[(z + 1) % M] = d[(z - 1) % M] = int(row[z] >= B)
    for j in range(1, M):
        i = (z + j) % M
        a[(i + 1) % M] = (row[i] + a[i]) // B
        i = (z - j) % M
        d[(i - 1) % M] = (row[i] + d[i]) // B
    e = [(row[i] + a[i]) % B for i in range(M)]
    f = [(row[i] + d[i]) % B for i in range(M)]
    return tuple(e[i] + f[(i - gam) % M] for i in range(M))

def block(row):
    for bit in G:
        row = phi(row, int(bit))
    return row

def canonical(row, k):
    rows = []
    for _ in range(k):
        rows.append(row)
        row = block(row)
    assert row == rows[0]
    return min(
        tuple(tuple(rows[(t + phase) % k][(i + rot) % M] for i in range(M))
              for t in range(k))
        for phase in range(k) for rot in range(M)
    )

def main(path):
    classes = defaultdict(list)
    periods = Counter()
    for line in open(path, encoding='utf-8'):
        m = re.fullmatch(r'AXIS=(\d+) K=(\d+) ROW=([0-9,]+)\n?', line)
        assert m, line
        axis, k = int(m[1]), int(m[2])
        row = tuple(map(int, m[3].split(',')))
        assert len(row) == M
        periods[k] += 1
        classes[(k, canonical(row, k))].append((axis, row))
    family = Counter(k for k, _ in classes)
    print('primitive cycles by k:', dict(sorted(periods.items())))
    print('families by k:', dict(sorted(family.items())))
    print('total cycles:', sum(periods.values()), 'families:', len(classes))
    assert dict(sorted(periods.items())) == {
        2: 45, 4: 54, 8: 9, 16: 36, 24: 18, 30: 9, 32: 18, 34: 9, 54: 9
    }
    assert dict(sorted(family.items())) == {
        2: 5, 4: 6, 8: 1, 16: 4, 24: 2, 30: 1, 32: 2, 34: 1, 54: 1
    }

if __name__ == '__main__':
    main(sys.argv[1])
