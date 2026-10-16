#!/usr/bin/env python3
"""Independent literal-integer replay of the frozen 185 two-step controls."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def radix(n, b):
    assert n > 0
    out = []
    power = 1
    while power <= n:
        out.append((n // power) % b)
        power *= b
    return out


def val(q, b):
    result = 0
    for a in reversed(q):
        result = b * result + a
    return result


def step(n, b):
    original, reverse = n, 0
    while n:
        reverse = b * reverse + n % b
        n //= b
    return original + reverse


def prefix_carries(q, b):
    # Carry from a prefix is its complete integer value divided by the
    # next place value. This does not use a columnwise carry recurrence.
    prefix, power, result = 0, 1, []
    for a in q:
        prefix += a * power
        power *= b
        result.append(prefix // power)
    return result


def audit_seam(q, lengths, b, stored):
    actual_carries = prefix_carries(q, b)
    raw = [0] * (len(q) + 1)
    defect = []
    offset = 0
    for width in lengths:
        block = q[offset:offset + width]
        integer = val(block, b)
        for j in range(width + 1):
            raw[offset + j] += (integer // b ** j) % b
        isolated_carries = prefix_carries(block, b)
        defect.extend(actual_carries[offset + j] - isolated_carries[j]
                      for j in range(width))
        offset += width
    assert offset == len(q)
    normalized = radix(val(q, b), b)
    assert stored['isolated_raw'] == raw
    assert stored['normalized'] == normalized
    assert stored['active_polynomial'] == defect
    deficit = sum(raw) - sum(normalized)
    assert deficit == (b - 1) * sum(defect) == stored['digit_mass_deficit']
    assert 2 * deficit == stored['pair_mass_deficit']
    correction = [-b * x for x in defect] + [0]
    for j, x in enumerate(defect):
        correction[j + 1] += x
    assert [x + y for x, y in zip(raw, correction)] == normalized + [0] * (len(raw) - len(normalized))


def key(kind, b, q):
    return kind, b, tuple(q)


def main():
    rows = json.loads((HERE / 'controls.json').read_text())
    producer = json.loads((HERE / 'verification.json').read_text())
    assert len(rows) == producer['cases'] == 185
    assert sha256((HERE / 'controls.json').read_bytes()).hexdigest() == producer['controls_sha256']
    assert sha256((HERE / 'check_obstruction.py').read_bytes()).hexdigest() == producer['source_sha256']
    expected = []
    for b in range(3, 13):
        h = (b - 1) // 2
        expected.extend(key('two_column_interval', b, [a, a]) for a in range(b, b + h))
        expected.extend(key('four_column_interval', b, [b, a, a, b]) for a in range(b - 1, b + h))
        for m in (1, 2, 4):
            expected.append(key('canonical_collision', b, [b, b] + [b - 1] * (2 * m) + [b, b]))
            expected.append(key('shorter_whole_word', b, [b] + [b - 1] * (2 * m) + [b]))
        for q in ([b, b], [b + 1, b + 1], [2 * b - 2] * 4,
                  [2 * b - 2, b - 1, b - 1, 2 * b - 2], [b, 2 * b - 2, 2 * b - 2, b]):
            expected.append(key('exact_adjacent_criterion', b, q))
        if b % 2 == 0:
            expected.append(key('exact_adjacent_criterion', b, [b]))
    assert Counter(expected) == Counter(key(row['kind'], row['base'], row['pair_word']) for row in rows)
    for row in rows:
        b, q, n = row['base'], row['pair_word'], row['seed']
        digits = radix(n, b)
        assert q == [a + c for a, c in zip(digits, reversed(digits))]
        assert q == q[::-1] and len(q) == len(digits)
        assert q[0] >= b and all(b - 1 <= a <= 2 * b - 2 for a in q)
        if len(q) % 2:
            assert q[len(q) // 2] % 2 == 0
        n1, n2 = step(n, b), step(step(n, b), b)
        assert (n1, n2) == (row['first_output'], row['second_output'])
        d1, d2 = radix(n1, b), radix(n2, b)
        assert d1 == [q[0] - b] + [a + 1 - b for a in q[1:]] + [1]
        assert (d1 == d1[::-1]) == all(a == b + 1 for a in q)
        r = [a - b + 1 for a in q]
        updated = [a + c for a, c in zip(d1, reversed(d1))]
        assert updated == [r[0]] + [r[j - 1] + r[j] for j in range(1, len(r))] + [r[0]]
        bounded = all(q[j - 1] + q[j] <= 3 * b - 3 for j in range(1, len(q)))
        assert (d2 == d2[::-1]) == bounded
        if row['kind'] == 'exact_adjacent_criterion':
            assert row['next_pair_word'] == updated
            assert row['all_adjacent_sums_bounded'] == bounded
            assert row['second_output_palindromic'] == bounded
            if not bounded:
                assert updated[0] // b == 0 and any(a // b == 1 for a in updated)
        else:
            h = (b - 1) // 2
            assert all(a <= b + h - 1 for a in q) and max(d1) <= h
            assert row['first_output_digits'] == d1 and row['second_output_digits'] == d2
            assert bounded and row['first_palindrome_time'] == (1 if d1 == d1[::-1] else 2)
        if row['kind'] == 'canonical_collision':
            m = row['m']
            assert n == b ** (2 * m + 4) - b ** (m + 2) + b + 1
            assert digits != digits[::-1]
            assert n1 == b ** (2 * m + 2) * (b * b + b + 1) + b
            assert row['isolated_overflow_bits'] == [val([b, b], b) // b ** 2,
                                                     val([b - 1] * (2 * m), b) // b ** (2 * m)] == [1, 0]
            audit_seam(q, [2, 2 * m, 2], b, row['three_block'])
            audit_seam(q, [1] * len(q), b, row['singleton'])
            assert row['three_block']['active_polynomial'] == [0, 0] + [1] * (2 * m) + [0, 0]
            assert max(updated) <= 2 < b
        if row['kind'] == 'shorter_whole_word':
            m = row['m']
            assert n == b ** (2 * m + 2) - b ** (m + 1) + 1
            assert n1 == (b + 1) * b ** (2 * m + 1)
            assert n2 == (b + 1) * (b ** (2 * m + 1) + 1)
            assert row['singleton_exterior_canonical'] == (b % 2 == 0)
    report = {
        'status': 'PASS_INDEPENDENT_185_CONTROLS', 'cases': len(rows),
        'kinds': dict(sorted(Counter(row['kind'] for row in rows).items())),
        'scope': 'Independent replay of every preserved control; all-parameter proof reviewed separately; no additional search.',
        'method': 'Literal integer reversal, power-based digit extraction, and whole-prefix quotients for actual-minus-isolated carry defects; no producer import.',
        'sha256': {name: sha256((HERE / name).read_bytes()).hexdigest() for name in
                   ['controls.json', 'check_obstruction.py', 'SEAM_PERSISTENCE_OBSTRUCTION.md', 'independent_audit.py']}
    }
    (HERE / 'independent_audit.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    result_path = HERE / 'independent_audit.json'
    result_path.write_text('{"status":"RUNNING"}\n')
    try:
        main()
    except Exception as error:
        result_path.write_text(json.dumps({'status': 'FAIL', 'error': repr(error)}, indent=2) + '\n')
        raise
