"""Independent finite arithmetic control for the two-parameter run identity.

The all-parameter proof is the carry calculation in astra_literature_findings.md.
This check does not establish a closed invariant or decimal Lychrel existence.
"""

from itertools import product
import json


def check(a, b):
    q = [16] * a + [2] * b + [16] * a
    carry = 0
    digits = []
    for value in q:
        total = value + carry
        digits.append(total % 10)
        carry = total // 10
    if carry:
        digits.append(carry)
    wanted_digits = ([6] + [7] * (a - 1) + [3] + [2] * (b - 1)
                     + [6] + [7] * (a - 1) + [1])
    assert digits == wanted_digits
    actual = [x + y for x, y in zip(digits, reversed(digits))]
    wanted = ([7] + [14] * (a - 1) + [9] + [4] * (b - 1)
              + [9] + [14] * (a - 1) + [7])
    assert actual == wanted
    assert digits != digits[::-1]
    # Realize q independently as a decimal numeral and add its integer reverse.
    ds = [value // 2 for value in q]
    n = int(''.join(map(str, reversed(ds))))
    out = n + int(str(n)[::-1])
    assert str(out)[::-1] == ''.join(map(str, digits))


if __name__ == '__main__':
    for a, b in product(range(1, 101), repeat=2):
        check(a, b)
    print(json.dumps({'checked_parameter_pairs': 10000,
                      'decimal_existence_proved': False}))
