#!/usr/bin/env python3
"""Numeric control of `actual_iterPairs_rank4` on the CONCRETE tree `ranks4`
(supplementary evidence only; the theorem itself is kernel-checked).

For every A in [lo, hi) and t <= TMAX, compute the actual pair-sum word of
T^t(A) (q_i = d_i + d_{L-1-i}, i = 0 is the units column), project it to its
first min(L, 4) entries (= project4), and whenever that projection is a node
of ranks4 with rank r, check t <= r.

Usage: rank_tree_control.py RANK4DATA_LEAN LO HI TMAX OUT_JSON
"""
import json
import re
import sys

path, lo, hi, tmax, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
src = open(path, encoding='utf-8').read()
nodes = re.findall(r'\.node (\d+) \[([0-9,]*)\] (\d+) ', src)
rank = {}
for _, w, r in nodes:
    key = tuple(int(x) for x in w.split(',')) if w else ()
    assert key not in rank
    rank[key] = int(r)
assert len(rank) == 7776, len(rank)

hits = 0
viol = []
tight = 0
by_len = {}
for A in range(lo, hi):
    n = A
    for t in range(tmax + 1):
        s = str(n)
        d = [int(ch) for ch in reversed(s)]
        L = len(d)
        k = min(L, 4)
        proj = tuple(d[i] + d[L - 1 - i] for i in range(k))
        r = rank.get(proj)
        if r is not None:
            hits += 1
            by_len[k] = by_len.get(k, 0) + 1
            if t == r:
                tight += 1
            if t > r:
                viol.append([A, t, list(proj), r])
        n = n + int(s[::-1])

res = {'range': [lo, hi], 'tmax': tmax, 'tree_nodes': len(rank),
       'in_tree_events': hits, 'in_tree_events_by_projection_length': by_len,
       'events_with_t_equal_rank': tight,
       'violation_count': len(viol), 'violations': viol[:50]}
json.dump(res, open(out, 'w'), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != 'violations'}))
