#!/usr/bin/env python3
"""Literal-integer control (supplementary evidence, not proof).

For every A in [lo, hi) iterate T(n) = n + reverse(n) for t = 0..TMAX and,
whenever T^t(A) is a palindrome of width >= 3 whose leading three digits are a
table4 prefix, check t <= B.  Also checks width-2 palindrome 33 and the whole
two-digit class 33 against bound 5.

Usage: literal_control.py TABLE4_LEAN LO HI TMAX OUT_JSON
"""
import json
import re
import sys

lean_path, lo, hi, tmax, out_path = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
body = open(lean_path, encoding='utf-8').read().split('def table4')[1]
table = {}
for a, b, c, B in re.findall(r'\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)', body):
    table[a + b + c] = int(B)
assert len(table) == 229

hits = 0
violations = []
per_prefix_max = {}
per_prefix_hits = {}
pal_events = 0
c33_hits = 0
c33_max = -1
c33_viol = []
witness = {}
for A in range(lo, hi):
    n = A
    for t in range(tmax + 1):
        s = str(n)
        if s == s[::-1]:
            pal_events += 1
            if len(s) >= 3:
                p = s[:3]
                B = table.get(p)
                if B is not None:
                    hits += 1
                    per_prefix_hits[p] = per_prefix_hits.get(p, 0) + 1
                    if t > per_prefix_max.get(p, -1):
                        per_prefix_max[p] = t
                        witness[p] = [A, t, s]
                    if t > B:
                        violations.append([A, t, s, B])
            if s.startswith('33'):
                c33_hits += 1
                if t > c33_max:
                    c33_max = t
                if t > 5:
                    c33_viol.append([A, t, s])
        n = n + int(s[::-1])

tight = sorted(p for p in per_prefix_max if per_prefix_max[p] == table[p])
res = {
    'range': [lo, hi], 'tmax': tmax,
    'palindrome_events': pal_events,
    'listed_prefix_hits': hits,
    'violations': violations[:50], 'violation_count': len(violations),
    'distinct_listed_prefixes_hit': len(per_prefix_max),
    'listed_prefixes_never_hit': sorted(set(table) - set(per_prefix_max)),
    'prefixes_where_observed_max_equals_B': tight,
    'per_prefix_max_t': dict(sorted(per_prefix_max.items())),
    'per_prefix_hits': dict(sorted(per_prefix_hits.items())),
    'per_prefix_deepest_witness': dict(sorted(witness.items())),
    'class33_hits_all_widths': c33_hits, 'class33_max_t': c33_max,
    'class33_violations': c33_viol[:50],
}
json.dump(res, open(out_path, 'w'), indent=1)
print(json.dumps({k: res[k] for k in ('range', 'tmax', 'palindrome_events', 'listed_prefix_hits',
                                       'violation_count', 'distinct_listed_prefixes_hit',
                                       'class33_hits_all_widths', 'class33_max_t')}))
