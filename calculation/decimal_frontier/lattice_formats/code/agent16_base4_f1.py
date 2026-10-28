#!/usr/bin/env python3
"""Exact independent root-column enumeration for overflow word 101100.

Only tests F1 compatibility of bauto3's canonical starting cut state.
No SCC or infinite reverse-and-add orbit is claimed.
"""

from itertools import product

WORD = '101100'


def enumerate_first_column(base: int, word: str):
    g = tuple(map(int, word))
    p = len(g)
    roots = []
    for x0 in range(1, 2*base-1):
        for c in product((0, 1), repeat=p):
            x = x0
            trail = []
            for t, bit in enumerate(g):
                if (x+c[t])//base != bit:
                    break
                trail.append(x)
                x = (x % base) + (1 if bit else (x+c[t]) % base)
            else:
                if x == x0:
                    roots.append((tuple(trail), c))
    return roots


def rotate(s, n):
    return s[n:]+s[:n]


def expected_paths(b):
    if b == 4:
        return (4,1,3,4,1,2)
    if b == 5:
        return (6,2,4,5,1,3)
    if b == 6:
        return (7,2,5,6,1,3)
    return None


def main():
    for b in range(2, 201):
        for k in range(6):
            actual = enumerate_first_column(b, rotate(WORD, k))
            assert len(actual) == (4 if b in (4,5,6) else 0), (b, k, actual)
            if b in (4,5,6):
                assert all(path == tuple(expected_paths(b)[k:]+expected_paths(b)[:k])
                           for path, _ in actual), (b,k,actual)
        if b in (4,5,6,7,16,40,100,200):
            print('base',b,'paths',len(enumerate_first_column(b,WORD)),
                  'example',enumerate_first_column(b,WORD)[:1])
    print('PASS: all six rotations, every base 2..200, exactly b=4,5,6 have four paths')


if __name__ == '__main__':
    main()
