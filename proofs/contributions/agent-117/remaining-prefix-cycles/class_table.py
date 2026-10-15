#!/usr/bin/env python3
"""Rebuild the prefix-class table of the pure k-column abstraction from the compact
outputs of wellfounded7.cpp:

  rows_rank<k>.bin   : one byte per long initial row (a,b,c,d_3,...,d_{k-1}), digits
                       0..9, a >= 1, lexicographic order; 255 = unbounded, else the rank.
  short_rank<k>.tsv  : "s_0,...,s_{n-1}<TAB>rank" for every complete word of width < k.

A class of D leading digits (3 <= D <= k) is CLOSED at k columns iff every long initial
row with that prefix and every complete short palindrome word of width 3..k-1 with that
prefix and an even centre is bounded; its bound is 1 + max rank over those states.

usage: class_table.py K DIR D [--list-closed | --list-open]   (prints counts; optional lists)
"""
import sys, gzip, pathlib
from itertools import product

def load(k, d):
    d = pathlib.Path(d)
    fn = d / f'rows_rank{k}.bin'
    rows = (gzip.open(str(fn) + '.gz').read() if not fn.exists() else fn.read_bytes())
    assert len(rows) == 9 * 10 ** (k - 1), len(rows)
    short = {}
    for l in open(d / f'short_rank{k}.tsv'):
        w, r = l.rstrip('\n').split('\t')
        short[tuple(int(x) for x in w.split(','))] = int(r)
    return rows, short

def row_index(digits, k):
    # digits: k digits with digits[0] >= 1
    idx = digits[0] - 1
    for x in digits[1:]:
        idx = idx * 10 + x
    return idx

def classes(k, rows, short, D):
    """yield (prefix string, closed, bound) for every D-digit prefix."""
    for head in product(range(1, 10), *([range(10)] * (D - 1))):
        closed, maxr = True, -1
        for tail in product(range(10), repeat=k - D):
            r = rows[row_index(head + tail, k)]
            if r == 255:
                closed = False
            elif r > maxr:
                maxr = r
        for n in range(max(3, D), k):
            h = (n + 1) // 2
            for mid in product(range(10), repeat=max(0, h - D)):
                half = (head + mid)[:h]
                w = half + half[:n // 2][::-1]
                if w[:D] != head or (n % 2 and w[n // 2] % 2):
                    continue
                r = short[w]
                if r == 255:
                    closed = False
                elif r > maxr:
                    maxr = r
        yield ''.join(map(str, head)), closed, (maxr + 1 if closed else -1)

if __name__ == '__main__':
    k, d, D = int(sys.argv[1]), sys.argv[2], int(sys.argv[3])
    rows, short = load(k, d)
    n = closed = 0
    for pre, c, b in classes(k, rows, short, D):
        n += 1; closed += c
        if ('--list-closed' in sys.argv and c) or ('--list-open' in sys.argv and not c):
            print(pre, b)
    print(f'k={k} D={D} classes={n} closed={closed}')
