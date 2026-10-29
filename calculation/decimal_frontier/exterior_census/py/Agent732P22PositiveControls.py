#!/usr/bin/env python3
"""Independent ordinary-integer positive controls for two lattice certificates.

Read the base-9 finite certificate and the base-13 Lean certificate already on
main. Validate all 201 whole pairwords, 200 carry/overflow bits and 200
reverse-and-add steps using both digit vectors and Python big integers.
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[4]  # src/ or py/ under calculation/decimal_frontier/exterior_census
FORMATS = ROOT / 'calculation' / 'decimal_frontier' / 'lattice_formats'


def value(digits, base):
    out = 0
    for d in reversed(digits):
        out = out * base + d
    return out


def digits_of(n, base):
    out = []
    while n:
        n, d = divmod(n, base)
        out.append(d)
    return out or [0]


def ordinary_next(ds, b):
    carry = 0
    out = []
    for a, c in zip(ds, reversed(ds)):
        s = a + c + carry
        carry, digit = divmod(s, b)
        out.append(digit)
    if carry:
        out.append(carry)
    # Independent Python bigint addition and base-b reversal.
    n = value(ds, b)
    result = n + value(list(reversed(ds)), b)
    assert out == digits_of(result, b), 'BIGINT/DIGIT DISAGREEMENT'
    return out


def split_pairword(P, b):
    assert P == P[::-1]
    ds = [0] * len(P)
    for i in range(len(P) // 2):
        ds[i] = P[i] // 2
        ds[-i - 1] = P[i] - ds[i]
    if len(P) % 2:
        assert P[len(P)//2] % 2 == 0
        ds[len(P)//2] = P[len(P)//2] // 2
    assert ds[-1] > 0 and all(0 <= d < b for d in ds)
    return ds


def verify(label, b, B, W, gamma, l0, steps=200):
    p = len(gamma)
    m = len(W[0])
    assert len(B) == len(W) == p
    assert all(len(row) == len(B[0]) for row in B)
    assert all(len(row) == m for row in W)
    P0 = B[0] + [W[0][i % m] for i in range(l0)] + B[0][::-1]
    ds = split_pairword(P0, b)
    initial = len(ds)
    l = l0
    for t in range(steps+1):
        r = t % p
        expected = B[r] + [W[r][i % m] for i in range(l)] + B[r][::-1]
        actual = [ds[i] + ds[-i - 1] for i in range(len(ds))]
        assert actual == expected, (label, 'pairword', t)
        assert ds != ds[::-1], (label, 'palindrome', t)
        if t == steps:
            break
        ds2 = ordinary_next(ds, b)
        assert len(ds2) - len(ds) == gamma[r], (label, 'overflow', t)
        ds = ds2
        l += gamma[r]
    print(f'{label}: |B|={len(B[0])} m={m} steps={steps} '
          f'pairwords={steps+1} initial={initial} final={len(ds)} '
          'zero_palindromes BIGINT_AND_DIGITS_OK')


def run():
    b9 = json.loads((FORMATS / 'cert_b9_rec0.json').read_text())
    assert b9['base'] == 9 and b9['gam'] == [int(c) for c in '1100011000']
    assert b9['nB'] == 61 and b9['m'] == 4
    verify('b9 g1100011000', 9, b9['B_t'], b9['w_t'], b9['gam'], b9['l0'])
    lean = (ROOT / 'lean' / 'P196' / 'AbsorbingBand' / 'Base13.lean').read_text()
    b13 = [None] * 10
    for i, raw in re.findall(r'def\s+B([0-9]+)\s*:\s*List\s+Nat\s*:=\s*\[([^]]+)\]', lean):
        b13[int(i)] = [int(x) for x in raw.split(',')]
    assert len(b13) == 10 and all(row is not None and len(row) == 75 for row in b13)
    gamma13 = [int(c) for c in '1010010000']
    w13 = [[16 if t % 2 == 0 else 8] for t in range(10)]
    verify('b13 g1010010000', 13, b13, w13, gamma13, 1)


if __name__ == '__main__':
    run()
