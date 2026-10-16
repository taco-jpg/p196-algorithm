#!/usr/bin/env python3
"""Exact ancestry depth H(n) = max{k : exists A >= 1, T^k(A) = n} for all n < N.

Since T(m) = m + rev(m) > m for m >= 1, every predecessor of n is < n, so a
single increasing pass  depth[T(m)] = max(depth[T(m)], depth[m] + 1)  is exact.
Then every palindrome P < N is checked against table4 (width >= 3) and against
the two-digit class 33 (width >= 2, bound 5).  Supplementary evidence only:
this covers palindromes of width <= len(str(N-1)) exhaustively.

Usage: exact_depth.py TABLE4_LEAN N OUT_JSON
"""
import json
import re
import sys
import time

lean_path, N, out_path = sys.argv[1], int(sys.argv[2]), sys.argv[3]
body = open(lean_path, encoding='utf-8').read().split('def table4')[1]
table = {a + b + c: int(B) for a, b, c, B in re.findall(r'\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)', body)}
assert len(table) == 229

t0 = time.time()
depth = bytearray(N)
for m in range(1, N):
    n = m + int(str(m)[::-1])
    if n < N:
        d = depth[m] + 1
        if d > depth[n]:
            depth[n] = d
t1 = time.time()


def palindromes(width):
    half = (width + 1) // 2
    for left in range(10 ** (half - 1), 10 ** half):
        s = str(left)
        yield int(s + (s[-2::-1] if width % 2 else s[::-1]))


maxw = len(str(N - 1))
checked = 0
violations = []
per_prefix = {}
per_prefix_width = {}
c33 = {}
c33_viol = []
global_max = 0
for w in range(1, maxw + 1):
    for P in palindromes(w):
        if P >= N:
            continue
        h = depth[P]
        global_max = max(global_max, h)
        s = str(P)
        if w >= 2 and s.startswith('33'):
            if h > c33.get(w, -1):
                c33[w] = h
            if h > 5:
                c33_viol.append([P, h])
        if w >= 3 and s[:3] in table:
            checked += 1
            p = s[:3]
            if h > per_prefix.get(p, (-1, None))[0]:
                per_prefix[p] = (h, P)
            key = f'{p}/w{w}'
            per_prefix_width[key] = max(per_prefix_width.get(key, -1), h)
            if h > table[p]:
                violations.append([P, h, table[p]])

slack = {p: table[p] - per_prefix[p][0] for p in per_prefix}
res = {
    'N': N, 'max_width_exhaustive': maxw, 'dp_seconds': round(t1 - t0, 1),
    'max_depth_any_palindrome_below_N': global_max,
    'listed_palindromes_checked': checked,
    'violations': violations[:50], 'violation_count': len(violations),
    'prefixes_with_some_palindrome_below_N': len(per_prefix),
    'per_prefix_exact_max_H_and_witness': {p: list(v) for p, v in sorted(per_prefix.items())},
    'prefixes_where_exact_max_H_equals_B': sorted(p for p in slack if slack[p] == 0),
    'slack_histogram': {str(k): sum(1 for v in slack.values() if v == k) for k in sorted(set(slack.values()))},
    'class33_exact_max_H_by_width': {str(k): v for k, v in sorted(c33.items())},
    'class33_violations': c33_viol[:50],
    'H_33': depth[33] if N > 33 else None,
    'H_333': depth[333] if N > 333 else None,
    'H_33266233': depth[33266233] if N > 33266233 else None,
}
json.dump(res, open(out_path, 'w'), indent=1)
print(json.dumps({k: res[k] for k in ('N', 'dp_seconds', 'max_depth_any_palindrome_below_N',
                                       'listed_palindromes_checked', 'violation_count',
                                       'prefixes_with_some_palindrome_below_N',
                                       'class33_exact_max_H_by_width', 'H_33', 'H_333',
                                       'H_33266233', 'slack_histogram')}))
