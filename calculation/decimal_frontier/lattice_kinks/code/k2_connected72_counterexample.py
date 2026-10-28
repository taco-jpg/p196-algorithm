#!/usr/bin/env python3
"""COMPUTED: explicit connected 11-site stationary 72-step defect for p12/m9.
Reproduce from repository root:
 python3 calculation/decimal_frontier/lattice_kinks/code/k2_connected72_counterexample.py
No third-party packages, no untrusted certificate, and no infinite-orbit claim.
"""
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / 'data' / 'lat_p12m9.txt'
PHASE, LENGTH, START = 2, 800, 180
REPLACEMENTS = (6, 1, 0, 1, 11, 14, 10, 6, 11, 16, 1)
STEPS = 72


def lattice_data():
    it = iter(map(int, DATA.read_text().split()))
    p, width, m, b = (next(it) for _ in range(4))
    assert (p, width, m, b) == (12, 34, 9, 10)
    gamma = tuple(next(it) for _ in range(p))
    rows = [[next(it) for _ in range(m)] for _ in range(p)]
    _incoming_carries = [[next(it) for _ in range(m)] for _ in range(p)]
    border = [[next(it) for _ in range(width)] for _ in range(p)]
    assert next(it, None) is None
    return width, m, gamma, rows, border


def reference_word(data):
    width, m, _, rows, border = data
    pair = [0] * LENGTH
    for i in range(LENGTH // 2):
        q = border[PHASE][i] if i < width else rows[PHASE][(i-width) % m]
        pair[i] = pair[LENGTH-1-i] = q
    return pair


def integer_with_pairword(pair):
    # Independent canonical digit realization, deliberately using ordinary integers.
    n = len(pair)
    digits = [0] * n  # least significant first
    for i in range(n//2):
        x = pair[i]
        if i == 0:
            lo = max(1, x-9)
            hi = x - lo
            if hi == 0:
                lo -= 1; hi += 1
            assert 1 <= lo <= 9 and 1 <= hi <= 9
        else:
            lo = min(9, x)
            hi = x-lo
        digits[i], digits[n-1-i] = lo, hi
    if n & 1:
        assert pair[n//2] % 2 == 0
        digits[n//2] = pair[n//2]//2
    return int(''.join(str(c) for c in reversed(digits)))


def pairword_of_integer(number):
    digits = [int(x) for x in reversed(str(number))]
    return [digits[i] + digits[-1-i] for i in range(len(digits))]


def independently_schoolbook_step(pair):
    # Separate schoolbook carry path; *not* the integer reverse-and-add implementation.
    carry = 0
    digits = []
    for q in pair:
        total = q + carry
        digits.append(total % 10)
        carry = total // 10
    if carry:
        digits.append(carry)
    return [digits[i] + digits[-1-i] for i in range(len(digits))]


def verify():
    data = lattice_data()
    base = reference_word(data)
    changed = base.copy()
    for k, q in enumerate(REPLACEMENTS):
        i = START + k
        assert q != base[i] and 0 <= q <= 18
        changed[i] = changed[LENGTH-1-i] = q
    assert all(base[i] == changed[i] for i in range(START))
    assert all(base[i] != changed[i] for i in range(START, START + len(REPLACEMENTS)))
    assert all(base[i] == changed[i] for i in range(START + len(REPLACEMENTS), LENGTH//2))
    A = integer_with_pairword(base)
    B = integer_with_pairword(changed)
    assert len(str(A)) == len(str(B)) == LENGTH and A != B
    assert pairword_of_integer(A) == base
    assert pairword_of_integer(B) == changed
    pa, pb = base, changed
    gamma = data[2]
    for step in range(1, STEPS + 1):
        len_before = len(pa)
        # Two *independent* numeral algorithms must agree at every time.
        expected_a = independently_schoolbook_step(pa)
        expected_b = independently_schoolbook_step(pb)
        A += int(str(A)[::-1])
        B += int(str(B)[::-1])
        pa = pairword_of_integer(A)
        pb = pairword_of_integer(B)
        assert pa == expected_a and pb == expected_b, step
        assert len(pa) == len(pb) == len_before + gamma[(PHASE+step-1)%12], step
    assert len(pa) == LENGTH + 18 == 818
    diffs = [i for i,(x,y) in enumerate(zip(pa,pb)) if x != y]
    assert diffs and diffs[0] == START, diffs[:10]
    assert min(i for i in diffs if i < len(pa)//2) == START
    print('CONNECTED_72_STATIONARY_PASS', {
        'phase': PHASE, 'initial_length': LENGTH, 'final_length': len(pa),
        'first_input_defect': START, 'first_output_defect': diffs[0],
        'initial_connected_width': len(REPLACEMENTS),
        'output_difference_cells': len(diffs), 'steps': STEPS})


if __name__ == '__main__':
    verify()
