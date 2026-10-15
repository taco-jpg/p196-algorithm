#!/usr/bin/env python3
"""Reviewer's independent comparison of Table4.lean against section 6 of the
written source (p196_four_column_obstruction.md), with the stated exclusions.

Usage: compare_table.py WRITTEN_MD TABLE4_LEAN OUT_JSON
"""
import json
import re
import sys

md_path, lean_path, out_path = sys.argv[1:4]

# ---- parse section 6 of the written source ----
md = open(md_path, encoding='utf-8').read()
sec6 = md.split('## 6.')[1].split('```python')[0]
written = {}
rows = 0
for line in sec6.splitlines():
    m = re.match(r'^\|\s*(\d\d)\s*\|\s*([0-9:,\s]+?)\s*\|\s*$', line)
    if not m:
        continue
    rows += 1
    ab = m.group(1)
    for item in m.group(2).split(','):
        c, b = item.strip().split(':')
        key = int(ab) * 10 + int(c)
        assert key not in written, key
        written[key] = int(b)

# ---- parse Table4.lean ----
lean = open(lean_path, encoding='utf-8').read()
body = lean.split('def table4')[1]
tuples = re.findall(r'\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)', body)
table4 = []
for a, b, c, B in tuples:
    table4.append((int(a), int(b), int(c), int(B)))
keys = [100 * a + 10 * b + c for a, b, c, _ in table4]
assert len(set(keys)) == len(keys), 'duplicate keys in table4'
t4 = {100 * a + 10 * b + c: B for a, b, c, B in table4}

EXCL2 = {10, 20, 32, 40, 41, 60, 64, 65, 76, 80, 81, 82, 83}
EXCL3 = {620}
expected = {k: v for k, v in written.items() if (k // 10) not in EXCL2 and k not in EXCL3}

missing = sorted(set(expected) - set(t4))
extra = sorted(set(t4) - set(expected))
mismatch = sorted(k for k in set(expected) & set(t4) if expected[k] != t4[k])
digit_ok = all(1 <= a <= 9 and 0 <= b <= 9 and 0 <= c <= 9 for a, b, c, _ in table4)
growth = sorted(k for k in t4 if k in (110, 111, 121, 122))
from collections import Counter
res = {
    'written_rows': rows,
    'written_entries': len(written),
    'written_max_bound': max(written.values()),
    'written_distribution': dict(sorted(Counter(written.values()).items())),
    'excluded_two_digit': sorted(EXCL2),
    'excluded_three_digit': sorted(EXCL3),
    'excluded_entry_count': len(written) - len(expected),
    'expected_entries': len(expected),
    'table4_entries': len(table4),
    'table4_unique_keys': len(set(keys)),
    'missing_from_table4': missing,
    'extra_in_table4': extra,
    'bound_mismatches': [(k, expected[k], t4[k]) for k in mismatch],
    'all_digits_valid': digit_ok,
    'growth_prefixes_in_table4': growth,
    'equal': not missing and not extra and not mismatch,
    'table4_max_bound': max(t4.values()),
    'table4_distribution': dict(sorted(Counter(t4.values()).items())),
}
json.dump(res, open(out_path, 'w'), indent=1)
print(json.dumps(res, indent=1))
