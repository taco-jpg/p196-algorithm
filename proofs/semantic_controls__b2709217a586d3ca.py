#!/usr/bin/env python3
"""Supplementary finite controls using independent integer reverse-and-add."""
from pathlib import Path
from itertools import product
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent
START = time.monotonic()

def digits(n, b):
    answer = []
    while n:
        n, r = divmod(n, b)
        answer.append(r)
    return answer

def evaluate(ds, b):
    return sum(d * b**i for i, d in enumerate(ds))

def rhs_zero(b, x, a, c):
    return ((x == 0 and a == c == 0) or
            (x == b and a == c == 0) or
            (x == b-1 and a == c == 1))

def rhs_max(b, x, a, c):
    return ((x == b-1 and a == c == 0) or
            (x == b-2 and a == c == 1) or
            (x == 2*b-2 and a == c == 1))

scalar_count = 0
for b in range(2, 33):
    for x in range(2*b-1):
        for a, c in product((0, 1), repeat=2):
            pair = (x+a) % b + (x+c) % b
            assert (pair == 0) == rhs_zero(b, x, a, c)
            assert (pair == 2*b-2) == rhs_max(b, x, a, c)
            if a != c:
                assert pair not in (0, 2*b-2)
            if b >= 3 and ((pair == 0 and x != 0) or
                           (pair == 2*b-2 and x != 2*b-2)):
                assert 0 < x < 2*b-2
            scalar_count += 1

by_base = []
for b in range(2, 11):
    max_width = 7 if b in (2, 3) else 4
    record = dict(base=b, max_input_width=max_width,
                  canonical_inputs=0, nooverflow_inputs=0,
                  nooverflow_pair_positions=0, overflow_inputs=0)
    for n in range(1, b**max_width):
        ds = digits(n, b)
        width = len(ds)
        rev = evaluate(ds[::-1], b)
        integer_output = digits(n + rev, b)
        qs = [ds[i] + ds[width-1-i] for i in range(width)]
        carry = [0]
        coefficient_output = []
        for q in qs:
            outgoing, emitted = divmod(q + carry[-1], b)
            carry.append(outgoing)
            coefficient_output.append(emitted)
        if carry[-1]:
            coefficient_output.append(carry[-1])
        assert coefficient_output == integer_output
        assert len(integer_output) == width + carry[-1]
        assert integer_output[-1] > 0
        assert all(0 <= d < b for d in integer_output)
        record['canonical_inputs'] += 1
        if carry[-1]:
            record['overflow_inputs'] += 1
            continue
        record['nooverflow_inputs'] += 1
        assert len(integer_output) == width
        for k, q in enumerate(qs):
            mirror = width-1-k
            actual_pair = integer_output[k] + integer_output[mirror]
            a, c = carry[k], carry[mirror]
            assert actual_pair == (q+a) % b + (q+c) % b
            assert (actual_pair == 0) == rhs_zero(b, q, a, c)
            assert (actual_pair == 2*b-2) == rhs_max(b, q, a, c)
            record['nooverflow_pair_positions'] += 1
    by_base.append(record)

result = dict(status='PASS', role='Supplementary controls, not unrestricted proof',
              script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              scalar_cases=scalar_count, scalar_base_range=[2,32],
              integer_controls=by_base,
              binary_swaps=[dict(x=0, carry_left=1, carry_right=1, output=2),
                            dict(x=2, carry_left=0, carry_right=0, output=0)],
              elapsed_seconds=time.monotonic()-START)
(HERE/'semantic_controls.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
