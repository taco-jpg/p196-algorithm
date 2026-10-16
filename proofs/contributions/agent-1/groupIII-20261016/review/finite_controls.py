#!/usr/bin/env python3
"""Independent finite arithmetic diagnostics, NOT an all-parameter proof."""
from pathlib import Path
import hashlib
import json

OUT = Path(__file__).resolve().parent


def normalize(coefficients):
    carry, digits = 0, []
    for a in coefficients:
        carry, digit = divmod(a + carry, 10)
        digits.append(digit)
    while carry:
        carry, digit = divmod(carry, 10)
        digits.append(digit)
    assert digits[-1] != 0
    return digits


def pair(digits):
    return [a + b for a, b in zip(digits, reversed(digits))]


def step_word(q):
    return pair(normalize(q))


def overlap(q):
    return [a + b for a, b in zip(q + [0], [0] + q)]


def value(digits):
    return sum(a * 10**i for i, a in enumerate(digits))


def digits_of(n):
    return [int(c) for c in str(n)[::-1]]


def realize(q, choice):
    """Choose bounded opposite digit pairs; require a nonzero leading digit."""
    d = [0] * len(q)
    for i in range((len(q) + 1) // 2):
        j = len(q) - 1 - i
        if i == j:
            assert q[i] % 2 == 0
            d[i] = q[i] // 2
        else:
            low, high = max(0, q[i] - 9), min(9, q[i])
            if i == 0:
                high = min(high, q[i] - 1)
            d[i] = (low, high, (low + high) // 2)[choice]
            d[j] = q[i] - d[i]
    assert all(0 <= a <= 9 for a in d) and d[-1] > 0
    assert pair(d) == q
    return value(d)


def main():
    cores = [(u, v) for u in range(10, 14) for v in (5, 6) if u + v <= 18]
    assert cores == [(10, 5), (10, 6), (11, 5), (11, 6), (12, 5), (12, 6), (13, 5)]
    rs = list(range(1, 13)) + [32, 128]
    count = witnesses = 0
    boundary = []
    for r in rs:
        for p in range(1, 5):
            for u, v in cores:
                a = [p] + [0] * r + [u, v, v, u] + [0] * r + [p]
                q = overlap(a)
                c = [4*p] + [0] * (r-1) + [2, 4*u-39, 4*v-17, 4*v-17, 4*u-39, 2] + [0] * (r-1) + [4*p]
                a1 = step_word(a)
                a2 = step_word(a1)
                q1 = step_word(q)
                q2 = step_word(q1)
                redundant = overlap(a1)
                assert a1 == [2*p] + [0] * (r-1) + [1, 2*u-20, 2*v+1, 2*v+1, 2*u-20, 1] + [0] * (r-1) + [2*p]
                assert len(a) == len(a1) == len(a2) == len(c) == 2*r+6
                assert len(q) == len(q1) == len(q2) == 2*r+7
                assert a2 == c and q2 == overlap(c) and q1 != redundant
                assert all(0 <= x <= 18 for x in q2)
                assert q2 == q2[::-1] and q2[0] > 0 and q2[len(q2)//2] % 2 == 0
                defect = [x-y for x, y in zip(q1, redundant)]
                expected = [0] * len(q)
                expected[r+2:r+5] = [1, -20, 1]
                assert defect == expected
                digit_defect = [x-y for x, y in zip(normalize(q1), normalize(redundant))]
                expected[r+2:r+5] = [1, 0, -1]
                assert digit_defect == expected
                assert digit_defect == [-x for x in digit_defect[::-1]]
                for choice in range(3):
                    n = realize(q, choice)
                    n1 = n + int(str(n)[::-1])
                    n2 = n1 + int(str(n1)[::-1])
                    assert n > 0
                    assert str(n1) != str(n1)[::-1] and str(n2) != str(n2)[::-1]
                    assert len(str(n1)) == len(str(n2)) == len(q)
                    assert pair(digits_of(n1)) == q1 and pair(digits_of(n2)) == overlap(c)
                    witnesses += 1
                count += 1
                if r == 1 and p == 4:
                    boundary.append({'r':r, 'p':p, 'u':u, 'v':v, 'component':a, 'returned_component':c, 'returned_whole':q2})
    result = {'status':'PASS_FINITE_DIAGNOSTICS_ONLY', 'not_a_theorem':True,
              'r_values':rs, 'p_values':list(range(1,5)), 'cores':cores,
              'parameter_tuples_checked':count, 'numeric_realizations_checked':witnesses,
              'r1_p4_boundary_cases':boundary,
              'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/'finite-controls-result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'r1_p4_boundary_cases'}))


if __name__ == '__main__':
    main()
