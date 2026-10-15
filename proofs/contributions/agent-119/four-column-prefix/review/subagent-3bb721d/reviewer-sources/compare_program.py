#!/usr/bin/env python3
"""Compare the bounds printed by the original written program with table4.

Usage: compare_program.py PROGRAM_STDOUT TABLE4_LEAN OUT_JSON
"""
import ast
import json
import re
import sys

stdout_path, lean_path, out_path = sys.argv[1:4]
bounds = None
for line in open(stdout_path, encoding='utf-8'):
    if line.startswith('bounds '):
        bounds = ast.literal_eval(line[len('bounds '):].strip())
assert isinstance(bounds, dict)

lean = open(lean_path, encoding='utf-8').read().split('def table4')[1]
t4 = {100 * int(a) + 10 * int(b) + int(c): int(B)
      for a, b, c, B in re.findall(r'\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)', lean)}

EXCL2 = {10, 20, 32, 40, 41, 60, 64, 65, 76, 80, 81, 82, 83}
EXCL3 = {620}
restricted = {k: v for k, v in bounds.items() if k // 10 not in EXCL2 and k not in EXCL3}
res = {
    'program_classes': len(bounds),
    'program_max_bound': max(bounds.values()),
    'restricted_classes': len(restricted),
    'table4_classes': len(t4),
    'missing_from_table4': sorted(set(restricted) - set(t4)),
    'extra_in_table4': sorted(set(t4) - set(restricted)),
    'bound_mismatches': sorted((k, restricted[k], t4[k]) for k in set(t4) & set(restricted)
                               if restricted[k] != t4[k]),
}
res['equal'] = not res['missing_from_table4'] and not res['extra_in_table4'] and not res['bound_mismatches']
json.dump(res, open(out_path, 'w'), indent=1)
print(json.dumps(res, indent=1))
