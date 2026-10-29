#!/usr/bin/env python3
"""Standalone Python bigint controls; does not import C++ code."""
import csv
import hashlib
import random
import sys
from pathlib import Path

EXPECTED_SHA = 'b79a51e8aae26e2bfab60653b35c9635ca35fcae8fdc121f16cf0326d216c86f'

def reverse_add(s):
    return str(int(s) + int(s[::-1]))

def padded(s, gap):
    midpoint = len(s) // 2
    return s[:midpoint] + '0' * gap + s[midpoint:]

def zero_corridor(s):
    m = len(s) // 2
    pairs = [int(s[i]) + int(s[-i-1]) for i in range(m)]
    last = max((j + 1 for j, pair in enumerate(pairs) if pair), default=0)
    return len(s) - 2 * last

rng = random.Random(120262810)
for _ in range(4000):
    w = rng.randint(1, 16)
    left = str(rng.randint(10 ** (w - 1), 10 ** w - 1))
    right = ''.join(str(rng.randrange(10)) for _ in range(w))
    s = left + '0' * rng.randint(4, 35) + right
    assert zero_corridor(s) >= 4
    a = reverse_add(s)
    for k in (1, 2, 7, 13):
        b = padded(s, k)
        assert reverse_add(b) == padded(a, k), (s, k)
        assert (b == b[::-1]) == (s == s[::-1]), (s, k)
print('PYTHON_BIGINT_PADDING_CONTROLS_PASS 16000')

master = Path(sys.argv[1])
assert hashlib.sha256(master.read_bytes()).hexdigest() == EXPECTED_SHA
rows = list(csv.DictReader(master.open()))
assert len(rows) == 257
assert [int(r['k']) for r in rows] == list(range(257))
assert [int(r['gap']) for r in rows] == list(range(31000,31257))
assert all(r['first_pal'] == '-1' and r['final_z'] == '0' for r in rows)
assert set(int(r['max_mismatch_index_through_collision']) for r in rows) == {21}
times = [int(r['first_zero']) for r in rows]
assert times[0] == 51464 and times[-1] == 51886
assert min(times) == 51464 and max(times) == 51886
assert sum(b < a for a, b in zip(times, times[1:])) == 42
assert all(int(r['activation']) < int(r['first_zero']) for r in rows)
for k, expected in [(0,51464),(1,51465),(2,51466),(3,51470),(4,51468),(16,51487),(32,51513),(64,51565),(96,51621),(128,51671),(160,51727),(192,51785),(224,51838),(256,51886)]:
    assert times[k] == expected, (k,times[k],expected)
print('257_MASTER_TRANSFER_TIMES_PASS 42_LOCAL_REVERSALS')

for gap, filename in [(31004,sys.argv[2]),(31256,sys.argv[3])] if len(sys.argv) == 4 else []:
    trace = list(csv.DictReader(open(filename)))
    t0 = next(i for i,x in enumerate(trace) if int(x['central_zeros']) == 0)
    expected = rows[gap-31000]
    assert t0 == int(expected['first_zero']),(gap,t0,expected)
    assert max(int(x['mismatch']) for x in trace[:t0+1]) == 21
    assert all(int(x['mismatch']) >= 0 for x in trace[:t0+1])
    assert int(trace[t0]['length']) > 52000
    print(f'INDEPENDENT_RADIX_1E9_FULL_SEED_PASS gap={gap} collision={t0}')
print('AGENT_N12_MASTER_SWEEP_COMPLETE_PASS' if len(sys.argv) == 4 else 'AGENT_N12_MASTER_SWEEP_TABLE_PASS (direct full-seed checks run separately)')
