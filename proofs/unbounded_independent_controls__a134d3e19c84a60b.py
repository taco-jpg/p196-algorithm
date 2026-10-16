"""Independent exact-integer controls, including empty-band boundaries.
This is a supplemental semantic check, not the universal proof.
"""
import json


def family(k, r):
    q = [1] + [9] * k + [1, 10] + [9] * (2 * r) + [10, 1] + [9] * k + [1]
    expected = [2] + [18] * k + [3, 1] + [0] * (2 * r) + [1, 3] + [18] * k + [2]
    return q, expected


def check(k, r):
    source, expected = family(k, r)
    width = len(source)
    assert width == 2 * k + 2 * r + 6
    assert source == source[::-1]
    assert all(q not in (0, 18) for q in source)
    # Build a fresh canonical digit witness; no imported project routines.
    digits = [0] * width
    for i in range(width // 2):
        digits[i] = source[i] // 2
        digits[width - 1 - i] = source[i] - digits[i]
    assert digits[-1] > 0 and all(0 <= d <= 9 for d in digits)
    n = sum(d * 10 ** i for i, d in enumerate(digits))
    next_n = n + int(str(n)[::-1])
    output = [int(d) for d in str(next_n)[::-1]]
    assert len(output) == width, (k, r, 'overflow')
    actual = [a + b for a, b in zip(output, reversed(output))]
    assert actual == expected, (k, r)
    zeros = [i for i, q in enumerate(actual) if q == 0]
    eighteens = [i for i, q in enumerate(actual) if q == 18]
    assert zeros == list(range(k + 3, k + 2 * r + 3))
    assert eighteens == list(range(1, k + 1)) + list(range(k + 2 * r + 5, 2 * k + 2 * r + 5))
    return {'k': k, 'r': r, 'width': width, 'new_zero_count': len(zeros), 'new_eighteen_count': len(eighteens)}


cases = [check(k, r) for k in range(8) for r in range(8)]
cases += [check(100, 0), check(0, 100), check(100, 100)]
print(json.dumps({'result': 'PASS', 'case_count': len(cases), 'boundary_zero_parameters': True,
                  'method': 'independent canonical digit witness and Python integer n+reverse(n)',
                  'cases': cases}, indent=2))
